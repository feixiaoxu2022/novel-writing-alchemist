import json

with open('outline_act1.json', 'r', encoding='utf-8') as f:
    act1 = json.load(f)
with open('outline_act2.json', 'r', encoding='utf-8') as f:
    act2 = json.load(f)
with open('outline_act3.json', 'r', encoding='utf-8') as f:
    act3 = json.load(f)

outline = {
    "act_one": act1["act_one"],
    "act_two": act2["act_two"],
    "act_three": act3["act_three"]
}

with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print("outline.json created successfully")
