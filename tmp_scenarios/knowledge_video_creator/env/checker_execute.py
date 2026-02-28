#!/usr/bin/env python3
"""
knowledge_video_creator — Checker 执行层
==========================================

执行所有检查项，返回逐项的 pass/fail/skip 结果。
基于 novel_to_script 架构，适配知识视频创作场景。

关键区别（vs novel_to_script）：
- 交付物除了 JSON 文件（knowledge_analysis / series_plan / episode_*.json），
  还有多媒体文件（slides.pptx / narration.mp3 / manifest.json / images/）
- 新增 multimedia_completeness 检查：PPT、配音、配图存在性
- SOP 是 5 步（多了 Step 5: 视频素材制作）
- 源材料是技术文档而非小说
- LLM Judge 的 system prompt 需要适配技术教育领域
"""

import glob
import json
import logging
import os
import re
import sys
import time
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# LiteLLM for LLM judge calls
try:
    import litellm
    litellm.set_verbose = False
except ImportError:
    litellm = None

logger = logging.getLogger(__name__)


# ============================================
# 工具函数
# ============================================

def create_check_item_result(conclusion: str, reason: str, details: str) -> Dict[str, Any]:
    """创建检查结果字典"""
    return {
        "check_result": conclusion,  # "pass" | "fail" | "skip"
        "reason": reason,
        "details": details
    }


def request_llm_with_litellm(
    messages: List[Dict],
    model_name: str,
    api_base: str,
    api_key: str,
    max_retries: int = 20
) -> Tuple[bool, str]:
    """调用LLM，带指数退避重试"""
    if litellm is None:
        return False, "litellm not installed"

    for attempt in range(max_retries):
        try:
            response = litellm.completion(
                model=model_name,
                messages=messages,
                custom_llm_provider="openai",
                api_base=api_base,
                api_key=api_key,
                response_format={"type": "json_object"},
                temperature=0.1,
                timeout=120
            )
            content = response.choices[0].message.content
            if content and len(content.strip()) > 0:
                return True, content.strip()
            else:
                return False, "Empty response from LLM"
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower():
                wait = min(5 * (2 ** attempt) + random.uniform(0, 3), 120)
                logger.warning(f"Rate limited, retry {attempt + 1}/{max_retries} after {wait:.1f}s")
                time.sleep(wait)
                continue
            elif attempt < max_retries - 1:
                wait = min(5 * (2 ** attempt) + random.uniform(0, 3), 120)
                logger.warning(f"LLM error: {error_str}, retry {attempt + 1}/{max_retries} after {wait:.1f}s")
                time.sleep(wait)
                continue
            else:
                return False, f"LLM call failed after {max_retries} retries: {error_str}"

    return False, f"LLM call failed after {max_retries} retries"


def safe_json_extract_single(response_text: str) -> Optional[Dict]:
    """从LLM响应中提取JSON，三种策略"""
    # 策略1：直接解析
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # 策略2：从 ```json ``` 代码块提取
    match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 策略3：提取任意 {...} 块
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def load_judge_criteria(params: Dict, work_dir: str) -> Optional[str]:
    """加载 LLM judge 评判标准

    支持两种路径格式：
    1. judge_criteria_file + judge_section（knowledge_video_creator 格式）
    2. llm_judge_criteria_file + llm_judge_criteria_section（novel_to_script 格式）
    3. llm_judge_criteria（内联字符串）
    """
    import yaml

    # 方式1：内联
    if "llm_judge_criteria" in params and isinstance(params["llm_judge_criteria"], str):
        return params["llm_judge_criteria"]

    # 方式2：judge_criteria_file + judge_section（新格式）
    criteria_file = params.get("judge_criteria_file") or params.get("llm_judge_criteria_file")
    section = params.get("judge_section") or params.get("llm_judge_criteria_section")

    if criteria_file:
        # 尝试多个路径
        candidates = [
            os.path.join(work_dir, criteria_file),
            os.path.join(work_dir, "check_definitions", criteria_file),
        ]
        # 如果路径已经以 check_definitions/ 开头，也加一个去掉前缀的版本
        if criteria_file.startswith("check_definitions/"):
            candidates.insert(0, os.path.join(work_dir, criteria_file))

        file_path = None
        for cand in candidates:
            if os.path.exists(cand):
                file_path = cand
                break

        if not file_path:
            logger.error(f"Judge criteria file not found: {criteria_file}, tried: {candidates}")
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)

            if section and isinstance(content, dict) and section in content:
                section_data = content[section]
                if isinstance(section_data, dict) and "judge_prompt" in section_data:
                    return section_data["judge_prompt"]
                elif isinstance(section_data, str):
                    return section_data
                else:
                    return json.dumps(section_data, ensure_ascii=False, indent=2)
            elif isinstance(content, str):
                return content
            else:
                # 返回整个文件内容
                return json.dumps(content, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Failed to load criteria file {file_path}: {e}")

    # 方式3：validation_rules 中的 evaluation_criteria
    if "validation_rules" in params:
        rules = params["validation_rules"]
        if rules and isinstance(rules, list) and len(rules) > 0:
            rule = rules[0]
            ec = rule.get("evaluation_criteria", {})
            if "validation_prompt" in ec:
                return ec["validation_prompt"]

    return None


def glob_workspace_files(work_dir: str, pattern: str) -> List[str]:
    """在workspace目录下glob文件，带嵌套容错"""
    workspace = os.path.join(work_dir, "workspace")

    # 先清理 pattern 中的 workspace/ 前缀（避免双重嵌套）
    clean_pattern = pattern.replace("workspace/", "", 1) if pattern.startswith("workspace/") else pattern

    # 标准搜索：work_dir/workspace/{clean_pattern}
    results = glob.glob(os.path.join(workspace, clean_pattern))

    # 嵌套容错：work_dir/workspace/workspace/{clean_pattern}
    if not results:
        nested = os.path.join(workspace, "workspace", clean_pattern)
        results = glob.glob(nested)

    # 原始 pattern 兜底
    if not results:
        results = glob.glob(os.path.join(workspace, pattern))

    return sorted(results)


def resolve_workspace_path(work_dir: str, path: str) -> Optional[str]:
    """解析workspace文件路径，带容错"""
    # 移除开头的 workspace/ 前缀（如果有）
    clean_path = path.replace("workspace/", "", 1) if path.startswith("workspace/") else path

    # 标准路径
    full_path = os.path.join(work_dir, "workspace", clean_path)
    if os.path.exists(full_path):
        return full_path

    # 嵌套容错
    nested_path = os.path.join(work_dir, "workspace", "workspace", clean_path)
    if os.path.exists(nested_path):
        return nested_path

    return None


def load_json_file(path: str) -> Optional[Dict]:
    """安全加载JSON文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        logger.warning(f"Failed to load JSON {path}: {e}")
        return None


def extract_json_field(data: Dict, field_path: str) -> Any:
    """从JSON中提取嵌套字段，支持 [*] 通配符和点分路径

    例：core_concepts → data["core_concepts"]
    例：script_body[*].narration → 提取所有segment的narration字段
    例：series_positioning.total_episodes → 嵌套提取
    """
    parts = field_path.replace("[*]", ".[*]").split(".")
    current = [data]

    for part in parts:
        if not part:
            continue
        next_level = []
        for item in current:
            if item is None:
                continue
            if part == "[*]":
                if isinstance(item, list):
                    next_level.extend(item)
            elif isinstance(item, dict):
                val = item.get(part)
                if val is not None:
                    next_level.append(val)
            elif isinstance(item, list):
                for elem in item:
                    if isinstance(elem, dict):
                        val = elem.get(part)
                        if val is not None:
                            next_level.append(val)
        current = next_level

    if len(current) == 1:
        return current[0]
    return current if current else None


# ============================================
# 检查器类
# ============================================

class FileSystemChecker:
    """文件存在性、字段值、命名模式、多媒体完整性检查"""

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def check(self, check_item: Dict) -> Dict[str, Any]:
        """分发 entity_attribute_equals 检查"""
        params = check_item.get("params", {})
        check_subtype = params.get("check_subtype", "")
        entity_type = params.get("entity_type", "")

        # 优先按 check_subtype 分发
        if check_subtype == "file_exists":
            return self._check_file_exists(params)
        elif check_subtype == "file_count":
            return self._check_file_count(params)
        elif check_subtype == "array_length_range":
            return self._check_array_length_range(params)
        elif check_subtype == "naming_pattern":
            return self._check_naming_pattern(params)
        elif check_subtype == "multimedia_completeness":
            return self._check_multimedia_completeness(params)

        # 兼容 required_fields（从 params 中直接判断）
        if "required_fields" in params:
            if "file_pattern" in params:
                return self._check_required_fields_pattern(params)
            else:
                return self._check_required_fields(params)

        # 兼容 entity_type 格式（novel_to_script 兼容）
        if entity_type == "file":
            return self._check_file_exists_legacy(params)
        elif entity_type == "directory":
            return self._check_directory_exists(params)
        elif entity_type == "file_naming_pattern":
            return self._check_naming_pattern_legacy(params)
        elif entity_type == "file_field":
            return self._check_file_field(params)
        elif entity_type == "file_count":
            return self._check_file_count_legacy(params)

        return create_check_item_result("skip", f"未知的check_subtype: {check_subtype}, entity_type: {entity_type}", "")

    def _check_file_exists(self, params: Dict) -> Dict[str, Any]:
        """检查单个文件是否存在"""
        file_path = params.get("file_path", "")
        path = resolve_workspace_path(self.work_dir, file_path)
        exists = path is not None and os.path.exists(path)

        if exists:
            return create_check_item_result("pass", f"文件存在: {file_path}", "")
        else:
            return create_check_item_result("fail", f"文件不存在: {file_path}", "")

    def _check_file_exists_legacy(self, params: Dict) -> Dict[str, Any]:
        """兼容 entity_type=file 格式"""
        target = params.get("target_id", "")
        expected = params.get("expected_value", True)
        path = resolve_workspace_path(self.work_dir, target)
        exists = path is not None and os.path.exists(path)

        if exists == expected:
            return create_check_item_result("pass", f"文件{'存在' if expected else '不存在'}: {target}", "")
        else:
            return create_check_item_result("fail", f"文件{'不存在' if expected else '已存在'}: {target}", "")

    def _check_directory_exists(self, params: Dict) -> Dict[str, Any]:
        target = params.get("target_id", params.get("directory", ""))
        path = resolve_workspace_path(self.work_dir, target)
        exists = path is not None and os.path.isdir(path)

        if exists:
            return create_check_item_result("pass", f"目录存在: {target}", "")
        else:
            return create_check_item_result("fail", f"目录不存在: {target}", "")

    def _check_file_count(self, params: Dict) -> Dict[str, Any]:
        """检查目录下文件数量"""
        directory = params.get("directory", "")
        pattern = params.get("pattern", "*")
        min_count = params.get("min_count")
        expected_count = params.get("expected_count")

        dir_path = resolve_workspace_path(self.work_dir, directory)
        if not dir_path or not os.path.isdir(dir_path):
            return create_check_item_result("fail", f"目录不存在: {directory}", "")

        files = glob.glob(os.path.join(dir_path, pattern))
        actual_count = len(files)
        file_names = [os.path.basename(f) for f in files]

        if min_count is not None:
            try:
                min_val = int(min_count)
            except (ValueError, TypeError):
                return create_check_item_result("skip", f"min_count 无法解析: {min_count}", "")
            if actual_count >= min_val:
                return create_check_item_result("pass", f"文件数量 {actual_count} >= {min_val}", f"文件: {file_names}")
            else:
                return create_check_item_result("fail", f"文件数量 {actual_count} < {min_val}", f"文件: {file_names}")

        if expected_count is not None:
            try:
                expected = int(expected_count)
            except (ValueError, TypeError):
                return create_check_item_result("skip", f"expected_count 无法解析: {expected_count}", "")
            if actual_count == expected:
                return create_check_item_result("pass", f"文件数量正确: {actual_count}", f"文件: {file_names}")
            else:
                return create_check_item_result("fail", f"文件数量 {actual_count} != {expected}", f"文件: {file_names}")

        return create_check_item_result("skip", "缺少 min_count 或 expected_count 参数", "")

    def _check_file_count_legacy(self, params: Dict) -> Dict[str, Any]:
        """兼容 entity_type=file_count"""
        return self._check_file_count(params)

    def _check_array_length_range(self, params: Dict) -> Dict[str, Any]:
        """检查JSON文件中数组字段的长度范围"""
        file_path = params.get("file_path", "")
        field = params.get("field", "")
        min_length = params.get("min_length", 0)
        max_length = params.get("max_length", 999)

        resolved = resolve_workspace_path(self.work_dir, file_path)
        if not resolved:
            return create_check_item_result("fail", f"文件不存在: {file_path}", "")

        data = load_json_file(resolved)
        if data is None:
            return create_check_item_result("fail", f"JSON解析失败: {file_path}", "")

        value = extract_json_field(data, field)
        if not isinstance(value, list):
            return create_check_item_result("fail", f"字段 {field} 不是数组", f"类型: {type(value).__name__}")

        count = len(value)
        if min_length <= count <= max_length:
            return create_check_item_result("pass", f"{field} 数量 {count} 在 [{min_length}, {max_length}] 范围内", "")
        else:
            return create_check_item_result("fail", f"{field} 数量 {count} 不在 [{min_length}, {max_length}] 范围内", "")

    def _check_naming_pattern(self, params: Dict) -> Dict[str, Any]:
        """检查目录下文件命名是否符合正则模式"""
        directory = params.get("directory", "")
        expected_pattern = params.get("pattern", "")

        dir_path = resolve_workspace_path(self.work_dir, directory)
        if not dir_path or not os.path.isdir(dir_path):
            return create_check_item_result("fail", f"目录不存在: {directory}", "")

        files = os.listdir(dir_path)
        pattern = re.compile(expected_pattern)
        non_matching = [f for f in files if not pattern.match(f) and not f.startswith(".")]

        if not non_matching:
            return create_check_item_result("pass", f"所有文件命名符合模式: {expected_pattern}", f"文件列表: {files}")
        else:
            return create_check_item_result(
                "fail",
                f"以下文件不符合命名规范: {non_matching}",
                f"期望模式: {expected_pattern}, 不匹配文件: {non_matching}"
            )

    def _check_naming_pattern_legacy(self, params: Dict) -> Dict[str, Any]:
        """兼容 entity_type=file_naming_pattern"""
        return self._check_naming_pattern(params)

    def _check_required_fields(self, params: Dict) -> Dict[str, Any]:
        """检查JSON文件包含所有必需字段"""
        file_path = params.get("file_path", "")
        required_fields = params.get("required_fields", [])

        resolved = resolve_workspace_path(self.work_dir, file_path)
        if not resolved:
            return create_check_item_result("fail", f"文件不存在: {file_path}", "")

        data = load_json_file(resolved)
        if data is None:
            return create_check_item_result("fail", f"JSON解析失败: {file_path}", "")

        if not isinstance(data, dict):
            return create_check_item_result("fail", f"JSON顶层不是object: {file_path}", "")

        missing = [f for f in required_fields if f not in data]
        if not missing:
            return create_check_item_result("pass", f"所有必需字段都存在", f"字段: {required_fields}")
        else:
            return create_check_item_result("fail", f"缺少字段: {missing}", f"期望: {required_fields}, 实际: {list(data.keys())}")

    def _check_required_fields_pattern(self, params: Dict) -> Dict[str, Any]:
        """检查匹配pattern的所有文件是否包含必需字段"""
        file_pattern = params.get("file_pattern", "")
        required_fields = params.get("required_fields", [])

        files = glob_workspace_files(self.work_dir, file_pattern)
        if not files:
            return create_check_item_result("fail", f"没有匹配的文件: {file_pattern}", "")

        failed = []
        for fp in files:
            data = load_json_file(fp)
            if data is None:
                failed.append(f"{os.path.basename(fp)}: JSON解析失败")
                continue
            if not isinstance(data, dict):
                failed.append(f"{os.path.basename(fp)}: 不是object")
                continue
            missing = [f for f in required_fields if f not in data]
            if missing:
                failed.append(f"{os.path.basename(fp)}: 缺少 {missing}")

        if not failed:
            return create_check_item_result("pass", f"所有 {len(files)} 个文件包含必需字段", "")
        else:
            return create_check_item_result("fail", f"{len(failed)} 个文件字段不完整", "; ".join(failed))

    def _check_file_field(self, params: Dict) -> Dict[str, Any]:
        """兼容 entity_type=file_field"""
        file_path = params.get("file_path", "")
        field_path = params.get("field_path", "")
        attribute = params.get("attribute", "")
        expected_range = params.get("expected_range")

        resolved = resolve_workspace_path(self.work_dir, file_path)
        if not resolved:
            return create_check_item_result("fail", f"文件不存在: {file_path}", "")

        data = load_json_file(resolved)
        if data is None:
            return create_check_item_result("fail", f"JSON解析失败: {file_path}", "")

        value = extract_json_field(data, field_path)

        if attribute == "length" and isinstance(value, list):
            count = len(value)
            if expected_range and len(expected_range) == 2:
                lo, hi = expected_range
                if lo <= count <= hi:
                    return create_check_item_result("pass", f"{field_path} 数量 {count} 在 [{lo}, {hi}] 范围内", "")
                else:
                    return create_check_item_result("fail", f"{field_path} 数量 {count} 不在 [{lo}, {hi}] 范围内", "")

        return create_check_item_result("skip", f"暂不支持的字段检查: attribute={attribute}", "")

    def _check_multimedia_completeness(self, params: Dict) -> Dict[str, Any]:
        """检查多媒体素材包完整性：videos/ 目录有PPT、配音、manifest"""
        ppt_path_param = params.get("ppt_pattern", "workspace/videos/slides.pptx")
        audio_path_param = params.get("audio_pattern", "workspace/videos/narration.mp3")
        manifest_path_param = params.get("manifest_pattern", "workspace/videos/manifest.json")

        # 检查 videos/ 目录是否存在
        videos_dir = resolve_workspace_path(self.work_dir, "workspace/videos")
        if not videos_dir or not os.path.isdir(videos_dir):
            return create_check_item_result("fail", "videos/ 目录不存在", "")

        # 检查关键文件
        missing = []
        ppt_path = resolve_workspace_path(self.work_dir, ppt_path_param)
        if not ppt_path or not os.path.exists(ppt_path):
            missing.append("slides.pptx")

        audio_path = resolve_workspace_path(self.work_dir, audio_path_param)
        if not audio_path or not os.path.exists(audio_path):
            # 也检查分段音频 audio/ 目录
            audio_dir = resolve_workspace_path(self.work_dir, "workspace/videos/audio")
            if audio_dir and os.path.isdir(audio_dir):
                audio_files = glob.glob(os.path.join(audio_dir, "*.mp3"))
                if not audio_files:
                    missing.append("narration.mp3 或 audio/*.mp3")
            else:
                missing.append("narration.mp3")

        manifest_path = resolve_workspace_path(self.work_dir, manifest_path_param)
        if not manifest_path or not os.path.exists(manifest_path):
            missing.append("manifest.json")

        if not missing:
            return create_check_item_result(
                "pass",
                "多媒体素材完整（PPT+配音+清单）",
                f"videos/ 目录内容: {os.listdir(videos_dir)}"
            )
        else:
            return create_check_item_result(
                "fail",
                f"多媒体素材不完整，缺少: {missing}",
                f"videos/ 目录内容: {os.listdir(videos_dir) if os.path.isdir(videos_dir) else '目录不存在'}"
            )


class JSONSchemaChecker:
    """JSON Schema 合规性检查"""

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def check(self, params: Dict) -> Dict[str, Any]:
        file_path = params.get("file_path")
        file_pattern = params.get("file_pattern")

        if file_path:
            return self._check_single_file(file_path)
        elif file_pattern:
            return self._check_pattern(file_pattern)
        else:
            return create_check_item_result("skip", "缺少 file_path 或 file_pattern", "")

    def _check_single_file(self, file_path: str) -> Dict[str, Any]:
        resolved = resolve_workspace_path(self.work_dir, file_path)
        if not resolved:
            return create_check_item_result("fail", f"文件不存在: {file_path}", "")

        data = load_json_file(resolved)
        if data is None:
            try:
                with open(resolved, "r", encoding="utf-8") as f:
                    raw = f.read()
                return create_check_item_result("fail", f"JSON语法错误: {file_path}", f"前200字符: {raw[:200]}")
            except Exception:
                return create_check_item_result("fail", f"无法读取文件: {file_path}", "")

        if not isinstance(data, dict):
            return create_check_item_result("fail", f"JSON顶层不是object: {file_path}", f"类型: {type(data).__name__}")

        return create_check_item_result("pass", f"JSON合法且为object: {file_path}", f"顶层键: {list(data.keys())[:10]}")

    def _check_pattern(self, file_pattern: str) -> Dict[str, Any]:
        files = glob_workspace_files(self.work_dir, file_pattern)
        if not files:
            return create_check_item_result("fail", f"没有匹配的文件: {file_pattern}", "")

        failed = []
        for fp in files:
            data = load_json_file(fp)
            if data is None:
                failed.append(os.path.basename(fp))

        if not failed:
            return create_check_item_result("pass", f"所有 {len(files)} 个文件JSON合法", f"文件: {[os.path.basename(f) for f in files]}")
        else:
            return create_check_item_result("fail", f"{len(failed)} 个文件JSON不合法", f"失败文件: {failed}")


class ToolCalledWithParamsChecker:
    """工具调用验证

    支持的检查模式：
    1. min_call_count — 工具至少被调用N次
    2. required_calls — 调用时参数必须包含指定内容
    3. ordered_sequence — 按顺序调用多个工具
    4. ordered_calls — 有序调用检查（兼容 novel_to_script 格式）
    """

    def __init__(self):
        pass

    def check(self, params: Dict, conversation_history: List) -> Dict[str, Any]:
        check_subtype = params.get("check_subtype", "")

        if check_subtype == "ordered_sequence":
            return self._check_ordered_sequence(params, conversation_history)
        elif "ordered_calls" in params:
            return self._check_ordered_calls(params, conversation_history)
        else:
            return self._check_tool_call(params, conversation_history)

    def _extract_tool_calls(self, conversation_history: List) -> List[Dict]:
        """从对话历史中提取所有工具调用"""
        calls = []
        for msg in conversation_history:
            if msg.get("role") == "assistant":
                tool_calls = msg.get("tool_calls", [])
                for tc in tool_calls:
                    func = tc.get("function", {})
                    name = func.get("name", "")
                    try:
                        args = json.loads(func.get("arguments", "{}"))
                    except (json.JSONDecodeError, TypeError):
                        args = {}
                    calls.append({"name": name, "arguments": args, "index": len(calls)})
        return calls

    def _check_tool_call(self, params: Dict, conversation_history: List) -> Dict[str, Any]:
        """检查工具调用：支持 min_call_count、required_calls"""
        tool_name = params.get("tool_name", "")
        min_call_count = params.get("min_call_count")
        required_calls = params.get("required_calls", [])
        expected_params = params.get("expected_params", {})

        calls = self._extract_tool_calls(conversation_history)

        # 构建候选工具名（MCP工具名可能带前缀）
        candidate_names = {tool_name}
        # MCP 工具名格式可能是 "server__tool_name"
        for call in calls:
            if call["name"].endswith(f"__{tool_name}"):
                candidate_names.add(call["name"])
            # 也兼容 write_file/write_files
            if tool_name == "write_file" and call["name"].endswith("__write_files"):
                candidate_names.add(call["name"])
            elif tool_name == "write_files" and call["name"].endswith("__write_file"):
                candidate_names.add(call["name"])

        matching_calls = [c for c in calls if c["name"] in candidate_names]

        # min_call_count 检查
        if min_call_count is not None:
            min_val = int(min_call_count)
            if len(matching_calls) >= min_val:
                # 如果有 required_calls，继续检查参数
                if required_calls:
                    return self._check_required_calls_detail(tool_name, matching_calls, required_calls)
                return create_check_item_result(
                    "pass", f"工具 {tool_name} 调用 {len(matching_calls)} 次 >= {min_val}",
                    f"调用参数示例: {matching_calls[0]['arguments'] if matching_calls else {}}"
                )
            else:
                return create_check_item_result(
                    "fail", f"工具 {tool_name} 调用 {len(matching_calls)} 次 < {min_val}",
                    f"共 {len(calls)} 次工具调用"
                )

        # required_calls 检查（无 min_call_count 时，至少1次匹配）
        if required_calls:
            return self._check_required_calls_detail(tool_name, matching_calls, required_calls)

        # expected_params 检查（兼容旧格式）
        if expected_params:
            if not matching_calls:
                return create_check_item_result("fail", f"工具 {tool_name} 未被调用", "")
            for call in matching_calls:
                if self._params_match(call["arguments"], expected_params):
                    return create_check_item_result("pass", f"工具 {tool_name} 调用参数匹配", "")
            return create_check_item_result("fail", f"工具 {tool_name} 参数不匹配", "")

        # 仅检查是否调用过
        if not matching_calls:
            return create_check_item_result("fail", f"工具 {tool_name} 未被调用", f"共 {len(calls)} 次工具调用")
        return create_check_item_result("pass", f"工具 {tool_name} 被调用 {len(matching_calls)} 次", "")

    def _check_required_calls_detail(self, tool_name: str, matching_calls: List[Dict], required_calls: List[Dict]) -> Dict[str, Any]:
        """检查 required_calls 中的每个条件"""
        for req in required_calls:
            params_contain = req.get("params_contain", {})
            found = False
            for call in matching_calls:
                if self._params_contain_match(call["arguments"], params_contain):
                    found = True
                    break
            if not found:
                return create_check_item_result(
                    "fail",
                    f"工具 {tool_name} 调用中未找到包含 {params_contain} 的调用",
                    f"实际调用参数: {[c['arguments'] for c in matching_calls[:5]]}"
                )

        return create_check_item_result(
            "pass",
            f"工具 {tool_name} 的 {len(required_calls)} 个调用条件都匹配",
            ""
        )

    def _check_ordered_sequence(self, params: Dict, conversation_history: List) -> Dict[str, Any]:
        """检查工具调用顺序（check_subtype=ordered_sequence）"""
        tool_name = params.get("tool_name", "")
        required_sequence = params.get("required_sequence", [])

        calls = self._extract_tool_calls(conversation_history)

        # 构建候选工具名
        candidate_names = {tool_name}
        for call in calls:
            if call["name"].endswith(f"__{tool_name}"):
                candidate_names.add(call["name"])
            if tool_name == "write_file" and call["name"].endswith("__write_files"):
                candidate_names.add(call["name"])
            elif tool_name == "write_files" and call["name"].endswith("__write_file"):
                candidate_names.add(call["name"])

        matching_calls = [c for c in calls if c["name"] in candidate_names]
        last_index = -1

        for seq_item in required_sequence:
            params_contain = seq_item.get("params_contain", {})
            found = False
            for call in matching_calls:
                if call["index"] <= last_index:
                    continue
                if self._params_contain_match(call["arguments"], params_contain):
                    last_index = call["index"]
                    found = True
                    break

            if not found:
                return create_check_item_result(
                    "fail",
                    f"工具 {tool_name} 调用顺序不符：未按序找到包含 {params_contain} 的调用",
                    f"期望顺序: {[s.get('params_contain') for s in required_sequence]}"
                )

        return create_check_item_result(
            "pass", f"工具 {tool_name} 调用顺序正确",
            f"验证了 {len(required_sequence)} 个有序调用"
        )

    def _check_ordered_calls(self, params: Dict, conversation_history: List) -> Dict[str, Any]:
        """兼容 novel_to_script 的 ordered_calls 格式"""
        ordered_calls = params.get("ordered_calls", [])
        if not ordered_calls:
            return create_check_item_result("skip", "ordered_calls 为空", "")

        calls = self._extract_tool_calls(conversation_history)
        last_index = -1

        for expected in ordered_calls:
            tool_name = expected.get("tool_name", "")
            params_contains = expected.get("params_contains", {})

            candidate_names = {tool_name}
            if tool_name.endswith("__write_file"):
                candidate_names.add(tool_name + "s")
            elif tool_name.endswith("__write_files"):
                candidate_names.add(tool_name[:-1])

            found = False
            for call in calls:
                if call["index"] <= last_index:
                    continue
                if call["name"] in candidate_names:
                    if self._params_contain_match(call["arguments"], params_contains):
                        last_index = call["index"]
                        found = True
                        break

            if not found:
                return create_check_item_result(
                    "fail",
                    f"工具调用顺序不符：{tool_name} 未在正确位置被调用",
                    f"期望顺序: {[c.get('tool_name') for c in ordered_calls]}"
                )

        return create_check_item_result(
            "pass", f"工具调用顺序正确",
            f"验证了 {len(ordered_calls)} 个有序调用"
        )

    def _params_match(self, actual: Dict, expected: Dict) -> bool:
        """检查参数是否匹配"""
        for key, constraint in expected.items():
            actual_val = actual.get(key, "")
            if isinstance(constraint, dict):
                if "contains" in constraint:
                    if constraint["contains"] not in str(actual_val):
                        return False
            elif str(actual_val) != str(constraint):
                return False
        return True

    def _params_contain_match(self, actual: Dict, params_contain: Dict) -> bool:
        """检查参数是否包含指定内容（子串匹配）"""
        for key, substring in params_contain.items():
            actual_val = str(actual.get(key, ""))
            if substring not in actual_val:
                # 也检查整个参数的JSON字符串形式
                actual_str = json.dumps(actual, ensure_ascii=False)
                if substring not in actual_str:
                    return False
        return True


class CrossFileConsistencyChecker:
    """跨文件一致性检查"""

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def check(self, params: Dict) -> Dict[str, Any]:
        check_subtype = params.get("check_subtype", "")
        consistency_rule = params.get("consistency_rule", "")

        # 优先按 check_subtype 分发
        if check_subtype == "count_equals":
            return self._check_count_equals(params)

        # 兼容 consistency_rule
        if consistency_rule in ("target_subset_of_source", "source_subset_of_target"):
            return self._check_subset(params)
        elif consistency_rule == "equal":
            return self._check_equal(params)

        return create_check_item_result("skip", f"未知的check_subtype: {check_subtype}, consistency_rule: {consistency_rule}", "")

    def _check_count_equals(self, params: Dict) -> Dict[str, Any]:
        """检查源文件字段值与目标文件数量是否一致

        支持两种模式：
        1. source_field(数值) vs target_directory 下的文件数
        2. source_field(数组) vs target_field(数组)
        """
        source_file = params.get("source_file", "")
        source_field = params.get("source_field", "")
        target_directory = params.get("target_directory", "")
        target_pattern = params.get("target_pattern", "*.json")
        target_file = params.get("target_file", "")
        target_field = params.get("target_field", "")

        # 加载 source
        source_path = resolve_workspace_path(self.work_dir, source_file)
        if not source_path:
            return create_check_item_result("fail", f"源文件不存在: {source_file}", "")

        source_data = load_json_file(source_path)
        if source_data is None:
            return create_check_item_result("fail", f"源文件JSON解析失败: {source_file}", "")

        source_value = extract_json_field(source_data, source_field)

        # 获取 source count
        if isinstance(source_value, (int, float)):
            source_count = int(source_value)
        elif isinstance(source_value, list):
            source_count = len(source_value)
        else:
            return create_check_item_result("fail", f"源字段 {source_field} 不是数值或数组: {source_value}", "")

        # 模式1：vs target_directory
        if target_directory:
            dir_path = resolve_workspace_path(self.work_dir, target_directory)
            if not dir_path or not os.path.isdir(dir_path):
                return create_check_item_result("fail", f"目标目录不存在: {target_directory}", "")

            target_files = glob.glob(os.path.join(dir_path, target_pattern))
            target_count = len(target_files)

            if source_count == target_count:
                return create_check_item_result(
                    "pass", f"数量一致: {source_count}",
                    f"源字段={source_count}, 文件数={target_count}"
                )
            else:
                return create_check_item_result(
                    "fail", f"数量不一致: 源={source_count}, 目标={target_count}",
                    f"源字段 {source_field}={source_count}, {target_directory}下{target_pattern}数量={target_count}"
                )

        # 模式2：vs target_file.target_field
        if target_file and target_field:
            tp = resolve_workspace_path(self.work_dir, target_file)
            if not tp:
                return create_check_item_result("fail", f"目标文件不存在: {target_file}", "")

            target_data = load_json_file(tp)
            if target_data is None:
                return create_check_item_result("fail", f"目标文件JSON解析失败: {target_file}", "")

            target_value = extract_json_field(target_data, target_field)
            if isinstance(target_value, list):
                target_count = len(target_value)
            elif isinstance(target_value, (int, float)):
                target_count = int(target_value)
            else:
                return create_check_item_result("fail", f"目标字段 {target_field} 不是数组或数值", "")

            if source_count == target_count:
                return create_check_item_result("pass", f"数量一致: {source_count}", "")
            else:
                return create_check_item_result("fail", f"数量不一致: 源={source_count}, 目标={target_count}", "")

        return create_check_item_result("skip", "缺少 target_directory 或 target_file", "")

    def _check_subset(self, params: Dict) -> Dict[str, Any]:
        """检查集合子集关系"""
        source_file = params.get("source_file", "")
        source_field = params.get("source_field", "")
        target_files = params.get("target_files", "")
        target_field = params.get("target_field", "")
        rule = params.get("consistency_rule")

        source_path = resolve_workspace_path(self.work_dir, source_file)
        if not source_path:
            return create_check_item_result("fail", f"源文件不存在: {source_file}", "")

        source_data = load_json_file(source_path)
        if source_data is None:
            return create_check_item_result("fail", f"源文件JSON解析失败: {source_file}", "")

        source_values = extract_json_field(source_data, source_field)
        if not isinstance(source_values, list):
            source_values = [source_values] if source_values else []
        source_set = set(str(v) for v in source_values if v)

        # 加载 target
        target_values_all = set()
        if "*" in target_files:
            target_file_list = glob_workspace_files(self.work_dir, target_files)
        else:
            tp = resolve_workspace_path(self.work_dir, target_files)
            target_file_list = [tp] if tp else []

        for tf in target_file_list:
            td = load_json_file(tf)
            if td:
                vals = extract_json_field(td, target_field)
                if isinstance(vals, list):
                    target_values_all.update(str(v) for v in vals if v)
                elif vals:
                    target_values_all.add(str(vals))

        if rule == "target_subset_of_source":
            extra = target_values_all - source_set
            if not extra:
                return create_check_item_result("pass", "目标值全部在源集合中", "")
            else:
                return create_check_item_result("fail", f"目标中有 {len(extra)} 个值不在源中", f"多余值: {extra}")
        else:
            missing = source_set - target_values_all
            if not missing:
                return create_check_item_result("pass", "源值全部在目标中有对应", "")
            else:
                return create_check_item_result("fail", f"源中有 {len(missing)} 个值在目标中缺失", f"缺失值: {missing}")

    def _check_equal(self, params: Dict) -> Dict[str, Any]:
        """兼容 consistency_rule=equal"""
        source_file = params.get("source_file", "")
        source_field = params.get("source_field", "")
        source_attribute = params.get("source_attribute", "")
        target_type = params.get("target_type", "")

        source_path = resolve_workspace_path(self.work_dir, source_file)
        if not source_path:
            return create_check_item_result("fail", f"源文件不存在: {source_file}", "")

        source_data = load_json_file(source_path)
        if source_data is None:
            return create_check_item_result("fail", f"源文件JSON解析失败", "")

        source_value = extract_json_field(source_data, source_field)
        if source_attribute == "length" and isinstance(source_value, list):
            source_count = len(source_value)
        else:
            source_count = source_value

        if target_type == "file_count":
            target_dir = params.get("target_directory", "")
            target_pattern = params.get("target_pattern", "*.json")
            dir_path = resolve_workspace_path(self.work_dir, target_dir)
            if not dir_path or not os.path.isdir(dir_path):
                return create_check_item_result("fail", f"目标目录不存在: {target_dir}", "")
            target_files = glob.glob(os.path.join(dir_path, target_pattern))
            target_count = len(target_files)

            if source_count == target_count:
                return create_check_item_result("pass", f"数量一致: {source_count}", "")
            else:
                return create_check_item_result("fail", f"数量不一致: 源={source_count}, 目标={target_count}", "")

        return create_check_item_result("skip", f"未知的target_type: {target_type}", "")


class SemanticChecker:
    """LLM语义检查 + 程序化内容检查"""

    def __init__(self, work_dir: str, model_name: str = "", api_base: str = "", api_key: str = ""):
        self.work_dir = work_dir
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key

    def check(self, params: Dict, sample_result: Dict) -> Dict[str, Any]:
        """分发 semantic_check"""
        check_subtype = params.get("check_subtype", "")
        use_llm = params.get("use_llm_judge", False)

        # 程序化子类型优先
        if check_subtype == "keyword_absence":
            return self._check_keyword_absence(params)

        # 有 judge_criteria_file / judge_section → LLM judge
        if params.get("judge_criteria_file") or params.get("llm_judge_criteria_file"):
            return self._llm_judge_check(params, sample_result)

        # 兼容旧格式
        validation_rules = params.get("validation_rules")
        if validation_rules and not use_llm:
            return self._programmatic_check(params)
        if use_llm and not validation_rules:
            return self._llm_judge_check(params, sample_result)
        if validation_rules and use_llm:
            prog_result = self._programmatic_check(params)
            if prog_result.get("check_result") == "fail":
                return prog_result
            return self._llm_judge_check(params, sample_result)

        return create_check_item_result("skip", "semantic_check 无有效的检查配置", "")

    def _check_keyword_absence(self, params: Dict) -> Dict[str, Any]:
        """程序化：检查禁止关键词"""
        file_pattern = params.get("file_pattern", "")
        field_path = params.get("field_path", "")
        forbidden_keywords = params.get("forbidden_keywords", [])

        files = glob_workspace_files(self.work_dir, file_pattern)
        if not files:
            return create_check_item_result("skip", f"未找到文件: {file_pattern}", "")

        violations = []
        for fp in files:
            data = load_json_file(fp)
            if not data:
                continue

            # 提取字段内容
            values = extract_json_field(data, field_path)
            if not isinstance(values, list):
                values = [values] if values else []

            for text in values:
                text_str = str(text)
                for kw in forbidden_keywords:
                    if kw in text_str:
                        violations.append({
                            "file": os.path.basename(fp),
                            "keyword": kw,
                            "context": text_str[:100]
                        })

        if not violations:
            return create_check_item_result("pass", f"禁止关键词检查通过（检查了{len(files)}个文件）", "")
        else:
            return create_check_item_result(
                "fail",
                f"发现 {len(violations)} 处禁止关键词",
                json.dumps(violations[:10], ensure_ascii=False)
            )

    def _programmatic_check(self, params: Dict) -> Dict[str, Any]:
        """程序化内容检查（兼容旧格式）"""
        rules = params.get("validation_rules", [])
        if not rules:
            return create_check_item_result("skip", "无validation_rules", "")

        for rule in rules:
            method = rule.get("validation_method", "")
            if method == "keyword_absence":
                return self._check_keyword_absence_rule(rule, params)

        return create_check_item_result("skip", f"不支持的validation_method", "")

    def _check_keyword_absence_rule(self, rule: Dict, params: Dict) -> Dict[str, Any]:
        """兼容旧格式的禁止关键词检查"""
        analysis_target = params.get("analysis_target", "")
        forbidden_keywords = rule.get("forbidden_keywords", [])
        threshold = rule.get("threshold", 0)

        files = self._resolve_target_files(analysis_target)
        violations = []

        for fp in files:
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
                for kw in forbidden_keywords:
                    if kw in content:
                        violations.append({"file": os.path.basename(fp), "keyword": kw})
            except Exception:
                pass

        if len(violations) <= threshold:
            return create_check_item_result("pass", f"禁止关键词检查通过（违规{len(violations)}次）", "")
        else:
            return create_check_item_result("fail", f"发现 {len(violations)} 处禁止关键词", json.dumps(violations[:10], ensure_ascii=False))

    def _llm_judge_check(self, params: Dict, sample_result: Dict) -> Dict[str, Any]:
        """LLM Judge 语义检查"""
        criteria = load_judge_criteria(params, self.work_dir)
        if not criteria:
            return create_check_item_result("skip", "无法加载LLM Judge评判标准", "")

        # 收集待评估内容
        content_to_evaluate = self._collect_evaluation_content(params)
        if not content_to_evaluate:
            return create_check_item_result("skip", "无法收集待评估内容", "")

        # 加载源材料（reference）
        reference_content = self._collect_source_content(params)

        # 构建 prompt
        prompt_parts = ["# 评估任务\n"]
        prompt_parts.append("请根据以下评判标准，评估待评内容的质量。\n")

        prompt_parts.append("## 评判标准\n")
        prompt_parts.append(criteria)
        prompt_parts.append("\n")

        if reference_content:
            max_ref_len = 8000
            if len(reference_content) > max_ref_len:
                reference_content = reference_content[:max_ref_len] + "\n...[源材料内容截断]..."
            prompt_parts.append("## 源技术文档（参考）\n")
            prompt_parts.append(reference_content)
            prompt_parts.append("\n")

        prompt_parts.append("## 待评估内容\n")
        max_content_len = 12000
        if len(content_to_evaluate) > max_content_len:
            content_to_evaluate = content_to_evaluate[:max_content_len] + "\n...[内容截断]..."
        prompt_parts.append(content_to_evaluate)

        prompt = "\n".join(prompt_parts)

        messages = [
            {"role": "system", "content": "你是一位专业的技术教育内容评审专家。请严格按照评判标准进行评估，以JSON格式返回结果。"},
            {"role": "user", "content": prompt}
        ]

        success, response = request_llm_with_litellm(
            messages, self.model_name, self.api_base, self.api_key
        )

        if not success:
            return create_check_item_result("skip", f"LLM调用失败: {response}", "")

        result_json = safe_json_extract_single(response)
        if result_json is None:
            return create_check_item_result("skip", f"LLM返回JSON解析失败", f"原始响应: {response[:500]}")

        # 兼容 LLM 返回 list 的情况
        if isinstance(result_json, list):
            dict_items = [item for item in result_json if isinstance(item, dict)]
            if dict_items:
                result_json = dict_items[0]
            else:
                return create_check_item_result("skip", "LLM返回JSON数组但无dict元素", "")

        # 兼容 passed / matched 两种字段名
        passed = result_json.get("passed", result_json.get("matched"))
        reason = result_json.get("reason", "")

        if passed is True:
            return create_check_item_result("pass", reason, json.dumps(result_json, ensure_ascii=False, indent=2))
        elif passed is False:
            return create_check_item_result("fail", reason, json.dumps(result_json, ensure_ascii=False, indent=2))
        else:
            return create_check_item_result("skip", f"LLM返回结果无法判断: {result_json}", "")

    def _resolve_target_files(self, target) -> List[str]:
        """解析文件路径为列表"""
        if isinstance(target, str):
            targets = [target]
        elif isinstance(target, list):
            targets = target
        else:
            return []

        files = []
        for t in targets:
            if "*" in t:
                files.extend(glob_workspace_files(self.work_dir, t))
            else:
                path = resolve_workspace_path(self.work_dir, t)
                if path:
                    if os.path.isdir(path):
                        # 如果是目录，列出所有 JSON 文件
                        for f in sorted(os.listdir(path)):
                            if f.endswith(".json"):
                                files.append(os.path.join(path, f))
                    else:
                        files.append(path)
        return files

    def _collect_evaluation_content(self, params: Dict) -> str:
        """收集待评估内容"""
        # 优先 reference_files（knowledge_video_creator 格式）
        target = params.get("reference_files") or params.get("analysis_target")
        files = self._resolve_target_files(target)

        if not files:
            return ""

        parts = []
        for fp in files:
            basename = os.path.basename(fp)
            if fp.endswith(".json"):
                data = load_json_file(fp)
                if data:
                    parts.append(f"### 文件: {basename}\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```\n")
            else:
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        content = f.read()
                    parts.append(f"### 文件: {basename}\n{content}\n")
                except Exception:
                    pass

        return "\n".join(parts)

    def _collect_source_content(self, params: Dict) -> str:
        """收集源材料内容（用于与Agent输出对照）"""
        source_files = params.get("source_files")
        reference_file = params.get("reference_file")

        targets = source_files or ([reference_file] if reference_file else None)
        if not targets:
            return ""

        files = self._resolve_target_files(targets)
        parts = []

        for fp in files:
            basename = os.path.basename(fp)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
                parts.append(f"### {basename}\n{content}\n")
            except Exception:
                pass

        return "\n".join(parts)


# ============================================
# SOP Stage Coverage 检查（Gate级）
# ============================================

def _check_sop_stage_coverage(check_item: Dict, work_dir: str) -> Dict[str, Any]:
    """Gate级检查：文件/目录是否存在且有实际内容"""
    params = check_item.get("params", {})
    required_evidence = params.get("required_evidence", [])

    for evidence in required_evidence:
        ev_type = evidence.get("type", "")

        if ev_type == "file_pattern_exists":
            pattern = evidence.get("pattern", "")
            min_count = evidence.get("min_count", 1)
            files = glob_workspace_files(work_dir, pattern)
            if len(files) < min_count:
                result = create_check_item_result(
                    "fail",
                    f"文件不足: {pattern} 需要至少 {min_count} 个，实际 {len(files)} 个",
                    ""
                )
                result["execution_collapsed"] = True
                return result

        elif ev_type == "file_not_empty":
            pattern = evidence.get("pattern", "")
            min_size = evidence.get("min_size_bytes", 0)
            files = glob_workspace_files(work_dir, pattern)
            for fp in files:
                size = os.path.getsize(fp)
                if size < min_size:
                    result = create_check_item_result(
                        "fail",
                        f"文件 {os.path.basename(fp)} 内容不足: {size} bytes < {min_size}",
                        ""
                    )
                    result["execution_collapsed"] = True
                    return result

        elif ev_type == "directory_exists":
            pattern = evidence.get("pattern", "")
            min_count = evidence.get("min_count", 1)
            dirs = glob_workspace_files(work_dir, pattern)
            dirs = [d for d in dirs if os.path.isdir(d)]
            if len(dirs) < min_count:
                result = create_check_item_result(
                    "fail",
                    f"目录不足: {pattern} 需要至少 {min_count} 个，实际 {len(dirs)} 个",
                    ""
                )
                result["execution_collapsed"] = True
                return result

    return create_check_item_result("pass", "SOP阶段产出检查通过", f"验证了 {len(required_evidence)} 项证据")


# ============================================
# 主执行函数
# ============================================

def execute_checks(
    check_list: List[Dict],
    sample_result: Dict,
    work_dir: str,
    model_name: str = "",
    api_base: str = "",
    api_key: str = ""
) -> Dict[str, Any]:
    """
    执行所有检查项

    Args:
        check_list: 检查项列表（从bench.json的check_list字段）
        sample_result: Agent执行结果（包含conversation_history）
        work_dir: 工作目录
        model_name: LLM模型名称
        api_base: LLM API地址
        api_key: LLM API密钥

    Returns:
        {"check_details": {"检查项ID": {result}}}
    """
    # 初始化各检查器
    fs_checker = FileSystemChecker(work_dir)
    schema_checker = JSONSchemaChecker(work_dir)
    tool_checker = ToolCalledWithParamsChecker()
    cross_checker = CrossFileConsistencyChecker(work_dir)
    semantic_checker = SemanticChecker(work_dir, model_name, api_base, api_key)

    conversation_history = sample_result.get("conversation_history", [])
    check_details = {}

    for idx, check_item in enumerate(check_list):
        check_id = check_item.get("check_id", f"检查项{idx + 1}")
        check_type = check_item.get("check_type", "")
        description = check_item.get("description", "")

        logger.info(f"[{idx + 1}/{len(check_list)}] 执行检查: {check_id} ({check_type})")

        try:
            if check_type == "entity_attribute_equals":
                result = fs_checker.check(check_item)
            elif check_type == "json_schema":
                result = schema_checker.check(check_item.get("params", {}))
            elif check_type == "tool_called_with_params":
                result = tool_checker.check(check_item.get("params", {}), conversation_history)
            elif check_type == "cross_file_consistency":
                result = cross_checker.check(check_item.get("params", {}))
            elif check_type == "semantic_check":
                result = semantic_checker.check(check_item.get("params", {}), sample_result)
            elif check_type == "sop_stage_coverage":
                result = _check_sop_stage_coverage(check_item, work_dir)
            else:
                result = create_check_item_result("skip", f"不支持的检查类型: {check_type}", "")
        except Exception as e:
            logger.error(f"检查项 {check_id} 执行异常: {e}")
            import traceback
            traceback.print_exc()
            result = create_check_item_result("skip", f"执行异常: {str(e)}", "")

        # 复制检查项元数据到结果
        result["description"] = description
        result["check_type"] = check_type
        for key in ["dimension_id", "subcategory_id", "quality_tier", "is_gate", "is_critical", "weight"]:
            if key in check_item:
                result[key] = check_item[key]

        check_details[check_id] = result
        logger.info(f"  → {result['check_result']}: {result['reason'][:80]}")

    return {"check_details": check_details}
