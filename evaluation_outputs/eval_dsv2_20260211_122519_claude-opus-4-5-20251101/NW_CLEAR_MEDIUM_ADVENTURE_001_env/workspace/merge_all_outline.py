#!/usr/bin/env python3
import json

# 读取现有的outline.json (包含完整的act_one)
with open('outline.json', 'r', encoding='utf-8') as f:
    outline = json.load(f)

# 读取act_two
with open('temp_act_two.json', 'r', encoding='utf-8') as f:
    act_two = json.load(f)

# 读取act_three part1
with open('temp_act_three.json', 'r', encoding='utf-8') as f:
    act_three_p1 = json.load(f)

# 读取act_three part2
with open('temp_act_three_part2.json', 'r', encoding='utf-8') as f:
    act_three_p2 = json.load(f)

# 合并act_three的chapters
act_three_full = {
    "description": act_three_p1["description"],
    "story_synopsis": act_three_p1["story_synopsis"],
    "key_chapters": act_three_p1["key_chapters"] + act_three_p2["key_chapters_continued"],
    "turning_point": act_three_p2.get("turning_point", "")
}

# 构建完整outline
full_outline = {
    "act_one": outline["act_one"],
    "act_two": act_two,
    "act_three": act_three_full
}

# 写入完整outline
with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(full_outline, f, ensure_ascii=False, indent=2)

print(f"合并完成！")
print(f"Act One: {len(outline['act_one']['key_chapters'])} chapters")
print(f"Act Two: {len(act_two['key_chapters'])} chapters")  
print(f"Act Three: {len(act_three_full['key_chapters'])} chapters")
print(f"Total: {len(outline['act_one']['key_chapters']) + len(act_two['key_chapters']) + len(act_three_full['key_chapters'])} chapters")
