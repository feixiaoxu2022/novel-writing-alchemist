#!/usr/bin/env python3
"""
从现有样本文件中提取 checklist，生成初始 revision。
这是一次性脚本，用于从现有的 eval_dsv2.jsonl 初始化 check_revisions 体系。
"""
import json
import sys
from pathlib import Path


def extract_checklists(samples_file: Path, output_file: Path):
    """从样本文件中提取每条样本的 data_id + check_list，输出为 checklist.jsonl"""
    count = 0
    with open(samples_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            sample = json.loads(line)
            entry = {
                "data_id": sample["data_id"],
                "check_list": sample["check_list"]
            }
            fout.write(json.dumps(entry, ensure_ascii=False) + '\n')
            count += 1
    return count


def main():
    base_dir = Path(__file__).resolve().parent.parent
    samples_file = base_dir / "samples" / "eval_dsv2.jsonl"
    output_file = Path(__file__).resolve().parent / "rev_001" / "checklist.jsonl"

    if not samples_file.exists():
        print(f"错误: 样本文件不存在: {samples_file}")
        return 1

    output_file.parent.mkdir(parents=True, exist_ok=True)
    count = extract_checklists(samples_file, output_file)
    print(f"✓ 从 {samples_file.name} 提取 {count} 条 checklist → {output_file}")

    # 统计检查项数量
    with open(output_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            check_count = len(entry["check_list"])
            print(f"  {entry['data_id']}: {check_count} checks")
            break  # 只看第一条作为示例

    return 0


if __name__ == "__main__":
    sys.exit(main())
