#!/usr/bin/env python3
"""
修补 agent.py 中的 _get_model_context_limit 方法。

问题：litellm 对 gemini-3-pro-preview 返回 65535（实际 1M+），导致 42K token 就触发 Handoff。
修复：已知模型表优先于 litellm 查询；硬上限改为 max(100K, 窗口*50%)。

用法（在远程服务器上）：
    cd ~/novel_eval/novel-writing-alchemist
    git pull
    python3 remote_deploy/patch_agent_context_limit.py

会自动修补 ~/novel_eval/mcp-benchmark/release/framework/benchkit/agent.py
"""
import os
import re
import sys
import shutil

AGENT_PATH = os.path.expanduser(
    "~/novel_eval/mcp-benchmark/release/framework/benchkit/agent.py"
)


def patch_get_model_context_limit(content: str) -> str:
    """替换 _get_model_context_limit 方法"""

    old_pattern = r'(    def _get_model_context_limit\(self\) -> int:.*?)(    def )'
    match = re.search(old_pattern, content, re.DOTALL)
    if not match:
        print("ERROR: 找不到 _get_model_context_limit 方法")
        sys.exit(1)

    new_method = '''    def _get_model_context_limit(self) -> int:
        """获取模型的上下文窗口大小

        优先级：已知模型表 > litellm > 默认值128K
        注意：litellm 对部分模型（如 gemini-3-pro-preview）返回的值严重偏小（65K），
        而实际窗口为 1M+，会导致过早触发 Handoff。因此已知模型表优先级最高。
        """
        # 第一优先级：已知模型的准确窗口大小（人工维护，确保正确）
        known_limits = {
            # Claude系列
            "claude-opus-4": 200000,
            "claude-sonnet-4": 200000,
            "claude-4.5-sonnet": 200000,
            "claude-4.5-opus": 200000,
            "claude-4.5-haiku": 200000,
            "claude-3": 200000,
            "claude-3.5": 200000,

            # GPT-5系列
            "gpt-5": 400000,
            "gpt-5-instant": 400000,
            "gpt-5-thinking": 400000,

            # GPT-4系列
            "gpt-4.1": 1000000,
            "gpt-4-turbo": 128000,
            "gpt-4-32k": 32768,
            "gpt-4": 8192,

            # OpenAI o系列
            "o1": 128000,
            "o1-mini": 128000,
            "o3": 200000,
            "o3-mini": 200000,
            "o4-mini": 200000,

            # Gemini系列
            "gemini-3-pro": 1000000,
            "gemini-3-flash": 1000000,
            "gemini-2.5-pro": 1000000,
            "gemini-2.5-flash": 1000000,

            # Kimi系列
            "kimi-k2.5": 256000,
            "kimi-k2-thinking": 256000,

            # 百度系列
            "ernie-5.0": 119000,
            "ernie-4.5": 119000,

            # 智谱系列
            "glm-4": 128000,

            # 阿里系列
            "qwen3": 131072,
            "qwen2.5": 131072,

            # 旧版本模型
            "gpt-3.5-turbo": 16385,
        }

        model_lower = self.model.lower()
        for model_prefix, limit in known_limits.items():
            if model_prefix in model_lower:
                return limit

        # 第二优先级：litellm 查询（可能有延迟或不准确）
        if LITELLM_AVAILABLE:
            try:
                max_tokens = get_max_tokens(self.model)  # type: ignore[possibly-undefined]
                if max_tokens:
                    logger.info(f"Using litellm context limit for {self.model}: {max_tokens}")
                    return max_tokens
            except Exception as e:
                logger.debug(f"Failed to get max tokens from litellm: {e}")

        # 默认值：128K
        return 128000

'''
    content = content[:match.start()] + new_method + match.group(2) + content[match.end():]
    return content


def patch_check_proactive_summarization(content: str) -> str:
    """修补 100k 硬上限为动态阈值"""

    # 替换 threshold_100k = 100000
    content = content.replace(
        "threshold_100k = 100000",
        "# 硬上限：取模型窗口的50%和100k中的较大值\n"
        "        # 对于大窗口模型（如Gemini 1M），100k硬上限太保守\n"
        "        threshold_hard = max(100000, int(context_limit * 0.5))"
    )

    # 替换引用
    content = content.replace("threshold_100k", "threshold_hard")

    # 替换触发日志文案
    content = content.replace(
        '达到100k tokens硬上限',
        '达到硬上限（{threshold_hard:,} tokens）'
    )
    # 修复 format string — 旧代码用 f-string，替换后需要保持一致
    content = content.replace(
        'f"达到硬上限（{threshold_hard:,} tokens）"',
        'f"达到硬上限（{threshold_hard:,} tokens）"'
    )

    return content


def main():
    if not os.path.isfile(AGENT_PATH):
        print(f"ERROR: agent.py 不存在: {AGENT_PATH}")
        sys.exit(1)

    # 备份
    backup_path = AGENT_PATH + ".bak"
    shutil.copy2(AGENT_PATH, backup_path)
    print(f"✓ 备份: {backup_path}")

    with open(AGENT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查是否已修补
    if "known_limits" in content and "threshold_hard" in content:
        print("✓ agent.py 已经修补过，无需重复操作")
        os.remove(backup_path)
        return

    content = patch_get_model_context_limit(content)
    content = patch_check_proactive_summarization(content)

    with open(AGENT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ 已修补: {AGENT_PATH}")
    print("  - _get_model_context_limit: 已知模型表优先于 litellm")
    print("  - _check_proactive_summarization: 硬上限改为 max(100K, 窗口*50%)")
    print(f"\n验证：python3 -c \"import sys; sys.path.insert(0,'{os.path.dirname(AGENT_PATH)}'); from agent import Agent; print('OK')\"")


if __name__ == "__main__":
    main()
