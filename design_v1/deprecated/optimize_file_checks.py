#!/usr/bin/env python3
"""
优化文件存在性检查：
1. 基础4文件已在common_16，从模板check_01中移除
2. 需要writing_log.md的long/ultra_long模板：修改check_01只检查writing_log.md
3. 不需要writing_log.md的模板：完全删除check_01
"""

import yaml
import sys

# 需要writing_log.md的模板（>8000字的任务）
TEMPLATES_NEED_WRITING_LOG = [
    'NW_CLEAR_LONG_ANGSTY',
    'NW_IP_LONG_NEUTRAL',
    'NW_IP_ULTRA_LONG_NEUTRAL'
]


def optimize_template_checks(template):
    """优化单个模板的文件检查"""
    template_id = template.get('need_template_id')
    check_list = template.get('check_list', [])

    # 找到check_01（必需文件存在性）
    check_01_idx = None
    for idx, item in enumerate(check_list):
        check_id = item.get('check_id', '')
        if 'check_01' in check_id or '必需文件' in item.get('check_name', ''):
            check_01_idx = idx
            break

    if check_01_idx is None:
        print(f"  {template_id}: No file existence check found, skipping")
        return check_list

    # 决定如何处理
    if template_id in TEMPLATES_NEED_WRITING_LOG:
        # 修改check_01只检查writing_log.md
        check_list[check_01_idx] = {
            'check_id': 'check_01_writing_log存在',
            'check_name': 'writing_log.md必须存在',
            'dimension_id': 'format_compliance',
            'subcategory_id': 'structural_integrity',
            'check_type': 'entity_attribute_equals',
            'params': {
                'workspace_path': '.',
                'required_files': ['writing_log.md']
            },
            'weight': 1.0,
            'is_critical': True
        }
        print(f"  {template_id}: Modified check_01 to only check writing_log.md")
    else:
        # 删除check_01
        del check_list[check_01_idx]
        print(f"  {template_id}: Removed check_01 (base files now in common_16)")

        # 重新编号剩余的check_id
        for idx, item in enumerate(check_list, 1):
            old_check_id = item.get('check_id', '')
            if '_' in old_check_id:
                parts = old_check_id.split('_')
                if len(parts) >= 3:
                    suffix = '_'.join(parts[2:])
                    item['check_id'] = f"check_{idx:02d}_{suffix}"
                else:
                    item['check_id'] = f"check_{idx:02d}"

    return check_list


def main():
    yaml_file = 'unified_scenario_design.yaml'

    print(f"Loading {yaml_file}...")
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    templates = data.get('user_need_templates', [])
    print(f"Found {len(templates)} templates\n")

    # 优化每个模板
    for template in templates:
        template['check_list'] = optimize_template_checks(template)

    # 保存回文件
    print(f"\nSaving optimized YAML to {yaml_file}...")
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=1000)

    print("✓ Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
