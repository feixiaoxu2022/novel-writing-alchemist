#!/usr/bin/env python3
"""检查各模型的实际执行情况"""

import json
from pathlib import Path

evaluation_outputs_dir = Path('/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs')

eval_dirs = [d for d in evaluation_outputs_dir.iterdir() if d.is_dir() and d.name.startswith('eval_v2_')]

for eval_dir in eval_dirs:
    model_name = '_'.join(eval_dir.name.split('_')[4:])
    print(f"\n{'='*80}")
    print(f"模型: {model_name}")
    print('='*80)

    # 统计所有样本目录
    env_dirs = [d for d in eval_dir.iterdir() if d.is_dir() and d.name.endswith('_env')]
    total_samples = len(env_dirs)

    completed = 0
    failed = 0
    no_check_result = 0
    poor_quality = 0

    failed_samples = []
    no_result_samples = []
    poor_samples = []

    for env_dir in env_dirs:
        sample_name = env_dir.name.replace('_env', '')

        # 查找check_result文件
        check_result_file = env_dir / 'check_result_v3.json'
        if not check_result_file.exists():
            check_result_file = env_dir / 'check_resultv3.json'

        if check_result_file.exists():
            with open(check_result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                completion_status = result.get('completion_status', 'unknown')
                overall_result = result.get('overall_result', {})
                overall_status = overall_result.get('status', 'unknown')
                total_score = overall_result.get('total_score', 0)

                if completion_status == 'completed':
                    completed += 1
                    # 检查质量状态
                    if overall_status == 'Poor':
                        poor_quality += 1
                        poor_samples.append(f"{sample_name} (score: {total_score:.2f})")
                else:
                    failed += 1
                    failed_samples.append(f"{sample_name} (status: {completion_status})")
        else:
            no_check_result += 1
            no_result_samples.append(sample_name)

    print(f"总样本数: {total_samples}")
    print(f"执行成功 (completed): {completed}")
    print(f"  - 其中Poor质量: {poor_quality}")
    print(f"执行失败 (有check_result但status!=completed): {failed}")
    print(f"无check_result文件: {no_check_result}")
    print(f"\n有效样本数（用于统计）: {completed}")

    if poor_samples:
        print(f"\nPoor质量的样本（可能是Agent执行失败）:")
        for s in poor_samples:
            print(f"  - {s}")

    if failed_samples:
        print(f"\n执行失败的样本:")
        for s in failed_samples:
            print(f"  - {s}")

    if no_result_samples:
        print(f"\n无check_result文件的样本:")
        for s in no_result_samples:
            print(f"  - {s}")
