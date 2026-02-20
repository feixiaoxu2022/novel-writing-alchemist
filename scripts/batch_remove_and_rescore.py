#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量从 check_result_rev008.json 中删除 workspace_file_compliance 检查项并重新打分。

用法:
    python scripts/batch_remove_and_rescore.py --eval-dir evaluation_outputs --revision 008
    python scripts/batch_remove_and_rescore.py --eval-dir evaluation_outputs --revision 008 --dry-run
"""

import json
import sys
import argparse
from pathlib import Path

# 添加 env/ 到路径，以便导入 checker_score
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "env"))
from checker_score import calculate_scores


def process_one_file(filepath: Path, subcategory_to_remove: str, dry_run: bool = False) -> dict:
    """
    处理单个 check_result 文件：删除指定 subcategory 的检查项，重新打分。
    
    Returns:
        {"path": str, "removed_keys": list, "old_score": float, "new_score": float}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    check_details = data.get("check_details", {})
    old_score = data.get("overall_result", {}).get("total_score", None)
    
    # 找到要删除的key
    keys_to_remove = []
    for key, item in check_details.items():
        if isinstance(item, dict) and item.get("subcategory_id") == subcategory_to_remove:
            keys_to_remove.append(key)
    
    if not keys_to_remove:
        return {
            "path": str(filepath),
            "removed_keys": [],
            "old_score": old_score,
            "new_score": old_score,
            "changed": False
        }
    
    # 删除
    for key in keys_to_remove:
        del check_details[key]
    
    # 重新打分
    execution_result = {
        "sample_id": data.get("sample_id", "unknown"),
        "check_timestamp": data.get("check_timestamp"),
        "check_details": check_details
    }
    new_result = calculate_scores(execution_result)
    new_score = new_result.get("overall_result", {}).get("total_score", None)
    
    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(new_result, f, ensure_ascii=False, indent=2)
    
    return {
        "path": str(filepath),
        "removed_keys": keys_to_remove,
        "old_score": old_score,
        "new_score": new_score,
        "changed": True
    }


def main():
    parser = argparse.ArgumentParser(description="批量删除检查项并重新打分")
    parser.add_argument("--eval-dir", required=True, help="evaluation_outputs 目录")
    parser.add_argument("--revision", default="008", help="修订版本号（默认 008）")
    parser.add_argument("--subcategory", default="workspace_file_compliance",
                        help="要删除的 subcategory_id")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入文件")
    args = parser.parse_args()
    
    eval_dir = Path(args.eval_dir)
    if not eval_dir.exists():
        print(f"[错误] 目录不存在: {eval_dir}")
        sys.exit(1)
    
    # 查找所有 check_result_revXXX.json 文件
    pattern = f"check_result_rev{args.revision}.json"
    files = sorted(eval_dir.rglob(pattern))
    
    if not files:
        print(f"[警告] 未找到匹配文件: {pattern}")
        sys.exit(1)
    
    print(f"[开始] 找到 {len(files)} 个文件")
    print(f"[配置] 删除 subcategory_id = '{args.subcategory}'")
    if args.dry_run:
        print("[模式] DRY RUN — 不会修改文件")
    print()
    
    changed_count = 0
    unchanged_count = 0
    score_diffs = []
    
    for filepath in files:
        result = process_one_file(filepath, args.subcategory, dry_run=args.dry_run)
        
        if result["changed"]:
            changed_count += 1
            diff = (result["new_score"] or 0) - (result["old_score"] or 0)
            score_diffs.append(diff)
            short_path = filepath.relative_to(eval_dir)
            print(f"  [改] {short_path}: 删除 {result['removed_keys']}, "
                  f"分数 {result['old_score']:.1f} → {result['new_score']:.1f} ({diff:+.1f})")
        else:
            unchanged_count += 1
    
    print(f"\n[完成] 已处理 {len(files)} 个文件")
    print(f"  - 有变更: {changed_count}")
    print(f"  - 无变更: {unchanged_count}")
    if score_diffs:
        avg_diff = sum(score_diffs) / len(score_diffs)
        print(f"  - 平均分数变化: {avg_diff:+.2f}")
        print(f"  - 分数变化范围: {min(score_diffs):+.2f} ~ {max(score_diffs):+.2f}")


if __name__ == "__main__":
    main()
