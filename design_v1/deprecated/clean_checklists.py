#!/usr/bin/env python3
"""
批量清理unified_scenario_design.yaml中所有模板的重复检查项
删除与common_check_list重复的4项：配方选择交互、写作准备确认、主题一致性、语言纯净性
"""

import yaml
import sys

def clean_template_checklist(template):
    """清理单个模板的check_list，删除重复项"""
    check_list = template.get('check_list', [])

    # 要删除的重复项（根据check_name或subcategory_id判断）
    duplicates_to_remove_names = [
        '配方选择阶段HITL调用',
        '写作准备阶段HITL调用',
        '故事主题一致',
        '无不合理的多语言混用'
    ]

    duplicates_to_remove_subcategories = [
        'confirmation_nodes',  # HITL交互相关
        'theme_consistency',   # 主题一致性
        'language_purity'      # 语言纯净性
    ]

    # 过滤掉重复项
    cleaned = []
    removed_count = 0
    for item in check_list:
        check_name = item.get('check_name', '')
        subcategory_id = item.get('subcategory_id', '')

        # 判断是否是重复项
        is_duplicate = (
            check_name in duplicates_to_remove_names or
            subcategory_id in duplicates_to_remove_subcategories
        )

        if not is_duplicate:
            cleaned.append(item)
        else:
            removed_count += 1
            print(f"    - Removing: {check_name} ({subcategory_id})")

    # 重新编号check_id
    for idx, item in enumerate(cleaned, 1):
        old_check_id = item.get('check_id', '')
        # 保留原check_id的后缀部分（如果有）
        if '_' in old_check_id:
            parts = old_check_id.split('_')
            if len(parts) >= 3:  # check_NN_xxx格式
                suffix = '_'.join(parts[2:])
                item['check_id'] = f"check_{idx:02d}_{suffix}"
            else:
                item['check_id'] = f"check_{idx:02d}"
        else:
            item['check_id'] = f"check_{idx:02d}"

    return cleaned


def main():
    yaml_file = 'unified_scenario_design.yaml'

    print(f"Loading {yaml_file}...")
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    templates = data.get('user_need_templates', [])
    print(f"Found {len(templates)} templates")

    # 清理每个模板
    for template in templates:
        template_id = template.get('need_template_id')
        original_count = len(template.get('check_list', []))

        # 清理check_list
        cleaned_list = clean_template_checklist(template)
        template['check_list'] = cleaned_list

        new_count = len(cleaned_list)
        print(f"  {template_id}: {original_count} → {new_count} checks")

    # 保存回文件
    print(f"\nSaving cleaned YAML to {yaml_file}...")
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=1000)

    print("✓ Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
