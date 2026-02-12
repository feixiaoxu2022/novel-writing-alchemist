#!/usr/bin/env python3
import yaml

with open('unified_scenario_design.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

templates_need_log = []
for template in data['user_need_templates']:
    word_count = template.get('word_count')
    template_id = template.get('need_template_id')

    # 判断是否需要writing_log
    if word_count in ['short', 'medium', 'long', 'ultra_long']:
        check_list = template.get('check_list', [])

        has_creation = any(c.get('subcategory_id') == 'log_file_creation' for c in check_list)
        has_usage = any(c.get('subcategory_id') == 'log_file_usage' for c in check_list)

        templates_need_log.append({
            'template_id': template_id,
            'word_count': word_count,
            'has_creation': has_creation,
            'has_usage': has_usage
        })

print('需要writing_log的模板检查（>8000字）：\n')
header = f"{'模板ID':<35} | {'创建检查':<10} | {'读取检查':<10} | 状态"
print(header)
print('-' * 80)

all_complete = True
for t in templates_need_log:
    creation = '✓ 有' if t['has_creation'] else '✗ 无'
    usage = '✓ 有' if t['has_usage'] else '✗ 无'
    status = '✓ 完整' if (t['has_creation'] and t['has_usage']) else '✗ 缺失'

    if not (t['has_creation'] and t['has_usage']):
        all_complete = False

    row = f"{t['template_id']:<35} | {creation:<10} | {usage:<10} | {status}"
    print(row)

print()
if all_complete:
    print('✅ 所有需要writing_log的模板都已完整配置！')
else:
    print('⚠️  仍有模板缺失检查项！')
