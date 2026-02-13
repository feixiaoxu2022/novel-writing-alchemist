#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说创作炼金术场景 - Checker执行模块

职责：执行checklist中的所有检查项（调用LLM），生成原始检查结果
输入：sample执行结果（conversation_history + workspace文件） + checklist
输出：execution_result.json（包含pass/fail和grading分数，不含维度聚合统计）

注意：本文件从shortdrama/env/checker.py恢复，支持7种check_types：
  1. entity_attribute_equals (FileSystemChecker)
  2. create_operation_verified (FileSystemChecker)
  3. json_schema (JSONSchemaChecker)
  4. cross_file_consistency (CrossFileConsistencyChecker)
  5. tool_called_with_params (ToolCalledWithParamsChecker)
  6. tool_call_absence (ToolCallAbsenceChecker)
  7. semantic_check (SemanticChecker)
"""

import json
import argparse
import re
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
import time
import glob as glob_module
import warnings
import os

# 过滤Pydantic序列化警告
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')

# 禁用LiteLLM的调试信息
os.environ['LITELLM_LOG'] = 'ERROR'
import litellm
litellm.suppress_debug_info = True
litellm.set_verbose = False
from litellm import completion


# =========================================
# 1. 辅助函数
# =========================================

def request_llm_with_litellm(messages, model_name, api_base, api_key, max_retries=3):
    """使用LiteLLM调用模型进行语义判断"""
    if api_base:
        litellm.api_base = api_base
    if api_key:
        litellm.api_key = api_key

    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg["role"],
            "content": msg.get("content", "")
        })

    for attempt in range(max_retries):
        try:
            print(f"[LLM调用] 尝试 {attempt + 1}/{max_retries}, model={model_name}", flush=True)

            # 打印请求内容（截断超长内容）
            for idx, msg in enumerate(formatted_messages):
                content = msg["content"]
                if len(content) > 500:
                    content_preview = content[:250] + f"\n... [省略{len(content)-500}字符] ...\n" + content[-250:]
                else:
                    content_preview = content
                print(f"[LLM请求] Message {idx+1} ({msg['role']}): {content_preview}", flush=True)

            response = completion(
                model=model_name,
                messages=formatted_messages,
                response_format={"type": "json_object"},
                api_base=api_base,
                api_key=api_key,
                custom_llm_provider="openai"
            )

            content = response.choices[0].message.content
            print(f"[LLM调用] 成功", flush=True)

            # 打印响应内容（截断超长内容）
            if len(content) > 1000:
                content_preview = content[:500] + f"\n... [省略{len(content)-1000}字符] ...\n" + content[-500:]
            else:
                content_preview = content
            print(f"[LLM响应]: {content_preview}", flush=True)

            return True, content

        except Exception as e:
            error_msg = str(e)
            print(f"[LLM调用] 失败 (尝试 {attempt + 1}/{max_retries}): {error_msg}", flush=True)
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            else:
                return False, error_msg

    return False, "所有重试均失败"


def safe_json_extract_single(response_text: str) -> Dict:
    """从响应文本中安全提取单个JSON对象"""
    if not response_text:
        raise ValueError("响应文本为空")

    # 尝试直接解析
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # 尝试提取JSON代码块
    try:
        json_pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(json_pattern, response_text, re.DOTALL)
        if matches:
            return json.loads(matches[0])
    except Exception:
        pass

    # 尝试提取大括号内容
    try:
        json_pattern = r'\{.*\}'
        matches = re.findall(json_pattern, response_text, re.DOTALL)
        if matches:
            return json.loads(matches[0])
    except Exception:
        pass

    raise ValueError(f"无法从响应中提取JSON: {response_text[:200]}")


# =========================================
# 2. 检查结果格式
# =========================================

def create_check_result_template() -> Dict:
    """创建标准检查结果模板"""
    return {
        "check_version": "scenario_v1.0",
        "check_timestamp": int(time.time()),
        "check_details": {},
        "overall_result": "Success",  # Success / Failure / Error
        "error_reason": "",
        "check_list_count": 0,
        "completion_status": "in_progress",  # in_progress / completed / failed
        "completion_reason": ""
    }


def create_check_item_result(conclusion: str, reason: str, details: str) -> Dict:
    """创建单个检查项结果"""
    return {
        "check_result": conclusion,  # pass / fail / skip
        "reason": reason,
        "details": details
    }


def _determine_check_level(description: str) -> str:
    """
    根据description判断检查项级别

    Returns:
        - "excellent": 优秀标准（包含"优秀"关键词）
        - "basic": 基础标准（包含"基础"关键词）
        - "must_have": 基本要求（其他所有）
    """
    if "优秀" in description:
        return "excellent"
    elif "基础" in description:
        return "basic"
    else:
        return "must_have"

def create_check_item_result(conclusion: str, reason: str, details: str) -> Dict:
    """创建单个检查项结果"""
    return {
        "check_result": conclusion,  # pass / fail / skip
        "reason": reason,
        "details": details
    }


def load_judge_criteria_from_params(params: Dict, work_dir: Path = None) -> str:
    """
    从params中加载judge criteria，支持文件引用。

    支持三种方式：
    1. 直接内联：params["llm_judge_criteria"] = "评估标准..."
    2. 文件引用：params["llm_judge_criteria_file"] = "docs/xxx.yaml"
                params["llm_judge_criteria_section"] = "检查项名称"
    3. validation_rules格式（v3规范）：
       params["validation_rules"][0]["evaluation_criteria"]["validation_prompt"]

    Args:
        params: 检查项参数字典
        work_dir: 工作目录，用于解析相对路径

    Returns:
        加载的judge criteria文本
    """
    # 优先使用内联的 llm_judge_criteria
    inline_criteria = params.get("llm_judge_criteria", "")
    if inline_criteria:
        return inline_criteria

    # 尝试从validation_rules格式提取（v3规范）
    validation_rules = params.get("validation_rules", [])
    if validation_rules and isinstance(validation_rules, list) and len(validation_rules) > 0:
        first_rule = validation_rules[0]
        if isinstance(first_rule, dict):
            # 检查validation_method
            validation_method = first_rule.get("validation_method", "")

            # 只有llm_semantic_analysis方法才需要criteria
            if validation_method == "llm_semantic_analysis":
                eval_criteria = first_rule.get("evaluation_criteria", {})
                if isinstance(eval_criteria, dict):
                    validation_prompt = eval_criteria.get("validation_prompt", "")
                    if validation_prompt:
                        return validation_prompt

    # 尝试从文件加载
    criteria_file = params.get("llm_judge_criteria_file")
    criteria_section = params.get("llm_judge_criteria_section")

    if not criteria_file:
        return ""

    # 解析文件路径（支持相对路径）
    if work_dir:
        file_path = work_dir / criteria_file
    else:
        file_path = Path(criteria_file)

    if not file_path.exists():
        print(f"警告: judge criteria文件不存在: {file_path}")
        return ""

    try:
        import yaml
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 如果指定了section，从yaml中提取特定section
        if criteria_section:
            # 简单的section提取：查找 "## {section}" 后的 "llm_judge_criteria: |" 内容
            # 支持两种格式：## <section> 或 ## 1. <section>
            # 注意：criteria内容中可能包含#字符（如markdown注释），所以用.*?而非[^#]*?
            # section边界用 "---" 分隔线或下一个 "## " 标题来识别
            section_pattern = rf'## (?:\d+\.\s+)?{re.escape(criteria_section)}.*?llm_judge_criteria:\s*\|(.*?)(?=\n---\n|\n## |\Z)'
            match = re.search(section_pattern, content, re.DOTALL)
            if match:
                criteria_text = match.group(1).strip()
                # 移除缩进
                lines = criteria_text.split('\n')
                if lines:
                    # 找到第一行的缩进
                    first_line = next((l for l in lines if l.strip()), '')
                    indent = len(first_line) - len(first_line.lstrip())
                    # 移除所有行的相同缩进
                    dedented_lines = [l[indent:] if len(l) > indent else l for l in lines]
                    return '\n'.join(dedented_lines).strip()

            print(f"警告: 在 {file_path} 中未找到section: {criteria_section}")
            return ""
        else:
            # 如果没有指定section，返回整个文件内容
            return content

    except Exception as e:
        print(f"警告: 加载judge criteria文件失败: {file_path}, 错误: {e}")
        return ""


# =========================================
# 2. FileSystemChecker类
# =========================================

class FileSystemChecker:
    """文件系统JSON文件检查器"""

    def __init__(self, work_dir: str, model_name=None, api_base=None, api_key=None):
        """
        Args:
            work_dir: 工作目录（包含workspace/子目录）
            model_name: LLM模型名（可选，用于JSON不合法时的semantic fallback）
            api_base: LLM API地址
            api_key: LLM API密钥
        """
        self.work_dir = Path(work_dir)
        self.workspace_dir = self.work_dir / "workspace"
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key

    def _load_json_file(self, file_path: Path) -> Dict:
        """加载JSON文件，JSON格式错误时保留原始内容供语义检查使用"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return json.loads(content)
        except json.JSONDecodeError as e:
            # JSON格式错误，但保留原始内容供语义检查fallback使用
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                return {
                    "_error": f"JSON格式不合法（行{e.lineno}列{e.colno}）",
                    "_raw_content": raw_content  # 保留原始文本
                }
            except Exception:
                return {"_error": f"JSON格式不合法（行{e.lineno}列{e.colno}）"}
        except Exception as e:
            return {"_error": f"文件读取失败：{str(e)}"}

    def _semantic_fallback_extract(self, raw_content: str, attribute_key: str, expected_value: Any, target_id: str) -> Dict:
        """
        JSON不合法时的语义兜底：用LLM从原始文本中提取字段值并比对

        解耦JSON合法性能力和意图理解能力：
        - JSON格式不合法 → 扣JSON格式分（由json_schema检查项负责）
        - 但字段语义是否正确 → 由本方法通过LLM语义提取判断

        Returns:
            check result dict，pass/fail/skip
        """
        if not self.model_name:
            # 没有LLM配置，无法做semantic fallback，保持原有fail行为
            return create_check_item_result(
                "fail", "文件读取失败（无LLM配置，无法semantic fallback）",
                f"文件 {target_id} JSON不合法，且未配置LLM无法进行语义兜底"
            )

        # 构造LLM提取prompt
        prompt = f"""以下是一个JSON格式不合法的文件内容，请从中语义提取指定字段的值。

**文件内容（原始文本）：**
{raw_content[:8000]}

**需要提取的字段路径：** {attribute_key}
**期望值：** {expected_value}

请分析原始文本，判断作者想要表达的 {attribute_key} 字段值是什么。即使JSON格式有语法错误，只要能从文本中识别出该字段的意图值即可。

请以JSON格式回复：
{{"extracted_value": "从文本中提取到的字段值（原样返回，包括特殊字符如↗↘✷）", "matched": true/false, "reason": "判断依据"}}"""

        messages = [
            {"role": "system", "content": "你是一个精确的文本分析助手。你的任务是从格式不完美的文本中提取指定字段的语义值。"},
            {"role": "user", "content": prompt}
        ]

        print(f"\033[1;33m[Semantic Fallback] 文件 {target_id} JSON不合法，尝试语义提取 {attribute_key}...\033[0m", flush=True)

        success, response = request_llm_with_litellm(
            messages, self.model_name, self.api_base, self.api_key
        )

        if not success:
            return create_check_item_result(
                "fail", "文件读取失败（semantic fallback也失败）",
                f"文件 {target_id} JSON不合法，LLM语义提取也失败: {response}"
            )

        try:
            result_data = safe_json_extract_single(response)
            matched = result_data.get("matched", False)
            extracted = result_data.get("extracted_value", "")
            reason = result_data.get("reason", "")

            if matched:
                result = create_check_item_result(
                    "pass", "属性值符合预期（semantic fallback）",
                    f"文件JSON不合法，但语义提取值='{extracted}'，匹配期望值'{expected_value}'。{reason}"
                )
                result["semantic_fallback"] = True
                result["json_parse_error"] = True
                return result
            else:
                result = create_check_item_result(
                    "fail", "属性值不符合预期（semantic fallback）",
                    f"文件JSON不合法，语义提取值='{extracted}'，不匹配期望值'{expected_value}'。{reason}"
                )
                result["semantic_fallback"] = True
                result["json_parse_error"] = True
                return result

        except Exception as e:
            return create_check_item_result(
                "fail", "文件读取失败（semantic fallback解析失败）",
                f"文件 {target_id} JSON不合法，LLM响应解析失败: {str(e)}"
            )

    def _glob_files(self, pattern: str) -> List[Path]:
        """
        使用glob模式匹配文件（容错处理workspace路径嵌套）

        容错逻辑：同时尝试正确路径和嵌套路径，覆盖Agent可能的两种行为：
        1. Agent写相对路径(如topic_brief.json) + tool加workspace/ = 正确
        2. Agent写完整路径(如workspace/topic_brief.json) + tool加workspace/ = 嵌套
        """
        # pattern示例: "workspace/characters/*.json"
        full_pattern = str(self.work_dir / pattern)
        matched_files = glob_module.glob(full_pattern)

        # 容错处理：如果没有匹配且pattern以workspace/开头，尝试嵌套路径
        if not matched_files and pattern.startswith("workspace/"):
            # 尝试workspace/workspace/路径
            nested_pattern = pattern.replace("workspace/", "workspace/workspace/", 1)
            full_nested_pattern = str(self.work_dir / nested_pattern)
            matched_files = glob_module.glob(full_nested_pattern)

        return [Path(f) for f in matched_files]

    def check_entity_attribute_equals(self, check_item: Dict) -> Dict:
        """
        检查文件字段值是否等于预期值

        check_item示例:
        {
            "check_type": "entity_attribute_equals",
            "params": {
                "entity_type": "file",
                "target_id": "workspace/topic_brief.json",
                "attribute_key": "hooks",
                "expected_value": {"array_min_length": 3}
            }
        }
        """
        params = check_item.get("params", {})
        entity_type = params.get("entity_type")
        target_id = params.get("target_id")
        attribute_key = params.get("attribute_key")
        expected_value = params.get("expected_value")

        if entity_type != "file":
            return create_check_item_result(
                "skip", "不支持的entity_type",
                f"当前仅支持entity_type='file'，收到：{entity_type}"
            )

        # 支持"+"连接的多文件路径（如"workspace/characters.json + workspace/outline.json"）
        if ' + ' in target_id:
            return self._check_cross_files_attribute(target_id, attribute_key, expected_value)

        # 处理glob模式
        if "*" in target_id:
            # 对于通配符，需要检查所有匹配文件
            files = self._glob_files(target_id)
            if not files:
                return create_check_item_result(
                    "fail", "未找到匹配文件",
                    f"模式 '{target_id}' 未匹配任何文件"
                )

            # 特殊处理：contains_value约束需要统计所有文件中符合条件的数量
            if isinstance(expected_value, dict) and "contains_value" in expected_value:
                target_value = expected_value["contains_value"]
                min_count = expected_value.get("min_count", 1)

                # 统计符合条件的文件数量
                matched_count = 0
                details_list = []
                for file_path in files:
                    data = self._load_json_file(file_path)
                    if "_error" in data:
                        details_list.append(f"{file_path.name}: 读取失败")
                        continue

                    actual_value = self._get_nested_value(data, attribute_key)
                    if actual_value == target_value:
                        matched_count += 1
                        details_list.append(f"{file_path.name}: {attribute_key} = {actual_value}")
                    else:
                        details_list.append(f"{file_path.name}: {attribute_key} = {actual_value}")

                if matched_count >= min_count:
                    return create_check_item_result(
                        "pass", "所有文件属性符合预期",
                        f"{matched_count}/{len(files)} 个文件符合 {attribute_key}={target_value}，≥ {min_count}; " + "; ".join(details_list)
                    )
                else:
                    return create_check_item_result(
                        "fail", "部分文件属性不符合预期",
                        f"{matched_count}/{len(files)} 个文件符合 {attribute_key}={target_value}，< {min_count}; " + "; ".join(details_list)
                    )

            # 对所有文件进行检查
            all_pass = True
            details_list = []
            for file_path in files:
                data = self._load_json_file(file_path)
                if "_error" in data:
                    all_pass = False
                    details_list.append(f"{file_path.name}: 读取失败 - {data['_error']}")
                    continue

                result = self._check_attribute_value(data, attribute_key, expected_value)
                if not result["pass"]:
                    all_pass = False
                details_list.append(f"{file_path.name}: {result['message']}")

            if all_pass:
                return create_check_item_result(
                    "pass", "所有文件属性符合预期",
                    "; ".join(details_list)
                )
            else:
                return create_check_item_result(
                    "fail", "部分文件属性不符合预期",
                    "; ".join(details_list)
                )

        else:
            # 单个文件或目录检查（容错处理workspace路径嵌套）
            file_path = self.work_dir / target_id

            print(f"[DEBUG FileSystemChecker] target_id={target_id}", flush=True)
            print(f"[DEBUG FileSystemChecker] work_dir={self.work_dir}", flush=True)
            print(f"[DEBUG FileSystemChecker] file_path={file_path}", flush=True)
            print(f"[DEBUG FileSystemChecker] file_path.exists()={file_path.exists()}", flush=True)
            print(f"[DEBUG FileSystemChecker] file_path.absolute()={file_path.absolute()}", flush=True)

            # 容错逻辑：如果文件不存在且路径以workspace/开头，尝试嵌套路径
            if not file_path.exists() and target_id.startswith("workspace/"):
                print(f"[DEBUG FileSystemChecker] Trying nested workspace/workspace/ fallback", flush=True)
                nested_target_id = target_id.replace("workspace/", "workspace/workspace/", 1)
                nested_file_path = self.work_dir / nested_target_id
                print(f"[DEBUG FileSystemChecker] nested_file_path={nested_file_path}", flush=True)
                print(f"[DEBUG FileSystemChecker] nested_file_path.exists()={nested_file_path.exists()}", flush=True)
                if nested_file_path.exists():
                    file_path = nested_file_path
                    target_id = nested_target_id
                    print(f"[DEBUG FileSystemChecker] Using nested path", flush=True)

            # 特殊处理：naming_pattern检查（针对目录）
            if attribute_key == "naming_pattern":
                if not file_path.exists():
                    return create_check_item_result(
                        "fail", "目录不存在",
                        f"目录 {target_id} 不存在"
                    )

                if not file_path.is_dir():
                    return create_check_item_result(
                        "fail", "路径不是目录",
                        f"路径 {target_id} 不是目录"
                    )

                # 列出目录中的文件
                try:
                    files = [f for f in file_path.iterdir() if f.is_file()]
                except Exception as e:
                    return create_check_item_result(
                        "fail", "目录读取失败",
                        f"无法读取目录 {target_id}: {str(e)}"
                    )

                if not files:
                    return create_check_item_result(
                        "fail", "目录为空",
                        f"目录 {target_id} 中没有文件"
                    )

                # 验证每个文件名是否符合naming_pattern
                if isinstance(expected_value, dict) and "regex" in expected_value:
                    import re
                    pattern = expected_value["regex"]
                    all_pass = True
                    details_list = []

                    for file in files:
                        filename = file.name
                        if re.match(pattern, filename):
                            details_list.append(f"{filename}: 匹配")
                        else:
                            all_pass = False
                            details_list.append(f"{filename}: 不匹配")

                    if all_pass:
                        return create_check_item_result(
                            "pass", "所有文件命名符合规范",
                            f"检查了 {len(files)} 个文件; " + "; ".join(details_list)
                        )
                    else:
                        return create_check_item_result(
                            "fail", "部分文件命名不符合规范",
                            "; ".join(details_list)
                        )
                else:
                    return create_check_item_result(
                        "fail", "naming_pattern需要regex约束",
                        f"expected_value必须包含regex字段"
                    )

            # 特殊处理：_exists或exists检查（兼容两种写法）
            if attribute_key == "_exists" or attribute_key == "exists":
                print(f"[DEBUG FileSystemChecker] Checking file existence, attribute_key={attribute_key}", flush=True)
                print(f"[DEBUG FileSystemChecker] file_path (before exists check)={file_path}", flush=True)
                print(f"[DEBUG FileSystemChecker] file_path.exists()={file_path.exists()}", flush=True)
                if file_path.exists():
                    return create_check_item_result(
                        "pass", "文件存在",
                        f"文件 {target_id} 存在"
                    )
                else:
                    return create_check_item_result(
                        "fail", "文件不存在",
                        f"文件 {target_id} 不存在"
                    )

            print(f"[DEBUG FileSystemChecker] Before final exists check: file_path={file_path}, attribute_key={attribute_key}", flush=True)
            print(f"[DEBUG FileSystemChecker] file_path.exists() at line 526={file_path.exists()}", flush=True)
            if not file_path.exists():
                # 检查其他属性时文件不存在，这是依赖失败（依赖于文件存在性检查）
                result = create_check_item_result(
                    "skip", "前置条件失败（文件不存在）",
                    f"文件 {target_id} 不存在，无法检查属性 {attribute_key}"
                )
                result["dependency_failure"] = True
                return result

            data = self._load_json_file(file_path)
            if "_error" in data:
                # JSON不合法时，尝试semantic fallback：从原始文本语义提取字段值
                # 解耦JSON格式能力和意图理解能力
                if "_raw_content" in data and data["_raw_content"]:
                    print(f"\033[1;33m[FileSystemChecker] JSON不合法，触发semantic fallback for {attribute_key}\033[0m", flush=True)
                    return self._semantic_fallback_extract(
                        data["_raw_content"], attribute_key, expected_value, target_id
                    )
                return create_check_item_result(
                    "fail", "文件读取失败",
                    f"文件 {target_id} 读取失败: {data['_error']}"
                )

            result = self._check_attribute_value(data, attribute_key, expected_value)
            if result["pass"]:
                return create_check_item_result(
                    "pass", "属性值符合预期",
                    result["message"]
                )
            else:
                return create_check_item_result(
                    "fail", "属性值不符合预期",
                    result["message"]
                )

    def _check_cross_files_attribute(self, target_id: str, attribute_key: str, expected_value: Any) -> Dict:
        """
        检查跨多个文件的属性（支持"+"连接的文件路径）

        Args:
            target_id: 文件路径，如"workspace/characters.json + workspace/outline.json"
            attribute_key: 属性键，如"main_characters_in_outline"
            expected_value: 期望值

        Returns:
            检查结果字典
        """
        # 分割文件路径
        paths = [p.strip() for p in target_id.split(' + ')]
        if len(paths) < 2:
            return create_check_item_result(
                "fail", "参数错误",
                f"跨文件检查需要至少2个文件路径，收到：{target_id}"
            )

        # 特殊处理：main_characters_in_outline 和 main_characters_in_chapters
        if attribute_key == "main_characters_in_outline":
            return self._check_main_characters_in_outline(paths)
        elif attribute_key == "main_characters_in_chapters":
            return self._check_main_characters_in_chapters(paths)
        else:
            return create_check_item_result(
                "skip", f"不支持的跨文件检查类型: {attribute_key}",
                f"当前仅支持 main_characters_in_outline 和 main_characters_in_chapters"
            )

    def _check_main_characters_in_outline(self, paths: List[str]) -> Dict:
        """检查主要角色是否在大纲中规划"""
        # 第一个路径应该是characters.json
        characters_path = self.work_dir / paths[0]
        outline_path = self.work_dir / paths[1]

        # 容错处理
        if not characters_path.exists() and paths[0].startswith("workspace/"):
            nested_path = paths[0].replace("workspace/", "workspace/workspace/", 1)
            characters_path = self.work_dir / nested_path

        if not outline_path.exists() and paths[1].startswith("workspace/"):
            nested_path = paths[1].replace("workspace/", "workspace/workspace/", 1)
            outline_path = self.work_dir / nested_path

        # 检查文件存在性
        if not characters_path.exists():
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json不存在）",
                f"文件 {paths[0]} 不存在"
            )
            result["dependency_failure"] = True
            return result

        if not outline_path.exists():
            result = create_check_item_result(
                "skip", "前置条件失败（outline.json不存在）",
                f"文件 {paths[1]} 不存在"
            )
            result["dependency_failure"] = True
            return result

        # 读取characters.json
        characters_data = self._load_json_file(characters_path)
        if "_error" in characters_data:
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json读取失败）",
                f"无法读取 {paths[0]}: {characters_data['_error']}"
            )
            result["dependency_failure"] = True
            return result

        # 提取主要角色名
        if not isinstance(characters_data, dict):
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json schema不合规）",
                f"characters.json顶层不是dict，而是{type(characters_data).__name__}"
            )
            result["dependency_failure"] = True
            result["schema_violation"] = True
            return result
        main_characters = characters_data.get("main_characters", [])
        if not main_characters:
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json schema不合规）",
                "main_characters字段为空或不存在，实际顶层字段: " + ", ".join(list(characters_data.keys())[:5])
            )
            result["dependency_failure"] = True
            result["schema_violation"] = True
            return result

        character_names = [char.get("name", "") for char in main_characters if isinstance(char, dict)]
        if not character_names:
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json schema不合规）",
                "main_characters中的角色对象缺少name字段"
            )
            result["dependency_failure"] = True
            result["schema_violation"] = True
            return result

        # 读取outline.json
        outline_data = self._load_json_file(outline_path)
        if "_error" in outline_data:
            # JSON格式错误，fallback到文本搜索
            try:
                with open(outline_path, 'r', encoding='utf-8') as f:
                    outline_text = f.read()
            except Exception as e:
                result = create_check_item_result(
                    "skip", "前置条件失败（outline.json读取失败）",
                    f"无法读取 {paths[1]}: {str(e)}"
                )
                result["dependency_failure"] = True
                return result
        else:
            # JSON合法，转为文本搜索
            import json
            outline_text = json.dumps(outline_data, ensure_ascii=False)

        # 检查每个角色是否在大纲中出现
        found_characters = []
        missing_characters = []

        for name in character_names:
            if name in outline_text:
                found_characters.append(name)
            else:
                missing_characters.append(name)

        # 判断结果
        if not missing_characters:
            return create_check_item_result(
                "pass", "所有主要角色都在大纲中规划",
                f"找到 {len(found_characters)} 个主要角色: {', '.join(found_characters)}"
            )
        else:
            return create_check_item_result(
                "fail", "部分主要角色未在大纲中规划",
                f"找到 {len(found_characters)} 个角色: {', '.join(found_characters)}; 缺失 {len(missing_characters)} 个角色: {', '.join(missing_characters)}"
            )

    def _check_main_characters_in_chapters(self, paths: List[str]) -> Dict:
        """检查主要角色是否在正文章节中出现"""
        # 第一个路径应该是characters.json
        characters_path = self.work_dir / paths[0]
        chapters_pattern = paths[1]  # 可能是"workspace/chapters/"

        # 容错处理
        if not characters_path.exists() and paths[0].startswith("workspace/"):
            nested_path = paths[0].replace("workspace/", "workspace/workspace/", 1)
            characters_path = self.work_dir / nested_path

        # 检查characters.json存在性
        if not characters_path.exists():
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json不存在）",
                f"文件 {paths[0]} 不存在"
            )
            result["dependency_failure"] = True
            return result

        # 读取characters.json
        characters_data = self._load_json_file(characters_path)
        if "_error" in characters_data:
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json读取失败）",
                f"无法读取 {paths[0]}: {characters_data['_error']}"
            )
            result["dependency_failure"] = True
            return result

        # 提取主要角色名
        if not isinstance(characters_data, dict):
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json schema不合规）",
                f"characters.json顶层不是dict，而是{type(characters_data).__name__}"
            )
            result["dependency_failure"] = True
            result["schema_violation"] = True
            return result
        main_characters = characters_data.get("main_characters", [])
        if not main_characters:
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json schema不合规）",
                "main_characters字段为空或不存在，实际顶层字段: " + ", ".join(list(characters_data.keys())[:5])
            )
            result["dependency_failure"] = True
            result["schema_violation"] = True
            return result

        character_names = [char.get("name", "") for char in main_characters if isinstance(char, dict)]
        if not character_names:
            result = create_check_item_result(
                "skip", "前置条件失败（characters.json schema不合规）",
                "main_characters中的角色对象缺少name字段"
            )
            result["dependency_failure"] = True
            result["schema_violation"] = True
            return result

        # 匹配章节文件（容错处理）
        if chapters_pattern.endswith('/'):
            chapters_pattern = chapters_pattern + '*.md'

        chapters_files = self._glob_files(chapters_pattern)

        if not chapters_files:
            result = create_check_item_result(
                "skip", "前置条件失败（章节文件不存在）",
                f"模式 '{paths[1]}' 未匹配任何章节文件"
            )
            result["dependency_failure"] = True
            return result

        # 读取所有章节内容
        all_chapters_text = ""
        for chapter_file in chapters_files:
            try:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    all_chapters_text += f.read() + "\n"
            except Exception as e:
                # 单个文件读取失败不影响整体
                pass

        if not all_chapters_text:
            result = create_check_item_result(
                "skip", "前置条件失败（章节内容读取失败）",
                f"无法读取章节文件内容"
            )
            result["dependency_failure"] = True
            return result

        # 检查每个角色是否在章节中出现
        found_characters = []
        missing_characters = []

        for name in character_names:
            if name in all_chapters_text:
                found_characters.append(name)
            else:
                missing_characters.append(name)

        # 判断结果
        if not missing_characters:
            return create_check_item_result(
                "pass", "所有主要角色都在正文中出现",
                f"在 {len(chapters_files)} 个章节中找到 {len(found_characters)} 个主要角色: {', '.join(found_characters)}"
            )
        else:
            return create_check_item_result(
                "fail", "部分主要角色未在正文中出现",
                f"在 {len(chapters_files)} 个章节中找到 {len(found_characters)} 个角色: {', '.join(found_characters)}; 缺失 {len(missing_characters)} 个角色: {', '.join(missing_characters)}"
            )

    def _check_attribute_value(self, data: Dict, attribute_key: str, expected_value: Any) -> Dict:
        """检查属性值是否符合预期"""
        # 支持JSONPath语法，如 "hooks[*].length"
        if "[*]" in attribute_key:
            # 数组元素检查
            parts = attribute_key.split("[*].")
            array_field = parts[0]
            item_field = parts[1] if len(parts) > 1 else None

            array_value = self._get_nested_value(data, array_field)
            if not isinstance(array_value, list):
                return {"pass": False, "message": f"{array_field} 不是数组"}

            if item_field:
                # 检查数组中每个元素的字段
                for i, item in enumerate(array_value):
                    item_value = item.get(item_field) if isinstance(item, dict) else None
                    if not self._value_matches_constraint(item_value, expected_value):
                        return {
                            "pass": False,
                            "message": f"{array_field}[{i}].{item_field} = {item_value}，不符合约束 {expected_value}"
                        }
                return {
                    "pass": True,
                    "message": f"数组 {array_field} 的所有元素 {item_field} 都符合约束"
                }
            else:
                # 检查数组本身
                if self._value_matches_constraint(array_value, expected_value):
                    return {"pass": True, "message": f"{array_field} 符合约束"}
                else:
                    return {"pass": False, "message": f"{array_field} 不符合约束 {expected_value}"}

        else:
            # 简单字段检查
            actual_value = self._get_nested_value(data, attribute_key)
            if self._value_matches_constraint(actual_value, expected_value):
                return {
                    "pass": True,
                    "message": f"{attribute_key} = {actual_value}，符合预期"
                }
            else:
                return {
                    "pass": False,
                    "message": f"{attribute_key} = {actual_value}，期望 {expected_value}"
                }

    def _get_nested_value(self, data: Dict, key_path: str) -> Any:
        """获取嵌套字段值，支持点号路径"""
        keys = key_path.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value

    def _value_matches_constraint(self, actual_value: Any, constraint: Any) -> bool:
        """检查值是否匹配约束（支持组合约束）"""
        if isinstance(constraint, dict):
            # 复杂约束 - 改用AND逻辑支持组合约束
            all_checks_pass = True

            # 1. regex约束（互斥的，不与其他约束组合）
            if "regex" in constraint:
                pattern = constraint["regex"]
                if not isinstance(actual_value, str):
                    return False
                import re
                return bool(re.match(pattern, actual_value))

            # 2. 数值范围约束（互斥的）
            if "min" in constraint and "max" in constraint:
                if actual_value is None:
                    return False
                if not isinstance(actual_value, (int, float)):
                    return False
                if not (constraint["min"] <= actual_value <= constraint["max"]):
                    return False
                # 注意：这里不直接return，允许与其他约束组合

            # 3. contains_value约束（互斥的）
            if "contains_value" in constraint:
                target_value = constraint["contains_value"]
                min_count = constraint.get("min_count", 1)

                if isinstance(min_count, str) and min_count.startswith("{{"):
                    pass  # 占位符，跳过检查
                elif isinstance(actual_value, list):
                    count = sum(1 for item in actual_value if item == target_value)
                    if count < int(min_count):
                        return False
                else:
                    return False

            # 4. 数组相关约束（可以组合）
            if "array_min_length" in constraint:
                if not isinstance(actual_value, list) or len(actual_value) < constraint["array_min_length"]:
                    return False

            if "array_max_length" in constraint:
                if not isinstance(actual_value, list) or len(actual_value) > constraint["array_max_length"]:
                    return False

            if "array_item_type" in constraint:
                expected_type = constraint["array_item_type"]
                if not isinstance(actual_value, list):
                    return False

                type_valid = False
                if expected_type == "dict" or expected_type == "object":
                    type_valid = all(isinstance(item, dict) for item in actual_value)
                elif expected_type == "str" or expected_type == "string":
                    type_valid = all(isinstance(item, str) for item in actual_value)
                elif expected_type == "int" or expected_type == "integer":
                    type_valid = all(isinstance(item, int) for item in actual_value)
                elif expected_type == "float" or expected_type == "number":
                    type_valid = all(isinstance(item, (int, float)) for item in actual_value)

                if not type_valid:
                    return False

            # 5. enum约束（可以与array_item_type组合）
            if "enum" in constraint:
                enum_values = constraint["enum"]

                # 占位符跳过
                if isinstance(enum_values, str) and enum_values.startswith("{{"):
                    pass
                else:
                    # 如果是数组，检查每个元素是否在枚举中
                    if isinstance(actual_value, list):
                        if not all(item in enum_values for item in actual_value):
                            return False
                    else:
                        # 单个值
                        if actual_value not in enum_values:
                            return False

            # 所有约束检查都通过
            return True
        else:
            # 简单相等检查
            return actual_value == constraint

    def check_create_operation_verified(self, check_item: Dict) -> Dict:
        """
        检查文件创建数量

        check_item示例:
        {
            "check_type": "create_operation_verified",
            "params": {
                "entity_type": "file",
                "filter_conditions": {"path_pattern": "workspace/characters/*.json"},
                "min_count": 4
            }
        }
        """
        params = check_item.get("params", {})
        entity_type = params.get("entity_type")
        filter_conditions = params.get("filter_conditions", {})
        min_count = params.get("min_count")
        max_count = params.get("max_count")
        expected_count = params.get("expected_count")

        if entity_type != "file":
            return create_check_item_result(
                "skip", "不支持的entity_type",
                f"当前仅支持entity_type='file'，收到：{entity_type}"
            )

        path_pattern = filter_conditions.get("path_pattern")
        if not path_pattern:
            return create_check_item_result(
                "fail", "缺少path_pattern",
                "filter_conditions中必须指定path_pattern"
            )

        # 匹配文件
        files = self._glob_files(path_pattern)
        actual_count = len(files)

        # 检查数量约束
        if expected_count is not None:
            # expected_count可能是占位符或动态值
            if isinstance(expected_count, str):
                if expected_count.startswith("{{"):
                    # 占位符，跳过检查
                    return create_check_item_result(
                        "skip", "expected_count为占位符",
                        f"expected_count={expected_count}，需要Sample Generator替换"
                    )
                elif expected_count == "dynamic":
                    # 动态值，跳过检查
                    return create_check_item_result(
                        "skip", "expected_count为dynamic",
                        "expected_count为dynamic，需要从模板参数获取"
                    )

            expected_count = int(expected_count)
            if actual_count == expected_count:
                return create_check_item_result(
                    "pass", "文件数量匹配",
                    f"匹配 {actual_count} 个文件，符合期望 {expected_count}"
                )
            else:
                return create_check_item_result(
                    "fail", "文件数量不匹配",
                    f"匹配 {actual_count} 个文件，期望 {expected_count}"
                )

        # 检查min_count
        if min_count is not None:
            if actual_count >= min_count:
                return create_check_item_result(
                    "pass", "文件数量满足最小要求",
                    f"匹配 {actual_count} 个文件，≥ {min_count}"
                )
            else:
                return create_check_item_result(
                    "fail", "文件数量不足",
                    f"匹配 {actual_count} 个文件，< {min_count}"
                )

        # 检查max_count
        if max_count is not None:
            if actual_count <= max_count:
                return create_check_item_result(
                    "pass", "文件数量满足最大限制",
                    f"匹配 {actual_count} 个文件，≤ {max_count}"
                )
            else:
                return create_check_item_result(
                    "fail", "文件数量超出限制",
                    f"匹配 {actual_count} 个文件，> {max_count}"
                )

        return create_check_item_result(
            "skip", "未指定数量约束",
            "未指定expected_count/min_count/max_count"
        )


# =========================================
# 3. JSON Schema检查器
# =========================================


# =========================================
# 3. JSONSchemaChecker类
# =========================================

class JSONSchemaChecker:
    """JSON Schema验证器"""

    def __init__(self, work_dir: str):
        self.work_dir = Path(work_dir)

    def check(self, params: Dict) -> Dict:
        """
        验证JSON文件结构

        params示例:
        {
            "file_pattern": "workspace/characters/*.json",
            "required_fields": ["character_name", "identity", "gap"]
        }
        """
        file_pattern = params.get("file_pattern")
        required_fields = params.get("required_fields", [])

        if not file_pattern:
            return create_check_item_result(
                "fail", "缺少file_pattern", ""
            )

        # 匹配文件（容错处理workspace路径嵌套）
        full_pattern = str(self.work_dir / file_pattern)
        matched_files = glob_module.glob(full_pattern)

        # 容错处理：如果没有匹配且pattern以workspace/开头，尝试嵌套路径
        if not matched_files and file_pattern.startswith("workspace/"):
            nested_pattern = file_pattern.replace("workspace/", "workspace/workspace/", 1)
            full_nested_pattern = str(self.work_dir / nested_pattern)
            matched_files = glob_module.glob(full_nested_pattern)

        if not matched_files:
            return create_check_item_result(
                "fail", "未找到匹配文件",
                f"模式 '{file_pattern}' 未匹配任何文件"
            )

        # 检查每个文件
        all_pass = True
        details_list = []

        for file_path in matched_files:
            file_path = Path(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                missing_fields = [field for field in required_fields if field not in data]

                if missing_fields:
                    all_pass = False
                    details_list.append(f"{file_path.name}: 缺少字段 {missing_fields}")
                else:
                    details_list.append(f"{file_path.name}: 字段完整")

            except json.JSONDecodeError as e:
                all_pass = False
                details_list.append(f"{file_path.name}: JSON格式不合法（行{e.lineno}列{e.colno}）")
            except Exception as e:
                all_pass = False
                details_list.append(f"{file_path.name}: 读取失败 - {str(e)}")

        if all_pass:
            return create_check_item_result(
                "pass", "所有文件结构完整",
                "; ".join(details_list)
            )
        else:
            return create_check_item_result(
                "fail", "部分文件结构不完整",
                "; ".join(details_list)
            )


# =========================================
# 4. 跨文件一致性检查器
# =========================================


# =========================================
# 4. CrossFileConsistencyChecker类
# =========================================

class CrossFileConsistencyChecker:
    """跨文件一致性检查器"""

    def __init__(self, work_dir: str):
        self.work_dir = Path(work_dir)

    def _glob_files_tolerant(self, pattern: str) -> list:
        """容错的glob匹配（处理workspace路径嵌套）"""
        matched_files = glob_module.glob(pattern)

        # 容错：如果没匹配且pattern包含workspace/，尝试workspace/workspace/
        if not matched_files and "workspace/" in pattern:
            nested_pattern = pattern.replace("workspace/", "workspace/workspace/", 1)
            matched_files = glob_module.glob(nested_pattern)

        return matched_files

    def check(self, params: Dict) -> Dict:
        """
        检查跨文件引用一致性

        params示例:
        {
            "source_files": "workspace/outlines/*.json",
            "source_field": "characters_involved",
            "reference_files": "workspace/characters/*.json",
            "reference_field": "character_name"
        }
        """
        match_type = params.get("match_type")

        if match_type == "count":
            # 文件数量一致性检查
            return self._check_count_consistency(params)
        elif match_type == "field_value":
            # 字段值一致性检查
            return self._check_field_value_consistency(params)
        else:
            # 默认：引用一致性检查
            return self._check_reference_consistency(params)

    def _check_count_consistency(self, params: Dict) -> Dict:
        """检查两个目录的文件数量是否一致"""
        dir1 = params.get("dir1")
        dir2 = params.get("dir2")

        if not dir1 or not dir2:
            return create_check_item_result(
                "fail", "缺少目录参数", "需要dir1和dir2参数"
            )

        pattern1 = str(self.work_dir / dir1 / "*.json")
        pattern2 = str(self.work_dir / dir2 / "*.json")

        files1 = self._glob_files_tolerant(pattern1)
        files2 = self._glob_files_tolerant(pattern2)

        count1 = len(files1)
        count2 = len(files2)

        if count1 == count2:
            return create_check_item_result(
                "pass", "文件数量一致",
                f"{dir1}: {count1}个文件，{dir2}: {count2}个文件"
            )
        else:
            return create_check_item_result(
                "fail", "文件数量不一致",
                f"{dir1}: {count1}个文件，{dir2}: {count2}个文件"
            )

    def _check_field_value_consistency(self, params: Dict) -> Dict:
        """检查对应文件的字段值是否一致"""
        file1_pattern = params.get("file1_pattern")
        file1_field = params.get("file1_field")
        file2_pattern = params.get("file2_pattern")
        file2_field = params.get("file2_field")
        operation = params.get("operation", "equals")

        if not all([file1_pattern, file1_field, file2_pattern, file2_field]):
            return create_check_item_result(
                "fail", "缺少参数",
                "需要file1_pattern, file1_field, file2_pattern, file2_field"
            )

        # 提取文件编号模式（如 episode_{N}.json）
        # 简化实现：假设文件名包含编号
        import re

        # 获取所有匹配的文件对
        pattern1_glob = file1_pattern.replace("{N}", "*")
        pattern2_glob = file2_pattern.replace("{N}", "*")

        full_pattern1 = str(self.work_dir / pattern1_glob)
        full_pattern2 = str(self.work_dir / pattern2_glob)

        # 使用数字排序而非字典序排序，避免episode_10排在episode_2前面
        # 见unified_scenario_design.yaml的checker_config.implementation_notes
        def extract_episode_number(filepath):
            """从文件路径中提取episode编号进行数字排序"""
            match = re.search(r'episode_(\d+)', filepath)
            return int(match.group(1)) if match else 0

        files1 = sorted(self._glob_files_tolerant(full_pattern1), key=extract_episode_number)
        files2 = sorted(self._glob_files_tolerant(full_pattern2), key=extract_episode_number)

        if len(files1) != len(files2):
            return create_check_item_result(
                "fail", "文件数量不匹配",
                f"file1匹配{len(files1)}个，file2匹配{len(files2)}个"
            )

        all_pass = True
        has_parse_error = False  # 标记是否存在文件解析失败
        details_list = []

        for file1, file2 in zip(files1, files2):
            try:
                # 读取并解析两个文件（JSON格式不合法时直接失败）
                with open(file1, 'r', encoding='utf-8') as f:
                    data1 = json.load(f)
                with open(file2, 'r', encoding='utf-8') as f:
                    data2 = json.load(f)

                value1 = data1.get(file1_field)
                value2 = data2.get(file2_field)

                # 比较值
                if operation == "count":
                    # value2应该是数组，比较长度
                    if isinstance(value2, list):
                        value2 = len(value2)

                    if value1 == value2:
                        details_list.append(
                            f"{Path(file1).name}: {file1_field}={value1} == len({file2_field})={value2}"
                        )
                    else:
                        all_pass = False
                        details_list.append(
                            f"{Path(file1).name}: {file1_field}={value1} != len({file2_field})={value2}"
                        )
                else:
                    if value1 == value2:
                        details_list.append(f"{Path(file1).name}: 一致")
                    else:
                        all_pass = False
                        details_list.append(f"{Path(file1).name}: 不一致")

            except json.JSONDecodeError as e:
                all_pass = False
                has_parse_error = True  # 标记为解析错误
                details_list.append(f"{Path(file1).name}: JSON格式不合法（行{e.lineno}列{e.colno}）")
            except Exception as e:
                all_pass = False
                has_parse_error = True  # 标记为解析错误
                details_list.append(f"{Path(file1).name}: 检查失败 - {str(e)}")

        full_detail = "; ".join(details_list)

        if all_pass:
            return create_check_item_result(
                "pass", "所有文件字段值一致",
                full_detail
            )
        else:
            # 如果存在文件解析失败，返回特殊结果标记依赖失败
            if has_parse_error:
                result = create_check_item_result(
                    "skip", "前置条件失败（文件解析错误）",
                    full_detail
                )
                result["_is_dependency_failure"] = True  # 添加内部标记
                return result
            else:
                return create_check_item_result(
                    "fail", "部分文件字段值不一致",
                    full_detail
                )

    def _check_reference_consistency(self, params: Dict) -> Dict:
        """检查引用字段的值是否在参考文件中存在"""
        source_files = params.get("source_files")
        source_field = params.get("source_field")
        reference_files = params.get("reference_files")
        reference_field = params.get("reference_field")

        if not all([source_files, source_field, reference_files, reference_field]):
            return create_check_item_result(
                "fail", "缺少参数",
                "需要source_files, source_field, reference_files, reference_field"
            )

        # 加载参考文件，构建有效值集合
        ref_pattern = str(self.work_dir / reference_files)
        ref_files = self._glob_files_tolerant(ref_pattern)

        if not ref_files:
            return create_check_item_result(
                "fail", "未找到参考文件",
                f"模式 '{reference_files}' 未匹配任何文件"
            )

        valid_values = set()
        invalid_ref_files = []

        # 第一步：从所有参考文件提取valid_values（只处理JSON合法的）
        for ref_file in ref_files:
            try:
                with open(ref_file, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                try:
                    data = json.loads(raw_content)

                    # 支持嵌套字段提取（如 scenes_detail[*].characters）
                    if "[*]" in reference_field:
                        parts = reference_field.split("[*].")
                        array_field = parts[0]
                        item_field = parts[1] if len(parts) > 1 else None

                        array_data = self._get_nested_value(data, array_field)
                        if array_data is None:
                            # 字段缺失，标记为无法提取
                            invalid_ref_files.append(f"{Path(ref_file).name}(缺少字段{array_field})")
                        elif isinstance(array_data, list):
                            for item in array_data:
                                if isinstance(item, dict) and item_field:
                                    values = item.get(item_field, [])
                                    if isinstance(values, list):
                                        valid_values.update(values)
                                    elif values:
                                        valid_values.add(values)
                    else:
                        # 简单字段
                        value = data.get(reference_field)
                        if value:
                            if isinstance(value, list):
                                valid_values.update(value)
                            else:
                                valid_values.add(value)

                except json.JSONDecodeError as e:
                    # JSON格式错误，标记但继续
                    invalid_ref_files.append(f"{Path(ref_file).name}(JSON格式不合法)")

            except Exception as e:
                invalid_ref_files.append(f"{Path(ref_file).name}(读取失败)")

        # 第二步：如果有valid_values，对JSON错误的参考文件用字符串搜索补充
        if valid_values and invalid_ref_files:
            for ref_file in ref_files:
                if any(Path(ref_file).name in err for err in invalid_ref_files):
                    try:
                        with open(ref_file, 'r', encoding='utf-8') as f:
                            raw_content = f.read()

                        # 简单字符串搜索
                        found = self._simple_text_search(raw_content, valid_values)
                        if found:
                            valid_values.update(found)
                            # 更新标记：成功fallback
                            for i, err in enumerate(invalid_ref_files):
                                if Path(ref_file).name in err:
                                    invalid_ref_files[i] = f"{Path(ref_file).name}(JSON格式不合法,文本模式找到{len(found)}个)"
                                    break
                    except Exception:
                        pass

        # 如果参考文件都无法读取，标记为dependency_failure
        if invalid_ref_files and not valid_values:
            result = create_check_item_result(
                "skip", "前置条件失败（参考文件无法提取数据）",
                f"无法从参考文件中提取有效值。问题文件: {', '.join(invalid_ref_files)}"
            )
            result["_is_dependency_failure"] = True
            return result

        # 记录跳过的参考文件信息（用于最终报告）
        skipped_ref_info = ""
        if invalid_ref_files:
            skipped_ref_info = f" [跳过{len(invalid_ref_files)}个参考文件: {', '.join(invalid_ref_files)}]"

        # 检查源文件中的引用
        src_pattern = str(self.work_dir / source_files)
        src_files = self._glob_files_tolerant(src_pattern)

        if not src_files:
            return create_check_item_result(
                "fail", "未找到源文件",
                f"模式 '{source_files}' 未匹配任何文件"
            )

        all_pass = True
        details_list = []
        skipped_src_files = []  # 记录跳过的源文件

        for src_file in src_files:
            try:
                with open(src_file, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                # 尝试解析JSON
                try:
                    data = json.loads(raw_content)

                    # 处理嵌套字段（如 scenes_detail[*].characters）
                    if "[*]" in source_field:
                        parts = source_field.split("[*].")
                        array_field = parts[0]
                        item_field = parts[1] if len(parts) > 1 else None

                        array_data = self._get_nested_value(data, array_field)
                        if isinstance(array_data, list):
                            for item in array_data:
                                if isinstance(item, dict) and item_field:
                                    values = item.get(item_field, [])
                                    if isinstance(values, list):
                                        invalid = [v for v in values if v not in valid_values]
                                        if invalid:
                                            all_pass = False
                                            details_list.append(f"{Path(src_file).name}: 引用了不存在的值 {invalid}")
                    else:
                        # 简单字段
                        values = data.get(source_field, [])
                        if not isinstance(values, list):
                            values = [values]

                        invalid = [v for v in values if v and v not in valid_values]
                        if invalid:
                            all_pass = False
                            details_list.append(f"{Path(src_file).name}: 引用了不存在的值 {invalid}")

                    if all_pass or not details_list:
                        details_list.append(f"{Path(src_file).name}: 引用一致")

                except json.JSONDecodeError as e:
                    # JSON格式错误，fallback到简单字符串搜索
                    found = self._simple_text_search(raw_content, valid_values)

                    if found:
                        # 检查找到的值是否都在valid_values中（理论上肯定在）
                        invalid = [v for v in found if v not in valid_values]
                        if invalid:
                            all_pass = False
                            skipped_src_files.append(f"{Path(src_file).name}(JSON格式不合法,文本模式)")
                            details_list.append(
                                f"{Path(src_file).name}: 引用了不存在的值 {invalid} (文本模式)"
                            )
                        else:
                            skipped_src_files.append(f"{Path(src_file).name}(JSON格式不合法,文本模式)")
                            details_list.append(f"{Path(src_file).name}: 引用一致 (文本模式)")
                    else:
                        # 无法找到任何值
                        all_pass = False
                        skipped_src_files.append(f"{Path(src_file).name}(JSON格式不合法,无法提取)")
                        details_list.append(f"{Path(src_file).name}: JSON格式不合法，无法提取字段内容")

            except Exception as e:
                all_pass = False
                skipped_src_files.append(f"{Path(src_file).name}(检查失败)")
                details_list.append(f"{Path(src_file).name}: 检查失败 - {str(e)}")

        # 构建完整的详情报告
        skipped_src_info = ""
        if skipped_src_files:
            skipped_src_info = f" [跳过{len(skipped_src_files)}个源文件: {', '.join(skipped_src_files)}]"

        full_detail = "; ".join(details_list) + skipped_ref_info + skipped_src_info

        if all_pass:
            return create_check_item_result(
                "pass", "所有引用一致",
                full_detail
            )
        else:
            return create_check_item_result(
                "fail", "存在无效引用",
                full_detail
            )

    def _get_nested_value(self, data: Dict, key_path: str) -> Any:
        """获取嵌套字段值"""
        keys = key_path.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value

    def _simple_text_search(self, raw_content: str, known_values: set) -> set:
        """
        简单字符串搜索（用于引用一致性检查的fallback）

        Args:
            raw_content: 原始文本内容
            known_values: 已知值集合（如角色名）

        Returns:
            找到的值集合
        """
        found = set()
        for value in known_values:
            # 搜索引号中的值
            if f'"{value}"' in raw_content or f"'{value}'" in raw_content:
                found.add(value)
        return found


# =========================================
# 5. 工具调用检查器（复用示例代码）
# =========================================


# =========================================
# 5. ToolCalledWithParamsChecker类
# =========================================

class ToolCalledWithParamsChecker:
    """工具调用参数检查器"""

    def __init__(self, work_dir: str = None):
        """
        Args:
            work_dir: 工作目录，用于skip_if_file_not_exists检查
        """
        self.work_dir = Path(work_dir) if work_dir else None

    def check(self, params: Dict, conversation_history: List[Dict]) -> Dict:
        """检查工具是否以正确参数被调用"""
        tool_name = params.get("tool_name")
        expected_params = params.get("expected_params", {})
        min_count = params.get("min_count", 1)
        skip_if_file_not_exists = params.get("skip_if_file_not_exists", False)

        print(f"\n[DEBUG] ToolCalledWithParamsChecker: tool_name={tool_name}", flush=True)
        print(f"[DEBUG] expected_params={expected_params}", flush=True)
        print(f"[DEBUG] min_count={min_count}", flush=True)
        print(f"[DEBUG] skip_if_file_not_exists={skip_if_file_not_exists}", flush=True)

        # 如果设置了skip_if_file_not_exists，先检查目标文件是否存在
        if skip_if_file_not_exists and self.work_dir:
            file_path = expected_params.get("path", "")
            if file_path:
                full_path = self.work_dir / file_path
                print(f"[DEBUG] Checking file existence: {full_path}", flush=True)
                if not full_path.exists():
                    print(f"[DEBUG] File not exists, skipping check", flush=True)
                    return create_check_item_result(
                        "skip", "环境中不存在该文件（skip_if_file_not_exists）",
                        f"文件 {file_path} 在当前环境中不存在，跳过此检查项"
                    )

        param_match_mode = params.get("param_match_mode", "exact")  # exact | contains

        # 从对话历史中查找工具调用
        matched_count = 0
        found_calls = []  # 记录找到的所有调用
        for message in conversation_history:
            if message.get("role") == "assistant" and "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    if tool_call.get("function", {}).get("name") == tool_name:
                        arguments = tool_call.get("function", {}).get("arguments", {})
                        if isinstance(arguments, str):
                            try:
                                arguments = json.loads(arguments)
                            except json.JSONDecodeError:
                                continue

                        found_calls.append(arguments)
                        print(f"[DEBUG] Found {tool_name} call with arguments: {arguments}", flush=True)

                        # 检查参数匹配（None作为通配符）
                        if param_match_mode == "contains":
                            # 子串匹配：检查参数值中是否包含期望的子串
                            matched = all(
                                v is None or str(v).lower() in str(arguments.get(k, "")).lower()
                                for k, v in expected_params.items()
                            )
                        else:
                            # 精确匹配（默认）
                            matched = all(
                                arguments.get(k) == v
                                for k, v in expected_params.items()
                                if v is not None
                            )

                        print(f"[DEBUG] Matching result: {matched}", flush=True)
                        if not matched:
                            print(f"[DEBUG] Mismatch details:", flush=True)
                            for k, v in expected_params.items():
                                if v is not None:
                                    actual_v = arguments.get(k)
                                    print(f"[DEBUG]   expected[{k}]={v}, actual[{k}]={actual_v}, match={actual_v==v}", flush=True)

                        if matched:
                            matched_count += 1

        print(f"[DEBUG] Total found {len(found_calls)} calls, matched {matched_count} calls", flush=True)

        if matched_count >= min_count:
            return create_check_item_result(
                "pass", "工具调用参数匹配",
                f"工具 '{tool_name}' 使用正确参数调用 {matched_count} 次"
            )
        else:
            return create_check_item_result(
                "fail", "工具未被调用或参数不匹配",
                f"工具 '{tool_name}' 匹配调用 {matched_count} 次，期望 ≥{min_count}"
            )


class ToolCallAbsenceChecker:
    """工具调用缺失检查器"""

    def check(self, params: Dict, conversation_history: List[Dict]) -> Dict:
        """检查指定的工具是否没有被调用"""
        forbidden_tools = params.get("forbidden_tools", [])

        called_forbidden_tools = []
        for message in conversation_history:
            if message.get("role") == "assistant" and "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    tool_name = tool_call.get("function", {}).get("name", "")
                    if tool_name in forbidden_tools:
                        called_forbidden_tools.append(tool_name)

        if not called_forbidden_tools:
            return create_check_item_result(
                "pass", "未调用禁止工具",
                f"Agent正确地没有调用禁止的工具: {forbidden_tools}"
            )
        else:
            return create_check_item_result(
                "fail", "调用了禁止工具",
                f"Agent调用了禁止的工具: {called_forbidden_tools}"
            )


# =========================================
# 6. 语义检查器
# =========================================


# =========================================
# 6. SemanticChecker类
# =========================================

class SemanticChecker:
    """语义检查器（支持response和文件字段）"""

    def __init__(self, work_dir: str, model_name=None, api_base=None, api_key=None):
        self.work_dir = Path(work_dir)
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key

    def check(self, params: Dict, result_data: Dict) -> Dict:
        """执行语义检查"""
        # 智能判断检查类型：
        # 1. 如果有analysis_target，说明要检查文件内容
        # 2. 否则使用target_type参数
        if "analysis_target" in params:
            target_type = "file_content_raw"  # 使用文件内容检查
        else:
            target_type = params.get("target_type", "response")

        use_raw_content = params.get("use_raw_content", False)  # 新增参数

        # 当use_raw_content=True时，强制使用raw content模式（解耦版本）
        if use_raw_content or target_type == "file_content_raw":
            return self._check_file_content_raw(params)

        if target_type == "response":
            return self._check_response(params, result_data)
        elif target_type == "file_field":
            return self._check_file_field(params)
        elif target_type == "file_content":
            return self._check_file_content(params)
        else:
            return create_check_item_result(
                "skip", f"不支持的target_type: {target_type}", ""
            )

    def _check_response(self, params: Dict, result_data: Dict) -> Dict:
        """检查Agent回复的语义"""
        expected_keywords = params.get("expected_keywords", [])
        use_llm = params.get("use_llm_judge", False)
        llm_judge_criteria = load_judge_criteria_from_params(params, self.work_dir)
        response = result_data.get("response", "")

        if not response:
            return create_check_item_result(
                "fail", "无响应内容", "result_data中没有响应内容"
            )

        # 尝试LLM语义判断
        if use_llm and self.model_name and self.api_base and self.api_key:
            try:
                # 构造LLM prompt
                prompt = f"""
请评估以下Agent回复是否满足业务需求：

**业务要求：** {llm_judge_criteria}
**期望关键信息：** {expected_keywords}
**Agent回复：** {response}

请评估关键信息覆盖度（0-100分）：
- 90-100分：完全满足业务要求，包含所有关键信息
- 70-89分：满足主要业务要求，包含主要关键信息
- 50-69分：部分满足业务要求
- 0-49分：不满足业务要求，缺少重要关键信息

评估标准：
1. 不要求精确的字符串匹配，而是语义相似性匹配
2. 考虑同义词、近义词和语义等价表达
3. 重点关注业务需求是否被满足

请以JSON格式回复：
{{"score": 85, "matched_keywords": ["匹配的关键信息"], "missing_keywords": ["缺失的关键信息"], "explanation": "详细说明"}}
"""

                success, llm_response = request_llm_with_litellm(
                    [{"role": "user", "content": prompt}],
                    self.model_name,
                    self.api_base,
                    self.api_key
                )

                if success:
                    try:
                        llm_result = safe_json_extract_single(llm_response)
                        score = llm_result.get("score", 0)
                        matched_keywords = llm_result.get("matched_keywords", [])
                        missing_keywords = llm_result.get("missing_keywords", [])
                        explanation = llm_result.get("explanation", "")

                        # 分数>=75认为通过
                        passed = score >= 75

                        if passed:
                            return create_check_item_result(
                                "pass", "语义匹配",
                                f"LLM评分: {score}/100. 匹配关键词: {matched_keywords}. {explanation}"
                            )
                        else:
                            return create_check_item_result(
                                "fail", "语义不匹配",
                                f"LLM评分: {score}/100. 缺失关键词: {missing_keywords}. {explanation}"
                            )
                    except Exception as parse_e:
                        # LLM响应解析失败,fallback到关键词匹配
                        pass
            except Exception:
                # LLM调用失败,fallback到关键词匹配
                pass

        # Fallback: 关键词匹配逻辑
        found = [kw for kw in expected_keywords if kw in response]

        # 至少包含一个关键词即可通过
        if found:
            return create_check_item_result(
                "pass", "包含期望关键词",
                f"响应包含: {found}"
            )
        else:
            return create_check_item_result(
                "fail", "缺少关键词",
                f"响应缺少所有关键词: {expected_keywords}"
            )

    def _check_file_field(self, params: Dict) -> Dict:
        """检查文件字段的语义"""
        file_pattern = params.get("file_pattern")
        field_path = params.get("field_path")
        expected_keywords = params.get("expected_keywords", [])
        llm_judge_criteria = load_judge_criteria_from_params(params, self.work_dir)
        min_count = params.get("min_count", 1)
        use_llm = params.get("use_llm_judge", False)

        if not file_pattern or not field_path:
            return create_check_item_result(
                "fail", "缺少参数", "需要file_pattern和field_path"
            )

        # 匹配文件（容错处理workspace路径嵌套）
        full_pattern = str(self.work_dir / file_pattern)
        matched_files = glob_module.glob(full_pattern)

        # 容错处理：如果没有匹配且pattern以workspace/开头，尝试嵌套路径
        if not matched_files and file_pattern.startswith("workspace/"):
            nested_pattern = file_pattern.replace("workspace/", "workspace/workspace/", 1)
            full_nested_pattern = str(self.work_dir / nested_pattern)
            matched_files = glob_module.glob(full_nested_pattern)

        if not matched_files:
            return create_check_item_result(
                "fail", "未找到匹配文件",
                f"模式 '{file_pattern}' 未匹配任何文件"
            )

        # 检查每个文件的字段
        matched_count = 0
        details_list = []

        for file_path in matched_files:
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                # 尝试解析JSON
                try:
                    data = json.loads(raw_content)
                    json_valid = True

                    # 支持JSONPath的[*]语法（如：hooks[*].hook_text）
                    if "[*]" in field_path:
                        # 分割array_field和item_field
                        parts = field_path.split("[*].")
                        array_field = parts[0]
                        item_field = parts[1] if len(parts) > 1 else None

                        # 获取数组
                        array_value = self._get_nested_value(data, array_field)
                        if not isinstance(array_value, list):
                            details_list.append(f"{Path(file_path).name}: {array_field}不是数组")
                            continue

                        # 对数组中的每个元素进行判断
                        array_matched_count = 0
                        array_details = []

                        for idx, item in enumerate(array_value):
                            # 格式容错：支持对象数组和简单类型数组
                            # 1. 如果是dict且指定了item_field，提取字段值
                            # 2. 如果是dict但没指定item_field，使用整个对象
                            # 3. 如果是简单类型（字符串等），直接使用
                            if isinstance(item, dict):
                                if item_field:
                                    item_value = item.get(item_field)
                                else:
                                    item_value = item
                            else:
                                # 简单类型（字符串、数字等），直接使用
                                # 这样可以支持 hooks = ["文本1", "文本2"] 格式
                                item_value = item

                            if not item_value:
                                continue

                            # 尝试LLM语义判断
                            is_matched = False
                            if use_llm and llm_judge_criteria and self.model_name and self.api_base and self.api_key:
                                try:
                                    # 构造LLM prompt
                                    prompt = f"""
请判断单个字段内容是否在**语义类型**上符合业务标准。

**业务标准：** {llm_judge_criteria}
**参考关键词类型：** {expected_keywords}
**待判断的字段内容：** {item_value}

⚠️ 重要说明：
- 你只需要判断这个字段内容的**语义类型**是否匹配标准要求的类型
- 不要考虑"数量"问题（如"至少2个"），数量统计由系统完成
- 内容可能来自格式不完整的JSON，请忽略格式问题，专注语义判断

评判规则：
1. 语义匹配优先：同义词、近义词都应认可
2. 只要字段内容中**包含任何一个**符合标准类型的元素，就应判定为匹配
3. 不要因为内容中还有其他类型就判定为不匹配

请以JSON格式回复：
{{"matched": true/false, "reason": "简要说明匹配或不匹配的语义类型依据"}}
"""

                                    success, llm_response = request_llm_with_litellm(
                                        [{"role": "user", "content": prompt}],
                                        self.model_name,
                                        self.api_base,
                                        self.api_key
                                    )

                                    if success:
                                        llm_result = safe_json_extract_single(llm_response)
                                        is_matched = llm_result.get("matched", False)
                                        reason = llm_result.get("reason", "")

                                        if is_matched:
                                            array_matched_count += 1
                                            array_details.append(f"元素{idx+1}: 匹配 (LLM: {reason})")
                                        else:
                                            array_details.append(f"元素{idx+1}: 不匹配 (LLM: {reason})")
                                    else:
                                        print(f"[DEBUG] LLM调用失败: {llm_response}", flush=True)
                                        # LLM失败时fallback到关键词匹配
                                        if any(kw in str(item_value) for kw in expected_keywords):
                                            array_matched_count += 1
                                            array_details.append(f"元素{idx+1}: 匹配 (关键词)")
                                        else:
                                            array_details.append(f"元素{idx+1}: 不匹配 (关键词)")

                                except Exception as e:
                                    print(f"[DEBUG] LLM调用异常: {str(e)}", flush=True)
                                    # 异常时fallback到关键词匹配
                                    if any(kw in str(item_value) for kw in expected_keywords):
                                        array_matched_count += 1
                                        array_details.append(f"元素{idx+1}: 匹配 (关键词)")
                                    else:
                                        array_details.append(f"元素{idx+1}: 不匹配 (关键词)")
                            else:
                                # 不使用LLM，使用关键词匹配
                                if any(kw in str(item_value) for kw in expected_keywords):
                                    array_matched_count += 1
                                    array_details.append(f"元素{idx+1}: 匹配 (关键词)")
                                else:
                                    array_details.append(f"元素{idx+1}: 不匹配 (关键词)")

                        # 汇总该文件的检查结果
                        if array_matched_count > 0:
                            matched_count += 1
                            details_list.append(f"{Path(file_path).name}: {array_matched_count}/{len(array_value)}个元素匹配; " + "; ".join(array_details))
                        else:
                            details_list.append(f"{Path(file_path).name}: 0/{len(array_value)}个元素匹配; " + "; ".join(array_details))

                        continue  # 处理完该文件，继续下一个文件

                    # 不包含[*]，按原逻辑处理
                    field_value = self._get_nested_value(data, field_path)

                except json.JSONDecodeError as e:
                    # JSON格式不合法，但可以尝试语义判断
                    json_valid = False
                    field_value = None
                    # 如果是语义检查且启用了LLM，尝试从原始文本提取相关内容
                    if use_llm and llm_judge_criteria:
                        # 尝试简单提取目标字段的内容（基于字段名）
                        field_name = field_path.split('.')[-1]  # 获取最后一级字段名
                        # 搜索字段名附近的内容作为field_value
                        import re
                        pattern = rf'"{field_name}"[:\s]*"([^"]+)"'
                        match = re.search(pattern, raw_content)
                        if match:
                            field_value = match.group(1)
                        else:
                            # 如果无法提取，使用整个文件内容（截取前500字符）
                            field_value = raw_content[:500]

                if not field_value:
                    if not json_valid:
                        details_list.append(f"{Path(file_path).name}: JSON格式不合法，且无法提取字段内容")
                    continue

                # 尝试LLM语义判断
                is_matched = False
                llm_attempted = False
                if use_llm and llm_judge_criteria and self.model_name and self.api_base and self.api_key:
                    llm_attempted = True
                    try:
                        # 根据JSON是否合法调整prompt
                        data_source_note = "(原始文本提取)" if not json_valid else ""

                        # 构造LLM prompt
                        prompt = f"""
请判断单个字段内容是否在**语义类型**上符合业务标准。

**业务标准：** {llm_judge_criteria}
**参考关键词类型：** {expected_keywords}
**待判断的字段内容{data_source_note}：** {field_value}

⚠️ 重要说明：
- 你只需要判断这个字段内容的**语义类型**是否匹配标准要求的类型
- 不要考虑"数量"问题（如"至少2个角色"），数量统计由系统完成
- 你的任务是：判断这个角色的motivation是否属于指定的类型（如"隐藏类型"）
- 内容可能来自格式不完整的JSON，请忽略格式问题，专注语义判断

评判规则：
1. 语义匹配优先：同义词、近义词都应认可
   - "守护" = "保护" ✓
   - "弥补" = "赎罪" ✓
   - "寻求答案" = "寻找" ✓
2. 只要字段内容中**包含任何一个**符合标准类型的动机，就应判定为匹配
3. 不要因为内容中还有其他类型的动机就判定为不匹配

示例：
- 字段内容："守护闺蜜的幸福" → 匹配（"守护"属于"保护"类）
- 字段内容："证明自己的价值" → 不匹配（属于"自我实现"类，不在标准范围内）
- 字段内容："保护家族企业，证明自己" → 匹配（包含"保护"类动机）

请以JSON格式回复：
{{"matched": true/false, "reason": "简要说明匹配或不匹配的语义类型依据"}}
"""

                        success, llm_response = request_llm_with_litellm(
                            [{"role": "user", "content": prompt}],
                            self.model_name,
                            self.api_base,
                            self.api_key
                        )

                        if success:
                            llm_result = safe_json_extract_single(llm_response)
                            is_matched = llm_result.get("matched", False)
                            reason = llm_result.get("reason", "")

                            method_label = "LLM-文本" if not json_valid else "LLM"
                            if is_matched:
                                matched_count += 1
                                details_list.append(f"{Path(file_path).name}: 匹配 ({method_label}: {reason})")
                            else:
                                details_list.append(f"{Path(file_path).name}: 不匹配 ({method_label}: {reason})")
                            continue  # LLM判断成功，跳过关键词匹配
                        else:
                            # LLM调用失败，打印错误信息
                            print(f"[DEBUG] LLM调用失败: {llm_response}", flush=True)

                    except Exception as e:
                        # LLM调用失败，fallback到关键词匹配
                        print(f"[DEBUG] LLM调用异常: {str(e)}", flush=True)

                # Fallback: 关键词匹配（仅在LLM不可用或失败时使用）
                if any(kw in str(field_value) for kw in expected_keywords):
                    matched_count += 1
                    kw_label = "关键词-文本" if not json_valid else "关键词"
                    details_list.append(f"{Path(file_path).name}: 匹配 ({kw_label})")
                else:
                    kw_label = "关键词-文本" if not json_valid else "关键词"
                    details_list.append(f"{Path(file_path).name}: 不匹配 ({kw_label})")

            except Exception as e:
                details_list.append(f"{Path(file_path).name}: 检查失败 - {str(e)}")

        # 判断结果并标注使用的方法
        llm_used = any("LLM" in detail and "匹配" in detail for detail in details_list)
        text_mode_used = any("文本" in detail for detail in details_list)

        if llm_used:
            if text_mode_used:
                method_note = " (LLM语义判断，部分文件使用文本模式)"
            else:
                method_note = " (LLM语义判断)"
        else:
            if text_mode_used:
                method_note = " (关键词匹配，部分文件使用文本模式)"
            else:
                method_note = " (关键词匹配)"
        
        if matched_count >= min_count:
            return create_check_item_result(
                "pass", f"语义检查通过{method_note}",
                f"匹配 {matched_count}/{len(matched_files)} 个文件，≥ {min_count}; " + "; ".join(details_list)
            )
        else:
            return create_check_item_result(
                "fail", f"语义检查失败{method_note}",
                f"匹配 {matched_count}/{len(matched_files)} 个文件，< {min_count}; " + "; ".join(details_list)
            )

    def _get_nested_value(self, data: Dict, key_path: str) -> Any:
        """获取嵌套字段值"""
        keys = key_path.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value

    def _check_file_content(self, params: Dict) -> Dict:
        """检查多个文件的整体内容"""
        file_pattern = params.get("file_pattern")
        llm_judge_criteria = load_judge_criteria_from_params(params, self.work_dir)
        use_llm = params.get("use_llm_judge", False)

        if not file_pattern:
            return create_check_item_result(
                "fail", "缺少参数", "需要file_pattern"
            )

        if not use_llm or not llm_judge_criteria:
            return create_check_item_result(
                "fail", "缺少参数", "file_content检查必须启用LLM并提供llm_judge_criteria"
            )

        # 匹配文件（容错处理workspace路径嵌套）
        full_pattern = str(self.work_dir / file_pattern)
        matched_files = glob_module.glob(full_pattern)

        # 容错处理
        if not matched_files and file_pattern.startswith("workspace/"):
            nested_pattern = file_pattern.replace("workspace/", "workspace/workspace/", 1)
            full_nested_pattern = str(self.work_dir / nested_pattern)
            matched_files = glob_module.glob(full_nested_pattern)

        if not matched_files:
            return create_check_item_result(
                "fail", "未找到匹配文件",
                f"模式 '{file_pattern}' 未匹配任何文件"
            )

        # 读取所有文件内容并合并
        all_contents = []
        file_names = []
        for file_path in matched_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_contents.append(content)
                    file_names.append(Path(file_path).name)
            except Exception as e:
                return create_check_item_result(
                    "fail", "文件读取失败",
                    f"无法读取 {Path(file_path).name}: {str(e)}"
                )

        # 合并所有内容（用分隔符）
        combined_content = "\n\n=== 文件分隔 ===\n\n".join(
            [f"文件: {name}\n{content}" for name, content in zip(file_names, all_contents)]
        )

        # 如果内容过长，截取（保留前后部分）
        max_length = 30000  # LLM上下文限制
        if len(combined_content) > max_length:
            # 保留前15000和后15000字符
            combined_content = combined_content[:15000] + "\n\n... [中间内容省略] ...\n\n" + combined_content[-15000:]

        # 使用LLM评估整体内容
        if not self.model_name or not self.api_base or not self.api_key:
            return create_check_item_result(
                "fail", "LLM配置缺失", "file_content检查需要LLM配置"
            )

        try:
            # 构造LLM prompt
            prompt = f"""
请评估以下所有文件的整体质量是否符合业务标准。

**业务标准：** {llm_judge_criteria}

**文件数量：** {len(matched_files)} 个文件

**文件内容：**
{combined_content}

⚠️ 重要说明：
- 你需要评估**所有文件的整体表现**，而不是单个文件
- 关注文件之间的连贯性、一致性、整体逻辑
- 如果内容被截断，请基于可见部分进行合理推断

请以JSON格式回复：
{{"matched": true/false, "reason": "详细说明评估依据，包括具体的优点或不足"}}
"""

            success, llm_response = request_llm_with_litellm(
                [{"role": "user", "content": prompt}],
                self.model_name,
                self.api_base,
                self.api_key
            )

            if success:
                llm_result = safe_json_extract_single(llm_response)
                is_matched = llm_result.get("matched", False)
                reason = llm_result.get("reason", "")

                if is_matched:
                    return create_check_item_result(
                        "pass", "整体内容符合标准 (LLM语义判断)",
                        f"检查了 {len(matched_files)} 个文件; LLM评估: {reason}"
                    )
                else:
                    return create_check_item_result(
                        "fail", "整体内容不符合标准 (LLM语义判断)",
                        f"检查了 {len(matched_files)} 个文件; LLM评估: {reason}"
                    )
            else:
                print(f"[DEBUG] LLM调用失败: {llm_response}", flush=True)
                return create_check_item_result(
                    "fail", "LLM调用失败",
                    f"无法评估文件内容: {llm_response}"
                )

        except Exception as e:
            print(f"[DEBUG] LLM调用异常: {str(e)}", flush=True)
            return create_check_item_result(
                "fail", "检查失败",
                f"检查过程出错: {str(e)}"
            )

    def _glob_files_flexible(self, pattern: str) -> list:
        """
        灵活匹配文件，容错文件命名差异

        支持的灵活性：
        1. workspace/ 路径嵌套
        2. episode_*_script.json vs episode_*.json
        3. 最后一集的动态匹配

        Args:
            pattern: 文件匹配模式，如"workspace/scripts/episode_1_script.json"

        Returns:
            匹配的文件路径列表
        """
        # 标准匹配
        full_pattern = str(self.work_dir / pattern)
        matched_files = glob_module.glob(full_pattern)

        # 容错1: workspace路径嵌套（历史遗留兼容）
        if not matched_files and pattern.startswith("workspace/"):
            nested_pattern = pattern.replace("workspace/", "workspace/workspace/", 1)
            full_nested_pattern = str(self.work_dir / nested_pattern)
            matched_files = glob_module.glob(full_nested_pattern)

        # 容错2: 非workspace/开头的路径，尝试在workspace/下找
        # 例如：chapters/ -> workspace/chapters/
        # 这是因为v3样本中某些路径省略了workspace/前缀
        if not matched_files and not pattern.startswith("workspace/"):
            workspace_pattern = f"workspace/{pattern}"
            full_workspace_pattern = str(self.work_dir / workspace_pattern)
            matched_files = glob_module.glob(full_workspace_pattern)

        # 容错2: 剧本文件命名差异 (episode_*_script.json vs episode_*.json)
        if not matched_files and "_script.json" in pattern:
            # 尝试不带_script的模式
            alt_pattern = pattern.replace("_script.json", ".json")
            full_alt_pattern = str(self.work_dir / alt_pattern)
            matched_files = glob_module.glob(full_alt_pattern)

        # 容错3: 最后一集的动态匹配
        # 如果pattern包含具体集数但未匹配，尝试匹配现有的最后一集
        if not matched_files and "episode_" in pattern:
            import re
            # 提取目录和基础模式
            match = re.match(r"(.*/)(episode_)(\\d+)(.*\\.json)", pattern)
            if match:
                dir_path, prefix, episode_num, suffix = match.groups()
                # 尝试匹配该目录下所有集数
                wildcard_pattern = f"{dir_path}{prefix}*{suffix}"
                full_wildcard = str(self.work_dir / wildcard_pattern)
                all_episodes = glob_module.glob(full_wildcard)

                if all_episodes:
                    # 提取集数并排序
                    def extract_num(filepath):
                        m = re.search(r'episode_(\\d+)', filepath)
                        return int(m.group(1)) if m else 0

                    all_episodes_sorted = sorted(all_episodes, key=extract_num)
                    # 返回最后一集
                    matched_files = [all_episodes_sorted[-1]]

        return matched_files

    def _check_file_content_raw(self, params: Dict) -> Dict:
        """
        使用raw content进行语义检查（解耦版本）

        与_check_file_content()和_check_file_field()的区别：
        - 不解析JSON，不提取字段
        - 直接读取文件原始内容交给LLM judge（或统计字数）
        - 兼容JSON格式错误的文件
        - 灵活匹配文件名模式（支持episode_*和episode_*_script混用）

        适用场景：语义检查（吸引力、动机深度等）+ 字数统计检查
        """
        # 兼容两种参数名：file_pattern（旧）和 analysis_target（新）
        file_pattern = params.get("file_pattern") or params.get("analysis_target")
        use_llm = params.get("use_llm_judge", False)
        llm_judge_criteria = load_judge_criteria_from_params(params, self.work_dir)

        # 检查是否是不需要LLM的程序化检查类型
        validation_rules = params.get("validation_rules", [])
        is_word_count_check = False
        is_programmatic_check = False  # P1-P5程序化检查标志
        programmatic_method = None  # 具体的程序化检查方法名
        expected_range = None

        if validation_rules and isinstance(validation_rules, list) and len(validation_rules) > 0:
            first_rule = validation_rules[0]
            if isinstance(first_rule, dict):
                validation_method = first_rule.get("validation_method", "")
                if validation_method == "word_count_range":
                    is_word_count_check = True
                    expected_range = first_rule.get("expected_range")
                elif validation_method in (
                    "chapter_cloning_detection",
                    "alternating_repetition_detection",
                    "chapter_completion_ratio",
                    "chapter_length_stability",
                    "paragraph_repetition_detection",
                ):
                    is_programmatic_check = True
                    programmatic_method = validation_method
                elif validation_method == "llm_semantic_analysis":
                    # 自动启用LLM
                    if llm_judge_criteria:
                        use_llm = True

        if not file_pattern:
            return create_check_item_result(
                "fail", "缺少参数", "需要file_pattern或analysis_target"
            )

        # 支持"+"连接的多个路径（如"chapters/ + characters.json"）
        if ' + ' in file_pattern:
            patterns = [p.strip() for p in file_pattern.split(' + ')]
        else:
            patterns = [file_pattern]

        # 处理每个pattern
        all_matched_files = []
        for pattern in patterns:
            # 如果pattern以/结尾（目录），自动补全通配符匹配目录下所有文件
            if pattern.endswith('/'):
                pattern = pattern + '*'

            # 灵活匹配文件（容错文件命名差异）
            matched_files = self._glob_files_flexible(pattern)
            if matched_files:
                all_matched_files.extend(matched_files)

        # word_count_range和P1-P5程序化检查不需要LLM
        if not is_word_count_check and not is_programmatic_check and (not use_llm or not llm_judge_criteria):
            return create_check_item_result(
                "fail", "缺少参数", "llm_semantic_analysis方法需要启用LLM并提供llm_judge_criteria"
            )

        # 使用合并后的文件列表
        matched_files = all_matched_files

        if not matched_files:
            return create_check_item_result(
                "fail", "未找到匹配文件",
                f"模式 '{file_pattern}' 未匹配任何文件"
            )

        # ========== 新增：白名单文件检查（用于"后期跑偏"等检查项）==========
        required_files = params.get("required_files", [])
        whitelist_check_info = ""
        is_workspace_check = required_files and file_pattern.rstrip('/') == "workspace"
        
        if is_workspace_check:
            # 获取workspace目录下的所有文件和目录（一级）
            workspace_dir = self.work_dir / "workspace"
            if not workspace_dir.exists():
                # 容错：尝试嵌套路径
                workspace_dir = self.work_dir / "workspace" / "workspace"
            
            if workspace_dir.exists():
                actual_items = []
                for item in workspace_dir.iterdir():
                    # 获取相对名称，目录加/后缀
                    if item.is_dir():
                        actual_items.append(item.name + "/")
                    else:
                        actual_items.append(item.name)
                
                # 更精确的对比：去掉/后缀再比较
                whitelist_names = set(w.rstrip('/') for w in required_files)
                extra_items = []
                for item in actual_items:
                    item_name = item.rstrip('/')
                    if item_name not in whitelist_names:
                        extra_items.append(item)
                
                if extra_items:
                    whitelist_check_info = f"[白名单检查失败] workspace中发现额外文件/目录: {extra_items}"
                    # 如果有额外文件，直接返回失败（不需要再调LLM）
                    return create_check_item_result(
                        "fail", "workspace中存在白名单之外的文件",
                        f"白名单: {required_files}; 实际: {actual_items}; 额外: {extra_items}"
                    )
                else:
                    whitelist_check_info = f"[白名单检查通过] workspace文件列表: {actual_items}"
            
            # 白名单检查通过后，重新定位到chapters目录进行内容检查
            # 因为workspace/下的json文件不需要交给LLM检查内容跑偏
            chapters_dir = workspace_dir / "chapters"
            if chapters_dir.exists():
                # 重新匹配chapters目录下的所有文件
                matched_files = list(chapters_dir.glob("*.md"))
                if not matched_files:
                    matched_files = list(chapters_dir.glob("*"))  # fallback
        # ========== 白名单检查结束 ==========

        # 读取所有文件的raw content
        all_contents = []
        file_names = []
        for file_path in matched_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_contents.append(content)
                    file_names.append(Path(file_path).name)
            except Exception as e:
                return create_check_item_result(
                    "fail", "文件读取失败",
                    f"无法读取 {Path(file_path).name}: {str(e)}"
                )

        # 合并所有内容（如果有多个文件）
        if len(matched_files) == 1:
            combined_content = all_contents[0]
            context_info = f"文件: {file_names[0]}"
        else:
            combined_content = "\\n\\n=== 文件分隔 ===\\n\\n".join(
                [f"文件: {name}\\n{content}" for name, content in zip(file_names, all_contents)]
            )
            context_info = f"共{len(matched_files)}个文件: {', '.join(file_names[:3])}{'...' if len(file_names) > 3 else ''}"

        # 特殊处理：word_count_range检查（不使用LLM）
        if is_word_count_check:
            if not expected_range or len(expected_range) != 2:
                return create_check_item_result(
                    "fail", "参数错误",
                    f"word_count_range方法需要expected_range参数（长度为2的数组）"
                )

            # 统计所有文件的总字数
            total_word_count = sum(len(content) for content in all_contents)
            min_count, max_count = expected_range

            # 判断是否在范围内
            if min_count <= total_word_count <= max_count:
                return create_check_item_result(
                    "pass", "字数符合要求",
                    f"总字数 {total_word_count} 在范围 [{min_count}, {max_count}] 内; {context_info}"
                )
            else:
                return create_check_item_result(
                    "fail", "字数不符合要求",
                    f"总字数 {total_word_count} 不在范围 [{min_count}, {max_count}] 内; {context_info}"
                )

        # ========== P1-P5 程序化检查（不使用LLM）==========
        if is_programmatic_check:
            return self._execute_programmatic_check(
                programmatic_method, params, matched_files, all_contents, file_names, context_info
            )

        # 长度限制（避免超过LLM上下文）
        max_length = 50000  # 增加到50k以支持多文件
        if len(combined_content) > max_length:
            # 保留前25k和后25k
            combined_content = combined_content[:25000] + "\\n\\n... [中间内容省略] ...\\n\\n" + combined_content[-25000:]

        # 使用LLM评估
        if not self.model_name or not self.api_base or not self.api_key:
            return create_check_item_result(
                "fail", "LLM配置缺失", "语义检查需要LLM配置"
            )

        try:
            # 构造LLM prompt
            prompt = f"""请评估以下内容是否符合业务标准。

**业务标准：**
{llm_judge_criteria}

**待评估内容：** ({context_info})
{combined_content}

⚠️ 重要说明：
- 内容可能是JSON格式，也可能不是，请关注语义本身，不要因格式问题影响评估
- 如果内容被截断，请基于可见部分进行合理推断
- 重点评估内容质量，而非格式规范

请以JSON格式回复：
{{"matched": true/false, "reason": "详细说明评估依据，包括具体的优点或不足"}}
"""

            success, llm_response = request_llm_with_litellm(
                [{"role": "user", "content": prompt}],
                self.model_name,
                self.api_base,
                self.api_key
            )

            if success:
                llm_result = safe_json_extract_single(llm_response)
                is_matched = llm_result.get("matched", False)
                reason = llm_result.get("reason", "")

                # 提取结构化硬伤数据（逻辑硬伤等 check 项会返回 flaws 数组）
                flaw_count = llm_result.get("flaw_count")
                flaws = llm_result.get("flaws")

                # 如果是workspace检查，在结果中包含白名单检查信息
                extra_info = f"; {whitelist_check_info}" if whitelist_check_info else ""

                if is_matched:
                    result = create_check_item_result(
                        "pass", "内容符合标准 (LLM语义判断-解耦模式)",
                        f"检查了{len(matched_files)}个文件{extra_info}; LLM评估: {reason}"
                    )
                else:
                    result = create_check_item_result(
                        "fail", "内容不符合标准 (LLM语义判断-解耦模式)",
                        f"检查了{len(matched_files)}个文件{extra_info}; LLM评估: {reason}"
                    )

                # 附加结构化硬伤数据（如果 LLM 返回了 flaws）
                if flaws is not None and isinstance(flaws, list):
                    result["flaw_count"] = flaw_count if flaw_count is not None else len(flaws)
                    result["flaws"] = flaws

                return result
            else:
                print(f"[DEBUG] LLM调用失败: {llm_response}", flush=True)
                return create_check_item_result(
                    "fail", "LLM调用失败",
                    f"无法评估内容: {llm_response}"
                )

        except Exception as e:
            print(f"[DEBUG] LLM调用异常: {str(e)}", flush=True)
            return create_check_item_result(
                "fail", "检查失败",
                f"检查过程出错: {str(e)}"
            )

    # ========== P1-P5 程序化质量检查 ==========

    def _execute_programmatic_check(
        self,
        method: str,
        params: Dict,
        matched_files: list,
        all_contents: list,
        file_names: list,
        context_info: str,
    ) -> Dict:
        """P1-P5程序化内容质量检查的分发入口。

        所有检查纯程序化实现，不调用LLM，检测成本为零。
        """
        try:
            if method == "chapter_cloning_detection":
                return self._check_chapter_cloning(matched_files, all_contents, file_names)
            elif method == "alternating_repetition_detection":
                return self._check_alternating_repetition(matched_files, all_contents, file_names)
            elif method == "chapter_completion_ratio":
                return self._check_chapter_completion(params, matched_files, file_names)
            elif method == "chapter_length_stability":
                return self._check_chapter_length_stability(all_contents, file_names)
            elif method == "paragraph_repetition_detection":
                return self._check_paragraph_repetition(all_contents, file_names)
            else:
                return create_check_item_result(
                    "skip", f"未知的程序化检查方法: {method}", ""
                )
        except Exception as e:
            return create_check_item_result(
                "fail", "程序化检查异常", f"方法 {method} 执行出错: {str(e)}"
            )

    def _check_chapter_cloning(
        self, matched_files: list, all_contents: list, file_names: list
    ) -> Dict:
        """P1: 章节克隆检测。

        检测逻辑:
        1. 对每个chapter文件，去掉第一行（标题行），计算剩余内容的MD5
        2. 连续 >= 2 章完全克隆(hash一致) → fail
        3. 去掉标题行后前500字符一致的连续 >= 3 章（近似克隆）→ fail
        """
        import hashlib

        if len(all_contents) < 4:
            return create_check_item_result(
                "skip", "章节数不足", f"仅{len(all_contents)}章，跳过克隆检测（需>=4章）"
            )

        # 计算每章去掉第一行后的完整hash和前500字符hash
        full_hashes = []
        prefix_hashes = []
        for content in all_contents:
            lines = content.split("\n", 1)
            body = lines[1] if len(lines) > 1 else ""
            full_hashes.append(hashlib.md5(body.encode("utf-8")).hexdigest())
            prefix_500 = body[:500]
            prefix_hashes.append(hashlib.md5(prefix_500.encode("utf-8")).hexdigest())

        # 检测完全克隆：连续相同full_hash的最长序列
        max_clone_run = 1
        clone_start_idx = 0
        cur_run = 1
        cur_start = 0
        for i in range(1, len(full_hashes)):
            if full_hashes[i] == full_hashes[i - 1]:
                cur_run += 1
                if cur_run > max_clone_run:
                    max_clone_run = cur_run
                    clone_start_idx = cur_start
            else:
                cur_run = 1
                cur_start = i

        if max_clone_run >= 2:
            clone_end_idx = clone_start_idx + max_clone_run - 1
            return create_check_item_result(
                "fail",
                f"检测到{max_clone_run}章完全克隆",
                f"章节 {file_names[clone_start_idx]} 到 {file_names[clone_end_idx]} "
                f"（共{max_clone_run}章）去掉标题行后内容完全相同 "
                f"(hash: {full_hashes[clone_start_idx][:12]}...)",
            )

        # 检测近似克隆：连续相同prefix_hash的最长序列
        max_prefix_run = 1
        prefix_start_idx = 0
        cur_run = 1
        cur_start = 0
        for i in range(1, len(prefix_hashes)):
            if prefix_hashes[i] == prefix_hashes[i - 1]:
                cur_run += 1
                if cur_run > max_prefix_run:
                    max_prefix_run = cur_run
                    prefix_start_idx = cur_start
            else:
                cur_run = 1
                cur_start = i

        if max_prefix_run >= 3:
            prefix_end_idx = prefix_start_idx + max_prefix_run - 1
            return create_check_item_result(
                "fail",
                f"检测到{max_prefix_run}章近似克隆",
                f"章节 {file_names[prefix_start_idx]} 到 {file_names[prefix_end_idx]} "
                f"（共{max_prefix_run}章）前500字符完全相同 "
                f"(prefix_hash: {prefix_hashes[prefix_start_idx][:12]}...)",
            )

        return create_check_item_result(
            "pass",
            "未检测到章节克隆",
            f"共{len(all_contents)}章，无连续完全克隆或近似克隆",
        )

    def _check_alternating_repetition(
        self, matched_files: list, all_contents: list, file_names: list
    ) -> Dict:
        """P2: 交替重复检测（A-B-A-B循环模式）。

        检测逻辑:
        1. 提取每章的文件字节大小
        2. 检测是否存在 size_A, size_B 交替出现的模式（容差5%）
        3. 连续交替 >= 3 轮（即6章） → fail
        """
        if len(all_contents) < 8:
            return create_check_item_result(
                "skip", "章节数不足", f"仅{len(all_contents)}章，跳过交替重复检测（需>=8章）"
            )

        sizes = [len(content.encode("utf-8")) for content in all_contents]

        # 从后半部分开始检测（交替重复通常出现在后期）
        half = len(sizes) // 2
        check_sizes = sizes[half:]
        check_names = file_names[half:]

        if len(check_sizes) < 6:
            return create_check_item_result(
                "pass", "后半部分章节不足", f"后半部分仅{len(check_sizes)}章，不构成交替模式"
            )

        # 检测A-B-A-B模式
        max_alternating = 0
        best_start = 0
        for start in range(len(check_sizes) - 5):
            size_a = check_sizes[start]
            size_b = check_sizes[start + 1]
            # A和B不能太接近（否则就是普通克隆而不是交替）
            if size_a == 0 or size_b == 0:
                continue
            if abs(size_a - size_b) / max(size_a, size_b) < 0.03:
                continue  # A和B太接近，跳过

            count = 2  # 已有A, B
            for j in range(start + 2, len(check_sizes)):
                expected = size_a if (j - start) % 2 == 0 else size_b
                actual = check_sizes[j]
                # 容差5%
                if expected > 0 and abs(actual - expected) / expected <= 0.05:
                    count += 1
                else:
                    break

            rounds = count // 2
            if rounds > max_alternating:
                max_alternating = rounds
                best_start = start

        if max_alternating >= 3:
            actual_start = half + best_start
            actual_end = actual_start + max_alternating * 2 - 1
            size_a = sizes[actual_start]
            size_b = sizes[actual_start + 1]
            return create_check_item_result(
                "fail",
                f"检测到{max_alternating}轮交替重复",
                f"从 {file_names[actual_start]} 到 {file_names[min(actual_end, len(file_names)-1)]} "
                f"呈现 A({size_a}bytes)-B({size_b}bytes) 交替模式，共{max_alternating}轮",
            )

        return create_check_item_result(
            "pass", "未检测到交替重复", f"共{len(all_contents)}章，无A-B-A-B交替模式"
        )

    def _check_chapter_completion(
        self, params: Dict, matched_files: list, file_names: list
    ) -> Dict:
        """P3: 章节完成度检测。

        检测逻辑:
        1. 从outline.json推断规划章节数
        2. 实际章节数 / 规划章节数 < 30% → fail
        3. 无法推断规划数时: MEDIUM类型样本实际<=1章 → fail
        """
        actual_count = len(file_names)

        # 尝试从outline.json读取规划章节数
        planned_count = None
        outline_path = self.work_dir / "workspace" / "outline.json"
        if not outline_path.exists():
            outline_path = self.work_dir / "workspace" / "workspace" / "outline.json"

        if outline_path.exists():
            try:
                import json
                with open(outline_path, "r", encoding="utf-8") as f:
                    outline = json.load(f)
                if isinstance(outline, dict):
                    # 尝试多种常见大纲结构
                    for key in ["chapters", "outline", "chapter_outlines", "volume_structure"]:
                        val = outline.get(key)
                        if isinstance(val, list) and len(val) > 0:
                            planned_count = len(val)
                            break
                    if planned_count is None:
                        # 尝试统计act结构中的key_chapters
                        total_from_acts = 0
                        for act_key in ["act_one", "act_two", "act_three", "act_four"]:
                            act = outline.get(act_key, {})
                            if isinstance(act, dict):
                                kc = act.get("key_chapters", [])
                                if isinstance(kc, list):
                                    total_from_acts += len(kc)
                        if total_from_acts > 0:
                            planned_count = total_from_acts
                elif isinstance(outline, list):
                    planned_count = len(outline)
            except Exception:
                pass

        # 从params中获取最低阈值（可选配置）
        min_ratio = params.get("validation_rules", [{}])[0].get("min_completion_ratio", 0.30) if params.get("validation_rules") else 0.30

        if planned_count and planned_count > 0:
            ratio = actual_count / planned_count
            if ratio < min_ratio:
                return create_check_item_result(
                    "fail",
                    f"章节完成度不足({ratio:.0%})",
                    f"大纲规划{planned_count}章，实际仅完成{actual_count}章 "
                    f"(完成率{ratio:.1%}，阈值{min_ratio:.0%})",
                )
            return create_check_item_result(
                "pass",
                f"章节完成度合格({ratio:.0%})",
                f"大纲规划{planned_count}章，实际完成{actual_count}章 (完成率{ratio:.1%})",
            )

        # 无法从大纲推断规划数时的兜底判断
        if actual_count == 0:
            return create_check_item_result(
                "fail", "未写出任何章节", "chapters目录中没有任何章节文件"
            )
        if actual_count <= 1:
            return create_check_item_result(
                "fail",
                f"仅写出{actual_count}章",
                f"无法从大纲推断规划章节数，但仅{actual_count}章明显不足",
            )

        return create_check_item_result(
            "pass",
            f"完成{actual_count}章",
            f"无法从大纲推断规划章节数，实际完成{actual_count}章",
        )

    def _check_chapter_length_stability(
        self, all_contents: list, file_names: list
    ) -> Dict:
        """P4: 章节长度稳定性检测。

        检测逻辑:
        1. 计算前1/3章节平均字数和后1/4章节平均字数
        2. 后1/4 < 前1/3 × 0.25 → fail（严重崩塌）
        3. 后1/4中任何单章 < 200字 → fail（极端退化）
        """
        n = len(all_contents)
        if n < 6:
            return create_check_item_result(
                "skip", "章节数不足", f"仅{n}章，跳过长度稳定性检测（需>=6章）"
            )

        char_counts = [len(content) for content in all_contents]

        # 前1/3
        first_n = max(n // 3, 2)
        first_avg = sum(char_counts[:first_n]) / first_n

        # 后1/4
        last_n = max(n // 4, 2)
        last_chars = char_counts[-last_n:]
        last_avg = sum(last_chars) / last_n
        last_min = min(last_chars)
        last_min_idx = len(char_counts) - last_n + last_chars.index(last_min)

        # 极端退化：单章<200字
        if last_min < 200:
            return create_check_item_result(
                "fail",
                f"后期章节极端退化(最短{last_min}字)",
                f"后{last_n}章中 {file_names[last_min_idx]} 仅{last_min}字; "
                f"前{first_n}章均值{first_avg:.0f}字, 后{last_n}章均值{last_avg:.0f}字",
            )

        # 严重崩塌
        if first_avg > 0:
            ratio = last_avg / first_avg
            if ratio < 0.25:
                return create_check_item_result(
                    "fail",
                    f"章节长度严重崩塌(后期仅为前期{ratio:.0%})",
                    f"前{first_n}章均值{first_avg:.0f}字, 后{last_n}章均值{last_avg:.0f}字 "
                    f"(衰减至{ratio:.1%}); 后{last_n}章: {', '.join(f'{file_names[n-last_n+i]}={last_chars[i]}字' for i in range(last_n))}",
                )

        return create_check_item_result(
            "pass",
            "章节长度稳定",
            f"前{first_n}章均值{first_avg:.0f}字, 后{last_n}章均值{last_avg:.0f}字 "
            f"(比率{last_avg/first_avg:.1%})" if first_avg > 0 else f"前{first_n}章均值{first_avg:.0f}字",
        )

    def _check_paragraph_repetition(
        self, all_contents: list, file_names: list
    ) -> Dict:
        """P5: 段落级重复检测。

        检测逻辑:
        1. 将每章按空行分隔为段落
        2. 对每个 >= 50字的段落计算hash
        3. 同章内完全相同段落 >= 2处 → fail
        4. 跨章完全相同段落 >= 5处 → fail
        """
        import hashlib
        from collections import defaultdict

        MIN_PARA_LEN = 50  # 最短段落长度（跳过短段落如标题行）

        # 收集所有段落hash -> [(chapter_idx, para_text_preview)]
        para_hash_map = defaultdict(list)
        # 同章内重复检测
        intra_chapter_duplicates = []

        for ch_idx, content in enumerate(all_contents):
            # 按空行分段
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            seen_in_chapter = {}  # hash -> first occurrence para preview

            for para in paragraphs:
                if len(para) < MIN_PARA_LEN:
                    continue
                h = hashlib.md5(para.encode("utf-8")).hexdigest()

                # 同章内重复
                if h in seen_in_chapter:
                    intra_chapter_duplicates.append(
                        (file_names[ch_idx], para[:80] + "..." if len(para) > 80 else para)
                    )
                else:
                    seen_in_chapter[h] = para[:80]

                # 跨章追踪
                para_hash_map[h].append((ch_idx, para[:60]))

        # 判定：同章内重复
        if len(intra_chapter_duplicates) >= 2:
            examples = intra_chapter_duplicates[:3]
            example_strs = "; ".join(f"[{fn}] \"{preview}\"" for fn, preview in examples)
            return create_check_item_result(
                "fail",
                f"同章内段落重复{len(intra_chapter_duplicates)}处",
                f"示例: {example_strs}",
            )

        # 判定：跨章重复
        cross_chapter_duplicates = []
        for h, occurrences in para_hash_map.items():
            if len(occurrences) >= 2:
                # 确认确实是不同章节
                chapter_indices = set(o[0] for o in occurrences)
                if len(chapter_indices) >= 2:
                    cross_chapter_duplicates.append((len(occurrences), occurrences[0][1], occurrences))

        if len(cross_chapter_duplicates) >= 5:
            # 按出现次数降序，取前3个示例
            cross_chapter_duplicates.sort(key=lambda x: -x[0])
            examples = cross_chapter_duplicates[:3]
            example_strs = "; ".join(
                f"\"{preview}...\" 出现在{count}章"
                for count, preview, _ in examples
            )
            return create_check_item_result(
                "fail",
                f"跨章段落重复{len(cross_chapter_duplicates)}组",
                f"有{len(cross_chapter_duplicates)}个段落在多章中完全相同。示例: {example_strs}",
            )

        # 汇总
        intra_count = len(intra_chapter_duplicates)
        cross_count = len(cross_chapter_duplicates)
        return create_check_item_result(
            "pass",
            "段落重复在可接受范围",
            f"同章内重复{intra_count}处, 跨章重复{cross_count}组 (阈值: 同章>=2, 跨章>=5)",
        )


# =========================================
# 7. 主执行逻辑
# =========================================


def _check_file_whitelist(check_item: Dict, work_dir: Path) -> Dict:
    """检查workspace目录中是否存在白名单之外的文件。
    
    params中需要:
      - analysis_target: 要检查的目录（如 "workspace/"）
      - required_files: 允许存在的文件/目录白名单列表
    """
    params = check_item.get("params", {})
    analysis_target = params.get("analysis_target", "workspace/")
    whitelist = params.get("required_files", [])
    
    # 构建目标目录路径
    target_dir = work_dir / analysis_target.rstrip("/")
    
    # 也检查嵌套路径 workspace/workspace/（部分Agent会创建）
    if not target_dir.exists():
        nested_dir = work_dir / "workspace" / analysis_target.rstrip("/")
        if nested_dir.exists():
            target_dir = nested_dir
        else:
            return create_check_item_result(
                "skip",
                f"目标目录不存在: {analysis_target}",
                f"检查路径: {target_dir}"
            )
    
    # 标准化白名单：去掉目录的尾部斜杠用于匹配
    whitelist_names = set()
    whitelist_dirs = set()
    for item in whitelist:
        if item.endswith("/"):
            whitelist_dirs.add(item.rstrip("/"))
        else:
            whitelist_names.add(item)
    
    # 扫描目标目录下的所有顶层条目
    extra_files = []
    for entry in target_dir.iterdir():
        name = entry.name
        # 跳过隐藏文件中已在白名单的
        if name in whitelist_names:
            continue
        if entry.is_dir() and name in whitelist_dirs:
            continue
        # __pycache__ 等Python缓存目录不算违规
        if name == "__pycache__":
            continue
        extra_files.append(name)
    
    if extra_files:
        return create_check_item_result(
            "fail",
            f"workspace中存在白名单外的文件: {extra_files}",
            f"白名单: {whitelist}, 额外文件: {extra_files}"
        )
    else:
        return create_check_item_result(
            "pass",
            "workspace中所有文件均在白名单内",
            f"白名单: {whitelist}"
        )


def execute_checks(sample_result: Dict, check_list: List[Dict],
                  model_config: Dict = None) -> Dict:
    """
    执行所有检查项

    Args:
        sample_result: sample执行结果（包含conversation_history和workspace路径）
        check_list: 检查项列表（来自unified_scenario_design.yaml）
        model_config: LLM配置

    Returns:
        {
            "sample_id": "...",
            "check_timestamp": int,
            "check_details": {
                "检查项1": {...},
                "检查项2": {...}
            }
        }
    """
    sample_id = sample_result.get("sample_id", "unknown")
    conversation_history = sample_result.get("conversation_history", [])
    workspace_path = Path(sample_result.get("workspace_path", ""))

    if not workspace_path.exists():
        return {
            "sample_id": sample_id,
            "check_timestamp": int(time.time()),
            "check_details": {},
            "error": f"workspace路径不存在: {workspace_path}"
        }

    # 获取workspace的父目录作为work_dir
    # FileSystemChecker等依赖这个路径结构（work_dir/workspace/）
    work_dir = workspace_path.parent

    # 创建所有checker实例
    # FileSystemChecker也需要LLM配置，用于JSON不合法时的semantic fallback
    llm_model_name = model_config.get("model_name") if model_config else None
    llm_api_base = model_config.get("api_base") if model_config else None
    llm_api_key = model_config.get("api_key") if model_config else None
    fs_checker = FileSystemChecker(str(work_dir), llm_model_name, llm_api_base, llm_api_key)
    schema_checker = JSONSchemaChecker(str(work_dir))
    cross_checker = CrossFileConsistencyChecker(str(work_dir))
    tool_checker = ToolCalledWithParamsChecker(str(work_dir))
    tool_absence_checker = ToolCallAbsenceChecker()
    
    # SemanticChecker需要LLM配置
    semantic_checker = None
    if model_config and model_config.get("model_name"):
        semantic_checker = SemanticChecker(
            str(work_dir),
            model_config.get("model_name"),
            model_config.get("api_base"),
            model_config.get("api_key")
        )

    # 执行所有检查
    check_details = {}
    for i, check_item in enumerate(check_list, 1):
        check_idx = f"检查项{i}"
        check_type = check_item.get("check_type")
        description = check_item.get("description", "")
        
        print(f"\033[1;36m[执行] {check_idx}: {description} ({check_type})...\033[0m", flush=True)

        # 根据check_type分发到对应的checker
        if check_type == "entity_attribute_equals":
            result = fs_checker.check_entity_attribute_equals(check_item)
        elif check_type == "create_operation_verified":
            result = fs_checker.check_create_operation_verified(check_item)
        elif check_type == "json_schema":
            result = schema_checker.check(check_item.get("params", {}))
        elif check_type == "cross_file_consistency":
            result = cross_checker.check(check_item.get("params", {}))
        elif check_type == "tool_called_with_params":
            result = tool_checker.check(check_item.get("params", {}), conversation_history)
        elif check_type == "tool_call_absence":
            result = tool_absence_checker.check(check_item.get("params", {}), conversation_history)
        elif check_type == "semantic_check":
            if semantic_checker:
                result = semantic_checker.check(check_item.get("params", {}), sample_result)
            else:
                result = create_check_item_result(
                    "skip", "缺少LLM配置", "semantic_check需要LLM模型配置"
                )
        elif check_type == "file_whitelist_check":
            result = _check_file_whitelist(check_item, work_dir)
        else:
            result = create_check_item_result(
                "skip", f"不支持的检查类型: {check_type}", ""
            )

        # 添加元信息
        result["description"] = description
        result["check_type"] = check_type
        
        # 添加其他元数据字段
        for key in ["dimension_id", "subcategory_id", "quality_tier", "is_critical"]:
            if key in check_item:
                result[key] = check_item[key]
        
        check_details[check_idx] = result

    return {
        "sample_id": sample_id,
        "check_timestamp": int(time.time()),
        "check_details": check_details
    }


# =========================================
# 8. CLI入口
# =========================================

def main():
    parser = argparse.ArgumentParser(
        description="小说创作炼金术场景 - Checker执行模块（执行检查，不计算维度统计）"
    )
    parser.add_argument("--sample-result", required=True,
                       help="sample执行结果文件路径（包含conversation_history和workspace路径）")
    parser.add_argument("--checklist", required=True,
                       help="checklist文件路径（unified_scenario_design.yaml的check_list）")
    parser.add_argument("--model-name", default=None, help="LLM模型名称（用于semantic检查）")
    parser.add_argument("--api-base", default=None, help="LLM API base URL")
    parser.add_argument("--api-key", default=None, help="LLM API key")
    parser.add_argument("--output", required=True,
                       help="输出文件路径（execution_result.json）")
    args = parser.parse_args()

    # 加载输入文件
    print(f"[加载] Sample Result: {args.sample_result}")
    with open(args.sample_result, "r", encoding="utf-8") as f:
        sample_result = json.load(f)

    print(f"[加载] Checklist: {args.checklist}")
    with open(args.checklist, "r", encoding="utf-8") as f:
        checklist_data = json.load(f)
        check_list = checklist_data.get("check_list", [])

    # 准备LLM配置
    model_config = {}
    if args.model_name:
        model_config = {
            "model_name": args.model_name,
            "api_base": args.api_base,
            "api_key": args.api_key
        }
        print(f"[配置] LLM模型: {args.model_name}")
    else:
        print("[警告] 未配置LLM模型，semantic_check将被跳过")

    # 执行检查
    print(f"\n\033[1;36m[执行] 开始检查...\033[0m")
    result = execute_checks(sample_result, check_list, model_config)

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n[完成] 输出文件: {output_path}")

    # 打印统计
    details = result.get("check_details", {})
    passed = sum(1 for v in details.values() if v["check_result"] == "pass")
    failed = sum(1 for v in details.values() if v["check_result"] == "fail")
    skipped = sum(1 for v in details.values() if v["check_result"] == "skip")

    print(f"\n[统计] 总计: {len(details)} 项")
    print(f"[统计] ✓ Pass: {passed} 项")
    print(f"[统计] ✗ Fail: {failed} 项")
    print(f"[统计] ⊘ Skip: {skipped} 项")


if __name__ == "__main__":
    main()
