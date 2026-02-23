import json

# 读取所有分散的大纲文件
with open('outline_act_one.json', 'r', encoding='utf-8') as f:
    act_one_data = json.load(f)

with open('outline_act_two_part1.json', 'r', encoding='utf-8') as f:
    act_two_part1 = json.load(f)

with open('outline_act_two_part2.json', 'r', encoding='utf-8') as f:
    act_two_part2 = json.load(f)

with open('outline_act_two_part3.json', 'r', encoding='utf-8') as f:
    act_two_part3 = json.load(f)

with open('outline_act_two_part4.json', 'r', encoding='utf-8') as f:
    act_two_part4 = json.load(f)

with open('outline_act_three_part1.json', 'r', encoding='utf-8') as f:
    act_three_part1 = json.load(f)

with open('outline_act_three_part2.json', 'r', encoding='utf-8') as f:
    act_three_part2 = json.load(f)

# 合并第二幕章节
act_two_chapters = (
    act_two_part1['act_two_part1']['chapters'] +
    act_two_part2['act_two_part2']['chapters'] +
    act_two_part3['act_two_part3']['chapters'] +
    act_two_part4['act_two_part4']['chapters']
)

# 合并第三幕章节
act_three_chapters = (
    act_three_part1['act_three_part1']['chapters'] +
    act_three_part2['act_three_part2']['chapters']
)

# 构建完整的outline
outline = {
    "act_one": act_one_data['act_one'],
    "act_two": {
        "description": "三线作战：法律追讨、行业围堵、造假产业链。女主从被动挨打到开始反击，最终在至暗时刻迎来转机",
        "story_synopsis": "第一次开庭，顾家律师团咄咄逼人，冯律师沉着应对抓住证据漏洞。庭外顾母威胁沈青瓷：她在圈子里的面子够让沈青瓷一件都卖不出去。沈青瓷约吴敏对质，发现吴敏从一开始就是钱永年的眼线。她强压愤怒，决定将计就计——让吴敏继续当双面间谍。程砚洲主动联系沈青瓷，邀请她为私人藏家鉴定一批瓷器，两人开始合作。在鉴定过程中，沈青瓷看走眼了一件晚清官窑，意识到自己的专业局限性。与此同时，钱永年设局想坑她买假货，她凭借对永乐瓷器的熟悉识破了陷阱。程砚洲查到白行舟那批瓷器的来源有问题，与钱永年、徐鸣的造假链有关联。沈青瓷发现顾家也买过钱永年的假货，决定以此为筹码逼顾母撤诉。谈判成功后，钱永年发现沈青瓷在查他，展开疯狂报复——散布谣言、安排人诬告她卖假货。沈青瓷被警方带走，青花罐被扣押，跌入至暗时刻。就在她几乎绝望时，白行舟案发牵出整条造假产业链，程砚洲带来转机。沈青瓷决定让吴敏站出来作证，彻底反击。",
        "key_chapters": act_two_chapters,
        "turning_point": act_two_part4['act_two_part4']['turning_point']
    },
    "act_three": {
        "description": "猎物反杀：法律翻案、商业突围、行业清算、感情线收束、开放式结局",
        "story_synopsis": "吴敏的证词成为关键反转。警方重新调查，诬告罪名被撤销，永乐青花罐被归还。顾家也在压力下撤诉，法律战线彻底胜利。沈青瓷通过程砚洲找到正规藏家，以六千五百万的价格卖掉青花罐，获得开工作室的资本。钱永年和徐鸣被警方拘留，造假产业链被端掉。沈青瓷用卖罐子的钱租下店面，开设自己的鉴定工作室。开业初期生意冷清，但她靠专业和诚信逐渐建立口碑——敢说不懂，也敢说假。程砚洲追回祖父的旧藏，两人发现其中一件是沈青瓷外公当年修复过的，两家的渊源终于完整浮现。顾母通过中间人约见沈青瓷，没有道歉，只说'以后井水不犯河水'。沈青瓷点头离开，彻底告别过去。程砚洲正式约沈青瓷吃饭，两人确认了彼此的好感，但没有急于在一起——各自继续努力，开始慢慢约会。故事结束在一个普通的傍晚，沈青瓷关上工作室的门，看着招牌上自己的名字，想起一年前那个孤立无援的自己。路还长，但她不怕了。",
        "key_chapters": act_three_chapters
    }
}

# 写入合并后的文件
with open('outline.json', 'w', encoding='utf-8') as f:
    json.dump(outline, f, ensure_ascii=False, indent=2)

print("outline.json 合并完成")
print(f"第一幕: {len(outline['act_one']['key_chapters'])} 章")
print(f"第二幕: {len(outline['act_two']['key_chapters'])} 章")
print(f"第三幕: {len(outline['act_three']['key_chapters'])} 章")
