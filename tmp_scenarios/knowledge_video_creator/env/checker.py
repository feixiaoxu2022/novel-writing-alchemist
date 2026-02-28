#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_video_creator — Checker 入口（与 benchkit 适配）

职责：作为统一入口，调用 checker_execute 和 checker_score
输入：bench.json（包含 check_list）+ result.json（Agent执行结果）
输出：check_result.json（完整评估结果）

内部流程：
  1. 调用 checker_execute.execute_checks() 生成逐项 pass/fail/skip
  2. 调用 checker_score.calculate_scores() 生成维度聚合和质量等级

增量模式：
  --existing-result: 基于已有 check_result，只执行新增/指定的 check 项
  --only-checks: 逗号分隔的检查项标识，支持语义 ID 和数字序号：
    · 语义化ID: --only-checks "知识提炼能力基础,视觉化设计能力基础"
    · 数字序号: --only-checks "15,16,17"
    · 可混用
  两者可组合使用：
    - --only-checks 单独使用：只跑指定项
    - --existing-result + --only-checks: 在已有结果上重跑指定项（覆盖）
    - --existing-result 单独使用：增跑 checklist 中有但已有结果中没有的项
"""

import json
import argparse
import sys
import time
from pathlib import Path

# 导入两个子模块（同目录下）
from checker_execute import execute_checks
from checker_score import calculate_scores


def main():
    parser = argparse.ArgumentParser(
        description="knowledge_video_creator 场景自动评估检查脚本"
    )
    parser.add_argument("--bench", required=True,
                        help="bench.json 文件路径（包含 check_list）")
    parser.add_argument("--result", required=True,
                        help="result.json 文件路径（Agent 执行结果）")
    parser.add_argument("--model", required=True,
                        help="检查用的模型名称（用于 semantic 检查）")
    parser.add_argument("--base-url", required=True,
                        help="模型 API base URL")
    parser.add_argument("--api-key", required=True,
                        help="模型 API 密钥")
    parser.add_argument("--output", default="check_result.json",
                        help="输出文件路径")
    parser.add_argument("--work-dir", default=".",
                        help="工作目录（workspace 的父目录）")
    parser.add_argument("--capability-taxonomy", default=None,
                        help="能力体系配置文件路径（可选）")
    parser.add_argument("--existing-result", default=None,
                        help="已有的 check_result.json 路径，用于增量模式")
    parser.add_argument("--only-checks", default=None,
                        help="逗号分隔的检查项标识（支持语义 ID 或数字序号）")
    args = parser.parse_args()

    print("[Checker] 加载输入文件...")

    # 加载输入文件
    with open(args.bench, "r", encoding="utf-8") as f:
        bench_data = json.load(f)
    with open(args.result, "r", encoding="utf-8") as f:
        result_data = json.load(f)

    # 准备基本信息
    sample_id = bench_data.get("data_id", "unknown")
    work_dir = str(Path(args.work_dir).resolve())

    sample_result = {
        "sample_id": sample_id,
        "conversation_history": result_data.get("conversation_history", []),
    }

    # 准备 check_list
    check_list = bench_data.get("check_list", [])

    # ========== 增量模式处理 ==========
    existing_check_details = {}
    existing_result_data = None

    # 加载已有结果
    if args.existing_result:
        existing_path = Path(args.existing_result)
        if existing_path.exists():
            with open(existing_path, "r", encoding="utf-8") as f:
                existing_result_data = json.load(f)
            existing_check_details = existing_result_data.get("check_details", {})
            print(f"[Checker] 增量模式：加载已有结果，包含 {len(existing_check_details)} 个检查项")
        else:
            print(f"[Checker] 警告：--existing-result 文件不存在: {existing_path}，将执行全量检查")

    # 解析 --only-checks（同时支持数字序号和语义化 check_id）
    only_check_indices = None
    only_check_ids = None
    if args.only_checks:
        only_check_indices = set()
        only_check_ids = set()
        for part in args.only_checks.split(","):
            part = part.strip()
            if part.isdigit():
                only_check_indices.add(int(part))
            elif part:
                only_check_ids.add(part)
        if not only_check_indices:
            only_check_indices = None
        if not only_check_ids:
            only_check_ids = None
        display_parts = []
        if only_check_indices:
            display_parts.append(f"序号: {sorted(only_check_indices)}")
        if only_check_ids:
            display_parts.append(f"ID: {sorted(only_check_ids)}")
        print(f"[Checker] 指定检查项: {', '.join(display_parts)}")

    # 确定需要执行的检查项
    checks_to_run = []

    for i, check_item in enumerate(check_list, 1):
        check_key = check_item.get("check_id", f"检查项{i}")

        if only_check_indices is not None or only_check_ids is not None:
            # --only-checks 模式
            matched = False
            if only_check_indices and i in only_check_indices:
                matched = True
            if only_check_ids and check_key in only_check_ids:
                matched = True
            if matched:
                checks_to_run.append((i, check_key, check_item))
        elif existing_check_details:
            # --existing-result 单独使用（add模式）
            if check_key not in existing_check_details:
                checks_to_run.append((i, check_key, check_item))
        else:
            # 全量模式
            checks_to_run.append((i, check_key, check_item))

    if not checks_to_run:
        if only_check_indices is not None or only_check_ids is not None:
            print(f"[Checker] 指定的检查项在 checklist 中均不存在，无需执行")
        else:
            print(f"[Checker] 所有检查项已有结果，无需执行新检查")

        # 仍然用已有结果重新算分
        if existing_result_data:
            print(f"[Checker] 使用已有结果重新计算分数...")
            execution_result = {
                "sample_id": sample_id,
                "check_timestamp": existing_result_data.get("check_timestamp", int(time.time())),
                "check_details": existing_check_details
            }
        else:
            print(f"[Checker] 无已有结果且无需执行的检查项，退出")
            sys.exit(0)
    else:
        # 构建只含需要执行项的 check_list
        filtered_check_list = [item for _, _, item in checks_to_run]
        run_keys = [key for _, key, _ in checks_to_run]

        mode_desc = "增量" if existing_check_details else ("指定项" if (only_check_indices or only_check_ids) else "全量")
        print(f"\n[Checker] 第1步：执行检查（{mode_desc}模式）...")
        print(f"[Checker]   - Sample ID: {sample_id}")
        print(f"[Checker]   - Work Dir: {work_dir}")
        print(f"[Checker]   - 待执行: {len(checks_to_run)}/{len(check_list)} 项")
        print(f"[Checker]   - IDs: {run_keys}")
        print(f"[Checker]   - Model: {args.model}")

        # 执行检查
        try:
            partial_result = execute_checks(
                check_list=filtered_check_list,
                sample_result=sample_result,
                work_dir=work_dir,
                model_name=args.model,
                api_base=args.base_url,
                api_key=args.api_key
            )
        except Exception as e:
            print(f"[Checker] 错误：执行检查失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

        partial_details = partial_result.get("check_details", {})

        # 合并结果：已有 + 新执行（新的覆盖旧的）
        merged_details = {}
        if existing_check_details:
            merged_details.update(existing_check_details)

        # 清理被替代的旧检查项（replaces 机制）
        replaced_keys = set()
        for check_item in check_list:
            replaces = check_item.get("params", {}).get("replaces", [])
            if isinstance(replaces, str):
                replaces = [replaces]
            for old_key in replaces:
                replaced_keys.add(old_key)
        if replaced_keys:
            for old_key in replaced_keys:
                if old_key in merged_details:
                    del merged_details[old_key]
                    print(f"[Checker] 清理被替代的旧检查项: {old_key}")
            # 也按 subcategory_id 清理
            keys_to_remove = []
            for key, val in merged_details.items():
                if isinstance(val, dict) and val.get("subcategory_id") in replaced_keys:
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del merged_details[key]
                print(f"[Checker] 清理被替代的旧检查项（按 subcategory_id 匹配）: {key}")

        merged_details.update(partial_details)

        execution_result = {
            "sample_id": sample_id,
            "check_timestamp": int(time.time()),
            "check_details": merged_details
        }

    # ========== 第2步：计算维度分数 ==========
    print(f"\n[Checker] 第2步：计算维度分数和质量等级...")

    capability_taxonomy = None
    if args.capability_taxonomy:
        import yaml
        with open(args.capability_taxonomy, "r", encoding="utf-8") as f:
            capability_taxonomy = yaml.safe_load(f)

    try:
        check_result = calculate_scores(
            execution_result,
            capability_taxonomy
        )
    except Exception as e:
        print(f"[Checker] 错误：计算分数失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(check_result, f, ensure_ascii=False, indent=2)

    print(f"\n[Checker] 检查完成！")
    print(f"[Checker]   - 输出文件: {output_path}")

    # ========== 打印结果摘要 ==========
    overall = check_result["overall_result"]
    dimension_scores = check_result["dimension_scores"]

    print(f"\n[结果] 状态: {overall['status']}")
    print(f"[结果] 总分: {overall['total_score']}/100")
    print(f"[结果] 内容分: {overall.get('content_score', '?')}/100 (权重70%)")
    print(f"[结果] 流程分: {overall.get('process_score', '?')}/100 (权重30%)")
    if overall.get("gate_triggered"):
        print(f"[结果] ⚠ Gate 层触发惩罚")
    print(f"[结果] 通过率: {overall['pass_rate'] * 100:.1f}% ({overall['passed_checks']}/{overall['total_checks']})")

    print(f"\n[维度分数]")
    for dim_id in ["format_compliance", "business_rule_compliance", "data_consistency", "content_quality"]:
        if dim_id not in dimension_scores:
            continue
        dim_data = dimension_scores[dim_id]
        if dim_id == "content_quality":
            print(f"  - {dim_id}: {dim_data['overall_score']:.1f}分 [{dim_data['quality_level']}]")
            print(f"    · gate: {dim_data['gate_layer']['passed']}/{dim_data['gate_layer']['total']}"
                  f"{'  ⚠ 触发' if dim_data['gate_triggered'] else ''}")
            print(f"    · basic: {dim_data['basic_layer']['passed']}/{dim_data['basic_layer']['total']}")
            if dim_data["basic_layer"]["failed_items"]:
                print(f"      失败项: {', '.join(dim_data['basic_layer']['failed_items'])}")
            print(f"    · advanced: {dim_data['advanced_layer']['passed']}/{dim_data['advanced_layer']['total']}")
            if dim_data["advanced_layer"]["failed_items"]:
                print(f"      失败项: {', '.join(dim_data['advanced_layer']['failed_items'])}")
            # 评分拆解
            breakdown = dim_data.get("score_breakdown", {})
            if breakdown:
                print(f"    · 评分: 基准{breakdown.get('base', 60)} "
                      f"gate{breakdown.get('gate_penalty', 0):+.1f} "
                      f"basic{breakdown.get('basic_deduction', 0):+.1f} "
                      f"adv{breakdown.get('advanced_bonus', 0):+.1f}")
        else:
            print(f"  - {dim_id}: {dim_data['pass_rate'] * 100:.1f}% ({dim_data['passed']}/{dim_data['total']})")
            if dim_data["failed_items"]:
                print(f"    · 失败项: {', '.join(dim_data['failed_items'])}")


if __name__ == "__main__":
    main()
