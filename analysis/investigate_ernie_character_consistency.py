#!/usr/bin/env python3
"""调查Ernie 5.0在人物设定一致性（character_trait_consistency）上的0分问题"""

import json
from pathlib import Path
from collections import defaultdict

ernie_eval_dir = Path('/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs/eval_v2_20260205_140957_ernie-5.0-thinking-preview')

# 统计数据
total_samples = 0
execution_success_samples = 0
check18_passed = 0
check18_failed = 0
check18_not_found = 0

failed_cases = []

# 遍历所有样本目录
for sample_dir in ernie_eval_dir.iterdir():
    if not sample_dir.is_dir() or not sample_dir.name.endswith('_env'):
        continue

    total_samples += 1

    # 查找check_result文件
    check_result_file = sample_dir / 'check_result_v3.json'
    if not check_result_file.exists():
        check_result_file = sample_dir / 'check_resultv3.json'

    if not check_result_file.exists():
        continue

    with open(check_result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)

    # 只统计execution_success的样本
    output_completeness = result.get('output_completeness', {})
    if output_completeness.get('score', 0) == 0:
        continue

    execution_success_samples += 1

    # 检查检查项18
    check_details = result.get('check_details', {})
    check18 = check_details.get('检查项18', {})

    if not check18:
        check18_not_found += 1
        continue

    check_result = check18.get('检查结论', '')

    if check_result == '合格':
        check18_passed += 1
    else:
        check18_failed += 1
        failed_cases.append({
            'sample_id': result.get('sample_id', sample_dir.name.replace('_env', '')),
            'result': check_result,
            'reason': check18.get('原因', ''),
            'details': check18.get('详情', '')[:500]  # 只取前500字符
        })

print("=" * 100)
print("Ernie 5.0 人物设定一致性（检查项18）分析报告")
print("=" * 100)
print(f"\n总样本目录数: {total_samples}")
print(f"执行成功样本数 (output_completeness > 0): {execution_success_samples}")
print(f"\n检查项18统计:")
print(f"  - 合格: {check18_passed}")
print(f"  - 不合格: {check18_failed}")
print(f"  - 未找到检查项18: {check18_not_found}")
print(f"  - 通过率: {check18_passed / execution_success_samples * 100:.1f}%" if execution_success_samples > 0 else "  - 通过率: N/A")

print("\n" + "=" * 100)
print(f"失败案例详情（共{len(failed_cases)}个）")
print("=" * 100)

for i, case in enumerate(failed_cases[:5], 1):  # 只显示前5个
    print(f"\n【案例 {i}】")
    print(f"样本ID: {case['sample_id']}")
    print(f"检查结论: {case['result']}")
    print(f"原因: {case['reason']}")
    print(f"详情（前500字）:\n{case['details']}")
    print("-" * 100)
