#!/usr/bin/env python3
"""
从 evaluation_outputs 中提取 logical_contradiction 和 character_design_adherence 的
LLM judge reason，用于分析 checker 合理性。

Part A: logical_contradiction - 强模型 FAIL 案例 + PASS 案例
Part B: character_design_adherence - 全模型 fail 率统计 + DSV1/DSV2 配对分析
"""
import json
import os
import random
import sys
from collections import defaultdict

random.seed(42)

EVAL_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "evaluation_outputs"
)

# 模型名称映射
MODEL_MAP = {
    "claude-opus-4-5-20251101": "claude-4.5",
    "claude-opus-4-6": "claude-4.6",
    "gemini-3-pro-preview": "gemini-3-pro",
    "kimi-k2.5": "kimi-k2.5",
    "ernie-5.0-thinking-preview": "ernie-5.0",
    "openai_EB5-0209-A35B-midtrain-128k-chat": "EB5-midtrain",
    "qwen3-max-2026-01-23": "qwen3-max",
    "doubao-seed-2-0-pro-260215": "doubao-2.0-pro",
}

STRONG_MODELS = {"claude-4.6", "claude-4.5", "gemini-3-pro"}


def extract_model_name(dirname):
    parts = dirname.split("_", 4)
    if len(parts) >= 5:
        model_suffix = parts[4]
    else:
        model_suffix = parts[-1]
    return MODEL_MAP.get(model_suffix, model_suffix)


def extract_version(dirname):
    if "dsv1" in dirname:
        return "dsv1"
    elif "dsv2" in dirname:
        return "dsv2"
    return "unknown"


def load_all_check_details():
    """遍历所有 eval 目录，提取 logical_contradiction 和 character_design_adherence 的完整 check 信息"""
    records = []

    for dirname in sorted(os.listdir(EVAL_DIR)):
        full_path = os.path.join(EVAL_DIR, dirname)
        if not os.path.isdir(full_path) or not dirname.startswith("eval_dsv"):
            continue
        if "ultra_short" in dirname:
            continue

        version = extract_version(dirname)
        model = extract_model_name(dirname)

        for env_dirname in sorted(os.listdir(full_path)):
            env_path = os.path.join(full_path, env_dirname)
            if not os.path.isdir(env_path) or not env_dirname.endswith("_env"):
                continue

            sample_id = env_dirname.replace("_env", "")
            rev006_path = os.path.join(env_path, "check_result_rev006.json")
            if not os.path.exists(rev006_path):
                continue

            with open(rev006_path, "r", encoding="utf-8") as f:
                check_result = json.load(f)

            details = check_result.get("check_details", {})
            for check_name, check_info in details.items():
                subcat = check_info.get("subcategory_id", "")
                if subcat in ("logical_contradiction", "character_design_adherence"):
                    records.append({
                        "model": model,
                        "version": version,
                        "sample_id": sample_id,
                        "dir": dirname,
                        "check_name": check_name,
                        "subcategory_id": subcat,
                        "check_result": check_info.get("check_result", ""),
                        "reason": check_info.get("reason", ""),
                        "details": check_info.get("details", ""),
                        "flaws": check_info.get("flaws", []),
                    })

    return records


def get_data_id(sample_id):
    """从 sample_id 提取可配对的 data_id"""
    # NW_CLEAR_MEDIUM_ANGSTY_001 -> CLEAR_MEDIUM_ANGSTY_001
    if sample_id.startswith("NW_"):
        return sample_id[3:]
    return sample_id


def print_separator(char="=", length=100):
    print(char * length)


def print_case(case, idx=None, extra_fields=None):
    """打印单个案例的完整信息"""
    prefix = f"[案例 {idx}] " if idx else ""
    print(f"\n{prefix}model={case['model']}, sample_id={case['sample_id']}, version={case['version']}")
    print(f"  check_result: {case['check_result']}")
    print(f"  reason: {case['reason']}")
    print(f"  details (完整):")
    print(f"    {case['details']}")
    if case.get("flaws"):
        print(f"  flaws ({len(case['flaws'])} 项):")
        for i, flaw in enumerate(case["flaws"]):
            print(f"    [{i+1}] type={flaw.get('type','')}, severity={flaw.get('severity','')}")
            print(f"        location: {flaw.get('location','')}")
            print(f"        description: {flaw.get('description','')}")
    else:
        print(f"  flaws: (无)")
    if extra_fields:
        for k, v in extra_fields.items():
            print(f"  {k}: {v}")


def part_a(records):
    """Part A: logical_contradiction 强模型分析"""
    print_separator("=")
    print("PART A: logical_contradiction (强模型: claude-4.6, claude-4.5, gemini-3-pro)")
    print_separator("=")

    lc_records = [r for r in records if r["subcategory_id"] == "logical_contradiction"]
    strong_lc = [r for r in lc_records if r["model"] in STRONG_MODELS]

    print(f"\n总 logical_contradiction 检查项: {len(lc_records)}")
    print(f"其中强模型: {len(strong_lc)}")

    # 统计
    strong_fail = [r for r in strong_lc if r["check_result"] == "fail"]
    strong_pass = [r for r in strong_lc if r["check_result"] == "pass"]
    strong_skip = [r for r in strong_lc if r["check_result"] == "skip"]

    print(f"  FAIL: {len(strong_fail)}, PASS: {len(strong_pass)}, SKIP: {len(strong_skip)}")

    # 按模型+版本统计
    model_version_stats = defaultdict(lambda: {"fail": 0, "pass": 0, "skip": 0})
    for r in strong_lc:
        key = f"{r['model']}_{r['version']}"
        model_version_stats[key][r["check_result"]] += 1

    print(f"\n{'模型_版本':<30} {'FAIL':>5} {'PASS':>5} {'SKIP':>5}")
    print("-" * 50)
    for k in sorted(model_version_stats.keys()):
        s = model_version_stats[k]
        print(f"{k:<30} {s['fail']:>5} {s['pass']:>5} {s['skip']:>5}")

    # 随机抽 5 个 FAIL 案例
    print_separator("-")
    print(f"\n随机抽取 5 个 FAIL 案例 (共 {len(strong_fail)} 个可选):")
    sampled_fail = random.sample(strong_fail, min(5, len(strong_fail)))
    for i, case in enumerate(sampled_fail, 1):
        print_case(case, idx=i)

    # 随机抽 2 个 PASS 案例
    print_separator("-")
    print(f"\n随机抽取 2 个 PASS 案例 (共 {len(strong_pass)} 个可选):")
    sampled_pass = random.sample(strong_pass, min(2, len(strong_pass)))
    for i, case in enumerate(sampled_pass, 1):
        print_case(case, idx=i)


def part_b(records):
    """Part B: character_design_adherence 全模型分析"""
    print_separator("=")
    print("\nPART B: character_design_adherence (全模型)")
    print_separator("=")

    cda_records = [r for r in records if r["subcategory_id"] == "character_design_adherence"]
    print(f"\n总 character_design_adherence 检查项: {len(cda_records)}")

    # 按模型+版本统计 fail 率
    model_version_stats = defaultdict(lambda: {"fail": 0, "pass": 0, "skip": 0, "total": 0})
    for r in cda_records:
        key = (r["model"], r["version"])
        model_version_stats[key][r["check_result"]] += 1
        model_version_stats[key]["total"] += 1

    print(f"\n{'模型':<20} {'版本':<6} {'FAIL':>5} {'PASS':>5} {'SKIP':>5} {'总计':>5} {'Fail率':>8}")
    print("-" * 70)
    for (m, v) in sorted(model_version_stats.keys()):
        s = model_version_stats[(m, v)]
        denominator = s["fail"] + s["pass"]
        fail_rate = s["fail"] / denominator if denominator > 0 else 0
        print(f"{m:<20} {v:<6} {s['fail']:>5} {s['pass']:>5} {s['skip']:>5} {s['total']:>5} {fail_rate:>7.1%}")

    # DSV1 vs DSV2 汇总
    print(f"\n--- DSV1 vs DSV2 汇总 (按模型) ---")
    models = sorted(set(r["model"] for r in cda_records))
    print(f"\n{'模型':<20} {'DSV1 Fail率':>12} {'DSV2 Fail率':>12} {'差异':>8}")
    print("-" * 55)
    for m in models:
        dsv1 = model_version_stats.get((m, "dsv1"), {"fail": 0, "pass": 0})
        dsv2 = model_version_stats.get((m, "dsv2"), {"fail": 0, "pass": 0})
        d1 = dsv1["fail"] + dsv1["pass"]
        d2 = dsv2["fail"] + dsv2["pass"]
        r1 = dsv1["fail"] / d1 if d1 > 0 else -1
        r2 = dsv2["fail"] / d2 if d2 > 0 else -1
        diff = r2 - r1 if r1 >= 0 and r2 >= 0 else float("nan")
        r1_str = f"{r1:.1%}" if r1 >= 0 else "N/A"
        r2_str = f"{r2:.1%}" if r2 >= 0 else "N/A"
        diff_str = f"{diff:+.1%}" if not (diff != diff) else "N/A"
        print(f"{m:<20} {r1_str:>12} {r2_str:>12} {diff_str:>8}")

    # 寻找 DSV2 fail 但 DSV1 pass 的配对
    print_separator("-")
    print("\n寻找同模型同 task: DSV2 FAIL 但 DSV1 PASS 的配对...")

    # 建立索引: (model, data_id, version) -> record
    index = {}
    for r in cda_records:
        data_id = get_data_id(r["sample_id"])
        index[(r["model"], data_id, r["version"])] = r

    paired_cases = []
    for r in cda_records:
        if r["version"] == "dsv2" and r["check_result"] == "fail":
            data_id = get_data_id(r["sample_id"])
            dsv1_r = index.get((r["model"], data_id, "dsv1"))
            if dsv1_r and dsv1_r["check_result"] == "pass":
                paired_cases.append((dsv1_r, r))

    if len(paired_cases) >= 3:
        print(f"找到 {len(paired_cases)} 个配对，随机抽取 3 个:")
        sampled_pairs = random.sample(paired_cases, min(3, len(paired_cases)))
        for i, (dsv1_case, dsv2_case) in enumerate(sampled_pairs, 1):
            print(f"\n--- 配对 {i} ---")
            print(f"model={dsv1_case['model']}, sample_id={dsv1_case['sample_id']}")
            print(f"\n  [DSV1 PASS]")
            print(f"  reason: {dsv1_case['reason']}")
            print(f"  details (完整):")
            print(f"    {dsv1_case['details']}")
            if dsv1_case.get("flaws"):
                print(f"  flaws ({len(dsv1_case['flaws'])} 项):")
                for j, flaw in enumerate(dsv1_case["flaws"]):
                    print(f"    [{j+1}] type={flaw.get('type','')}, severity={flaw.get('severity','')}, location={flaw.get('location','')}")
                    print(f"        description: {flaw.get('description','')}")
            print(f"\n  [DSV2 FAIL]")
            print(f"  reason: {dsv2_case['reason']}")
            print(f"  details (完整):")
            print(f"    {dsv2_case['details']}")
            if dsv2_case.get("flaws"):
                print(f"  flaws ({len(dsv2_case['flaws'])} 项):")
                for j, flaw in enumerate(dsv2_case["flaws"]):
                    print(f"    [{j+1}] type={flaw.get('type','')}, severity={flaw.get('severity','')}, location={flaw.get('location','')}")
                    print(f"        description: {flaw.get('description','')}")
    else:
        print(f"只找到 {len(paired_cases)} 个配对 (不足 3 个)")
        if paired_cases:
            print("输出所有找到的配对:")
            for i, (dsv1_case, dsv2_case) in enumerate(paired_cases, 1):
                print(f"\n--- 配对 {i} ---")
                print(f"model={dsv1_case['model']}, sample_id={dsv1_case['sample_id']}")
                print(f"\n  [DSV1 PASS] reason: {dsv1_case['reason']}")
                print(f"  details: {dsv1_case['details']}")
                print(f"\n  [DSV2 FAIL] reason: {dsv2_case['reason']}")
                print(f"  details: {dsv2_case['details']}")

        # 补充：分别输出 DSV1 pass 和 DSV2 fail 的案例
        print(f"\n--- 补充：分别输出 DSV1 PASS 和 DSV2 FAIL 案例各 3 个 ---")

        dsv1_pass = [r for r in cda_records if r["version"] == "dsv1" and r["check_result"] == "pass"]
        dsv2_fail = [r for r in cda_records if r["version"] == "dsv2" and r["check_result"] == "fail"]

        print(f"\nDSV1 PASS 案例 (共 {len(dsv1_pass)} 个, 抽 3 个):")
        for i, case in enumerate(random.sample(dsv1_pass, min(3, len(dsv1_pass))), 1):
            print_case(case, idx=i)

        print(f"\nDSV2 FAIL 案例 (共 {len(dsv2_fail)} 个, 抽 3 个):")
        for i, case in enumerate(random.sample(dsv2_fail, min(3, len(dsv2_fail))), 1):
            print_case(case, idx=i)


def main():
    print("正在加载所有 check_result_rev006.json 文件...")
    records = load_all_check_details()
    print(f"共加载 {len(records)} 条相关检查项记录\n")

    lc_count = sum(1 for r in records if r["subcategory_id"] == "logical_contradiction")
    cda_count = sum(1 for r in records if r["subcategory_id"] == "character_design_adherence")
    print(f"  logical_contradiction: {lc_count}")
    print(f"  character_design_adherence: {cda_count}")

    part_a(records)
    print("\n\n")
    part_b(records)


if __name__ == "__main__":
    main()
