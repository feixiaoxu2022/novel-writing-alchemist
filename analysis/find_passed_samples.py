#!/usr/bin/env python3
import json
from pathlib import Path

# 找出检查项19通过的样本
eval_dir = Path('/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/tmp_scenarios/novel_writing_alchemist/evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101')

for result_file in eval_dir.glob('*/check_result_v3.json'):
    with open(result_file) as f:
        data = json.load(f)
        check19 = data['check_details'].get('检查项19', {})
        if check19.get('检查结论') == '合格':
            sample_id = data.get('sample_id', 'unknown')
            print(f'找到通过的样本: {sample_id}')
            print(f'文件路径: {result_file}')
            break
