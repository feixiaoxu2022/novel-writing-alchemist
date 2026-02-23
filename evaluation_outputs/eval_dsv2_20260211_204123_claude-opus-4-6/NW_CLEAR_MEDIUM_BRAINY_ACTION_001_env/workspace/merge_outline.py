import json

# Read act_one (already complete)
with open('outline.json', 'r', encoding='utf-8') as f:
    outline = json.load(f)

# Read act_two story synopsis from draft
with open('outline_act23_draft.json', 'r', encoding='utf-8') as f:
    draft = json.load(f)

# Read act_two chapters
with open('outline_act2_part1.json', 'r', encoding='utf-8') as f:
    a2p1 = json.load(f)
with open('outline_act2_part2.json', 'r', encoding='utf-8') as f:
    a2p2 = json.load(f)
with open('outline_act2_part3.json', 'r', encoding='utf-8') as f:
    a2p3 = json.load(f)

# Read act_three chapters
with open('outline_act3_part1.json', 'r', encoding='utf-8') as f:
    a3p1 = json.load(f)
with open('outline_act3_part2.json', 'r', encoding='utf-8') as f:
    a3p2 = json.load(f)

# Build act_two
all_act2_chapters = (a2p1['chapters_8_to_11'] + a2p2['chapters_12_to_15'] + a2p3['chapters_16_to_18'])

outline['act_two'] = {
    "description": draft['act_two_data']['description'],
    "story_synopsis": draft['act_two_data']['story_synopsis'],
    "key_chapters": all_act2_chapters,
    "turning_point": "连环真相引爆：傅知行是织网者的观察员'棋手'，沈夜霜是十二年前将许芸送入异域的执行者'七号'。卫燃为传递情报被织网者清洗致死。许长安一夜之间失去了对所有核心关系的信任——但他选择带着伤痛继续前行，因为母亲在深层异域等他，这条路上的终点比沿途的背叛更重要。"
}

# Build act_three
all_act3_chapters = (a3p1['chapters_19_to_22'] + a3p2['chapters_23_to_25'])

outline['act_three'] = {
    "description": draft['act_three_data']['description'],
    "story_synopsis": draft['act_three_data']['story_synopsis'],
    "key_chapters": all_act3_chapters,
    "turning_point": "许长安在裴见深的'修补'方案和母亲的'封堵'方案之间找到了第三条路——他不修补也不封堵，而是让规则学会自我修正，让世界接受自己的不完美。母亲许芸在元规则生效后消散，但她的路标指引儿子走到了终点。"
}

# Write final outline
with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print(f"Merged outline.json: {len(outline['act_one']['key_chapters'])} + {len(outline['act_two']['key_chapters'])} + {len(outline['act_three']['key_chapters'])} chapters")
print(f"Total chapters: {len(outline['act_one']['key_chapters']) + len(outline['act_two']['key_chapters']) + len(outline['act_three']['key_chapters'])}")
