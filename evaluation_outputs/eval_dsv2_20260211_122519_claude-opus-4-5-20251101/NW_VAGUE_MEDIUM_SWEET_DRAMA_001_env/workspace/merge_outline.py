import json

# 读取第一幕
with open('outline_act_one.json', 'r', encoding='utf-8') as f:
    act_one_data = json.load(f)

# 读取第二幕（三个部分）
with open('outline_act_two_p1.json', 'r', encoding='utf-8') as f:
    act_two_p1 = json.load(f)
with open('outline_act_two_p2.json', 'r', encoding='utf-8') as f:
    act_two_p2 = json.load(f)
with open('outline_act_two_p3.json', 'r', encoding='utf-8') as f:
    act_two_p3 = json.load(f)

# 读取第三幕
with open('outline_act_three.json', 'r', encoding='utf-8') as f:
    act_three_data = json.load(f)

# 合并第二幕
act_two = {
    "description": act_two_p1["act_two_part1"]["description"],
    "story_synopsis": act_two_p1["act_two_part1"]["story_synopsis"],
    "key_chapters": (
        act_two_p1["act_two_part1"]["key_chapters"] +
        act_two_p2["act_two_part2"]["key_chapters"] +
        act_two_p3["act_two_part3"]["key_chapters"]
    ),
    "turning_point": act_two_p3["act_two_part3"]["turning_point"]
}

# 构建完整大纲
outline = {
    "act_one": act_one_data["act_one"],
    "act_two": act_two,
    "act_three": act_three_data["act_three"]
}

# 写入完整大纲文件
with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print("outline.json 合并完成！")
