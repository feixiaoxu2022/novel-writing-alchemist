import json

act1_meta = json.load(open('temp_act1_meta.json', 'r'))
act1_ch1to5 = json.load(open('temp_act1_chapters_1to5.json', 'r'))
act1_ch6to10 = json.load(open('temp_act1_chapters_6to10.json', 'r'))
act2_meta = json.load(open('temp_act2_meta.json', 'r'))
act2_ch11to15 = json.load(open('temp_act2_chapters_11to15.json', 'r'))
act2_ch16to20 = json.load(open('temp_act2_chapters_16to20.json', 'r'))
act2_ch21to25 = json.load(open('temp_act2_chapters_21to25.json', 'r'))
act3_meta = json.load(open('temp_act3_meta.json', 'r'))
act3_ch26to30 = json.load(open('temp_act3_chapters_26to30.json', 'r'))
act3_ch31to35 = json.load(open('temp_act3_chapters_31to35.json', 'r'))

outline = {
    "act_one": {
        "description": act1_meta["act_one_meta"]["description"],
        "story_synopsis": act1_meta["act_one_meta"]["story_synopsis"],
        "key_chapters": act1_ch1to5 + act1_ch6to10,
        "turning_point": act1_meta["act_one_meta"]["turning_point"]
    },
    "act_two": {
        "description": act2_meta["act_two_meta"]["description"],
        "story_synopsis": act2_meta["act_two_meta"]["story_synopsis"],
        "key_chapters": act2_ch11to15 + act2_ch16to20 + act2_ch21to25,
        "turning_point": act2_meta["act_two_meta"]["turning_point"]
    },
    "act_three": {
        "description": act3_meta["act_three_meta"]["description"],
        "story_synopsis": act3_meta["act_three_meta"]["story_synopsis"],
        "key_chapters": act3_ch26to30 + act3_ch31to35
    }
}

with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print('outline.json created successfully!')
print('Act One: %d chapters' % len(outline["act_one"]["key_chapters"]))
print('Act Two: %d chapters' % len(outline["act_two"]["key_chapters"]))
print('Act Three: %d chapters' % len(outline["act_three"]["key_chapters"]))
total = len(outline['act_one']['key_chapters']) + len(outline['act_two']['key_chapters']) + len(outline['act_three']['key_chapters'])
print('Total chapters: %d' % total)

all_chars = set()
for act_key in ['act_one', 'act_two', 'act_three']:
    for ch in outline[act_key]['key_chapters']:
        for scene in ch['scene_sequence']:
            for c in scene['characters_present']:
                all_chars.add(c)
print('Characters in outline: %s' % all_chars)

chars = json.load(open('characters.json', 'r'))
designed = set()
for mc in chars['main_characters']:
    designed.add(mc['name'])
for sc in chars['supporting_characters']:
    designed.add(sc['name'])
missing = designed - all_chars
if missing:
    print('WARNING missing: %s' % missing)
else:
    print('All designed characters appear in outline!')
