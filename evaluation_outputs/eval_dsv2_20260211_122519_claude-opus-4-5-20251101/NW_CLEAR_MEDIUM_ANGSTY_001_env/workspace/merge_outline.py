#!/usr/bin/env python3
import json

# 读取第一幕总纲
with open('outline_act1.json', 'r', encoding='utf-8') as f:
    act1_main = json.load(f)

# 读取第一幕各章节
act1_chapters = []
for fname in ['outline_act1_ch1_2.json', 'outline_act1_ch3_4.json', 
              'outline_act1_ch5_6.json', 'outline_act1_ch7_8.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = list(data.keys())[0]
        act1_chapters.extend(data[key])

# 读取第二幕总纲
with open('outline_act2.json', 'r', encoding='utf-8') as f:
    act2_main = json.load(f)

# 读取第二幕各章节
act2_chapters = []
for fname in ['outline_act2_ch9_10.json', 'outline_act2_ch11_12.json',
              'outline_act2_ch13_14.json', 'outline_act2_ch15_16.json',
              'outline_act2_ch17_18.json', 'outline_act2_ch19_20.json',
              'outline_act2_ch21_22.json', 'outline_act2_ch23_24.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = [k for k in data.keys() if 'chapters' in k][0]
        act2_chapters.extend(data[key])

# 读取第三幕总纲
with open('outline_act3.json', 'r', encoding='utf-8') as f:
    act3_main = json.load(f)

# 读取第三幕各章节
act3_chapters = []
for fname in ['outline_act3_ch25_26.json', 'outline_act3_ch27_28.json',
              'outline_act3_ch29_30.json', 'outline_act3_ch31_32.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = [k for k in data.keys() if 'chapters' in k][0]
        act3_chapters.extend(data[key])

# 构建完整大纲
outline = {
    "act_one": {
        "description": act1_main["act_one"]["description"],
        "story_synopsis": act1_main["act_one"]["story_synopsis"],
        "key_chapters": act1_chapters,
        "turning_point": act1_main["act_one"]["turning_point"]
    },
    "act_two": {
        "description": act2_main["act_two"]["description"],
        "story_synopsis": act2_main["act_two"]["story_synopsis"],
        "key_chapters": act2_chapters,
        "turning_point": act2_main["act_two"]["turning_point"]
    },
    "act_three": {
        "description": act3_main["act_three_synopsis"]["description"],
        "story_synopsis": act3_main["act_three_synopsis"]["story_synopsis"],
        "key_chapters": act3_chapters,
        "turning_point": act3_main["act_three_synopsis"]["turning_point"]
    }
}

# 写入合并后的文件
with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print("outline.json created successfully!")
print(f"Act 1: {len(act1_chapters)} chapters")
print(f"Act 2: {len(act2_chapters)} chapters")
print(f"Act 3: {len(act3_chapters)} chapters")
