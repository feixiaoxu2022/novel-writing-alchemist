#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复check_result文件：
1. 删除 output_completeness 字段
2. 中文字段名改英文
3. 中文值改英文
"""

import json
import glob
from pathlib import Path


def fix_check_result(data: dict) -> dict:
    """修复单个check_result数据"""

    # 1. 删除 output_completeness
    if "output_completeness" in data:
        del data["output_completeness"]

    # 2. 修复 check_details 中的字段名和值
    if "check_details" in data:
        for check_id, check_info in data["check_details"].items():
            # 字段名：检查结论 -> check_result
            if "检查结论" in check_info:
                check_info["check_result"] = check_info.pop("检查结论")

            # 字段名：原因 -> reason
            if "原因" in check_info:
                check_info["reason"] = check_info.pop("原因")

            # 字段名：详情 -> details
            if "详情" in check_info:
                check_info["details"] = check_info.pop("详情")

            # 值：合格 -> pass
            if check_info.get("check_result") == "合格":
                check_info["check_result"] = "pass"

            # 值：不合格 -> fail
            if check_info.get("check_result") == "不合格":
                check_info["check_result"] = "fail"

            # 值：跳过 -> skip
            if check_info.get("check_result") == "跳过":
                check_info["check_result"] = "skip"

    return data


def main():
    # 查找所有check_result文件
    eval_dir = "/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101"

    check_files = glob.glob(f"{eval_dir}/*_env/check_result*.json")

    print(f"找到 {len(check_files)} 个check_result文件")

    success_count = 0
    failed_count = 0

    for file_path in check_files:
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 修复数据
            fixed_data = fix_check_result(data)

            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(fixed_data, f, ensure_ascii=False, indent=2)

            print(f"✅ {Path(file_path).parent.name}/{Path(file_path).name}")
            success_count += 1

        except Exception as e:
            print(f"❌ {Path(file_path).parent.name}/{Path(file_path).name}: {str(e)}")
            failed_count += 1

    print(f"\n处理完成:")
    print(f"  成功: {success_count}")
    print(f"  失败: {failed_count}")


if __name__ == "__main__":
    main()
