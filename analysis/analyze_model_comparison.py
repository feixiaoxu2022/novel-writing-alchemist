#!/usr/bin/env python3
"""
模型横评分析脚本
将 DSV1 + DSV2 的所有样本视为独立 case（29 个 case × 8 模型），
输出结构化 JSON 供报告引用。
"""
import json
import os
import sys
import argparse
import statistics
from collections import defaultdict

parser = argparse.ArgumentParser(description="模型横评分析")
parser.add_argument("--revision", default="008", help="数据 revision（默认 008）")
args = parser.parse_args()

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ANALYSIS_DIR, f"rev{args.revision}_all_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    all_data = json.load(f)

# ==================== Config ====================

MODELS_ORDERED = [
    "claude-4.6", "gemini-3-pro", "claude-4.5",
    "doubao-2.0-pro", "qwen3-max", "kimi-k2.5", "ernie-5.0",
    "EB5-midtrain"
]

TIER_MAP = {
    "claude-4.6": "强", "gemini-3-pro": "强", "claude-4.5": "强",
    "doubao-2.0-pro": "中", "qwen3-max": "中", "kimi-k2.5": "中", "ernie-5.0": "中",
    "EB5-midtrain": "弱"
}

TIERS = {
    "强": ["claude-4.6", "gemini-3-pro", "claude-4.5"],
    "中": ["doubao-2.0-pro", "qwen3-max", "kimi-k2.5", "ernie-5.0"],
    "弱": ["EB5-midtrain"]
}

# Display-only subcategories (不计分)
DISPLAY_ONLY = {"character_naming_quality"}

# Content subcategories by layer
GATE_SUBCATS = [
    "chapter_output_existence", "chapter_cloning",
    "alternating_repetition", "chapter_completion"
]

BASIC_CONTENT_SUBCATS = [
    "character_design_adherence", "dialogue_character_distinction",
    "narrative_density", "genre_fit", "outline_execution_fidelity",
    "plot_progression", "full_narrative_content", "late_stage_digression",
    "paragraph_repetition", "naming_convention", "repeated_endings",
    "narrative_tone_match", "structural_logic_defect", "fixable_logic_inconsistency",
]

ADVANCED_CONTENT_SUBCATS = [
    "pacing_rationality_advanced", "hook_design", "imagery_system",
    "structural_design", "emotional_gradient", "emotional_delivery_match",
    "semantic_redundancy",
]

PROCESS_SUBCATS = [
    "required_skill_reading", "sop_compliance",
    "log_file_creation", "log_file_usage",
    "range_constraint", "quantity_constraint", "enum_validity",
    "output_completeness", "structural_integrity",
    "theme_consistency", "main_character_consistency",
    "character_trait_consistency", "language_purity",
]


def get_length(data_id):
    if "ULTRA_SHORT" in data_id:
        return "ULTRA_SHORT"
    elif "SHORT" in data_id:
        return "SHORT"
    elif "MEDIUM" in data_id:
        return "MEDIUM"
    return "UNKNOWN"


def safe_avg(lst):
    return sum(lst) / len(lst) if lst else None


def calc_subcat_fail_rate(items, subcat):
    """计算某个 subcategory 在一组样本上的 fail rate"""
    total = 0
    fail = 0
    for item in items:
        sr = item.get("subcategory_results", {})
        if subcat in sr:
            f = sr[subcat].get("fail", 0)
            p = sr[subcat].get("pass", 0)
            total += f + p  # skip 不算
            fail += f
    if total == 0:
        return None
    return fail / total * 100


# ==================== Group data ====================
by_model = defaultdict(list)
for item in all_data:
    by_model[item["model"]].append(item)

result = {}

# ==================== 1. Model Overview ====================
model_overview = {}
for m in MODELS_ORDERED:
    items = by_model[m]
    n = len(items)
    scores = [i["total_score"] for i in items]
    content_scores = [i["content_score"] for i in items]
    process_scores = [i["process_score"] for i in items]
    gate_fail = sum(1 for i in items if i.get("gate_triggered", False))

    non_gate_items = [i for i in items if not i.get("gate_triggered", False)]
    ng_n = len(non_gate_items)

    model_overview[m] = {
        "tier": TIER_MAP[m],
        "n": n,
        "total_mean": safe_avg(scores),
        "total_median": statistics.median(scores) if scores else None,
        "total_std": statistics.stdev(scores) if len(scores) > 1 else 0,
        "total_min": min(scores) if scores else None,
        "total_max": max(scores) if scores else None,
        "content_mean": safe_avg(content_scores),
        "process_mean": safe_avg(process_scores),
        "content_process_gap": safe_avg(content_scores) - safe_avg(process_scores) if content_scores and process_scores else None,
        "gate_fail_count": gate_fail,
        "gate_fail_rate": gate_fail / n * 100 if n > 0 else 0,
        # non-gate averages
        "non_gate_n": ng_n,
        "non_gate_total": safe_avg([i["total_score"] for i in non_gate_items]) if non_gate_items else None,
        "non_gate_content": safe_avg([i["content_score"] for i in non_gate_items]) if non_gate_items else None,
        "non_gate_process": safe_avg([i["process_score"] for i in non_gate_items]) if non_gate_items else None,
        # Content layers
        "content_gate_pass": safe_avg([i.get("content_gate_layer_pass_rate", 0) or 0 for i in items]) * 100,
        "content_basic_pass": safe_avg([i.get("content_basic_layer_pass_rate", 0) or 0 for i in items]) * 100,
        "content_advanced_pass": safe_avg([i.get("content_advanced_layer_pass_rate", 0) or 0 for i in items]) * 100,
        # Process dimensions
        "format_pass": safe_avg([i.get("format_compliance_pass_rate") or 0 for i in items]) * 100,
        "bizrule_pass": safe_avg([i.get("business_rule_compliance_pass_rate") or 0 for i in items]) * 100,
        "memory_pass": safe_avg([i.get("memory_management_pass_rate") or 0 for i in items]) * 100,
        # Score distribution
        "score_dist": {
            "lt30": sum(1 for s in scores if s < 30),
            "30_50": sum(1 for s in scores if 30 <= s < 50),
            "50_70": sum(1 for s in scores if 50 <= s < 70),
            "70_85": sum(1 for s in scores if 70 <= s < 85),
            "gte85": sum(1 for s in scores if s >= 85),
        },
        # High process low content count
        "high_process_low_content": sum(1 for i in items if i["process_score"] > 70 and i["content_score"] < 50),
    }

result["model_overview"] = model_overview

# ==================== 2. Tier Averages ====================
tier_summary = {}
for tier_name, tier_models in TIERS.items():
    items = []
    for m in tier_models:
        items.extend(by_model[m])
    n = len(items)
    gate_fail = sum(1 for i in items if i.get("gate_triggered", False))
    tier_summary[tier_name] = {
        "models": tier_models,
        "n": n,
        "total_mean": safe_avg([i["total_score"] for i in items]),
        "content_mean": safe_avg([i["content_score"] for i in items]),
        "process_mean": safe_avg([i["process_score"] for i in items]),
        "gate_fail_count": gate_fail,
        "gate_fail_rate": gate_fail / n * 100 if n > 0 else 0,
        "content_gate_pass": safe_avg([i.get("content_gate_layer_pass_rate", 0) or 0 for i in items]) * 100,
        "content_basic_pass": safe_avg([i.get("content_basic_layer_pass_rate", 0) or 0 for i in items]) * 100,
        "content_advanced_pass": safe_avg([i.get("content_advanced_layer_pass_rate", 0) or 0 for i in items]) * 100,
    }

result["tier_summary"] = tier_summary

# ==================== 3. Length Breakdown ====================
length_breakdown = {}
for m in MODELS_ORDERED:
    items = by_model[m]
    by_len = defaultdict(list)
    for item in items:
        by_len[get_length(item["data_id"])].append(item)

    length_breakdown[m] = {}
    for length in ["MEDIUM", "SHORT", "ULTRA_SHORT"]:
        li = by_len[length]
        if li:
            length_breakdown[m][length] = {
                "n": len(li),
                "total_mean": safe_avg([i["total_score"] for i in li]),
                "content_mean": safe_avg([i["content_score"] for i in li]),
                "process_mean": safe_avg([i["process_score"] for i in li]),
                "gate_fail": sum(1 for i in li if i.get("gate_triggered", False)),
            }
        else:
            length_breakdown[m][length] = {"n": 0}

result["length_breakdown"] = length_breakdown

# ==================== 4. Subcategory Fail Rates ====================
all_subcats = set()
for item in all_data:
    all_subcats.update(item.get("subcategory_results", {}).keys())

subcat_fail_rates = {}
for sc in sorted(all_subcats):
    if sc in DISPLAY_ONLY:
        continue
    subcat_fail_rates[sc] = {}
    for m in MODELS_ORDERED:
        rate = calc_subcat_fail_rate(by_model[m], sc)
        subcat_fail_rates[sc][m] = rate

result["subcat_fail_rates"] = subcat_fail_rates

# Also compute character_naming_quality separately (display only)
character_naming = {}
for m in MODELS_ORDERED:
    rate = calc_subcat_fail_rate(by_model[m], "character_naming_quality")
    character_naming[m] = rate
result["character_naming_quality"] = character_naming

# ==================== 5. Key Differentiators ====================
# Find subcats with largest spread between best and worst model
subcat_spread = {}
for sc, rates in subcat_fail_rates.items():
    vals = [v for v in rates.values() if v is not None]
    if len(vals) >= 4:
        subcat_spread[sc] = {
            "min": min(vals),
            "max": max(vals),
            "spread": max(vals) - min(vals),
            "mean": safe_avg(vals),
        }
# Sort by spread
key_differentiators = sorted(subcat_spread.items(), key=lambda x: -x[1]["spread"])[:20]
result["key_differentiators"] = {k: v for k, v in key_differentiators}

# ==================== 6. Per-model Strength/Weakness Profile ====================
profiles = {}
for m in MODELS_ORDERED:
    strengths = []
    weaknesses = []
    for sc, rates in subcat_fail_rates.items():
        rate = rates.get(m)
        if rate is None:
            continue
        # Compare with overall average
        all_rates = [v for v in rates.values() if v is not None]
        avg_rate = safe_avg(all_rates)
        if avg_rate is None:
            continue
        diff = rate - avg_rate
        if diff < -15 and rate < 20:  # significantly better than avg and low fail rate
            strengths.append({"subcat": sc, "fail_rate": rate, "avg": avg_rate, "diff": diff})
        elif diff > 15 and rate > 40:  # significantly worse than avg and high fail rate
            weaknesses.append({"subcat": sc, "fail_rate": rate, "avg": avg_rate, "diff": diff})

    strengths.sort(key=lambda x: x["diff"])
    weaknesses.sort(key=lambda x: -x["diff"])
    profiles[m] = {"strengths": strengths[:10], "weaknesses": weaknesses[:10]}

result["profiles"] = profiles

# ==================== Output ====================
output_file = os.path.join(ANALYSIS_DIR, f"model_comparison_output.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"分析完成，输出到 {output_file}")
print(f"数据点: {len(all_data)} 条, 模型: {len(MODELS_ORDERED)}, Case: 29 (14 DSV1 + 15 DSV2)")

# ==================== Print Summary ====================
print("\n" + "=" * 80)
print("模型总分排名（含所有 case）")
print("=" * 80)
print(f"{'排名':<4} {'模型':<18} {'梯队':<4} {'N':>3} {'总分':>7} {'内容':>7} {'流程':>7} {'GateFail':>9}")
print("-" * 80)
for rank, m in enumerate(MODELS_ORDERED, 1):
    o = model_overview[m]
    print(f"{rank:<4} {m:<18} {o['tier']:<4} {o['n']:>3} {o['total_mean']:>7.1f} {o['content_mean']:>7.1f} {o['process_mean']:>7.1f} {o['gate_fail_count']:>9}")
