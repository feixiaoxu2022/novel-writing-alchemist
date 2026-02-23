import json
import os

# Load all parts
parts_dir = "outline_parts"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load act metadata
act1_meta = load_json(os.path.join(parts_dir, "act1_meta.json"))
act2_meta = load_json(os.path.join(parts_dir, "act2_meta.json"))
act3_meta = load_json(os.path.join(parts_dir, "act3_meta.json"))

# Load chapter files and combine
act1_chapters = []
for fn in ["act1_ch01_02.json", "act1_ch03_04.json", "act1_ch05_06.json", "act1_ch07_08.json"]:
    act1_chapters.extend(load_json(os.path.join(parts_dir, fn)))

act2_chapters = []
for fn in ["act2_ch09_10.json", "act2_ch11_12.json", "act2_ch13_14.json", "act2_ch15_16.json", "act2_ch17_18.json", "act2_ch19_20.json", "act2_ch21_22.json"]:
    act2_chapters.extend(load_json(os.path.join(parts_dir, fn)))

act3_chapters = []
for fn in ["act3_ch23_24.json", "act3_ch25_26.json", "act3_ch27_28.json", "act3_ch29_30.json"]:
    act3_chapters.extend(load_json(os.path.join(parts_dir, fn)))

# Build the final outline
outline = {
    "act_one": {
        "description": act1_meta["description"],
        "story_synopsis": act1_meta["story_synopsis"],
        "key_chapters": act1_chapters,
        "turning_point": act1_meta["turning_point"]
    },
    "act_two": {
        "description": act2_meta["description"],
        "story_synopsis": act2_meta["story_synopsis"],
        "key_chapters": act2_chapters,
        "turning_point": act2_meta["turning_point"]
    },
    "act_three": {
        "description": act3_meta["description"],
        "story_synopsis": act3_meta["story_synopsis"],
        "key_chapters": act3_chapters
    }
}

# Write the combined outline
with open("outline.json", 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print(f"outline.json generated successfully!")
print(f"Act 1: {len(act1_chapters)} chapters")
print(f"Act 2: {len(act2_chapters)} chapters")
print(f"Act 3: {len(act3_chapters)} chapters")
print(f"Total: {len(act1_chapters) + len(act2_chapters) + len(act3_chapters)} chapters")
