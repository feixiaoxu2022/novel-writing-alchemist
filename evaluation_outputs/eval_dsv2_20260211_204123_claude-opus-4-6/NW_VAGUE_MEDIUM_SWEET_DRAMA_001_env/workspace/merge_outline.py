import json
with open('outline_act1.json','r') as f:
    a1=json.load(f)
with open('outline_act2_part1.json','r') as f:
    a2p1=json.load(f)
with open('outline_act2_part2.json','r') as f:
    a2p2=json.load(f)
with open('outline_act3.json','r') as f:
    a3=json.load(f)
chs = a2p1['act_two_part1']['chapters_8_to_13'] + a2p2['act_two_part2']['chapters_14_to_18']
outline = {
    'act_one': a1['act_one'],
    'act_two': {
        'description': a2p1['act_two_part1']['description'],
        'story_synopsis': a2p1['act_two_part1']['story_synopsis'],
        'key_chapters': chs,
        'turning_point': a2p2['turning_point']
    },
    'act_three': a3['act_three']
}
with open('outline.json','w') as f:
    json.dump(outline,f,ensure_ascii=False,indent=2)
tc = len(outline['act_one']['key_chapters'])+len(outline['act_two']['key_chapters'])+len(outline['act_three']['key_chapters'])
print('Total chapters:',tc)
