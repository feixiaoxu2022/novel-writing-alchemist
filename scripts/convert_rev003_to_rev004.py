#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rev003 → rev004 检查结果转换脚本

将已有的 check_result_rev003.json 转换为 check_result_rev004.json，
复用1-32项（完全一致）的结果，对33项之后按映射关系重新编号。

映射关系：
  rev003 1-32  → rev004 1-32   (直接复用)
  rev003 33    → 丢弃          (rev003是semantic复合检查，rev004拆分为33+34)
  rev003 34    → rev004 35     (character_presence_in_outline)
  rev003 35    → rev004 36     (character_presence_in_chapters)
  rev003 36    → rev004 37     (writing_log exists)
  rev003 37    → rev004 38     (read writing_log)
  rev003 38    → rev004 39     (字数范围)
  rev003 39    → rev004 40     (情感基调)
  rev003 40    → rev004 41     (条件性读取，如SHORT_STORY_GUIDE)

需要新跑的项：
  rev004 33    (file_whitelist_check, 不需要LLM)
  rev004 34    (late_stage_digression, 需要LLM)
  rev004 42    (文笔风格, 需要LLM)

用法：
  python3 convert_rev003_to_rev004.py --eval-dir <eval目录>
  python3 convert_rev003_to_rev004.py --eval-dir evaluation_outputs/eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat

转换后：
  - 生成 check_result_rev004.json（包含映射后的1-32 + 35-41项，33/34/42留空）
  - 然后用 recheck 的 --only-checks 33,34,42 补跑缺失项
"""

import json
import argparse
import os
import glob
import time
from pathlib import Path


# rev003 → rev004 的映射表
# key = rev003 序号, value = rev004 序号
MAPPING = {
    # 1-32: 直接映射
    **{i: i for i in range(1, 33)},
    # 33: 丢弃（rev003 的复合检查在 rev004 中被拆分）
    # 34-40: 各偏移一位
    34: 35,  # character_presence_in_outline
    35: 36,  # character_presence_in_chapters
    36: 37,  # writing_log exists
    37: 38,  # read writing_log
    38: 39,  # 字数范围
    39: 40,  # 情感基调
    40: 41,  # 条件性读取
}


def convert_single(env_dir: str, dry_run: bool = False) -> bool:
    """转换单个样本的 check_result"""
    rev003_path = os.path.join(env_dir, 'check_result_rev003.json')
    rev004_path = os.path.join(env_dir, 'check_result_rev004.json')
    
    if not os.path.exists(rev003_path):
        return False
    
    # 如果已有 rev004 结果，跳过
    if os.path.exists(rev004_path):
        print(f'  跳过（已有rev004）: {os.path.basename(env_dir)}')
        return True
    
    with open(rev003_path, 'r', encoding='utf-8') as f:
        rev003 = json.load(f)
    
    old_details = rev003.get('check_details', {})
    new_details = {}
    
    mapped_count = 0
    skipped_count = 0
    
    for old_key, old_value in old_details.items():
        old_num = int(old_key.replace('检查项', ''))
        
        if old_num in MAPPING:
            new_num = MAPPING[old_num]
            new_key = f'检查项{new_num}'
            new_details[new_key] = old_value
            mapped_count += 1
        else:
            # rev003 的 33 项（复合检查）被丢弃
            skipped_count += 1
    
    if dry_run:
        print(f'  [DRY RUN] {os.path.basename(env_dir)}: 映射{mapped_count}项, 丢弃{skipped_count}项')
        return True
    
    # 构建 rev004 结果（先只含映射的项，分数稍后重算）
    rev004 = {
        'check_version': rev003.get('check_version', 'novel_writing_v1.0'),
        'sample_id': rev003.get('sample_id', 'unknown'),
        'check_timestamp': int(time.time()),
        'dimension_scores': {},  # 先空着，后续 rerun 时会重算
        'overall_result': {},    # 先空着
        'check_details': new_details,
        'completion_status': 'partial_converted',
        'conversion_note': f'从rev003转换，映射{mapped_count}项，丢弃{skipped_count}项，待补跑: 33,34,42'
    }
    
    with open(rev004_path, 'w', encoding='utf-8') as f:
        json.dump(rev004, f, ensure_ascii=False, indent=2)
    
    print(f'  ✅ {os.path.basename(env_dir)}: 映射{mapped_count}项, 丢弃{skipped_count}项 → check_result_rev004.json')
    return True


def main():
    parser = argparse.ArgumentParser(description='rev003 → rev004 检查结果转换')
    parser.add_argument('--eval-dir', required=True, help='评测输出目录')
    parser.add_argument('--dry-run', action='store_true', help='只显示计划，不实际转换')
    args = parser.parse_args()
    
    eval_dir = args.eval_dir
    if not os.path.isdir(eval_dir):
        print(f'错误: 目录不存在: {eval_dir}')
        return
    
    # 找所有有 rev003 结果的 env 目录
    env_dirs = sorted(glob.glob(os.path.join(eval_dir, 'NW_*_env')))
    
    print(f'目录: {os.path.basename(eval_dir)}')
    print(f'找到 {len(env_dirs)} 个样本目录')
    print()
    
    converted = 0
    skipped = 0
    no_rev003 = 0
    
    for env_dir_path in env_dirs:
        if not os.path.isdir(env_dir_path):
            continue
        
        rev003_exists = os.path.exists(os.path.join(env_dir_path, 'check_result_rev003.json'))
        if not rev003_exists:
            print(f'  ⚠️  无rev003: {os.path.basename(env_dir_path)}')
            no_rev003 += 1
            continue
        
        if convert_single(env_dir_path, args.dry_run):
            converted += 1
    
    print()
    print(f'完成: 转换{converted}个, 无rev003 {no_rev003}个')
    
    if not args.dry_run and converted > 0:
        print()
        print('下一步: 补跑缺失的检查项 33(file_whitelist), 34(late_stage_digression), 42(文笔风格)')
        print(f'  ./scripts/recheck_with_new_checklist.sh \\')
        print(f'    --agent-results {eval_dir} \\')
        print(f'    --revision 004 \\')
        print(f'    --only-checks 33,34,42')


if __name__ == '__main__':
    main()
