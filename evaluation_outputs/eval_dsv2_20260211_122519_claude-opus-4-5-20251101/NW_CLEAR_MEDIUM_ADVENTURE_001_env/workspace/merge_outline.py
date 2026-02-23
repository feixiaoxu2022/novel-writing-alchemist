import json

# 读取第一幕
with open('outline.json', 'r', encoding='utf-8') as f:
    outline = json.load(f)

# 读取第二幕
with open('temp_act_two.json', 'r', encoding='utf-8') as f:
    act_two = json.load(f)

# 读取第三幕
with open('temp_act_three.json', 'r', encoding='utf-8') as f:
    act_three_p1 = json.load(f)

with open('temp_act_three_part2.json', 'r', encoding='utf-8') as f:
    act_three_p2 = json.load(f)

# 整合第二幕
outline['act_two'] = act_two

# 整合第三幕
act_three = {
    'description': act_three_p1['description'],
    'story_synopsis': act_three_p1['story_synopsis'],
    'key_chapters': act_three_p1['key_chapters'] + act_three_p2['key_chapters_continued'],
    'turning_point': act_three_p2['turning_point']
}
outline['act_three'] = act_three

# 写入完整大纲
with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print("大纲整合完成！")
print(f"第一幕章节数: {len(outline['act_one']['key_chapters'])}")
print(f"第二幕章节数: {len(outline['act_two']['key_chapters'])}")
print(f"第三幕章节数: {len(outline['act_three']['key_chapters'])}")
print(f"总章节数: {len(outline['act_one']['key_chapters']) + len(outline['act_two']['key_chapters']) + len(outline['act_three']['key_chapters'])}")
