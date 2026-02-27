#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说创作炼金术场景 - Checker入口（与benchkit适配）

职责：作为统一入口，调用checker_execute和checker_score
输入：bench.json（包含check_list）+ result.json（执行结果）
输出：check_result.json（完整的评估结果）

内部流程：
1. 调用checker_execute.py生成execution_result.json（包含pass/fail和grading）
2. 调用checker_score.py生成check_result.json（维度聚合和质量等级）

增量模式：
- --existing-result: 基于已有check_result，只执行新增/指定的check项
- --only-checks: 逗号分隔的检查项序号（如 33,35,36），只执行这些项
  两者可组合使用：
  - --only-checks 单独使用：只跑指定项，输出只含这些项
  - --existing-result + --only-checks: 在已有结果上重跑指定项（覆盖）
  - --existing-result 单独使用：在已有结果上增跑新checklist中有但已有结果中没有的项
"""

import json
import argparse
import sys
from pathlib import Path
import tempfile

# 导入两个子模块
from checker_execute import execute_checks
from checker_score import calculate_scores


def main():
    parser = argparse.ArgumentParser(description="小说创作炼金术场景自动评估检查脚本")
    parser.add_argument("--bench", required=True, help="bench.json文件路径（包含check_list）")
    parser.add_argument("--result", required=True, help="result.json文件路径（执行结果）")
    parser.add_argument("--model", required=True, help="检查用的模型名称（用于semantic检查）")
    parser.add_argument("--base-url", required=True, help="模型API base URL")
    parser.add_argument("--api-key", required=True, help="模型API密钥")
    parser.add_argument("--output", default="check_result.json", help="输出文件路径")
    parser.add_argument("--work-dir", default=".", help="工作目录")
    parser.add_argument("--capability-taxonomy", default=None,
                       help="能力体系配置文件路径（可选）")
    parser.add_argument("--existing-result", default=None,
                       help="已有的check_result.json路径，用于增量模式")
    parser.add_argument("--only-checks", default=None,
                       help="逗号分隔的检查项序号（如 33,35,36），只执行这些项")
    args = parser.parse_args()

    print("[Checker] 加载输入文件...")
    # 加载输入文件
    with open(args.bench, "r", encoding="utf-8") as f:
        bench_data = json.load(f)
    with open(args.result, "r", encoding="utf-8") as f:
        result_data = json.load(f)

    # 准备sample_result（用于checker_execute）
    sample_id = bench_data.get("data_id", "unknown")
    # work_dir就是env目录，workspace是其子目录
    workspace_path = str(Path(args.work_dir) / "workspace")

    sample_result = {
        "sample_id": sample_id,
        "conversation_history": result_data.get("conversation_history", []),
        "workspace_path": workspace_path
    }

    # 准备check_list
    check_list = bench_data.get("check_list", [])

    # 准备LLM配置
    model_config = {
        "model_name": args.model,
        "api_base": args.base_url,
        "api_key": args.api_key
    }

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

    # 解析 --only-checks
    only_check_indices = None
    if args.only_checks:
        only_check_indices = set()
        for part in args.only_checks.split(","):
            part = part.strip()
            if part.isdigit():
                only_check_indices.add(int(part))
        print(f"[Checker] 指定检查项: {sorted(only_check_indices)}")

    # 确定需要执行的检查项
    checks_to_run = []
    check_index_map = {}  # index -> check_item，用于后续合并

    for i, check_item in enumerate(check_list, 1):
        check_key = f"检查项{i}"
        check_index_map[i] = (check_key, check_item)

        if only_check_indices is not None:
            # --only-checks 模式：只跑指定项
            if i in only_check_indices:
                checks_to_run.append((i, check_key, check_item))
        elif existing_check_details:
            # --existing-result 单独使用（add模式）：只跑已有结果中没有的项
            if check_key not in existing_check_details:
                checks_to_run.append((i, check_key, check_item))
        else:
            # 全量模式
            checks_to_run.append((i, check_key, check_item))

    if not checks_to_run:
        if only_check_indices is not None:
            print(f"[Checker] 指定的检查项序号在checklist中均不存在，无需执行")
        else:
            print(f"[Checker] 所有检查项已有结果，无需执行新检查")

        # 仍然需要用已有结果重新算分（checker可能更新了）
        if existing_result_data:
            print(f"[Checker] 使用已有结果重新计算分数...")
            execution_result = {
                "sample_id": sample_id,
                "check_timestamp": existing_result_data.get("check_timestamp",
                    int(__import__('time').time())),
                "check_details": existing_check_details
            }
        else:
            print(f"[Checker] 无已有结果且无需执行的检查项，退出")
            sys.exit(0)
    else:
        # 构建只含需要执行项的 check_list
        filtered_check_list = [item for _, _, item in checks_to_run]
        run_indices = [idx for idx, _, _ in checks_to_run]

        mode_desc = "增量" if existing_check_details else ("指定项" if only_check_indices else "全量")
        print(f"\n[Checker] 第1步：执行检查（{mode_desc}模式）...")
        print(f"[Checker]   - Sample ID: {sample_id}")
        print(f"[Checker]   - Workspace: {workspace_path}")
        print(f"[Checker]   - 待执行: {len(checks_to_run)}/{len(check_list)} 项 (序号: {run_indices})")
        print(f"[Checker]   - Model: {args.model}")

        # 执行检查
        try:
            partial_result = execute_checks(
                sample_result,
                filtered_check_list,
                model_config
            )
        except Exception as e:
            print(f"[Checker] 错误：执行检查失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

        # 将 execute_checks 返回的结果（检查项1,2,3...）映射回正确的序号
        partial_details = partial_result.get("check_details", {})
        remapped_details = {}
        for j, (orig_idx, check_key, _) in enumerate(checks_to_run, 1):
            partial_key = f"检查项{j}"
            if partial_key in partial_details:
                remapped_details[check_key] = partial_details[partial_key]

        # 合并结果：已有结果 + 新执行结果（新的覆盖旧的）
        merged_details = {}
        if existing_check_details:
            merged_details.update(existing_check_details)
        merged_details.update(remapped_details)

        import time
        execution_result = {
            "sample_id": sample_id,
            "check_timestamp": int(time.time()),
            "check_details": merged_details
        }

    # ========== 第2步：计算维度分数 ==========
    print(f"\n[Checker] 第2步：计算维度分数和质量等级...")

    # 加载能力体系配置（如果提供）
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

    # 打印摘要
    overall = check_result["overall_result"]
    print(f"\n[结果] 状态: {overall['status']}")
    print(f"[结果] 总分: {overall['total_score']}/100")
    print(f"[结果] 通过率: {overall['pass_rate']*100:.1f}% ({overall['passed_checks']}/{overall['total_checks']})")

    # 打印维度分数
    dimension_scores = check_result["dimension_scores"]
    print(f"\n[维度分数]")
    for dim_id, dim_data in dimension_scores.items():
        if dim_id == "content_quality":
            # content_quality特殊显示
            print(f"  - {dim_id}: {dim_data['overall_score']:.1f}分 [{dim_data['quality_level']}]")
            print(f"    · basic: {dim_data['basic_layer']['passed']}/{dim_data['basic_layer']['total']}")
            print(f"    · advanced: {dim_data['advanced_layer']['passed']}/{dim_data['advanced_layer']['total']}")
        else:
            # 普通维度
            print(f"  - {dim_id}: {dim_data['pass_rate']*100:.1f}分 ({dim_data['passed']}/{dim_data['total']})")


if __name__ == "__main__":
    main()
