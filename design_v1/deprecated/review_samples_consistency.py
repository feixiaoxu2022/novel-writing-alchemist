#!/usr/bin/env python3
"""
详细review样本的一致性：
1. extension元数据与query的一致性
2. user_simulator_prompt与extension的一致性
3. check_list与extension的一致性
"""

import json
import re


def review_sample(sample):
    """详细review单个样本的一致性"""
    data_id = sample['data_id']
    query = sample['query']
    extension = sample['extension']
    user_sim = sample.get('user_simulator_prompt', '')
    check_list = sample['check_list']

    print(f"\n{'='*80}")
    print(f"样本: {data_id}")
    print(f"元数据: word_count={extension['word_count']}, tone={extension['tone']}")
    print(f"{'='*80}")

    issues = []

    # ========== 1. Query与Extension的一致性 ==========
    print("\n【1】Query与Extension元数据的一致性:")
    print(f"Query: {query[:200]}...")

    # 检查tone一致性
    tone = extension['tone']
    tone_keywords = {
        'sweet': ['甜', '爽', '不虐', '不要虐', 'HE', '甜宠'],
        'angsty': ['虐', '悲剧', '虐心', 'BE', '刀'],
        'suspense': ['烧脑', '悬疑', '反转', '悬念'],
        'neutral': []  # neutral可能没有明确的情感关键词
    }

    if tone in tone_keywords:
        expected_keywords = tone_keywords[tone]
        if expected_keywords:
            found = any(kw in query for kw in expected_keywords)
            if found:
                print(f"  ✓ Tone一致: {tone} (query中包含相关关键词)")
            else:
                issues.append(f"Tone不一致: extension为{tone}，但query中未找到相关关键词{expected_keywords}")
                print(f"  ✗ {issues[-1]}")
        else:
            print(f"  ✓ Tone={tone} (无需关键词验证)")

    # 检查word_count一致性
    word_count = extension['word_count']
    word_count_keywords = {
        'ultra_short': ['6500', '7000', '8000', '9000', '10000', '一万', '6.5k', '10k'],
        'short': ['15000', '20000', '25000', '30000', '35000', '40000', '1.5万', '2万', '3万', '4万', '15k', '40k', '短篇'],
        'medium': ['80000', '100000', '150000', '200000', '250000', '8万', '10万', '15万', '20万', '25万', '80k', '250k', '中篇'],
        'long': ['400000', '500000', '600000', '40万', '50万', '60万', '400k', '600k', '长篇'],
        'ultra_long': ['1000000', '2000000', '3000000', '100万', '200万', '300万', '1M', '3M', '超长篇']
    }

    if word_count in word_count_keywords:
        expected_keywords = word_count_keywords[word_count]
        found = any(kw in query for kw in expected_keywords)
        if found:
            print(f"  ✓ Word_count一致: {word_count} (query中包含篇幅描述)")
        else:
            # 可能query没有明确篇幅要求，这不一定是错误
            print(f"  ⚠ Word_count={word_count}，但query中未明确提及篇幅（可能是隐含要求）")

    # ========== 2. User_simulator与Extension的一致性 ==========
    print("\n【2】User_simulator_prompt与Extension的一致性:")

    if not user_sim:
        issues.append("缺少user_simulator_prompt")
        print(f"  ✗ {issues[-1]}")
    else:
        # 检查user_sim中是否提到了正确的word_count
        if word_count in user_sim or word_count.replace('_', ' ') in user_sim:
            print(f"  ✓ User_sim提到了word_count: {word_count}")
        else:
            # 检查中文描述
            cn_word_count_map = {
                'ultra_short': '超短篇',
                'short': '短篇',
                'medium': '中篇',
                'long': '长篇',
                'ultra_long': '超长篇'
            }
            cn_wc = cn_word_count_map.get(word_count, '')
            if cn_wc and cn_wc in user_sim:
                print(f"  ✓ User_sim提到了篇幅: {cn_wc}")
            else:
                issues.append(f"User_sim未提到word_count: {word_count}")
                print(f"  ✗ {issues[-1]}")

        # 检查user_sim中是否提到了正确的tone
        if tone != 'neutral':
            tone_descriptions = {
                'sweet': ['甜爽', '甜宠', '不虐', '爽文'],
                'angsty': ['虐心', '悲剧', '虐'],
                'suspense': ['烧脑', '悬疑', '反转']
            }
            if tone in tone_descriptions:
                expected = tone_descriptions[tone]
                found = any(kw in user_sim for kw in expected)
                if found:
                    print(f"  ✓ User_sim提到了tone: {tone}")
                else:
                    issues.append(f"User_sim未提到tone: {tone}")
                    print(f"  ✗ {issues[-1]}")
        else:
            print(f"  ✓ Tone=neutral (user_sim无需特定tone描述)")

    # ========== 3. Check_list与Extension的一致性 ==========
    print("\n【3】Check_list与Extension的一致性:")

    # 统计check_list
    check_descriptions = [c['description'] for c in check_list]

    # 检查reaction_strength检查项（通过subcategory_id判断）
    has_reaction_check = any(c.get('subcategory_id') == 'emotional_tone_constraint' for c in check_list)

    if tone in ['sweet', 'angsty', 'suspense']:
        if has_reaction_check:
            print(f"  ✓ Tone={tone}，check_list包含reaction_strength检查")
        else:
            issues.append(f"Tone={tone}但check_list缺少reaction_strength检查")
            print(f"  ✗ {issues[-1]}")
    elif tone == 'neutral':
        if has_reaction_check:
            issues.append(f"Tone=neutral但check_list包含reaction_strength检查")
            print(f"  ✗ {issues[-1]}")
        else:
            print(f"  ✓ Tone=neutral，check_list不包含reaction_strength检查")

    # 检查emotional_delivery检查项（通过subcategory_id判断）
    has_emotional_check = any(c.get('subcategory_id') == 'emotional_delivery_match' for c in check_list)

    if tone in ['sweet', 'angsty', 'suspense']:
        if has_emotional_check:
            print(f"  ✓ Tone={tone}，check_list包含情感交付检查")
        else:
            issues.append(f"Tone={tone}但check_list缺少情感交付检查")
            print(f"  ✗ {issues[-1]}")
    elif tone == 'neutral':
        if has_emotional_check:
            issues.append(f"Tone=neutral但check_list包含情感交付检查")
            print(f"  ✗ {issues[-1]}")
        else:
            print(f"  ✓ Tone=neutral，check_list不包含情感交付检查")

    # 检查word_count检查项
    word_count_check_map = {
        'ultra_short': '6500-10000',
        'short': '15000-40000',
        'medium': '80000-250000',
        'long': '400000-600000',
        'ultra_long': '1000000-3000000'
    }

    expected_range = word_count_check_map.get(word_count, '')
    has_word_count_check = any(expected_range in str(c) for c in check_list)

    if has_word_count_check:
        print(f"  ✓ Word_count={word_count}，check_list包含字数检查({expected_range})")
    else:
        issues.append(f"Word_count={word_count}但check_list缺少字数检查({expected_range})")
        print(f"  ✗ {issues[-1]}")

    # 检查writing_log检查项（通过description关键词判断）
    has_writing_log_check = any('writing_log' in c.get('description', '').lower() or '创作日志' in c.get('description', '') for c in check_list)

    if word_count in ['long', 'ultra_long']:
        if has_writing_log_check:
            print(f"  ✓ Word_count={word_count}，check_list包含writing_log检查")
        else:
            issues.append(f"Word_count={word_count}但check_list缺少writing_log检查")
            print(f"  ✗ {issues[-1]}")
    else:
        if has_writing_log_check:
            issues.append(f"Word_count={word_count}但check_list包含writing_log检查（不应该有）")
            print(f"  ✗ {issues[-1]}")
        else:
            print(f"  ✓ Word_count={word_count}，check_list不包含writing_log检查")

    # ========== 总结 ==========
    print("\n【总结】")
    if issues:
        print(f"  发现 {len(issues)} 个问题:")
        for i, issue in enumerate(issues, 1):
            print(f"    {i}. {issue}")
    else:
        print(f"  ✓ 所有检查通过，样本一致性良好")

    return issues


def main():
    with open('/tmp/random_5_samples.jsonl', 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]

    all_issues = {}

    for i, sample in enumerate(samples, 1):
        issues = review_sample(sample)
        if issues:
            all_issues[sample['data_id']] = issues

    print("\n\n")
    print("="*80)
    print("【汇总】5个样本一致性Review结果")
    print("="*80)

    if all_issues:
        print(f"\n发现 {len(all_issues)} 个样本存在问题:\n")
        for data_id, issues in all_issues.items():
            print(f"{data_id}:")
            for issue in issues:
                print(f"  - {issue}")
    else:
        print("\n✓ 所有5个样本一致性检查全部通过！")


if __name__ == '__main__':
    main()
