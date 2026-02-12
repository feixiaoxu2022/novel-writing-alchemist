#!/usr/bin/env python3
"""
统一check_id为中文，保持整体风格一致
"""

import yaml
import sys
import re


# 英文到中文的映射（按长度排序，优先匹配长词）
TRANSLATION_MAP = {
    'creative_intent_schema': 'creative_intent格式',
    'characters_schema': 'characters格式',
    'outline_schema': 'outline格式',
    'ultra_long': '超长篇',  # 必须在 long 之前
    'ultra_short': '超短篇',  # 必须在 short 之前
    'writing_log': '创作日志',
    'medium': '中篇',
    'short': '短篇',
    'long': '长篇',
}


def normalize_check_id(check_id):
    """
    统一check_id为中文

    Examples:
        creative_intent_schema → creative_intent格式
        ultra_short字数 → 超短篇字数
        writing_log存在 → 创作日志存在
    """
    # 替换英文部分为中文
    for en, zh in TRANSLATION_MAP.items():
        if en in check_id:
            check_id = check_id.replace(en, zh)

    return check_id


def normalize_checklist(check_list):
    """统一check_list中的所有check_id为中文"""
    for item in check_list:
        if 'check_id' in item:
            original = item['check_id']
            normalized = normalize_check_id(original)
            if original != normalized:
                item['check_id'] = normalized
                print(f"  {original} → {normalized}")


def main():
    yaml_file = 'unified_scenario_design.yaml'

    print(f"Loading {yaml_file}...")
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 统一common_check_list
    print("\n统一 common_check_list:")
    common_checks = data.get('common_check_list', {}).get('checks', [])
    normalize_checklist(common_checks)

    # 统一所有模板的check_list
    print("\n统一模板 check_list:")
    for template in data.get('user_need_templates', []):
        template_id = template.get('need_template_id')
        check_list = template.get('check_list', [])

        if check_list:
            print(f"\n{template_id}:")
            normalize_checklist(check_list)

    # 保存回文件
    print(f"\n保存统一后的YAML到 {yaml_file}...")
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=1000)

    print("✓ Done! 所有check_id已统一为中文")
    return 0


if __name__ == '__main__':
    sys.exit(main())
