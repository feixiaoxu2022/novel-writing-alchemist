#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说创作炼金术场景 - Checker评分模块 (v3.0)

职责：读取execution_result，按能力维度聚合统计，计算质量等级
输入：execution_result.json（checker_execute的输出）
输出：check_result.json（含维度分数、质量等级和overall统计）

v3.0变更（基准60分公式）：
- 内容分 = clamp(0, 100, 60 - gate惩罚 - basic扣分 + advanced加分)
- Gate fail: 每项 -20分（3项 gate，最多扣60分）
- Basic fail: 每项 -(60/basic_total)分（basic全fail → 扣60分 → 到0分）
- Advanced pass: 每项 +(40/adv_total)分（adv全过 → +40分 → 到100分）
- 总分 = 内容分×0.7 + 流程规范分×0.3
"""

import json
import argparse
import sys
from typing import Dict, List, Tuple
from pathlib import Path


# =========================================
# 1. 常量定义
# =========================================

# 4个能力维度
CAPABILITY_DIMENSIONS = [
    "format_compliance",           # 格式规范遵循
    "business_rule_compliance",    # 业务规则遵循
    "memory_management",           # 记忆管理
    "content_quality"              # 内容创作质量
]

# content_quality维度的两层
QUALITY_TIERS = ["basic", "advanced"]

# Gate层（一票否决）的subcategory_id
GATE_SUBCATEGORIES = {
    "chapter_cloning",          # P1
    "alternating_repetition",   # P2
    "chapter_completion",       # P3
    "sop_stage_coverage",       # P0: SOP执行完整性（未产出章节=执行崩坏）
}

# 权重配置
CONTENT_WEIGHT = 0.7   # 内容质量占70%
PROCESS_WEIGHT = 0.3   # 流程合规占30%

# 基准60分公式参数
BASE_SCORE = 60.0               # 基准分
GATE_PENALTY_PER_ITEM = 20.0    # Gate每项fail扣20分
BASIC_POOL = 60.0               # Basic层扣分池（basic全fail扣60分，到0分）
ADVANCED_POOL = 40.0            # Advanced层加分池（adv全过加40分，到100分）


# =========================================
# 2. 辅助函数
# =========================================

def calculate_dimension_score(checks: List[Dict]) -> Dict:
    """
    计算单个维度的通过率

    Args:
        checks: 该维度的所有检查项（每项包含check_id和result）

    Returns:
        {
            "pass_rate": 通过率(0-1),
            "total": 有效总数(排除skip),
            "passed": 通过数,
            "failed": 失败数,
            "skipped": 跳过数,
            "failed_items": [失败的check_id列表]
        }
    """
    total_all = len(checks)

    if total_all == 0:
        return {
            "pass_rate": 0.0,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "failed_items": []
        }

    # 兼容中英文字段名
    passed = sum(1 for c in checks if c.get("result") == "pass" or c.get("check_result") == "pass")
    failed = sum(1 for c in checks if c.get("result") == "fail" or c.get("check_result") == "fail")
    skipped = sum(1 for c in checks if c.get("result") == "skip" or c.get("check_result") == "skip")

    failed_items = [
        c.get("check_id", "未知")
        for c in checks
        if c.get("result") == "fail" or c.get("check_result") == "fail"
    ]

    # 计算pass_rate时排除skip，只统计pass和fail
    total = passed + failed
    if total == 0:
        # 全部都是skip
        pass_rate = 0.0
    else:
        pass_rate = passed / total

    return {
        "pass_rate": round(pass_rate, 3),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "failed_items": failed_items
    }


def separate_gate_checks(basic_checks: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    从basic检查项中分离出Gate层检查项。

    Gate层检查项通过 is_gate=True 或 subcategory_id 在 GATE_SUBCATEGORIES 中识别。

    Args:
        basic_checks: basic层所有检查项

    Returns:
        (gate_checks, non_gate_basic_checks)
    """
    gate_checks = []
    non_gate_checks = []

    for check in basic_checks:
        subcategory_id = check.get("subcategory_id", "")
        is_gate = check.get("is_gate", False)

        if is_gate or subcategory_id in GATE_SUBCATEGORIES:
            gate_checks.append(check)
        else:
            non_gate_checks.append(check)

    return gate_checks, non_gate_checks


def calculate_content_quality_score(basic_checks: List[Dict],
                                    advanced_checks: List[Dict]) -> Dict:
    """
    计算content_quality维度的分数（基准60分公式）

    评分逻辑：
    内容分 = clamp(0, 100, 60 - gate惩罚 - basic扣分 + advanced加分)
    - Gate fail: 每项 -20分（3项 gate，最多扣60分）
    - Basic fail: 每项 -(60/basic_total)分（basic全fail → 扣60分 → 到0分）
    - Advanced pass: 每项 +(40/adv_total)分（adv全过 → +40分 → 到100分）

    Args:
        basic_checks: basic层检查项（含Gate层）
        advanced_checks: advanced层检查项

    Returns:
        {
            "overall_score": 总分,
            "quality_level": "gate_failed/unqualified/qualified/excellent",
            "gate_layer": {...},
            "basic_layer": {...},
            "advanced_layer": {...},
            "gate_triggered": bool,
            "score_breakdown": {  # 新增：评分拆解
                "base": 60,
                "gate_penalty": -N,
                "basic_deduction": -N,
                "advanced_bonus": +N,
            }
        }
    """
    # 分离Gate层
    gate_checks, non_gate_basic_checks = separate_gate_checks(basic_checks)

    gate_score_info = calculate_dimension_score(gate_checks)
    basic_score_info = calculate_dimension_score(non_gate_basic_checks)
    advanced_score_info = calculate_dimension_score(advanced_checks)

    # 计算各层扣分/加分
    gate_penalty = gate_score_info["failed"] * GATE_PENALTY_PER_ITEM
    gate_triggered = gate_score_info["failed"] > 0

    basic_total = basic_score_info["total"]
    basic_deduction_per_item = BASIC_POOL / basic_total if basic_total > 0 else 0
    basic_deduction = basic_score_info["failed"] * basic_deduction_per_item

    adv_total = advanced_score_info["total"]
    adv_bonus_per_item = ADVANCED_POOL / adv_total if adv_total > 0 else 0
    advanced_bonus = advanced_score_info["passed"] * adv_bonus_per_item

    # 总分 = 基准 - gate惩罚 - basic扣分 + advanced加分
    overall_score = BASE_SCORE - gate_penalty - basic_deduction + advanced_bonus
    overall_score = max(0.0, min(100.0, overall_score))

    # 确定质量等级
    if gate_triggered:
        quality_level = "gate_failed"
    elif basic_score_info["failed"] > 0:
        quality_level = "unqualified"
    elif advanced_score_info["total"] == 0 or advanced_score_info["pass_rate"] < 0.7:
        quality_level = "qualified"
    else:
        quality_level = "excellent"

    return {
        "overall_score": round(overall_score, 2),
        "quality_level": quality_level,
        "gate_layer": gate_score_info,
        "basic_layer": basic_score_info,
        "advanced_layer": advanced_score_info,
        "gate_triggered": gate_triggered,
        "score_breakdown": {
            "base": BASE_SCORE,
            "gate_penalty": round(-gate_penalty, 2),
            "basic_deduction": round(-basic_deduction, 2),
            "advanced_bonus": round(advanced_bonus, 2),
        }
    }


def determine_status(total_score: float) -> str:
    """
    根据总分判定status

    Args:
        total_score: 总分(0-100)

    Returns:
        Excellent / Good / Fair / Poor
    """
    if total_score >= 90:
        return "Excellent"
    elif total_score >= 70:
        return "Good"
    elif total_score >= 50:
        return "Fair"
    else:
        return "Poor"


# =========================================
# 3. 主计算逻辑
# =========================================

def calculate_dimension_scores(check_details: Dict, capability_taxonomy: Dict = None) -> Dict:
    """
    按能力维度聚合统计（v2.0：内容70%+流程30%+Gate一票否决）

    Args:
        check_details: 检查详情结果（来自checker_execute）
        capability_taxonomy: 能力体系配置（可选）

    Returns:
        {
            "dimension_scores": {...},
            "overall_result": {...}
        }
    """
    # 按dimension_id分组
    dimension_checks = {dim: [] for dim in CAPABILITY_DIMENSIONS}

    # content_quality需要进一步按quality_tier分层
    content_quality_basic = []
    content_quality_advanced = []

    for check_id, result in check_details.items():
        dimension_id = result.get("dimension_id", "")

        # 准备check数据（带ID）
        check_data = result.copy()
        check_data["check_id"] = check_id

        # 分配到对应维度
        if dimension_id in dimension_checks:
            dimension_checks[dimension_id].append(check_data)

            # 如果是content_quality，进一步分层
            if dimension_id == "content_quality":
                quality_tier = result.get("quality_tier", "")
                if quality_tier == "basic":
                    content_quality_basic.append(check_data)
                elif quality_tier == "advanced":
                    content_quality_advanced.append(check_data)

    # 计算各维度分数
    dimension_scores = {}

    for dim_id in CAPABILITY_DIMENSIONS:
        if dim_id == "content_quality":
            # 使用三层评分体系（Gate + Basic + Advanced）
            dimension_scores[dim_id] = calculate_content_quality_score(
                content_quality_basic,
                content_quality_advanced
            )
        else:
            # 普通维度
            dimension_scores[dim_id] = calculate_dimension_score(
                dimension_checks[dim_id]
            )

    # 计算总分（v2.0：内容70% + 流程30%）
    # 内容分数
    content_score = dimension_scores.get("content_quality", {}).get("overall_score", 0.0)

    # 流程分数（format + business + memory 等权平均）
    process_scores = []
    for dim_id in ["format_compliance", "business_rule_compliance", "memory_management"]:
        dim = dimension_scores.get(dim_id, {})
        if dim.get("total", 0) > 0:
            process_scores.append(dim["pass_rate"] * 100)

    if process_scores:
        process_score = sum(process_scores) / len(process_scores)
    else:
        process_score = 0.0

    # 加权总分
    total_score = content_score * CONTENT_WEIGHT + process_score * PROCESS_WEIGHT

    # 统计总数
    total_checks = sum(
        dimension_scores[dim].get("total", 0)
        if dim != "content_quality"
        else (dimension_scores[dim]["gate_layer"]["total"] +
              dimension_scores[dim]["basic_layer"]["total"] +
              dimension_scores[dim]["advanced_layer"]["total"])
        for dim in CAPABILITY_DIMENSIONS
        if dim in dimension_scores
    )

    passed_checks = sum(
        dimension_scores[dim].get("passed", 0)
        if dim != "content_quality"
        else (dimension_scores[dim]["gate_layer"]["passed"] +
              dimension_scores[dim]["basic_layer"]["passed"] +
              dimension_scores[dim]["advanced_layer"]["passed"])
        for dim in CAPABILITY_DIMENSIONS
        if dim in dimension_scores
    )

    failed_checks = sum(
        dimension_scores[dim].get("failed", 0)
        if dim != "content_quality"
        else (dimension_scores[dim]["gate_layer"]["failed"] +
              dimension_scores[dim]["basic_layer"]["failed"] +
              dimension_scores[dim]["advanced_layer"]["failed"])
        for dim in CAPABILITY_DIMENSIONS
        if dim in dimension_scores
    )

    # 判定status
    status = determine_status(total_score)

    # Gate触发标记
    gate_triggered = dimension_scores.get("content_quality", {}).get("gate_triggered", False)

    # 过滤掉total=0的维度（没有检查项的维度不显示）
    filtered_dimension_scores = {}
    for dim_id, dim_score in dimension_scores.items():
        if dim_id == "content_quality":
            # content_quality检查三层total之和
            total = (dim_score["gate_layer"]["total"] +
                     dim_score["basic_layer"]["total"] +
                     dim_score["advanced_layer"]["total"])
            if total > 0:
                filtered_dimension_scores[dim_id] = dim_score
        else:
            # 普通维度检查total
            if dim_score.get("total", 0) > 0:
                filtered_dimension_scores[dim_id] = dim_score

    return {
        "dimension_scores": filtered_dimension_scores,
        "overall_result": {
            "status": status,
            "total_score": round(total_score, 2),
            "content_score": round(content_score, 2),
            "process_score": round(process_score, 2),
            "content_weight": CONTENT_WEIGHT,
            "process_weight": PROCESS_WEIGHT,
            "gate_triggered": gate_triggered,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "pass_rate": round(passed_checks / total_checks, 3) if total_checks > 0 else 0.0
        }
    }


def calculate_scores(execution_result: Dict, capability_taxonomy: Dict = None) -> Dict:
    """
    计算分层分数

    Args:
        execution_result: checker_execute的输出
        capability_taxonomy: 能力体系配置（可选）

    Returns:
        完整的check_result
    """
    sample_id = execution_result.get("sample_id", "unknown")
    check_timestamp = execution_result.get("check_timestamp")
    check_details = execution_result.get("check_details", {})

    # 计算维度分数
    dimension_scores_result = calculate_dimension_scores(
        check_details,
        capability_taxonomy
    )

    # 构建完整结果
    result = {
        "check_version": "novel_writing_v1.0",
        "sample_id": sample_id,
        "check_timestamp": check_timestamp,
        "dimension_scores": dimension_scores_result["dimension_scores"],
        "overall_result": dimension_scores_result["overall_result"],
        "check_details": check_details,
        "completion_status": "completed"
    }

    return result


def calculate_output_completeness(check_details: Dict) -> Dict:
    """
    计算交付物完整性（篇幅层面的完成度）

    包括：
    - 字数检查（semantic_check with word_count_range）
    - 文件存在性检查（entity_attribute_equals with exists）
    - 文件数量检查（create_operation_verified）

    Args:
        check_details: 检查详情结果

    Returns:
        {
            "score": 0.0-100.0,
            "pass_rate": 0.0-1.0,
            "total": int,
            "passed": int,
            "failed": int,
            "critical_items": [...],  # is_critical=True的检查项
            "all_items": [...]  # 所有相关检查项
        }
    """
    relevant_checks = []

    for check_id, result in check_details.items():
        check_type = result.get("check_type", "")
        params = result.get("params", {}) if isinstance(result.get("params"), dict) else {}
        attribute_key = params.get("attribute_key", "")
        subcategory_id = result.get("subcategory_id", "")

        # 判断是否属于交付物完整性检查
        is_relevant = False

        # 1. 字数检查（semantic_check + word_count_range）
        if check_type == "semantic_check":
            validation_rules = params.get("validation_rules", [])
            if validation_rules and isinstance(validation_rules, list):
                for rule in validation_rules:
                    if isinstance(rule, dict) and rule.get("validation_method") == "word_count_range":
                        is_relevant = True
                        break

        # 2. 文件存在性检查（entity_attribute_equals + exists）
        if check_type == "entity_attribute_equals" and (attribute_key == "exists" or attribute_key == "_exists"):
            is_relevant = True

        # 3. 文件数量检查（create_operation_verified）
        if check_type == "create_operation_verified":
            is_relevant = True

        # 4. 通过subcategory_id识别（output_completeness, range_constraint等）
        if subcategory_id in ["output_completeness", "range_constraint"]:
            is_relevant = True

        if is_relevant:
            check_data = result.copy()
            check_data["check_id"] = check_id
            relevant_checks.append(check_data)

    # 统计
    total = len(relevant_checks)
    passed = sum(1 for check in relevant_checks if check["check_result"] == "pass")
    failed = sum(1 for check in relevant_checks if check["check_result"] == "fail")
    skipped = sum(1 for check in relevant_checks if check["check_result"] == "skip")

    # 计算分数（跳过的不计入）
    effective_total = total - skipped
    if effective_total > 0:
        score = (passed / effective_total) * 100.0
        pass_rate = passed / effective_total
    else:
        score = 0.0
        pass_rate = 0.0

    # 提取关键检查项（is_critical=True）
    critical_items = [
        {
            "check_id": check["check_id"],
            "description": check.get("description", ""),
            "result": check["check_result"],
            "reason": check.get("reason", ""),
            "details": check.get("details", "")
        }
        for check in relevant_checks
        if check.get("is_critical", False)
    ]

    # 所有检查项摘要
    all_items = [
        {
            "check_id": check["check_id"],
            "description": check.get("description", ""),
            "result": check["check_result"]
        }
        for check in relevant_checks
    ]

    return {
        "score": round(score, 2),
        "pass_rate": round(pass_rate, 3),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "critical_items": critical_items,
        "all_items": all_items
    }



# =========================================
# 4. CLI入口
# =========================================

def main():
    parser = argparse.ArgumentParser(
        description="小说创作炼金术场景 - Checker评分模块（计算维度分数和质量等级）"
    )
    parser.add_argument("--execution-result", required=True,
                       help="execution_result文件路径（checker_execute的输出）")
    parser.add_argument("--capability-taxonomy", default=None,
                       help="能力体系配置文件路径（check_capability_taxonomy.yaml，可选）")
    parser.add_argument("--output", required=True,
                       help="输出文件路径（check_result.json）")
    args = parser.parse_args()

    # 加载输入文件
    print(f"[加载] Execution Result: {args.execution_result}")
    with open(args.execution_result, "r", encoding="utf-8") as f:
        execution_result = json.load(f)

    # 加载能力体系配置（可选）
    capability_taxonomy = None
    if args.capability_taxonomy:
        print(f"[加载] Capability Taxonomy: {args.capability_taxonomy}")
        import yaml
        with open(args.capability_taxonomy, "r", encoding="utf-8") as f:
            capability_taxonomy = yaml.safe_load(f)

    # 计算分数
    print(f"\n[计算] 开始计算维度分数...")
    result = calculate_scores(execution_result, capability_taxonomy)

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n[完成] 输出文件: {output_path}")

    # 打印结果
    overall = result["overall_result"]
    dimension_scores = result["dimension_scores"]

    print(f"\n[评分] 状态: {overall['status']}")
    print(f"[评分] 总分: {overall['total_score']}/100")
    print(f"[评分] 内容分: {overall.get('content_score', '?')}/100 (权重{CONTENT_WEIGHT*100:.0f}%)")
    print(f"[评分] 流程分: {overall.get('process_score', '?')}/100 (权重{PROCESS_WEIGHT*100:.0f}%)")
    if overall.get("gate_triggered"):
        print(f"[评分] ⚠ Gate层触发惩罚，每项-{GATE_PENALTY_PER_ITEM:.0f}分")
    print(f"[评分] 通过率: {overall['pass_rate']*100:.1f}% ({overall['passed_checks']}/{overall['total_checks']})")

    print(f"\n[维度分数]")
    for dim_id in CAPABILITY_DIMENSIONS:
        if dim_id not in dimension_scores:
            continue
        if dim_id == "content_quality":
            # content_quality特殊显示（三层）
            cq = dimension_scores[dim_id]
            print(f"  - {dim_id}: {cq['overall_score']:.1f}分 [{cq['quality_level']}]")
            print(f"    · gate层: {cq['gate_layer']['pass_rate']*100:.1f}% " +
                  f"({cq['gate_layer']['passed']}/{cq['gate_layer']['total']})" +
                  (f" ⚠ 一票否决" if cq['gate_triggered'] else ""))
            if cq['gate_layer']['failed_items']:
                print(f"      失败项: {', '.join(cq['gate_layer']['failed_items'])}")
            print(f"    · basic层: {cq['basic_layer']['pass_rate']*100:.1f}% " +
                  f"({cq['basic_layer']['passed']}/{cq['basic_layer']['total']})")
            if cq['basic_layer']['failed_items']:
                print(f"      失败项: {', '.join(cq['basic_layer']['failed_items'])}")
            print(f"    · advanced层: {cq['advanced_layer']['pass_rate']*100:.1f}% " +
                  f"({cq['advanced_layer']['passed']}/{cq['advanced_layer']['total']})")
            if cq['advanced_layer']['failed_items']:
                print(f"      失败项: {', '.join(cq['advanced_layer']['failed_items'])}")
        else:
            # 普通维度
            dim = dimension_scores[dim_id]
            print(f"  - {dim_id}: {dim['pass_rate']*100:.1f}分 ({dim['passed']}/{dim['total']})")
            if dim['failed_items']:
                print(f"    · 失败项: {', '.join(dim['failed_items'])}")


if __name__ == "__main__":
    main()
