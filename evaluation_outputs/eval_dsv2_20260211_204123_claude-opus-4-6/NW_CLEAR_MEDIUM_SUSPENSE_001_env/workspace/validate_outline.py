import json
import os

with open('outline.json', 'r', encoding='utf-8') as f:
    outline = json.load(f)

errors = []

# Basic structure
for act_name in ['act_one', 'act_two', 'act_three']:
    act = outline[act_name]
    print(f"{act_name}: {len(act['key_chapters'])} chapters, synopsis {len(act['story_synopsis'])} chars")
    
    if act_name in ['act_one', 'act_two']:
        if 'turning_point' not in act:
            errors.append(f"{act_name} missing turning_point")
    
    for ch in act['key_chapters']:
        cn = ch.get('chapter_number', '?')
        if len(ch.get('scene_sequence', [])) < 3:
            errors.append(f"Chapter {cn} has < 3 scenes")
        
        for scene in ch.get('scene_sequence', []):
            for field in ['scene_number', 'scene_location', 'characters_present', 'scene_purpose', 'core_action', 'conflict_point', 'emotional_shift', 'scene_outcome']:
                if field not in scene:
                    errors.append(f"Chapter {cn} scene {scene.get('scene_number','?')} missing {field}")

# Check characters
all_chars = set()
for act_name in ['act_one', 'act_two', 'act_three']:
    for ch in outline[act_name]['key_chapters']:
        for scene in ch['scene_sequence']:
            for char in scene['characters_present']:
                all_chars.add(char)

print(f"\nAll characters: {sorted(all_chars)}")
print(f"File size: {os.path.getsize('outline.json')} bytes")

if errors:
    print(f"\nErrors: {len(errors)}")
    for e in errors:
        print(f"  - {e}")
else:
    print("\nAll validations passed!")
