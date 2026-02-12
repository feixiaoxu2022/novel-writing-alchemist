#!/usr/bin/env python3
"""为缺少check_name的check items添加check_name"""

import yaml
from pathlib import Path

# check_id到check_name的映射
check_name_mapping = {
    'check_01_交互完整性': '交互完整性检查',
    'check_02_反应强度虐心': 'reaction_strength必须为↘（虐心向）',
    'check_03_短篇字数': '总字数应在15000-40000之间',
    'check_01_反应强度虐心': 'reaction_strength必须为↘（虐心向）',
    'check_02_中篇字数': '总字数应在80000-250000之间',
    'check_01_反应强度烧脑': 'reaction_strength必须为✷（烧脑向）',
    'check_01_中篇字数': '总字数应在80000-250000之间',
    'check_02_长篇字数': '总字数应在400000-600000之间',
    'check_01_长篇字数': '总字数应在400000-600000之间',
    'check_02_必需文件含log': '必需文件存在性（含writing_log.md）',
    'check_03_超长篇字数': '总字数应在1000000-3000000之间',
    'check_04_世界观支撑质量': '世界观深度和一致性质量',
}

def fix_check_names(yaml_path):
    """添加缺失的check_name"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    modified_count = 0

    for template in data['user_need_templates']:
        template_id = template['need_template_id']
        check_list = template.get('check_list', [])

        for check_item in check_list:
            check_id = check_item.get('check_id', '')

            # 如果缺少check_name但check_id在映射中
            if 'check_name' not in check_item and check_id in check_name_mapping:
                check_item['check_name'] = check_name_mapping[check_id]
                modified_count += 1
                print(f"[{template_id}] Added check_name for {check_id}: {check_name_mapping[check_id]}")

    # 保存修改
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

    print(f"\n✓ Modified {modified_count} check items")

if __name__ == "__main__":
    yaml_path = Path("unified_scenario_design.yaml")
    fix_check_names(yaml_path)
