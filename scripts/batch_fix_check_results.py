#!/usr/bin/env python3
"""
批量修复check_result_rev003.json中的两个问题：

1. 检查项1-5（读取v2新增skill文件）：
   - 对于v1样本（环境里没有这些文件），把fail改成skip
   - 检查环境中是否存在对应文件来判断

2. 检查项33（late_stage_digression）：
   - 如果失败原因是".hitl_context.json"被当作额外文件，改成pass
"""

import json
import os
from pathlib import Path

# v2新增的5个skill文件
V2_SKILL_FILES = [
    "data_pools/skills/RECIPE_KNOWLEDGE.md",
    "data_pools/skills/CHARACTER_DESIGN_GUIDE.md", 
    "data_pools/skills/OUTLINE_DESIGN_GUIDE.md",
    "data_pools/skills/WRITING_TECHNIQUE_GUIDE.md",
    "data_pools/skills/CONSISTENCY_MANAGEMENT_GUIDE.md",
]

def fix_check_result(check_result_path: Path):
    """修复单个check_result文件"""
    env_dir = check_result_path.parent
    
    with open(check_result_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    check_details = data.get("check_details", {})
    
    # 修复1: 检查项1-5（skill文件读取）
    for i in range(1, 6):
        check_key = f"检查项{i}"
        if check_key not in check_details:
            continue
            
        check_item = check_details[check_key]
        
        # 只处理fail的情况
        if check_item.get("check_result") != "fail":
            continue
            
        # 检查是否是skill reading相关
        if check_item.get("subcategory_id") != "required_skill_reading":
            continue
            
        # 检查环境中是否存在对应的skill文件
        skill_file = V2_SKILL_FILES[i-1] if i <= len(V2_SKILL_FILES) else None
        if skill_file:
            full_path = env_dir / skill_file
            if not full_path.exists():
                # 文件不存在，改成skip
                check_item["check_result"] = "skip"
                check_item["reason"] = "环境中不存在该文件（批量修复）"
                check_item["details"] = f"文件 {skill_file} 在当前环境中不存在，跳过此检查项"
                modified = True
                print(f"  {check_key}: fail -> skip (文件不存在)")
    
    # 修复2: 检查项33（late_stage_digression）
    check_33 = check_details.get("检查项33", {})
    if check_33.get("check_result") == "fail":
        details = check_33.get("details", "")
        # 检查是否是因为.hitl_context.json被当作额外文件
        if ".hitl_context.json" in details and "额外" in details:
            # 解析details，检查是否只有.hitl_context.json是额外文件
            # details格式: "白名单: [...]; 实际: [...]; 额外: ['.hitl_context.json']"
            if "额外: ['.hitl_context.json']" in details:
                check_33["check_result"] = "pass"
                check_33["reason"] = "workspace中只有允许的文件（批量修复：.hitl_context.json已加入白名单）"
                check_33["details"] = details.replace("额外: ['.hitl_context.json']", "额外: []（.hitl_context.json已加入白名单）")
                modified = True
                print(f"  检查项33: fail -> pass (.hitl_context.json白名单)")
    
    if modified:
        # 重新计算统计数据
        recalculate_stats(data)
        
        with open(check_result_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    return False

def recalculate_stats(data):
    """重新计算overall_result和dimension_scores"""
    check_details = data.get("check_details", {})
    
    # 统计各维度
    dimension_stats = {}
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    
    for check_key, check_item in check_details.items():
        result = check_item.get("check_result", "")
        dimension_id = check_item.get("dimension_id", "unknown")
        
        if dimension_id not in dimension_stats:
            dimension_stats[dimension_id] = {"passed": 0, "failed": 0, "skipped": 0, "total": 0}
        
        dimension_stats[dimension_id]["total"] += 1
        
        if result == "pass":
            dimension_stats[dimension_id]["passed"] += 1
            total_passed += 1
        elif result == "fail":
            dimension_stats[dimension_id]["failed"] += 1
            total_failed += 1
        elif result == "skip":
            dimension_stats[dimension_id]["skipped"] += 1
            total_skipped += 1
    
    # 更新dimension_scores
    for dim_id, stats in dimension_stats.items():
        if dim_id in data.get("dimension_scores", {}):
            dim_data = data["dimension_scores"][dim_id]
            # 对于content_quality，结构不同
            if dim_id == "content_quality" and "basic_layer" in dim_data:
                # content_quality有nested结构，跳过简单更新
                pass
            else:
                dim_data["total"] = stats["total"]
                dim_data["passed"] = stats["passed"]
                dim_data["failed"] = stats["failed"]
                dim_data["skipped"] = stats["skipped"]
                
                # 重新计算pass_rate和score
                effective_total = stats["total"] - stats["skipped"]
                if effective_total > 0:
                    dim_data["pass_rate"] = round(stats["passed"] / effective_total, 3)
                    dim_data["score"] = round(stats["passed"] / effective_total * 100, 2)
                else:
                    dim_data["pass_rate"] = 1.0
                    dim_data["score"] = 100.0
                
                # 更新failed_items
                failed_items = []
                for check_key, check_item in check_details.items():
                    if check_item.get("dimension_id") == dim_id and check_item.get("check_result") == "fail":
                        failed_items.append(check_key)
                dim_data["failed_items"] = failed_items
    
    # 更新overall_result
    total_checks = total_passed + total_failed + total_skipped
    effective_total = total_passed + total_failed  # skip的不计入
    
    data["overall_result"]["total_checks"] = total_checks
    data["overall_result"]["passed_checks"] = total_passed
    data["overall_result"]["failed_checks"] = total_failed
    if effective_total > 0:
        data["overall_result"]["pass_rate"] = round(total_passed / effective_total, 3)
    else:
        data["overall_result"]["pass_rate"] = 1.0


def main():
    base_dir = Path(__file__).parent.parent / "evaluation_outputs"
    
    # 找到所有check_result_rev003.json文件
    check_files = list(base_dir.glob("**/check_result_rev003.json"))
    
    print(f"找到 {len(check_files)} 个check_result_rev003.json文件")
    print("=" * 60)
    
    fixed_count = 0
    for check_file in check_files:
        print(f"\n处理: {check_file.relative_to(base_dir)}")
        if fix_check_result(check_file):
            fixed_count += 1
    
    print("\n" + "=" * 60)
    print(f"完成！修复了 {fixed_count}/{len(check_files)} 个文件")


if __name__ == "__main__":
    main()
