#!/usr/bin/env python3
"""
从 check_revisions 的 checklist.jsonl 中提取指定 data_id 的 bench 数据。
配合 recheck_with_new_checklist.sh 的 --revision 模式使用。

与 extract_bench_from_sample.py 的区别：
- extract_bench_from_sample.py: 从完整样本 jsonl 中提取（包含 query, system, environment 等所有字段）
- 本脚本: 从精简的 checklist.jsonl 中提取（只有 data_id + check_list），
  judge_criteria 从 revision 目录单独部署
"""
import json
import sys
import os
import shutil
import argparse


def deploy_criteria_files(criteria_dir, env_dir):
    """将 revision 的 judge_criteria 文件部署到 _env 目录

    Args:
        criteria_dir: revision 下的 judge_criteria/ 目录
        env_dir: 评测结果的 _env 目录
    Returns:
        deployed_count: 部署的文件数
    """
    if not os.path.isdir(criteria_dir):
        return 0

    deployed_count = 0
    dst_criteria = os.path.join(env_dir, "judge_criteria")
    os.makedirs(dst_criteria, exist_ok=True)

    for filename in os.listdir(criteria_dir):
        src = os.path.join(criteria_dir, filename)
        dst = os.path.join(dst_criteria, filename)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            deployed_count += 1

    return deployed_count


def extract_bench(checklist_file, data_id, output_file, criteria_dir=None, env_dir=None):
    """从 checklist.jsonl 中提取指定 data_id 的 bench 数据

    Args:
        checklist_file: checklist.jsonl 文件路径
        data_id: 要提取的 data_id
        output_file: 输出 bench.json 路径
        criteria_dir: 可选，revision 的 judge_criteria/ 目录
        env_dir: 可选，部署 criteria 的目标 _env 目录
    """
    try:
        # 先加载所有条目，建立索引
        entries = {}
        with open(checklist_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                entries[entry.get('data_id')] = entry

        # 精确匹配
        matched_entry = entries.get(data_id)

        # Fallback: 同模板的 _001（如 NW_CLEAR_SHORT_ANGSTY_002 -> NW_CLEAR_SHORT_ANGSTY_001）
        if not matched_entry:
            import re
            m = re.match(r'^(.+)_\d{3}$', data_id)
            if m:
                fallback_id = f"{m.group(1)}_001"
                matched_entry = entries.get(fallback_id)
                if matched_entry:
                    print(f'⚠️  未找到 {data_id}，使用同模板 fallback: {fallback_id}',
                          file=sys.stderr)

        if matched_entry:
            # 构造 bench.json（checker.py 需要的格式）
            # 注意：revision 模式下没有 environment 字段（criteria 通过文件部署）
            bench = {
                'data_id': data_id,  # 使用原始 data_id，不是 fallback 的
                'check_list': matched_entry['check_list'],
                'environment': [],  # revision 模式不通过 environment 传递文件
            }

            with open(output_file, 'w', encoding='utf-8') as out:
                json.dump(bench, out, ensure_ascii=True, indent=2)

            print(f'✓ 成功提取 {data_id} 的 checklist '
                  f'({len(matched_entry["check_list"])} checks)', file=sys.stderr)

            # 部署 judge_criteria 文件到 _env 目录
            if criteria_dir and env_dir:
                deployed = deploy_criteria_files(criteria_dir, env_dir)
                if deployed > 0:
                    print(f'✓ 已部署 {deployed} 个 judge_criteria 文件到 {env_dir}',
                          file=sys.stderr)

            return 0

        print(f'错误: 未找到 data_id={data_id} 的 checklist（也无同模板 fallback）',
              file=sys.stderr)
        return 1

    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='从 checklist.jsonl 提取 bench 数据（revision 模式）')
    parser.add_argument('--checklist', required=True,
                        help='checklist.jsonl 文件路径')
    parser.add_argument('--data-id', required=True,
                        help='要提取的 data_id')
    parser.add_argument('--output', required=True,
                        help='输出 bench.json 路径')
    parser.add_argument('--deploy-criteria-dir', default=None,
                        help='revision 的 judge_criteria/ 目录')
    parser.add_argument('--env-dir', default=None,
                        help='部署 criteria 的目标 _env 目录')

    args = parser.parse_args()
    return extract_bench(
        args.checklist, args.data_id, args.output,
        criteria_dir=args.deploy_criteria_dir,
        env_dir=args.env_dir
    )


if __name__ == '__main__':
    sys.exit(main())
