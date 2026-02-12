#!/usr/bin/env python3
"""对比Claude Opus 4.5和Ernie 5.0在人物设定一致性（检查项18）上的表现"""

import json
from pathlib import Path

claude_dir = Path('/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101')
ernie_dir = Path('/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs/eval_v2_20260205_140957_ernie-5.0-thinking-preview')

def analyze_model(model_name, eval_dir):
    """分析指定模型在检查项18上的表现"""
    execution_success = 0
    check18_passed = 0
    check18_failed = 0

    passed_cases = []
    failed_cases = []

    for sample_dir in eval_dir.iterdir():
        if not sample_dir.is_dir() or not sample_dir.name.endswith('_env'):
            continue

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

        execution_success += 1

        check18 = result.get('check_details', {}).get('检查项18', {})
        if not check18:
            continue

        check_result_val = check18.get('检查结论', '')
        sample_id = result.get('sample_id', sample_dir.name.replace('_env', ''))

        if check_result_val == '合格':
            check18_passed += 1
            passed_cases.append({
                'sample_id': sample_id,
                'reason': check18.get('原因', ''),
                'details': check18.get('详情', '')[:800]  # 前800字符
            })
        else:
            check18_failed += 1
            failed_cases.append({
                'sample_id': sample_id,
                'reason': check18.get('原因', ''),
                'details': check18.get('详情', '')[:800]
            })

    return {
        'model_name': model_name,
        'execution_success': execution_success,
        'check18_passed': check18_passed,
        'check18_failed': check18_failed,
        'pass_rate': check18_passed / execution_success * 100 if execution_success > 0 else 0,
        'passed_cases': passed_cases,
        'failed_cases': failed_cases
    }

# 分析两个模型
claude_stats = analyze_model('Claude Opus 4.5', claude_dir)
ernie_stats = analyze_model('Ernie 5.0', ernie_dir)

print("=" * 120)
print("Claude Opus 4.5 vs Ernie 5.0 - 人物设定一致性（检查项18）对比")
print("=" * 120)

print(f"\n【{claude_stats['model_name']}】")
print(f"执行成功样本数: {claude_stats['execution_success']}")
print(f"检查项18 - 合格: {claude_stats['check18_passed']}")
print(f"检查项18 - 不合格: {claude_stats['check18_failed']}")
print(f"通过率: {claude_stats['pass_rate']:.1f}%")

print(f"\n【{ernie_stats['model_name']}】")
print(f"执行成功样本数: {ernie_stats['execution_success']}")
print(f"检查项18 - 合格: {ernie_stats['check18_passed']}")
print(f"检查项18 - 不合格: {ernie_stats['check18_failed']}")
print(f"通过率: {ernie_stats['pass_rate']:.1f}%")

print("\n" + "=" * 120)
print(f"【Claude Opus 4.5 - 通过案例分析】（共{len(claude_stats['passed_cases'])}个，展示前3个）")
print("=" * 120)

for i, case in enumerate(claude_stats['passed_cases'][:3], 1):
    print(f"\n✅ 案例 {i}: {case['sample_id']}")
    print(f"原因: {case['reason']}")
    print(f"详情（前800字）:\n{case['details']}")
    print("-" * 120)

print("\n" + "=" * 120)
print(f"【Ernie 5.0 - 失败案例分析】（共{len(ernie_stats['failed_cases'])}个，展示前2个）")
print("=" * 120)

for i, case in enumerate(ernie_stats['failed_cases'][:2], 1):
    print(f"\n❌ 案例 {i}: {case['sample_id']}")
    print(f"原因: {case['reason']}")
    print(f"详情（前800字）:\n{case['details']}")
    print("-" * 120)
