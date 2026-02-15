#!/usr/bin/env python3
"""
提取所有模型 DSV1/DSV2 的 rev006 check 结果，输出结构化 JSON 供分析使用。
"""
import json
import os
import glob
import sys

EVAL_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "evaluation_outputs"
)

# 模型名称映射（目录后缀 → 简称）
MODEL_MAP = {
    "claude-opus-4-5-20251101": "claude-4.5",
    "claude-opus-4-6": "claude-4.6",
    "gemini-3-pro-preview": "gemini-3-pro",
    "kimi-k2.5": "kimi-k2.5",
    "ernie-5.0-thinking-preview": "ernie-5.0",
    "openai_EB5-0209-A35B-midtrain-128k-chat": "EB5-midtrain",
    "qwen3-max-2026-01-23": "qwen3-max",
    "glm-4.7": "glm-4.7",
    "doubao-seed-2-0-pro-260215": "doubao-2.0-pro",
}

def extract_model_name(dirname):
    """从目录名中提取模型简称"""
    # eval_dsv1_20260214_014809_claude-opus-4-6 → claude-opus-4-6
    parts = dirname.split("_", 4)  # split into at most 5 parts
    if len(parts) >= 5:
        model_suffix = parts[4]
    else:
        model_suffix = parts[-1]
    return MODEL_MAP.get(model_suffix, model_suffix)

def extract_version(dirname):
    """从目录名提取 dsv1 或 dsv2"""
    if "dsv1" in dirname:
        return "dsv1"
    elif "dsv2" in dirname:
        return "dsv2"
    return "unknown"

def extract_data_id(sample_id):
    """从 sample_id 提取 data_id (去掉 NW_ 前缀和 CLEAR_/VAGUE_/IP_/ULTRA_ 前缀的核心部分)
    
    实际上为了配对，我们需要保留完整的 sample_id 去掉 NW_ 前缀。
    共有 task 的判定基于文档中已知的 6 个：
    MEDIUM_ANGSTY_001, MEDIUM_SUSPENSE_001, MEDIUM_SWEET_001, 
    SHORT_ANGSTY_001, SHORT_SWEET_001, IP_NEUTRAL_001
    """
    # 返回去掉 NW_ 前缀的部分
    if sample_id.startswith("NW_"):
        return sample_id[3:]
    return sample_id

# 共有 task 的 DSV1 和 DSV2 sample_id 映射
SHARED_TASKS = {
    "MEDIUM_ANGSTY_001": {
        "dsv1": "NW_CLEAR_MEDIUM_ANGSTY_001",
        "dsv2": "NW_CLEAR_MEDIUM_ANGSTY_001"
    },
    "MEDIUM_SUSPENSE_001": {
        "dsv1": "NW_CLEAR_MEDIUM_SUSPENSE_001",
        "dsv2": "NW_CLEAR_MEDIUM_SUSPENSE_001"
    },
    "MEDIUM_SWEET_001": {
        "dsv1": "NW_CLEAR_MEDIUM_SWEET_001",
        "dsv2": "NW_CLEAR_MEDIUM_SWEET_001"
    },
    "SHORT_ANGSTY_001": {
        "dsv1": "NW_CLEAR_SHORT_ANGSTY_001",
        "dsv2": "NW_CLEAR_SHORT_ANGSTY_001"
    },
    "SHORT_SWEET_001": {
        "dsv1": "NW_CLEAR_SHORT_SWEET_001",
        "dsv2": "NW_CLEAR_SHORT_SWEET_001"
    },
    "IP_NEUTRAL_001": {
        "dsv1": "NW_IP_MEDIUM_NEUTRAL_001",
        "dsv2": "NW_IP_MEDIUM_NEUTRAL_001"
    },
}

def load_check_result(env_dir):
    """加载 rev006 check 结果"""
    rev006_path = os.path.join(env_dir, "check_result_rev006.json")
    if os.path.exists(rev006_path):
        with open(rev006_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def extract_scores(check_result):
    """从 check_result 中提取关键分数"""
    overall = check_result.get("overall_result", {})
    dims = check_result.get("dimension_scores", {})
    
    result = {
        "total_score": overall.get("total_score"),
        "content_score": overall.get("content_score"),
        "process_score": overall.get("process_score"),
        "pass_rate": overall.get("pass_rate"),
        "total_checks": overall.get("total_checks"),
        "passed_checks": overall.get("passed_checks"),
        "failed_checks": overall.get("failed_checks"),
        "gate_triggered": overall.get("gate_triggered"),
    }
    
    # 维度级别 pass_rate
    for dim_name in ["format_compliance", "business_rule_compliance", "memory_management"]:
        dim = dims.get(dim_name, {})
        result[f"{dim_name}_pass_rate"] = dim.get("pass_rate")
        result[f"{dim_name}_total"] = dim.get("total")
        result[f"{dim_name}_passed"] = dim.get("passed")
        result[f"{dim_name}_failed"] = dim.get("failed")
        result[f"{dim_name}_skipped"] = dim.get("skipped")
    
    # content_quality 各层
    cq = dims.get("content_quality", {})
    result["content_quality_overall_score"] = cq.get("overall_score")
    result["content_quality_quality_level"] = cq.get("quality_level")
    
    for layer in ["gate_layer", "basic_layer", "advanced_layer"]:
        layer_data = cq.get(layer, {})
        result[f"content_{layer}_pass_rate"] = layer_data.get("pass_rate")
        result[f"content_{layer}_total"] = layer_data.get("total")
        result[f"content_{layer}_passed"] = layer_data.get("passed")
        result[f"content_{layer}_failed"] = layer_data.get("failed")
        result[f"content_{layer}_skipped"] = layer_data.get("skipped")
    
    return result

def extract_subcategory_results(check_result):
    """提取每个 subcategory 的 pass/fail/skip"""
    details = check_result.get("check_details", {})
    subcats = {}
    for check_name, check_info in details.items():
        subcat = check_info.get("subcategory_id", "unknown")
        result = check_info.get("check_result", "skip")
        if subcat not in subcats:
            subcats[subcat] = {"pass": 0, "fail": 0, "skip": 0}
        subcats[subcat][result] = subcats[subcat].get(result, 0) + 1
    return subcats

def main():
    all_data = []
    
    for dirname in sorted(os.listdir(EVAL_DIR)):
        full_path = os.path.join(EVAL_DIR, dirname)
        if not os.path.isdir(full_path) or not dirname.startswith("eval_dsv"):
            continue
        
        version = extract_version(dirname)
        model = extract_model_name(dirname)
        
        # 遍历每个样本的 _env 目录
        for env_dirname in sorted(os.listdir(full_path)):
            env_path = os.path.join(full_path, env_dirname)
            if not os.path.isdir(env_path) or not env_dirname.endswith("_env"):
                continue
            
            sample_id = env_dirname.replace("_env", "")
            check_result = load_check_result(env_path)
            if check_result is None:
                continue
            
            scores = extract_scores(check_result)
            subcats = extract_subcategory_results(check_result)
            
            record = {
                "dir": dirname,
                "version": version,
                "model": model,
                "sample_id": sample_id,
                "data_id": extract_data_id(sample_id),
                **scores,
                "subcategory_results": subcats,
            }
            all_data.append(record)
    
    # 输出
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rev006_all_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    # 汇总统计
    print(f"共提取 {len(all_data)} 条记录")
    
    from collections import Counter
    version_model = Counter()
    for r in all_data:
        version_model[(r["version"], r["model"])] += 1
    
    print(f"\n{'版本':<6} {'模型':<20} {'样本数':>6}")
    print("-" * 40)
    for (v, m), cnt in sorted(version_model.items()):
        print(f"{v:<6} {m:<20} {cnt:>6}")

if __name__ == "__main__":
    main()
