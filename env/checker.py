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

    print(f"[Checker] 第1步：执行检查（LLM调用）...")
    print(f"[Checker]   - Sample ID: {sample_id}")
    print(f"[Checker]   - Workspace: {workspace_path}")
    print(f"[Checker]   - Check List: {len(check_list)} 项")
    print(f"[Checker]   - Model: {args.model}")

    # 第1步：执行检查（生成execution_result）
    try:
        execution_result = execute_checks(
            sample_result,
            check_list,
            model_config
        )
    except Exception as e:
        print(f"[Checker] 错误：执行检查失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 第2步：计算维度分数（生成check_result）
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
