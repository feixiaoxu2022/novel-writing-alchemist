#!/usr/bin/env python3
"""
清理unified_scenario_design.yaml中的check_id，去掉数字编号前缀，只保留语义化名称
"""

import yaml
import sys
import re


def cleanup_check_id(check_id):
    """
    清理check_id，去掉数字编号前缀

    Examples:
        check_01_02_反应强度虐心 → 反应强度虐心
        check_02_03_ultra_short字数 → ultra_short字数
        check_03_04_情感交付虐心 → 情感交付虐心
        check_01_writing_log存在 → writing_log存在
        common_01_章节命名格式 → 章节命名格式 (common保留作为标识)
    """
    # 如果是common开头，去掉common_XX_前缀，保留common标识
    if check_id.startswith('common_'):
        # common_01_章节命名格式 → 章节命名格式
        return re.sub(r'^common_\d+_', '', check_id)

    # 其他情况：去掉所有check_XX_前缀和check_XX_YY_前缀
    # check_01_02_反应强度虐心 → 反应强度虐心
    # check_01_writing_log存在 → writing_log存在
    return re.sub(r'^check_\d+(_\d+)?_', '', check_id)


def cleanup_checklist(check_list):
    """清理check_list中的所有check_id"""
    for item in check_list:
        if 'check_id' in item:
            original = item['check_id']
            cleaned = cleanup_check_id(original)
            item['check_id'] = cleaned
            print(f"  {original} → {cleaned}")


def main():
    yaml_file = 'unified_scenario_design.yaml'

    print(f"Loading {yaml_file}...")
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 清理common_check_list
    print("\n清理 common_check_list:")
    common_checks = data.get('common_check_list', {}).get('checks', [])
    cleanup_checklist(common_checks)

    # 清理所有模板的check_list
    print("\n清理模板 check_list:")
    for template in data.get('user_need_templates', []):
        template_id = template.get('need_template_id')
        check_list = template.get('check_list', [])

        if check_list:
            print(f"\n{template_id}:")
            cleanup_checklist(check_list)

    # 保存回文件
    print(f"\n保存清理后的YAML到 {yaml_file}...")
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=1000)

    print("✓ Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
