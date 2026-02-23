#!/usr/bin/env python3
"""
跨模型横评数据表生成器（通用版）
=======================================

直接扫描 evaluation_outputs/ 下所有 check_result*.json，按模型名自动聚合，
输出纯数据 markdown 表格（cross_model_data.md）。

此脚本可直接用于 NWA / NTS / SD 三个场景，差异通过场景配置文件适配。
分析报告（cross_model_report.md / model_comparison_report.md）由人工基于数据表编写。

用法:
    python scripts/analysis/generate_cross_model_report.py
    python scripts/analysis/generate_cross_model_report.py --config scripts/analysis/scenario_config.json
    python scripts/analysis/generate_cross_model_report.py --output analysis/cross_model_data.md
"""

import json
import argparse
import os
import re
import sys
import statistics as stat_module
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


# ============================================================
# 场景配置（默认值，可被 --config 覆盖）
# ============================================================

DEFAULT_CONFIG = {
    # 场景名称
    "scenario_name": "Novel Writing Alchemist",

    # check_result 文件名模式（正则）
    "check_result_pattern": r"check_result_rev\d+\.json",

    # eval 目录前缀过滤
    "eval_dir_prefixes": ["eval_dsv"],

    # 跳过的目录名关键词（废弃目录等）
    "skip_dir_keywords": ["deprecated"],

    # 模型名提取：从目录名 split("_") 后取第 N 个字段开始拼接
    # 例: eval_dsv1_20260214_014809_claude-opus-4-6 → parts[4:] = "claude-opus-4-6"
    "model_name_split_index": 4,

    # 模型名映射：目录后缀 → 显示名
    "model_name_map": {
        "claude-opus-4-5-20251101": "claude-4.5",
        "claude-opus-4-6": "claude-4.6",
        "gemini-3-pro-preview": "gemini-3-pro",
        "kimi-k2.5": "kimi-k2.5",
        "ernie-5.0-thinking-preview": "ernie-5.0",
        "openai_EB5-0209-A35B-midtrain-128k-chat": "EB5-midtrain",
        "qwen3-max-2026-01-23": "qwen3-max",
        "doubao-seed-2-0-pro-260215": "doubao-2.0-pro",
        "glm-5": "glm-5",
    },

    # 模型显示排序（按总分降序，可手动覆盖）
    "model_display_order": [],  # 空=自动按总分排序

    # 维度显示名
    "dimension_names": {
        "format_compliance": "格式规范",
        "business_rule_compliance": "业务规则",
        "memory_management": "记忆管理",
        "data_consistency": "数据一致性",
        "content_quality": "内容质量",
    },

    # 流程维度（用于计算流程分的维度）
    "process_dimensions": ["format_compliance", "business_rule_compliance", "memory_management"],

    # 跳过 execution_status != "success" 且无章节产出的样本
    "skip_error_without_output": True,

    # 章节文件模式（用于判断"有产出"）
    "chapter_file_pattern": "chapter_*.md",

    # 指定 check_result revision（None=自动选最新）
    "check_result_revision": None,

    # 每个检查项的"人话说明"
    "check_item_descriptions": {},

    # subcategory 的"人话说明"
    "subcategory_descriptions": {},
}


def load_config(config_path: Optional[str]) -> Dict:
    """加载场景配置，与默认配置合并"""
    config = dict(DEFAULT_CONFIG)
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        config.update(user_config)
        print(f"已加载场景配置: {config_path}")
    return config


# ============================================================
# 数据扫描与聚合
# ============================================================

def extract_model_name(dirname: str, config: Dict) -> str:
    """从 eval 目录名提取模型显示名"""
    parts = dirname.split("_")
    idx = config["model_name_split_index"]
    if len(parts) > idx:
        raw_name = "_".join(parts[idx:])
    else:
        raw_name = parts[-1]
    return config["model_name_map"].get(raw_name, raw_name)


def find_check_result(env_dir: Path, config: Dict) -> Optional[Path]:
    """在 _env 目录中找到 check_result 文件"""
    pattern = config["check_result_pattern"]
    rev = config.get("check_result_revision")

    # 如果指定了 revision，直接找
    if rev:
        target = env_dir / f"check_result_rev{rev}.json"
        if target.exists():
            return target
        return None

    # 自动找最新的
    candidates = []
    for f in env_dir.iterdir():
        if f.is_file() and re.match(pattern, f.name):
            candidates.append(f)
    # 也检查无 rev 后缀的
    plain = env_dir / "check_result.json"
    if plain.exists():
        candidates.append(plain)

    if not candidates:
        return None

    # 按 rev 号降序排，选最新
    def sort_key(p):
        m = re.search(r"rev(\d+)", p.name)
        return int(m.group(1)) if m else -1
    candidates.sort(key=sort_key, reverse=True)
    return candidates[0]


def should_skip_sample(eval_dir: Path, sample_id: str, env_dir: Path, config: Dict) -> bool:
    """判断是否应跳过该样本（error 且无产出）"""
    if not config.get("skip_error_without_output", False):
        return False

    sample_json = eval_dir / f"{sample_id}.json"
    if not sample_json.exists():
        return False

    try:
        with open(sample_json, "r", encoding="utf-8") as f:
            meta = json.load(f)
        if meta.get("execution_status") != "error":
            return False

        # error 样本：检查是否有章节产出
        workspace = env_dir / "workspace"
        if workspace.is_dir():
            import glob as globmod
            chapter_pattern = config.get("chapter_file_pattern", "chapter_*.md")
            for root, dirs, files in os.walk(workspace):
                for fname in files:
                    if re.match(chapter_pattern.replace("*", ".*"), fname):
                        return False  # 有产出，保留
        return True  # 无产出，跳过
    except Exception:
        return False


def scan_evaluation_outputs(eval_base: Path, config: Dict) -> Dict[str, List[Dict]]:
    """扫描所有 eval 目录，按模型聚合 check_result 数据。

    Returns:
        {model_display_name: [{"sample_id": str, "dir": str, "check_result": dict, "execution_status": str}, ...]}
    """
    model_data = defaultdict(list)
    prefixes = config.get("eval_dir_prefixes", ["eval_"])
    skip_kw = config.get("skip_dir_keywords", [])

    for dirname in sorted(os.listdir(eval_base)):
        full_path = eval_base / dirname
        if not full_path.is_dir():
            continue
        if not any(dirname.startswith(p) for p in prefixes):
            continue
        if any(kw in dirname for kw in skip_kw):
            continue

        model_name = extract_model_name(dirname, config)

        for entry in sorted(os.listdir(full_path)):
            env_path = full_path / entry
            if not env_path.is_dir() or not entry.endswith("_env"):
                continue

            sample_id = entry[:-4]  # remove "_env"

            # 跳过无产出 error 样本
            if should_skip_sample(full_path, sample_id, env_path, config):
                continue

            cr_path = find_check_result(env_path, config)
            if cr_path is None:
                continue

            with open(cr_path, "r", encoding="utf-8") as f:
                cr = json.load(f)

            # 读 execution_status
            exec_status = "unknown"
            sample_json = full_path / f"{sample_id}.json"
            if sample_json.exists():
                try:
                    with open(sample_json, "r", encoding="utf-8") as sf:
                        exec_status = json.load(sf).get("execution_status", "unknown")
                except Exception:
                    pass

            model_data[model_name].append({
                "sample_id": sample_id,
                "dir": dirname,
                "check_result": cr,
                "execution_status": exec_status,
            })

    return dict(model_data)


# ============================================================
# 数据提取辅助函数
# ============================================================

def safe_mean(values):
    return sum(values) / len(values) if values else None


def safe_median(values):
    return stat_module.median(values) if values else None


def safe_stdev(values):
    return stat_module.stdev(values) if len(values) >= 2 else 0.0


def fmt(v, decimals=1):
    """格式化数字，None 显示为 '-'"""
    if v is None:
        return "-"
    return f"{v:.{decimals}f}"


def fmt_pct(v, decimals=1):
    if v is None:
        return "-"
    return f"{v:.{decimals}f}%"


# ============================================================
# 报告生成
# ============================================================

def generate_data_tables(model_data: Dict[str, List[Dict]], config: Dict) -> List[str]:
    """从聚合数据生成全部数据表格"""
    lines = []

    # 模型排序：按总分降序
    model_stats = {}
    for model, samples in model_data.items():
        scores = [s["check_result"]["overall_result"]["total_score"]
                  for s in samples if s["check_result"].get("overall_result", {}).get("total_score") is not None]
        model_stats[model] = {
            "n": len(samples),
            "total_mean": safe_mean(scores),
            "scores": scores,
        }

    order = config.get("model_display_order", [])
    if not order:
        order = sorted(model_stats.keys(),
                       key=lambda m: model_stats[m]["total_mean"] or 0,
                       reverse=True)
    models = [m for m in order if m in model_data]

    # 总样本数
    total_samples = sum(model_stats[m]["n"] for m in models)

    # Header
    lines.append(f"# {config['scenario_name']} 跨模型数据表")
    lines.append("")
    lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 模型数: {len(models)} | 总数据点: {total_samples}")
    lines.append(f"> 评分公式: 总分 = 内容分×0.7 + 流程分×0.3")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 1. 总分排名 ──
    _gen_overview_table(lines, models, model_data, model_stats)

    # ── 2. 总分分布（稳定性） ──
    _gen_stability_table(lines, models, model_data, model_stats)

    # ── 3. 分数段分布 ──
    _gen_score_distribution(lines, models, model_data)

    # ── 4. 内容质量三层通过率 ──
    _gen_content_layer_table(lines, models, model_data)

    # ── 5. 流程维度通过率 ──
    _gen_process_dimension_table(lines, models, model_data, config)

    # ── 6. 逐检查项通过率（按维度/tier分组） ──
    _gen_per_check_item_tables(lines, models, model_data, config)

    return lines


def _gen_overview_table(lines, models, model_data, model_stats):
    """表1: 模型总分排名"""
    lines.append("## 1. 模型总分排名")
    lines.append("")
    lines.append("| 排名 | 模型 | N | 总分 | 内容分 | 流程分 | C-P差 | Gate Fail |")
    lines.append("|------|------|---|------|--------|--------|-------|-----------|")

    for rank, model in enumerate(models, 1):
        samples = model_data[model]
        n = len(samples)
        totals = [s["check_result"]["overall_result"]["total_score"] for s in samples
                  if s["check_result"]["overall_result"].get("total_score") is not None]
        contents = [s["check_result"]["overall_result"]["content_score"] for s in samples
                    if s["check_result"]["overall_result"].get("content_score") is not None]
        processes = [s["check_result"]["overall_result"]["process_score"] for s in samples
                     if s["check_result"]["overall_result"].get("process_score") is not None]
        gate_fails = sum(1 for s in samples if s["check_result"]["overall_result"].get("gate_triggered"))

        t_mean = safe_mean(totals)
        c_mean = safe_mean(contents)
        p_mean = safe_mean(processes)
        cp_gap = (c_mean - p_mean) if c_mean is not None and p_mean is not None else None

        gf_str = str(gate_fails)
        if gate_fails > 0 and n > 0:
            gf_str += f" ({gate_fails/n*100:.0f}%)"

        lines.append(f"| {rank} | {model} | {n} | **{fmt(t_mean)}** | {fmt(c_mean)} | {fmt(p_mean)} | {'+' if cp_gap and cp_gap > 0 else ''}{fmt(cp_gap)} | {gf_str} |")

    lines.append("")


def _gen_stability_table(lines, models, model_data, model_stats):
    """表2: 总分分布稳定性"""
    lines.append("## 2. 总分分布（稳定性）")
    lines.append("")
    lines.append("| 模型 | 均值 | 中位数 | 标准差 | 最低 | 最高 |")
    lines.append("|------|------|--------|--------|------|------|")

    for model in models:
        scores = model_stats[model]["scores"]
        if not scores:
            lines.append(f"| {model} | - | - | - | - | - |")
            continue
        lines.append(f"| {model} | {fmt(safe_mean(scores))} | {fmt(safe_median(scores))} | {fmt(safe_stdev(scores))} | {fmt(min(scores))} | {fmt(max(scores))} |")

    lines.append("")


def _gen_score_distribution(lines, models, model_data):
    """表3: 分数段分布"""
    lines.append("## 3. 分数段分布")
    lines.append("")
    lines.append("| 模型 | <30 | 30-50 | 50-70 | 70-85 | ≥85 | 优秀率(≥85) |")
    lines.append("|------|-----|-------|-------|-------|-----|------------|")

    for model in models:
        samples = model_data[model]
        scores = [s["check_result"]["overall_result"]["total_score"] for s in samples
                  if s["check_result"]["overall_result"].get("total_score") is not None]
        bins = {"lt30": 0, "30_50": 0, "50_70": 0, "70_85": 0, "gte85": 0}
        for sc in scores:
            if sc < 30:
                bins["lt30"] += 1
            elif sc < 50:
                bins["30_50"] += 1
            elif sc < 70:
                bins["50_70"] += 1
            elif sc < 85:
                bins["70_85"] += 1
            else:
                bins["gte85"] += 1
        n = len(scores)
        exc_rate = f"{bins['gte85']/n*100:.0f}%" if n > 0 else "-"
        lines.append(f"| {model} | {bins['lt30']} | {bins['30_50']} | {bins['50_70']} | {bins['70_85']} | {bins['gte85']} | {exc_rate} |")

    lines.append("")


def _gen_content_layer_table(lines, models, model_data):
    """表4: 内容质量 Gate/Basic/Advanced 通过率"""
    lines.append("## 4. 内容质量三层通过率")
    lines.append("")
    lines.append("| 模型 | Gate层 | Basic层 | Advanced层 | 内容均分 |")
    lines.append("|------|--------|---------|------------|----------|")

    for model in models:
        samples = model_data[model]
        gate_rates, basic_rates, adv_rates, content_scores = [], [], [], []

        for s in samples:
            cr = s["check_result"]
            cq = cr.get("dimension_scores", {}).get("content_quality", {})
            if not cq:
                continue

            gl = cq.get("gate_layer", {})
            bl = cq.get("basic_layer", {})
            al = cq.get("advanced_layer", {})

            if gl.get("total", 0) > 0:
                gate_rates.append(gl.get("pass_rate", 0))
            if bl.get("total", 0) > 0:
                basic_rates.append(bl.get("pass_rate", 0))
            if al.get("total", 0) > 0:
                adv_rates.append(al.get("pass_rate", 0))

            cs = cr["overall_result"].get("content_score")
            if cs is not None:
                content_scores.append(cs)

        g = safe_mean(gate_rates)
        b = safe_mean(basic_rates)
        a = safe_mean(adv_rates)
        c = safe_mean(content_scores)

        lines.append(f"| {model} | {fmt_pct(g*100 if g is not None else None)} | {fmt_pct(b*100 if b is not None else None)} | {fmt_pct(a*100 if a is not None else None)} | {fmt(c)} |")

    lines.append("")


def _gen_process_dimension_table(lines, models, model_data, config):
    """表5: 流程维度通过率"""
    proc_dims = config.get("process_dimensions", [])
    dim_names = config.get("dimension_names", {})

    lines.append("## 5. 流程维度通过率")
    lines.append("")

    header = "| 模型 |"
    for dim in proc_dims:
        header += f" {dim_names.get(dim, dim)} |"
    header += " 流程均分 |"
    lines.append(header)
    lines.append("|------|" + "------|" * len(proc_dims) + "------|")

    for model in models:
        samples = model_data[model]
        dim_rates = {dim: [] for dim in proc_dims}
        process_scores = []

        for s in samples:
            cr = s["check_result"]
            ds = cr.get("dimension_scores", {})
            for dim in proc_dims:
                d = ds.get(dim, {})
                total = d.get("total", 0)
                passed = d.get("passed", 0)
                if total > 0:
                    dim_rates[dim].append(passed / total)

            ps = cr["overall_result"].get("process_score")
            if ps is not None:
                process_scores.append(ps)

        row = f"| {model} |"
        for dim in proc_dims:
            r = safe_mean(dim_rates[dim])
            row += f" {fmt_pct(r*100 if r is not None else None)} |"
        row += f" {fmt(safe_mean(process_scores))} |"
        lines.append(row)

    lines.append("")


def _gen_per_check_item_tables(lines, models, model_data, config):
    """表6+: 按 subcategory_id 聚合通过率，按维度分组，内容质量按 tier 分组。

    同一 subcategory 下不同名称的检查项（如 "检查项14" 和 "章节命名格式"）
    会合并为一行，避免因 checklist 版本差异导致行分裂。
    """
    lines.append("## 6. 按子类聚合通过率")
    lines.append("")

    # 按 (subcategory_id, model) 聚合 pass/fail/skip
    # subcat_stats[subcat_id][model] = {pass: N, fail: N, skip: N}
    subcat_stats = defaultdict(lambda: defaultdict(lambda: {"pass": 0, "fail": 0, "skip": 0}))
    # subcat 元信息（dimension_id, quality_tier, description）
    subcat_meta = {}

    for model in models:
        for s in model_data[model]:
            details = s["check_result"].get("check_details", {})
            for check_name, check_info in details.items():
                sub_id = check_info.get("subcategory_id", "")
                if not sub_id:
                    continue

                # 记录元信息（取第一次遇到的）
                if sub_id not in subcat_meta:
                    subcat_meta[sub_id] = {
                        "dimension_id": check_info.get("dimension_id", ""),
                        "quality_tier": check_info.get("quality_tier", ""),
                        "description": check_info.get("description", ""),
                    }
                # 有些检查项在不同版本间 quality_tier 可能不同，优先保留非空值
                if not subcat_meta[sub_id]["quality_tier"] and check_info.get("quality_tier"):
                    subcat_meta[sub_id]["quality_tier"] = check_info["quality_tier"]

                result = check_info.get("check_result", "")
                if result in ("pass", "fail", "skip"):
                    subcat_stats[sub_id][model][result] += 1

    # 按维度分组
    dim_groups = defaultdict(list)  # dim_id -> [(sub_id, meta, {model: stats})]
    for sub_id, meta in subcat_meta.items():
        dim_id = meta.get("dimension_id", "unknown")
        model_stats = {m: dict(subcat_stats[sub_id][m]) for m in models}
        dim_groups[dim_id].append((sub_id, meta, model_stats))

    dim_names = config.get("dimension_names", {})

    # 维度输出顺序
    dim_order = list(config.get("process_dimensions", [])) + ["content_quality"]
    for dim_id in dim_groups:
        if dim_id not in dim_order:
            dim_order.append(dim_id)

    for dim_id in dim_order:
        if dim_id not in dim_groups:
            continue

        dim_label = dim_names.get(dim_id, dim_id)
        items = dim_groups[dim_id]

        if dim_id == "content_quality":
            _gen_content_quality_items(lines, items, models, dim_label, config)
        else:
            lines.append(f"### {dim_label}")
            lines.append("")
            _append_subcat_table(lines, items, models, config)
            lines.append("")


def _gen_content_quality_items(lines, items, models, dim_label, config):
    """内容质量按 gate/basic/advanced/unknown 分组"""
    tier_groups = {"gate": [], "basic": [], "advanced": [], "": []}

    for sub_id, meta, model_stats in items:
        tier = meta.get("quality_tier") or ""
        if tier not in tier_groups:
            tier_groups.setdefault("", []).append((sub_id, meta, model_stats))
        else:
            tier_groups[tier].append((sub_id, meta, model_stats))

    lines.append(f"### {dim_label}")
    lines.append("")

    for tier, label in [("gate", "Gate层"), ("basic", "Basic层"), ("advanced", "Advanced层"), ("", "其他")]:
        tier_items = tier_groups.get(tier, [])
        if not tier_items:
            continue
        lines.append(f"#### {label}")
        lines.append("")
        _append_subcat_table(lines, tier_items, models, config)
        lines.append("")


def _append_subcat_table(lines, items, models, config):
    """输出按 subcategory 聚合的通过率表格"""
    subcat_descs = config.get("subcategory_descriptions", {})

    # 按 subcategory_id 字母序排序
    items.sort(key=lambda x: x[0])

    header = "| 子类 | 人话说明 |"
    for m in models:
        header += f" {m} |"
    lines.append(header)
    sep = "|------|----------|"
    for _ in models:
        sep += "------|"
    lines.append(sep)

    for sub_id, meta, model_stats in items:
        desc = subcat_descs.get(sub_id, "") or meta.get("description", "")
        if len(desc) > 40:
            desc = desc[:38] + ".."

        row = f"| {sub_id} | {desc} |"
        for model in models:
            s = model_stats.get(model, {"pass": 0, "fail": 0, "skip": 0})
            p, f, sk = s["pass"], s["fail"], s["skip"]
            effective = p + f
            if effective > 0:
                rate = round(p / effective * 100)
                cell = f"{rate}% ({p}/{effective})"
                row += f" {cell} |"
            elif sk > 0:
                row += f" skip({sk}) |"
            else:
                row += " - |"
        lines.append(row)


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="生成跨模型横评数据表（通用版）")
    parser.add_argument("--config", default="scripts/analysis/scenario_config.json",
                        help="场景配置文件 (默认: scripts/analysis/scenario_config.json)")
    parser.add_argument("--eval-base", default="evaluation_outputs",
                        help="评测结果根目录 (默认: evaluation_outputs)")
    parser.add_argument("--output", default="analysis/cross_model_data.md",
                        help="输出文件 (默认: analysis/cross_model_data.md)")
    args = parser.parse_args()

    config = load_config(args.config)
    eval_base = Path(args.eval_base)
    output_file = Path(args.output)

    if not eval_base.exists():
        print(f"错误: 评测目录不存在: {eval_base}")
        sys.exit(1)

    print(f"场景: {config['scenario_name']}")
    print(f"扫描: {eval_base}/")
    print()

    model_data = scan_evaluation_outputs(eval_base, config)

    if not model_data:
        print("错误: 未找到任何有效的 check_result 数据")
        sys.exit(1)

    # 打印扫描结果
    print(f"找到 {len(model_data)} 个模型:")
    for model, samples in sorted(model_data.items(), key=lambda x: -len(x[1])):
        print(f"  {model}: {len(samples)} 个样本")

    print()
    lines = generate_data_tables(model_data, config)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"数据表已生成: {output_file}")


if __name__ == "__main__":
    main()
