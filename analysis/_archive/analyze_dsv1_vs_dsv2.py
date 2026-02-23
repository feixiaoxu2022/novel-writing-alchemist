#!/usr/bin/env python3
"""
DSV1 vs DSV2 Context Engineering 收益分析
支持指定 revision（默认 rev008）
"""
import json
import os
import sys
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="DSV1 vs DSV2 对比分析")
parser.add_argument("--revision", default="008", help="数据 revision（默认 008）")
args = parser.parse_args()

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ANALYSIS_DIR, f"rev{args.revision}_all_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    all_data = json.load(f)

# ==================== 1. 总分对比表 ====================
print("=" * 100)
print(f"1. 总分对比表（DSV1 vs DSV2，rev{args.revision} 统一度量）")
print("=" * 100)

# 按 (version, model) 聚合
from collections import defaultdict
agg = defaultdict(lambda: {"total": [], "content": [], "process": [], "pass_rate": [], "count": 0})

for r in all_data:
    key = (r["version"], r["model"])
    if r["total_score"] is not None:
        agg[key]["total"].append(r["total_score"])
    if r["content_score"] is not None:
        agg[key]["content"].append(r["content_score"])
    if r["process_score"] is not None:
        agg[key]["process"].append(r["process_score"])
    if r["pass_rate"] is not None:
        agg[key]["pass_rate"].append(r["pass_rate"])
    agg[key]["count"] += 1

def avg(lst):
    return sum(lst) / len(lst) if lst else None

def fmt(val, decimals=2):
    if val is None:
        return "—"
    return f"{val:.{decimals}f}"

# 获取所有模型
models = sorted(set(r["model"] for r in all_data))

# 计算每个模型在配对样本中的 gate fail 率，用于过滤不可靠的配对分析
# 如果一个模型的配对样本中超过 50% 至少一方 gate fail，则该模型的配对 Δ 不具备分析价值
GATE_FAIL_THRESHOLD = 0.5  # gate fail 率阈值

_PAIRED_IDS = [
    # 3 MEDIUM (non-IP)
    "NW_CLEAR_MEDIUM_ANGSTY_001", "NW_CLEAR_MEDIUM_SUSPENSE_001",
    "NW_CLEAR_MEDIUM_SWEET_001",
    # 1 MEDIUM (IP)
    "NW_IP_MEDIUM_NEUTRAL_001",
    # 2 SHORT
    "NW_CLEAR_SHORT_ANGSTY_001", "NW_CLEAR_SHORT_SWEET_001",
    # 5 ULTRA_SHORT
    "NW_ULTRA_SHORT_ANGSTY_001", "NW_ULTRA_SHORT_ANGSTY_002",
    "NW_ULTRA_SHORT_ANGSTY_003", "NW_ULTRA_SHORT_ANGSTY_004",
    "NW_ULTRA_SHORT_ANGSTY_005",
]
_idx_tmp = {}
for r in all_data:
    _idx_tmp[(r["version"], r["model"], r["sample_id"])] = r

gate_fail_models = set()  # 配对 gate fail 率过高的模型
_model_gate_info = {}
for m in models:
    pairs_total = 0
    pairs_gate = 0  # 至少一方 gate fail 的配对数
    for sid in _PAIRED_IDS:
        r1 = _idx_tmp.get(("dsv1", m, sid))
        r2 = _idx_tmp.get(("dsv2", m, sid))
        if r1 and r2:
            pairs_total += 1
            if r1.get("gate_triggered") or r2.get("gate_triggered"):
                pairs_gate += 1
    gate_rate = pairs_gate / pairs_total if pairs_total > 0 else 0
    _model_gate_info[m] = {"pairs": pairs_total, "gate_pairs": pairs_gate, "gate_rate": gate_rate}
    if gate_rate > GATE_FAIL_THRESHOLD:
        gate_fail_models.add(m)

if gate_fail_models:
    print(f"\n⚠️  以下模型配对 gate fail 率 > {GATE_FAIL_THRESHOLD*100:.0f}%，将从配对汇总和均值中排除：")
    for m in sorted(gate_fail_models):
        info = _model_gate_info[m]
        print(f"   {m}: {info['gate_pairs']}/{info['pairs']} 配对至少一方 gate fail ({info['gate_rate']*100:.0f}%)")
    print()

del _idx_tmp

# 排除 gate fail 率过高模型后的有效模型列表（多处使用）
valid_models = [m for m in models if m not in gate_fail_models]

print(f"\n{'模型':<20} {'N(v1)':>5} {'N(v2)':>5} │ {'总分v1':>7} {'总分v2':>7} {'Δ':>7} │ {'内容v1':>7} {'内容v2':>7} {'Δ':>7} │ {'流程v1':>7} {'流程v2':>7} {'Δ':>7}")
print("─" * 120)

model_summary = {}
for m in models:
    v1 = agg.get(("dsv1", m), {"total": [], "content": [], "process": [], "count": 0})
    v2 = agg.get(("dsv2", m), {"total": [], "content": [], "process": [], "count": 0})
    
    t1, t2 = avg(v1["total"]), avg(v2["total"])
    c1, c2 = avg(v1["content"]), avg(v2["content"])
    p1, p2 = avg(v1["process"]), avg(v2["process"])
    
    dt = (t2 - t1) if (t1 is not None and t2 is not None) else None
    dc = (c2 - c1) if (c1 is not None and c2 is not None) else None
    dp = (p2 - p1) if (p1 is not None and p2 is not None) else None
    
    marker = " *" if v1["count"] < 10 or v2["count"] < 5 else ""
    
    print(f"{m:<20} {v1['count']:>5} {v2['count']:>5} │ {fmt(t1):>7} {fmt(t2):>7} {fmt(dt, 1):>7} │ {fmt(c1):>7} {fmt(c2):>7} {fmt(dc, 1):>7} │ {fmt(p1):>7} {fmt(p2):>7} {fmt(dp, 1):>7}{marker}")
    
    model_summary[m] = {
        "dsv1_total": t1, "dsv2_total": t2, "delta_total": dt,
        "dsv1_content": c1, "dsv2_content": c2, "delta_content": dc,
        "dsv1_process": p1, "dsv2_process": p2, "delta_process": dp,
        "dsv1_n": v1["count"], "dsv2_n": v2["count"],
    }

print("\n* = 样本数较少，数据参考性有限")

# ==================== 2. 共有 task 配对对比 ====================
print("\n\n" + "=" * 100)
print("2. 共有 Task 配对对比（11 个共有 data_id）")
print("=" * 100)

# 共有的 sample_id（11 个：4 MEDIUM + 2 SHORT + 5 ULTRA_SHORT）
SHARED_SAMPLE_IDS = [
    # 3 MEDIUM (non-IP)
    "NW_CLEAR_MEDIUM_ANGSTY_001",
    "NW_CLEAR_MEDIUM_SUSPENSE_001", 
    "NW_CLEAR_MEDIUM_SWEET_001",
    # 1 MEDIUM (IP) — IP_MEDIUM_NEUTRAL_001 按长度归为 MEDIUM
    "NW_IP_MEDIUM_NEUTRAL_001",
    # 2 SHORT
    "NW_CLEAR_SHORT_ANGSTY_001",
    "NW_CLEAR_SHORT_SWEET_001",
    # 5 ULTRA_SHORT
    "NW_ULTRA_SHORT_ANGSTY_001",
    "NW_ULTRA_SHORT_ANGSTY_002",
    "NW_ULTRA_SHORT_ANGSTY_003",
    "NW_ULTRA_SHORT_ANGSTY_004",
    "NW_ULTRA_SHORT_ANGSTY_005",
]

# 长度分组定义 — IP_MEDIUM 归入 MEDIUM
LENGTH_GROUPS = {
    "MEDIUM": [
        "NW_CLEAR_MEDIUM_ANGSTY_001", "NW_CLEAR_MEDIUM_SUSPENSE_001",
        "NW_CLEAR_MEDIUM_SWEET_001", "NW_IP_MEDIUM_NEUTRAL_001",
    ],
    "SHORT": [
        "NW_CLEAR_SHORT_ANGSTY_001", "NW_CLEAR_SHORT_SWEET_001",
    ],
    "ULTRA_SHORT": [
        "NW_ULTRA_SHORT_ANGSTY_001", "NW_ULTRA_SHORT_ANGSTY_002",
        "NW_ULTRA_SHORT_ANGSTY_003", "NW_ULTRA_SHORT_ANGSTY_004",
        "NW_ULTRA_SHORT_ANGSTY_005",
    ],
}

# 建立索引: (version, model, sample_id) -> record
idx = {}
for r in all_data:
    idx[(r["version"], r["model"], r["sample_id"])] = r

print(f"\n{'模型':<20} │ {'共有task v1均分':>12} {'共有task v2均分':>12} {'Δ':>7} │ {'v1内容':>8} {'v2内容':>8} {'Δ':>7} │ {'v1流程':>8} {'v2流程':>8} {'Δ':>7} │ {'配对数':>5}")
print("─" * 120)

paired_summary = {}
for m in models:
    v1_totals = []
    v2_totals = []
    v1_contents = []
    v2_contents = []
    v1_processes = []
    v2_processes = []
    pairs = 0
    
    for sid in SHARED_SAMPLE_IDS:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["total_score"] is not None and r2["total_score"] is not None:
            v1_totals.append(r1["total_score"])
            v2_totals.append(r2["total_score"])
            v1_contents.append(r1["content_score"])
            v2_contents.append(r2["content_score"])
            v1_processes.append(r1["process_score"])
            v2_processes.append(r2["process_score"])
            pairs += 1
    
    t1, t2 = avg(v1_totals), avg(v2_totals)
    c1, c2 = avg(v1_contents), avg(v2_contents)
    p1, p2 = avg(v1_processes), avg(v2_processes)
    dt = (t2 - t1) if (t1 is not None and t2 is not None) else None
    dc = (c2 - c1) if (c1 is not None and c2 is not None) else None
    dp = (p2 - p1) if (p1 is not None and p2 is not None) else None
    
    gate_marker = " ⚠️gate" if m in gate_fail_models else ""
    print(f"{m:<20} │ {fmt(t1):>12} {fmt(t2):>12} {fmt(dt, 1):>7} │ {fmt(c1):>8} {fmt(c2):>8} {fmt(dc, 1):>7} │ {fmt(p1):>8} {fmt(p2):>8} {fmt(dp, 1):>7} │ {pairs:>5}{gate_marker}")
    
    paired_summary[m] = {
        "dsv1_total": t1, "dsv2_total": t2, "delta_total": dt,
        "dsv1_content": c1, "dsv2_content": c2, "delta_content": dc,
        "dsv1_process": p1, "dsv2_process": p2, "delta_process": dp,
        "pairs": pairs,
    }

# 2b. 排除 gate_triggered 样本的配对对比（反映"正常完成时"的质量差异）
print(f"\n--- 排 gate_triggered 后的配对对比（仅保留双方均非 gate fail 的配对）---")
print(f"{'模型':<20} │ {'v1内容':>8} {'v2内容':>8} {'Δ':>7} │ {'v1总分':>8} {'v2总分':>8} {'Δ':>7} │ {'n':>3} {'排gate数':>7}")
print("─" * 90)

paired_no_gate = {}
for m in models:
    v1c, v2c, v1t, v2t, v1p, v2p = [], [], [], [], [], []
    gate_excluded = 0
    total_pairs = 0
    for sid in SHARED_SAMPLE_IDS:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["total_score"] is not None and r2["total_score"] is not None:
            total_pairs += 1
            if r1.get("gate_triggered") or r2.get("gate_triggered"):
                gate_excluded += 1
                continue
            v1c.append(r1["content_score"])
            v2c.append(r2["content_score"])
            v1t.append(r1["total_score"])
            v2t.append(r2["total_score"])
            v1p.append(r1["process_score"])
            v2p.append(r2["process_score"])
    
    c1, c2 = avg(v1c), avg(v2c)
    t1, t2 = avg(v1t), avg(v2t)
    p1, p2 = avg(v1p), avg(v2p)
    dc = (c2 - c1) if (c1 is not None and c2 is not None) else None
    dt = (t2 - t1) if (t1 is not None and t2 is not None) else None
    dp = (p2 - p1) if (p1 is not None and p2 is not None) else None
    n = len(v1c)
    
    gate_marker = " ⚠️" if m in gate_fail_models else ""
    print(f"{m:<20} │ {fmt(c1):>8} {fmt(c2):>8} {fmt(dc, 1):>7} │ {fmt(t1):>8} {fmt(t2):>8} {fmt(dt, 1):>7} │ {n:>3} {gate_excluded:>7}{gate_marker}")
    
    paired_no_gate[m] = {
        "dsv1_content": c1, "dsv2_content": c2, "delta_content": dc,
        "dsv1_total": t1, "dsv2_total": t2, "delta_total": dt,
        "dsv1_process": p1, "dsv2_process": p2, "delta_process": dp,
        "n": n, "total_pairs": total_pairs, "gate_excluded": gate_excluded,
    }

# 逐 task 逐模型明细
print(f"\n\n--- 逐 Task 明细（总分）---")
print(f"{'Task':<35} │", end="")
for m in models:
    print(f" {m[:10]:>10}", end="")
print()
print("─" * (37 + 11 * len(models)))

for sid in SHARED_SAMPLE_IDS:
    short_name = sid.replace("NW_CLEAR_", "").replace("NW_IP_", "IP_")
    # DSV1
    print(f"  v1 {short_name:<30} │", end="")
    for m in models:
        r = idx.get(("dsv1", m, sid))
        val = r["total_score"] if r and r["total_score"] is not None else None
        print(f" {fmt(val):>10}", end="")
    print()
    # DSV2
    print(f"  v2 {short_name:<30} │", end="")
    for m in models:
        r = idx.get(("dsv2", m, sid))
        val = r["total_score"] if r and r["total_score"] is not None else None
        print(f" {fmt(val):>10}", end="")
    print()
    # Delta
    print(f"  Δ  {short_name:<30} │", end="")
    for m in models:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["total_score"] is not None and r2["total_score"] is not None:
            d = r2["total_score"] - r1["total_score"]
            print(f" {d:>+10.1f}", end="")
        else:
            print(f" {'—':>10}", end="")
    print()
    print()


# ==================== 3. 维度级别对比 ====================
print("\n" + "=" * 100)
print("3. 维度级别 Pass Rate 对比")
print("=" * 100)

dims = ["format_compliance", "business_rule_compliance", "memory_management"]
content_layers = ["content_gate_layer", "content_basic_layer", "content_advanced_layer"]

for dim in dims + content_layers:
    pr_key = f"{dim}_pass_rate"
    print(f"\n--- {dim} ---")
    print(f"{'模型':<20} │ {'v1 pass_rate':>12} {'v2 pass_rate':>12} {'Δ (pp)':>10}")
    print("─" * 60)
    
    for m in models:
        v1_rates = [r[pr_key] for r in all_data if r["model"] == m and r["version"] == "dsv1" and r.get(pr_key) is not None]
        v2_rates = [r[pr_key] for r in all_data if r["model"] == m and r["version"] == "dsv2" and r.get(pr_key) is not None]
        
        r1, r2 = avg(v1_rates), avg(v2_rates)
        delta = ((r2 - r1) * 100) if (r1 is not None and r2 is not None) else None
        
        r1_pct = f"{r1*100:.1f}%" if r1 is not None else "—"
        r2_pct = f"{r2*100:.1f}%" if r2 is not None else "—"
        d_str = f"{delta:>+.1f}pp" if delta is not None else "—"
        
        print(f"{m:<20} │ {r1_pct:>12} {r2_pct:>12} {d_str:>10}")


# ==================== 4. Subcategory 级别对比 ====================
print("\n\n" + "=" * 100)
print("4. Subcategory 级别 Pass Rate 对比（前30个变化最大的）")
print("=" * 100)

# 收集所有 subcategory
subcat_data = {}

for r in all_data:
    key = (r["version"], r["model"])
    for subcat, counts in r.get("subcategory_results", {}).items():
        compound_key = (key, subcat)
        if compound_key not in subcat_data:
            subcat_data[compound_key] = {"pass": 0, "fail": 0, "skip": 0, "total_eval": 0}
        sd = subcat_data[compound_key]
        sd["pass"] += counts.get("pass", 0)
        sd["fail"] += counts.get("fail", 0)
        sd["skip"] += counts.get("skip", 0)
        sd["total_eval"] = sd["pass"] + sd["fail"]

# 收集所有 subcategory names
all_subcats = sorted(set(sc for (_, sc) in subcat_data.keys()))

# 计算每个模型每个 subcategory 的 v1 vs v2 差异
subcat_deltas = []
for m in models:
    for sc in all_subcats:
        v1 = subcat_data.get((("dsv1", m), sc), {"pass": 0, "fail": 0, "total_eval": 0})
        v2 = subcat_data.get((("dsv2", m), sc), {"pass": 0, "fail": 0, "total_eval": 0})
        
        v1_te = v1["pass"] + v1["fail"]
        v2_te = v2["pass"] + v2["fail"]
        
        if v1_te > 0 and v2_te > 0:
            v1_pr = v1["pass"] / v1_te
            v2_pr = v2["pass"] / v2_te
            delta = (v2_pr - v1_pr) * 100
            subcat_deltas.append({
                "model": m, "subcategory": sc,
                "v1_pass_rate": v1_pr, "v2_pass_rate": v2_pr,
                "delta_pp": delta,
                "v1_n": v1_te, "v2_n": v2_te,
            })

# 按 abs(delta) 排序，取前30
subcat_deltas.sort(key=lambda x: abs(x["delta_pp"]), reverse=True)

print(f"\n{'模型':<20} {'Subcategory':<35} │ {'v1':>8} {'v2':>8} {'Δ(pp)':>8} │ {'v1_n':>4} {'v2_n':>4}")
print("─" * 95)
for item in subcat_deltas[:40]:
    print(f"{item['model']:<20} {item['subcategory']:<35} │ {item['v1_pass_rate']*100:>7.1f}% {item['v2_pass_rate']*100:>7.1f}% {item['delta_pp']:>+7.1f} │ {item['v1_n']:>4} {item['v2_n']:>4}")


# ==================== 4.5 篇幅检查（range_constraint）单独展示 ====================
print("\n\n" + "=" * 100)
print("4.5. 篇幅检查（range_constraint）单独分析")
print("=" * 100)

# 提取每个样本的 range_constraint 通过情况
range_constraint_data = []
for r in all_data:
    subcats = r.get("subcategory_results", {})
    rc = subcats.get("range_constraint", {})
    if rc:
        total_eval = rc.get("pass", 0) + rc.get("fail", 0)
        if total_eval > 0:
            range_constraint_data.append({
                "version": r["version"],
                "model": r["model"],
                "sample_id": r["sample_id"],
                "passed": rc.get("pass", 0) > 0,
                "pass_count": rc.get("pass", 0),
                "fail_count": rc.get("fail", 0),
            })

# 4.5a: 全样本 range_constraint pass rate by model
print(f"\n--- 全样本 range_constraint 通过率 ---")
print(f"{'模型':<25} │ {'v1通过率':>10} {'v1(n)':>6} │ {'v2通过率':>10} {'v2(n)':>6} │ {'Δ(pp)':>8}")
print("─" * 80)

for m in models:
    v1_items = [d for d in range_constraint_data if d["model"] == m and d["version"] == "dsv1"]
    v2_items = [d for d in range_constraint_data if d["model"] == m and d["version"] == "dsv2"]
    v1_pass = sum(1 for d in v1_items if d["passed"])
    v2_pass = sum(1 for d in v2_items if d["passed"])
    v1_rate = v1_pass / len(v1_items) if v1_items else None
    v2_rate = v2_pass / len(v2_items) if v2_items else None
    delta = ((v2_rate - v1_rate) * 100) if (v1_rate is not None and v2_rate is not None) else None
    
    v1_str = f"{v1_rate*100:.1f}%" if v1_rate is not None else "—"
    v2_str = f"{v2_rate*100:.1f}%" if v2_rate is not None else "—"
    d_str = f"{delta:>+.1f}pp" if delta is not None else "—"
    print(f"{m:<25} │ {v1_str:>10} {len(v1_items):>6} │ {v2_str:>10} {len(v2_items):>6} │ {d_str:>8}")

# 4.5b: 配对口径 (11 shared tasks)
print(f"\n--- 配对口径 range_constraint（{len(SHARED_SAMPLE_IDS)} shared tasks，排gate fail模型）---")
print(f"{'模型':<25} │ {'v1通过':>6} {'v1总':>4} {'v1率':>8} │ {'v2通过':>6} {'v2总':>4} {'v2率':>8} │ {'Δ(pp)':>8}")
print("─" * 85)

range_paired_summary = {}
for m in models:
    v1_pass, v1_total, v2_pass, v2_total = 0, 0, 0, 0
    for sid in SHARED_SAMPLE_IDS:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["total_score"] is not None and r2["total_score"] is not None:
            rc1 = r1.get("subcategory_results", {}).get("range_constraint", {})
            rc2 = r2.get("subcategory_results", {}).get("range_constraint", {})
            if (rc1.get("pass", 0) + rc1.get("fail", 0)) > 0:
                v1_total += 1
                if rc1.get("pass", 0) > 0:
                    v1_pass += 1
            if (rc2.get("pass", 0) + rc2.get("fail", 0)) > 0:
                v2_total += 1
                if rc2.get("pass", 0) > 0:
                    v2_pass += 1
    
    v1_rate = v1_pass / v1_total if v1_total > 0 else None
    v2_rate = v2_pass / v2_total if v2_total > 0 else None
    delta = ((v2_rate - v1_rate) * 100) if (v1_rate is not None and v2_rate is not None) else None
    
    gate_marker = " ⚠️" if m in gate_fail_models else ""
    v1_str = f"{v1_rate*100:.1f}%" if v1_rate is not None else "—"
    v2_str = f"{v2_rate*100:.1f}%" if v2_rate is not None else "—"
    d_str = f"{delta:>+.1f}pp" if delta is not None else "—"
    print(f"{m:<25} │ {v1_pass:>6} {v1_total:>4} {v1_str:>8} │ {v2_pass:>6} {v2_total:>4} {v2_str:>8} │ {d_str:>8}{gate_marker}")
    
    range_paired_summary[m] = {
        "v1_pass": v1_pass, "v1_total": v1_total, "v1_rate": v1_rate,
        "v2_pass": v2_pass, "v2_total": v2_total, "v2_rate": v2_rate,
        "delta_pp": delta,
    }

# 4.5c: 按长度分组
print(f"\n--- 按长度分组 range_constraint（排gate fail模型）---")
print(f"{'长度':<15} │ {'v1通过率':>10} │ {'v2通过率':>10} │ {'Δ(pp)':>8}")
print("─" * 55)

range_by_length = {}
for grp_name, grp_ids in LENGTH_GROUPS.items():
    v1_pass, v1_total, v2_pass, v2_total = 0, 0, 0, 0
    for m in valid_models:
        for sid in grp_ids:
            r1 = idx.get(("dsv1", m, sid))
            r2 = idx.get(("dsv2", m, sid))
            if r1 and r2 and r1["total_score"] is not None and r2["total_score"] is not None:
                rc1 = r1.get("subcategory_results", {}).get("range_constraint", {})
                rc2 = r2.get("subcategory_results", {}).get("range_constraint", {})
                if (rc1.get("pass", 0) + rc1.get("fail", 0)) > 0:
                    v1_total += 1
                    if rc1.get("pass", 0) > 0:
                        v1_pass += 1
                if (rc2.get("pass", 0) + rc2.get("fail", 0)) > 0:
                    v2_total += 1
                    if rc2.get("pass", 0) > 0:
                        v2_pass += 1
    
    v1_rate = v1_pass / v1_total if v1_total > 0 else None
    v2_rate = v2_pass / v2_total if v2_total > 0 else None
    delta = ((v2_rate - v1_rate) * 100) if (v1_rate is not None and v2_rate is not None) else None
    
    v1_str = f"{v1_rate*100:.1f}%" if v1_rate is not None else "—"
    v2_str = f"{v2_rate*100:.1f}%" if v2_rate is not None else "—"
    d_str = f"{delta:>+.1f}pp" if delta is not None else "—"
    print(f"{grp_name:<15} │ {v1_str:>10} │ {v2_str:>10} │ {d_str:>8}")
    range_by_length[grp_name] = {"v1_rate": v1_rate, "v2_rate": v2_rate, "delta_pp": delta}


# ==================== 5. 模型分层分析 ====================
print("\n\n" + "=" * 100)
print("5. 模型分层分析")
print("=" * 100)

# 按 DSV1 总分排序分层
sorted_models = sorted(
    [(m, s) for m, s in model_summary.items() if s["dsv1_total"] is not None and s["dsv2_total"] is not None],
    key=lambda x: x[1]["dsv1_total"],
    reverse=True
)

print(f"\n按 DSV1 总分排序:")
print(f"{'排名':>4} {'模型':<20} │ {'DSV1总分':>8} {'DSV2总分':>8} {'Δ总分':>8} │ {'DSV1内容':>8} {'DSV2内容':>8} {'Δ内容':>8} │ {'DSV1流程':>8} {'DSV2流程':>8} {'Δ流程':>8}")
print("─" * 120)

for i, (m, s) in enumerate(sorted_models, 1):
    tier = "强" if s["dsv1_total"] >= 75 else ("中" if s["dsv1_total"] >= 50 else "弱")
    print(f"{i:>3}[{tier}] {m:<20} │ {fmt(s['dsv1_total']):>8} {fmt(s['dsv2_total']):>8} {fmt(s['delta_total'], 1):>8} │ {fmt(s['dsv1_content']):>8} {fmt(s['dsv2_content']):>8} {fmt(s['delta_content'], 1):>8} │ {fmt(s['dsv1_process']):>8} {fmt(s['dsv2_process']):>8} {fmt(s['delta_process'], 1):>8}")


# ==================== 6. 共有 task 配对的 content_score 详细 ====================
print("\n\n" + "=" * 100)
print("6. 共有 Task 的 Content Score 配对对比")
print("=" * 100)

print(f"\n{'Task':<35} │", end="")
for m in models:
    print(f" {m[:10]:>10}", end="")
print()
print("─" * (37 + 11 * len(models)))

for sid in SHARED_SAMPLE_IDS:
    short_name = sid.replace("NW_CLEAR_", "").replace("NW_IP_", "IP_")
    # Content Delta
    print(f"  Δcontent {short_name:<24} │", end="")
    for m in models:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["content_score"] is not None and r2["content_score"] is not None:
            d = r2["content_score"] - r1["content_score"]
            print(f" {d:>+10.1f}", end="")
        else:
            print(f" {'—':>10}", end="")
    print()

print(f"\n  {'Δprocess':<35} │", end="")
print()
for sid in SHARED_SAMPLE_IDS:
    short_name = sid.replace("NW_CLEAR_", "").replace("NW_IP_", "IP_")
    print(f"  Δprocess {short_name:<24} │", end="")
    for m in models:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["process_score"] is not None and r2["process_score"] is not None:
            d = r2["process_score"] - r1["process_score"]
            print(f" {d:>+10.1f}", end="")
        else:
            print(f" {'—':>10}", end="")
    print()


# ==================== 6.5 按长度分组的配对分析 ====================
print("\n\n" + "=" * 100)
print("6.5. 按长度分组的配对 Content Score 对比")
print("=" * 100)

length_paired = {}  # {(model, length_group): {"v1_content": [], "v2_content": [], ...}}

for grp_name, grp_ids in LENGTH_GROUPS.items():
    print(f"\n--- {grp_name} ({len(grp_ids)} tasks) ---")
    print(f"{'模型':<25} │ {'v1内容':>8} {'v2内容':>8} {'Δ':>7} │ {'v1总分':>8} {'v2总分':>8} {'Δ':>7} │ {'n':>3}")
    print("─" * 90)
    
    for m in models:
        v1c, v2c, v1t, v2t = [], [], [], []
        for sid in grp_ids:
            r1 = idx.get(("dsv1", m, sid))
            r2 = idx.get(("dsv2", m, sid))
            if r1 and r2 and r1["content_score"] is not None and r2["content_score"] is not None:
                v1c.append(r1["content_score"])
                v2c.append(r2["content_score"])
                v1t.append(r1["total_score"])
                v2t.append(r2["total_score"])
        
        c1, c2 = avg(v1c), avg(v2c)
        t1, t2 = avg(v1t), avg(v2t)
        dc = (c2 - c1) if (c1 is not None and c2 is not None) else None
        dt = (t2 - t1) if (t1 is not None and t2 is not None) else None
        n = len(v1c)
        
        gate_marker = " ⚠️" if m in gate_fail_models else ""
        print(f"{m:<25} │ {fmt(c1):>8} {fmt(c2):>8} {fmt(dc, 1):>7} │ {fmt(t1):>8} {fmt(t2):>8} {fmt(dt, 1):>7} │ {n:>3}{gate_marker}")
        
        length_paired[(m, grp_name)] = {
            "v1_content": c1, "v2_content": c2, "delta_content": dc,
            "v1_total": t1, "v2_total": t2, "delta_total": dt,
            "n": n,
        }

# 按长度分组的跨模型汇总（排除 gate fail 率过高的模型）
print(f"\n--- 长度分组汇总（排gate fail模型）---")
print(f"{'长度':<15} │ {'Δcontent均值':>12} {'正/负/零':>10} │ {'Δtotal均值':>12} {'正/负/零':>10}")
print("─" * 70)
for grp_name in LENGTH_GROUPS:
    dc_vals = [length_paired[(m, grp_name)]["delta_content"] for m in valid_models
               if length_paired.get((m, grp_name), {}).get("delta_content") is not None]
    dt_vals = [length_paired[(m, grp_name)]["delta_total"] for m in valid_models
               if length_paired.get((m, grp_name), {}).get("delta_total") is not None]
    
    dc_avg = avg(dc_vals)
    dt_avg = avg(dt_vals)
    dc_pos = sum(1 for v in dc_vals if v > 0)
    dc_neg = sum(1 for v in dc_vals if v < 0)
    dc_zero = sum(1 for v in dc_vals if v == 0)
    dt_pos = sum(1 for v in dt_vals if v > 0)
    dt_neg = sum(1 for v in dt_vals if v < 0)
    dt_zero = sum(1 for v in dt_vals if v == 0)
    
    print(f"{grp_name:<15} │ {fmt(dc_avg, 1):>12} {dc_pos}/{dc_neg}/{dc_zero:>10} │ {fmt(dt_avg, 1):>12} {dt_pos}/{dt_neg}/{dt_zero:>10}")


# ==================== 7. 汇总统计 ====================
print("\n\n" + "=" * 100)
print("7. 汇总统计")
print("=" * 100)

# 全模型平均（排除配对 gate fail 率过高的模型）
# valid_models 已在前面定义

all_v1_total = [s["dsv1_total"] for m, s in model_summary.items() if m in valid_models and s["dsv1_total"] is not None]
all_v2_total = [s["dsv2_total"] for m, s in model_summary.items() if m in valid_models and s["dsv2_total"] is not None]

excluded_note = f"（排除gate fail率>{GATE_FAIL_THRESHOLD*100:.0f}%的模型: {', '.join(sorted(gate_fail_models))}）" if gate_fail_models else ""
print(f"\n全模型均值{excluded_note}:")
print(f"  DSV1 平均总分: {avg(all_v1_total):.2f}")
print(f"  DSV2 平均总分: {avg(all_v2_total):.2f}")
print(f"  Δ: {avg(all_v2_total) - avg(all_v1_total):+.2f}")

# 提升/下降模型数
up = sum(1 for m in valid_models if model_summary.get(m, {}).get("delta_total") is not None and model_summary[m]["delta_total"] > 0)
down = sum(1 for m in valid_models if model_summary.get(m, {}).get("delta_total") is not None and model_summary[m]["delta_total"] < 0)
print(f"\n总分提升模型: {up} 个")
print(f"总分下降模型: {down} 个")

# content 提升/下降
cup = sum(1 for m in valid_models if model_summary.get(m, {}).get("delta_content") is not None and model_summary[m]["delta_content"] > 0)
cdown = sum(1 for m in valid_models if model_summary.get(m, {}).get("delta_content") is not None and model_summary[m]["delta_content"] < 0)
print(f"\n内容分提升模型: {cup} 个")
print(f"内容分下降模型: {cdown} 个")

# process 提升/下降
pup = sum(1 for m in valid_models if model_summary.get(m, {}).get("delta_process") is not None and model_summary[m]["delta_process"] > 0)
pdown = sum(1 for m in valid_models if model_summary.get(m, {}).get("delta_process") is not None and model_summary[m]["delta_process"] < 0)
print(f"\n流程分提升模型: {pup} 个")
print(f"流程分下降模型: {pdown} 个")

# 配对对比汇总（11 shared tasks）
print(f"\n--- 共有 Task 配对对比汇总（{len(SHARED_SAMPLE_IDS)} shared tasks）---")
paired_up = sum(1 for m in valid_models if paired_summary.get(m, {}).get("delta_total") is not None and paired_summary[m]["delta_total"] > 0)
paired_down = sum(1 for m in valid_models if paired_summary.get(m, {}).get("delta_total") is not None and paired_summary[m]["delta_total"] < 0)
print(f"配对总分提升模型: {paired_up} 个")
print(f"配对总分下降模型: {paired_down} 个")

paired_cup = sum(1 for m in valid_models if paired_summary.get(m, {}).get("delta_content") is not None and paired_summary[m]["delta_content"] > 0)
paired_cdown = sum(1 for m in valid_models if paired_summary.get(m, {}).get("delta_content") is not None and paired_summary[m]["delta_content"] < 0)
print(f"配对内容分提升模型: {paired_cup} 个")
print(f"配对内容分下降模型: {paired_cdown} 个")

# 按模型打印配对 Δcontent 排名
print(f"\n  模型配对 Δcontent 排名（排gate fail）:")
ranked = sorted(
    [(m, paired_summary[m]) for m in valid_models if paired_summary.get(m, {}).get("delta_content") is not None],
    key=lambda x: x[1]["delta_content"], reverse=True
)
for m, ps in ranked:
    sign = "+" if ps["delta_content"] >= 0 else ""
    print(f"    {m:<25} Δcontent={sign}{ps['delta_content']:.1f}  (n={ps['pairs']})")

# 输出为 JSON 供报告引用
# 将 length_paired 转换为 JSON 友好格式（tuple key -> string key）
length_paired_json = {}
for (m, grp), vals in length_paired.items():
    if m not in length_paired_json:
        length_paired_json[m] = {}
    length_paired_json[m][grp] = vals

# 配对口径的 subcategory 聚合分析（7 valid models × 11 shared tasks）
paired_subcat_agg = defaultdict(lambda: {"v1_pass": 0, "v1_fail": 0, "v2_pass": 0, "v2_fail": 0})
for m in valid_models:
    for sid in SHARED_SAMPLE_IDS:
        r1 = idx.get(("dsv1", m, sid))
        r2 = idx.get(("dsv2", m, sid))
        if r1 and r2 and r1["total_score"] is not None and r2["total_score"] is not None:
            for ver, prefix in [("dsv1", "v1"), ("dsv2", "v2")]:
                r = idx.get((ver, m, sid))
                for sc, counts in r.get("subcategory_results", {}).items():
                    paired_subcat_agg[sc][f"{prefix}_pass"] += counts.get("pass", 0)
                    paired_subcat_agg[sc][f"{prefix}_fail"] += counts.get("fail", 0)

paired_subcat_deltas = []
for sc, d in paired_subcat_agg.items():
    v1t = d["v1_pass"] + d["v1_fail"]
    v2t = d["v2_pass"] + d["v2_fail"]
    if v1t > 0 and v2t > 0:
        v1_fail = d["v1_fail"] / v1t
        v2_fail = d["v2_fail"] / v2t
        delta_pp = (v2_fail - v1_fail) * 100
        paired_subcat_deltas.append({
            "subcategory": sc,
            "v1_fail_rate": round(v1_fail, 4),
            "v2_fail_rate": round(v2_fail, 4),
            "delta_pp": round(delta_pp, 1),
            "v1_n": v1t, "v2_n": v2t,
        })
paired_subcat_deltas.sort(key=lambda x: abs(x["delta_pp"]), reverse=True)

output = {
    "model_summary": model_summary,
    "paired_summary": paired_summary,
    "paired_no_gate": paired_no_gate,
    "length_paired": length_paired_json,
    "subcat_deltas_top40": subcat_deltas[:40],
    "paired_subcat_deltas": paired_subcat_deltas,
    "range_constraint": {
        "paired_by_model": range_paired_summary,
        "by_length": range_by_length,
    },
    "meta": {
        "revision": args.revision,
        "shared_task_count": len(SHARED_SAMPLE_IDS),
        "shared_tasks": SHARED_SAMPLE_IDS,
        "gate_fail_models": sorted(gate_fail_models),
        "valid_models": valid_models,
    },
}
with open(os.path.join(ANALYSIS_DIR, "dsv1_v2_analysis_output.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n分析数据已保存到 dsv1_v2_analysis_output.json")
