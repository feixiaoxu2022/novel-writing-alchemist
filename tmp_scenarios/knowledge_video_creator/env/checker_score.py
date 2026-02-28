#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_video_creator — Checker 评分模块 (v1.0)

职责：读取 execution_result，按能力维度聚合统计，计算质量等级
输入：execution_result（checker_execute 的输出）
输出：check_result（含维度分数、质量等级和 overall 统计）

评分公式（基准60分）：
  内容分 = clamp(0, 100, 60 - gate惩罚 - basic扣分 + advanced加分)
  Gate fail: 每项 -20分
  Basic fail: 每项 -(60/basic_total)分
  Advanced pass: 每项 +(40/adv_total)分
  总分 = 内容分×0.7 + 流程规范分×0.3
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
    "data_consistency",            # 数据一致性（跨文件一致性）
    "content_quality"              # 内容创作质量
]

# content_quality 维度的两个计分层
QUALITY_TIERS = ["basic", "advanced"]

# Gate 层的 subcategory_id（一票否决项）
# 与 novel_to_script 区别：多了 multimedia_production 的 gate 项
GATE_SUBCATEGORIES = {
    "script_content_gate",       # 脚本文件存在且有实际内容
    "multimedia_production",     # 视频素材包存在性（本场景独有）
}

# 权重配置
CONTENT_WEIGHT = 0.7   # 内容质量占 70%
PROCESS_WEIGHT = 0.3   # 流程合规占 30%

# 基准60分公式参数
BASE_SCORE = 60.0               # 基准分
GATE_PENALTY_PER_ITEM = 20.0    # Gate 每项 fail 扣 20 分
BASIC_POOL = 60.0               # Basic 层扣分池（basic 全 fail → 扣 60 分 → 到 0 分）
ADVANCED_POOL = 40.0            # Advanced 层加分池（adv 全过 → 加 40 分 → 到 100 分）


# =========================================
# 2. 辅助函数
# =========================================

def calculate_dimension_score(checks: List[Dict]) -> Dict:
    """
    计算单个维度的通过率

    Args:
        checks: 该维度的所有检查项（每项包含 check_id 和 result）

    Returns:
        {
            "pass_rate": 通过率(0-1),
            "total": 有效总数(排除skip),
            "passed": 通过数,
            "failed": 失败数,
            "skipped": 跳过数,
            "failed_items": [失败的 check_id 列表]
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

    # 计算 pass_rate 时排除 skip，只统计 pass 和 fail
    total = passed + failed
    if total == 0:
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
    从 basic 检查项中分离出 Gate 层检查项。

    Gate 层检查项通过 is_gate=True 或 subcategory_id 在 GATE_SUBCATEGORIES 中
    且 quality_tier 为 gate 来识别。

    Args:
        basic_checks: basic + gate 层所有检查项

    Returns:
        (gate_checks, non_gate_basic_checks)
    """
    gate_checks = []
    non_gate_checks = []

    for check in basic_checks:
        subcategory_id = check.get("subcategory_id", "")
        is_gate = check.get("is_gate", False)
        quality_tier = check.get("quality_tier", "")

        if is_gate or quality_tier == "gate" or subcategory_id in GATE_SUBCATEGORIES:
            gate_checks.append(check)
        else:
            non_gate_checks.append(check)

    return gate_checks, non_gate_checks


def calculate_content_quality_score(basic_checks: List[Dict],
                                    advanced_checks: List[Dict]) -> Dict:
    """
    计算 content_quality 维度的分数（基准60分公式）

    评分逻辑：
    内容分 = clamp(0, 100, 60 - gate惩罚 - basic扣分 + advanced加分)

    Args:
        basic_checks: basic + gate 层检查项
        advanced_checks: advanced 层检查项

    Returns:
        {
            "overall_score": 总分,
            "quality_level": "gate_failed/unqualified/qualified/excellent",
            "gate_layer": {...},
            "basic_layer": {...},
            "advanced_layer": {...},
            "gate_triggered": bool,
            "score_breakdown": {...}
        }
    """
    # 分离 Gate 层
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
    """根据总分判定 status"""
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
    按能力维度聚合统计（内容70% + 流程30% + Gate一票否决）

    Args:
        check_details: 检查详情结果（来自 checker_execute）
        capability_taxonomy: 能力体系配置（可选）

    Returns:
        {
            "dimension_scores": {...},
            "overall_result": {...}
        }
    """
    # 按 dimension_id 分组
    dimension_checks = {dim: [] for dim in CAPABILITY_DIMENSIONS}

    # content_quality 需要进一步按 quality_tier 分层
    content_quality_basic = []
    content_quality_advanced = []

    for check_id, result in check_details.items():
        dimension_id = result.get("dimension_id", "")

        # 准备 check 数据（带 ID）
        check_data = result.copy()
        check_data["check_id"] = check_id

        # 分配到对应维度
        if dimension_id in dimension_checks:
            dimension_checks[dimension_id].append(check_data)

            # 如果是 content_quality，进一步分层
            if dimension_id == "content_quality":
                quality_tier = result.get("quality_tier", "")
                if quality_tier in ("basic", "gate"):
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

    # 计算总分（内容 70% + 流程 30%）
    content_score = dimension_scores.get("content_quality", {}).get("overall_score", 0.0)

    # 流程分数（format + business + data_consistency 等权平均）
    process_scores = []
    for dim_id in ["format_compliance", "business_rule_compliance", "data_consistency"]:
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

    # 判定 status
    status = determine_status(total_score)

    # Gate 触发标记
    gate_triggered = dimension_scores.get("content_quality", {}).get("gate_triggered", False)

    # 过滤掉 total=0 的维度
    filtered_dimension_scores = {}
    for dim_id, dim_score in dimension_scores.items():
        if dim_id == "content_quality":
            total = (dim_score["gate_layer"]["total"] +
                     dim_score["basic_layer"]["total"] +
                     dim_score["advanced_layer"]["total"])
            if total > 0:
                filtered_dimension_scores[dim_id] = dim_score
        else:
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
        execution_result: checker_execute 的输出
        capability_taxonomy: 能力体系配置（可选）

    Returns:
        完整的 check_result
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
        "check_version": "knowledge_video_creator_v1.0",
        "sample_id": sample_id,
        "check_timestamp": check_timestamp,
        "dimension_scores": dimension_scores_result["dimension_scores"],
        "overall_result": dimension_scores_result["overall_result"],
        "check_details": check_details,
        "completion_status": "completed"
    }

    return result


# =========================================
# 4. CLI 入口
# =========================================

def main():
    parser = argparse.ArgumentParser(
        description="knowledge_video_creator — Checker 评分模块（计算维度分数和质量等级）"
    )
    parser.add_argument("--execution-result", required=True,
                        help="execution_result 文件路径（checker_execute 的输出）")
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

    # 打印结果摘要
    overall = result["overall_result"]
    dimension_scores = result["dimension_scores"]

    print(f"\n[评分] 状态: {overall['status']}")
    print(f"[评分] 总分: {overall['total_score']}/100")
    print(f"[评分] 内容分: {overall.get('content_score', '?')}/100 (权重{CONTENT_WEIGHT * 100:.0f}%)")
    print(f"[评分] 流程分: {overall.get('process_score', '?')}/100 (权重{PROCESS_WEIGHT * 100:.0f}%)")
    if overall.get("gate_triggered"):
        print(f"[评分] ⚠ Gate层触发惩罚，每项-{GATE_PENALTY_PER_ITEM:.0f}分")
    print(f"[评分] 通过率: {overall['pass_rate'] * 100:.1f}% ({overall['passed_checks']}/{overall['total_checks']})")

    print(f"\n[维度分数]")
    for dim_id in CAPABILITY_DIMENSIONS:
        if dim_id not in dimension_scores:
            continue
        if dim_id == "content_quality":
            cq = dimension_scores[dim_id]
            print(f"  - {dim_id}: {cq['overall_score']:.1f}分 [{cq['quality_level']}]")
            print(f"    · gate层: {cq['gate_layer']['pass_rate'] * 100:.1f}% "
                  f"({cq['gate_layer']['passed']}/{cq['gate_layer']['total']})"
                  f"{' ⚠ 一票否决' if cq['gate_triggered'] else ''}")
            if cq["gate_layer"]["failed_items"]:
                print(f"      失败项: {', '.join(cq['gate_layer']['failed_items'])}")
            print(f"    · basic层: {cq['basic_layer']['pass_rate'] * 100:.1f}% "
                  f"({cq['basic_layer']['passed']}/{cq['basic_layer']['total']})")
            if cq["basic_layer"]["failed_items"]:
                print(f"      失败项: {', '.join(cq['basic_layer']['failed_items'])}")
            print(f"    · advanced层: {cq['advanced_layer']['pass_rate'] * 100:.1f}% "
                  f"({cq['advanced_layer']['passed']}/{cq['advanced_layer']['total']})")
            if cq["advanced_layer"]["failed_items"]:
                print(f"      失败项: {', '.join(cq['advanced_layer']['failed_items'])}")
        else:
            dim = dimension_scores[dim_id]
            print(f"  - {dim_id}: {dim['pass_rate'] * 100:.1f}% ({dim['passed']}/{dim['total']})")
            if dim["failed_items"]:
                print(f"    · 失败项: {', '.join(dim['failed_items'])}")


if __name__ == "__main__":
    main()
