# 模型评测对比统计报告

生成时间: 2026-02-12 18:14:46

使用check_result文件: **check_result_rev004.json**

## 1. 模型整体表现摘要

**字段说明**：

- `total_sample_dirs`: 总样本目录数

- `has_check_result`: 有check_result文件的样本数（完成评测）

- `no_check_result`: 完全无check_result文件的样本数（Agent崩溃/超时）

- `good_or_fair`: Good或Fair质量的样本数

- `poor`: Poor质量的样本数


| model_name                              |   total_sample_dirs | has_check_result   | no_check_result   | good_or_fair       | poor            | avg_pass_rate   |
|:----------------------------------------|--------------------:|:-------------------|:------------------|:-------------------|:----------------|:----------------|
| gemini-3-pro-preview                    |                  10 | 8 (80.0%, 8/10)    | 2 (20.0%, 2/10)   | 8 (100.0%, 8/8)    | 0 (0.0%, 0/8)   | 79.88%          |
| kimi-k2.5                               |                  10 | 10 (100.0%, 10/10) | 0 (0.0%, 0/10)    | 9 (90.0%, 9/10)    | 1 (10.0%, 1/10) | 70.08%          |
| openai_EB5-0209-A35B-midtrain-128k-chat |                  10 | 7 (70.0%, 7/10)    | 3 (30.0%, 3/10)   | 3 (42.9%, 3/7)     | 4 (57.1%, 4/7)  | 52.24%          |
| ernie-5.0-thinking-preview              |                   4 | 4 (100.0%, 4/4)    | 0 (0.0%, 0/4)     | 2 (50.0%, 2/4)     | 2 (50.0%, 2/4)  | 65.42%          |
| claude-opus-4-5-20251101                |                  10 | 10 (100.0%, 10/10) | 0 (0.0%, 0/10)    | 10 (100.0%, 10/10) | 0 (0.0%, 0/10)  | 86.97%          |
| claude-opus-4-6                         |                   7 | 7 (100.0%, 7/7)    | 0 (0.0%, 0/7)     | 7 (100.0%, 7/7)    | 0 (0.0%, 0/7)   | 93.03%          |


## 2. Layer1 维度对比 (dimension_id)

| dimension_id             | claude-opus-4-5-20251101_pass_rate   | claude-opus-4-6_pass_rate   | ernie-5.0-thinking-preview_pass_rate   | gemini-3-pro-preview_pass_rate   | kimi-k2.5_pass_rate   | openai_EB5-0209-A35B-midtrain-128k-chat_pass_rate   |
|:-------------------------|:-------------------------------------|:----------------------------|:---------------------------------------|:---------------------------------|:----------------------|:----------------------------------------------------|
| format_compliance        | 90.0% (36/40)                        | 96.4% (27/28)               | 81.2% (13/16)                          | 100.0% (32/32)                   | 80.0% (32/40)         | 71.4% (20/28)                                       |
| business_rule_compliance | 89.3% (184/206)                      | 95.3% (137/144)             | 76.4% (60/78)                          | 79.0% (130/164)                  | 75.3% (155/206)       | 58.2% (81/137)                                      |
| memory_management        | 95.0% (19/20)                        | 92.9% (13/14)               | 37.5% (3/8)                            | 81.2% (13/16)                    | 70.0% (14/20)         | 42.9% (6/14)                                        |
| content_quality          | 81.5% (116/142)                      | 88.8% (89/100)              | 50.0% (29/58)                          | 75.2% (87/116)                   | 59.6% (81/137)        | 39.6% (39/97)                                       |


## 3. Layer2 子类别对比 (subcategory_id)

| dimension_id             | subcategory_id                 | 中文名称                            | check_type   | claude-opus-4-5-20251101_pass_rate   | claude-opus-4-6_pass_rate   | ernie-5.0-thinking-preview_pass_rate   | gemini-3-pro-preview_pass_rate   | kimi-k2.5_pass_rate   | openai_EB5-0209-A35B-midtrain-128k-chat_pass_rate   |
|:-------------------------|:-------------------------------|:--------------------------------|:-------------|:-------------------------------------|:----------------------------|:---------------------------------------|:---------------------------------|:----------------------|:----------------------------------------------------|
| format_compliance        | naming_convention              | 输出文件的命名规不规范                     | rule         | 100.0% (10/10)                       | 100.0% (7/7)                | 50.0% (2/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| format_compliance        | structural_integrity           | JSON文件能不能正常解析、符不符合Schema        | rule         | 86.7% (26/30)                        | 95.2% (20/21)               | 91.7% (11/12)                          | 100.0% (24/24)                   | 73.3% (22/30)         | 76.2% (16/21)                                       |
| business_rule_compliance | required_skill_reading         | 开工前有没有先读skill文档                 | rule         | 90.5% (86/95)                        | 97.0% (64/66)               | 73.0% (27/37)                          | 81.6% (62/76)                    | 71.6% (68/95)         | 64.2% (43/67)                                       |
| business_rule_compliance | sop_compliance                 | 该走HITL确认的环节有没有走                 | rule         | 66.7% (14/21)                        | 93.3% (14/15)               | 77.8% (7/9)                            | 100.0% (16/16)                   | 90.5% (19/21)         | 60.0% (9/15)                                        |
| business_rule_compliance | output_completeness            | 该交付的文件类型齐不齐                     | rule         | 97.5% (39/40)                        | 100.0% (28/28)              | 87.5% (14/16)                          | 100.0% (32/32)                   | 100.0% (40/40)        | 75.0% (21/28)                                       |
| business_rule_compliance | enum_validity                  | 配方参数值是否在合法枚举范围内                 | rule         | 100.0% (20/20)                       | 100.0% (14/14)              | 100.0% (6/6)                           | 62.5% (10/16)                    | 70.0% (14/20)         | 40.0% (4/10)                                        |
| business_rule_compliance | quantity_constraint            | 配方参数数量对不对（如Y轴标签要求2-3个）          | rule         | 100.0% (20/20)                       | 100.0% (14/14)              | 83.3% (5/6)                            | 62.5% (10/16)                    | 70.0% (14/20)         | 40.0% (4/10)                                        |
| business_rule_compliance | range_constraint               | 总字数在不在要求的范围内                    | semantic     | 50.0% (5/10)                         | 42.9% (3/7)                 | 25.0% (1/4)                            | 0.0% (0/8)                       | 0.0% (0/10)           | 0.0% (0/7)                                          |
| business_rule_compliance | workspace_file_compliance      | workspace中不能有白名单之外的文件           | rule         | 0.0% (0/0)                           | 0.0% (0/0)                  | 0.0% (0/0)                             | 0.0% (0/0)                       | 0.0% (0/0)            | 0.0% (0/0)                                          |
| memory_management        | log_file_creation              | 有没有创建writing_log记录创作进度          | rule         | 100.0% (10/10)                       | 100.0% (7/7)                | 50.0% (2/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 71.4% (5/7)                                         |
| memory_management        | log_file_usage                 | 续写时有没有先读writing_log了解前文         | rule         | 90.0% (9/10)                         | 85.7% (6/7)                 | 25.0% (1/4)                            | 62.5% (5/8)                      | 40.0% (4/10)          | 14.3% (1/7)                                         |
| content_quality          | full_narrative_content         | 章节内容是完整正文还是大纲摘要                 | semantic     | 90.0% (9/10)                         | 100.0% (7/7)                | 25.0% (1/4)                            | 100.0% (8/8)                     | 70.0% (7/10)          | 42.9% (3/7)                                         |
| content_quality          | language_purity                | 正文有没有不合理的中英混用                   | semantic     | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 87.5% (7/8)                      | 50.0% (5/10)          | 42.9% (3/7)                                         |
| content_quality          | character_presence_in_outline  | 设计的主角在大纲中有没有规划                  | rule         | 88.9% (8/9)                          | 100.0% (7/7)                | 50.0% (2/4)                            | 25.0% (2/8)                      | 28.6% (2/7)           | 16.7% (1/6)                                         |
| content_quality          | character_presence_in_chapters | 设计的主角在正文章节中出没出现                 | rule         | 90.0% (9/10)                         | 85.7% (6/7)                 | 33.3% (1/3)                            | 25.0% (2/8)                      | 28.6% (2/7)           | 16.7% (1/6)                                         |
| content_quality          | character_design_adherence     | 正文中角色表现符不符合characters.json的人设   | semantic     | 83.3% (10/12)                        | 100.0% (8/8)                | 60.0% (3/5)                            | 80.0% (8/10)                     | 50.0% (6/12)          | 75.0% (6/8)                                         |
| content_quality          | character_trait_consistency    | 同一角色的性格前后章节有没有变                 | semantic     | 90.0% (9/10)                         | 100.0% (7/7)                | 50.0% (2/4)                            | 100.0% (8/8)                     | 80.0% (8/10)          | 57.1% (4/7)                                         |
| content_quality          | theme_consistency              | 故事核心主题从头到尾有没有跑偏                 | semantic     | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| content_quality          | plot_progression               | 章节之间情节有没有在往前推进                  | semantic     | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| content_quality          | emotional_delivery_match       | 写出来的内容读起来是不是要求的那个味（甜/虐/烧脑）      | semantic     | 81.8% (9/11)                         | 87.5% (7/8)                 | 50.0% (3/6)                            | 60.0% (6/10)                     | 72.7% (8/11)          | 14.3% (1/7)                                         |
| content_quality          | narrative_tone_match           | 文笔画风跟题材搭不搭（烧脑文不能写成言情调）          | semantic     | 60.0% (6/10)                         | 100.0% (7/7)                | 75.0% (3/4)                            | 75.0% (6/8)                      | 20.0% (2/10)          | 42.9% (3/7)                                         |
| content_quality          | logical_contradiction          | 情节有没有逻辑硬伤（死人复活/前后矛盾）            | semantic     | 0.0% (0/10)                          | 14.3% (1/7)                 | 0.0% (0/4)                             | 12.5% (1/8)                      | 0.0% (0/10)           | 0.0% (0/7)                                          |
| content_quality          | main_character_consistency     | 前中后主要角色保持一致，主角不能消失或被替换          | semantic     | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 42.9% (3/7)                                         |
| content_quality          | repeated_endings               | 不能出现多次结局标记（全文完/全书完/后记）          | semantic     | 80.0% (8/10)                         | 71.4% (5/7)                 | 50.0% (2/4)                            | 87.5% (7/8)                      | 60.0% (6/10)          | 57.1% (4/7)                                         |
| content_quality          | late_stage_digression          | 后期章节不能跑偏写非正文内容（作者感想/读者互动/番外预告等） | semantic     | 80.0% (8/10)                         | 85.7% (6/7)                 | 0.0% (0/4)                             | 100.0% (8/8)                     | 50.0% (5/10)          | 28.6% (2/7)                                         |


## 4. Checklist 检查项对比

| check_id   | description                                    | dimension_id             | subcategory_id                 | claude-opus-4-5-20251101_pass_rate   | claude-opus-4-6_pass_rate   | ernie-5.0-thinking-preview_pass_rate   | gemini-3-pro-preview_pass_rate   | kimi-k2.5_pass_rate   | openai_EB5-0209-A35B-midtrain-128k-chat_pass_rate   |
|:-----------|:-----------------------------------------------|:-------------------------|:-------------------------------|:-------------------------------------|:----------------------------|:---------------------------------------|:---------------------------------|:----------------------|:----------------------------------------------------|
| 检查项1       | 必须读取RECIPE_KNOWLEDGE.md（配方知识库）                 | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 100.0% (10/10)        | 100.0% (7/7)                                        |
| 检查项2       | 必须读取CHARACTER_DESIGN_GUIDE.md（人物设计指南）          | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 100.0% (10/10)        | 100.0% (7/7)                                        |
| 检查项3       | 必须读取OUTLINE_DESIGN_GUIDE.md（大纲设计指南）            | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 100.0% (10/10)        | 100.0% (7/7)                                        |
| 检查项4       | 必须读取WRITING_TECHNIQUE_GUIDE.md（写作技巧指南）         | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| 检查项5       | 必须读取CONSISTENCY_MANAGEMENT_GUIDE.md（设定一致性管理指南） | business_rule_compliance | required_skill_reading         | 40.0% (4/10)                         | 100.0% (7/7)                | 0.0% (0/4)                             | 100.0% (8/8)                     | 0.0% (0/10)           | 57.1% (4/7)                                         |
| 检查项6       | 必须读取CHARACTER_NAMING_GUIDE.md（角色命名规范）          | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 100.0% (10/10)        | 100.0% (7/7)                                        |
| 检查项7       | 必须读取creative_intent.schema.json（输出格式规范）        | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 62.5% (5/8)                      | 70.0% (7/10)          | 42.9% (3/7)                                         |
| 检查项8       | 必须读取characters.schema.json（输出格式规范）             | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 50.0% (2/4)                            | 37.5% (3/8)                      | 40.0% (4/10)          | 14.3% (1/7)                                         |
| 检查项9       | 必须读取outline.schema.json（输出格式规范）                | business_rule_compliance | required_skill_reading         | 100.0% (10/10)                       | 100.0% (7/7)                | 50.0% (2/4)                            | 37.5% (3/8)                      | 40.0% (4/10)          | 14.3% (1/7)                                         |
| 检查项10      | 章节文件命名必须为chapter_NN.md格式                       | format_compliance        | naming_convention              | 100.0% (10/10)                       | 100.0% (7/7)                | 50.0% (2/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| 检查项11      | creative_intent.json的Schema验证                  | format_compliance        | structural_integrity           | 70.0% (7/10)                         | 85.7% (6/7)                 | 75.0% (3/4)                            | 100.0% (8/8)                     | 90.0% (9/10)          | 57.1% (4/7)                                         |
| 检查项12      | characters.json的Schema验证                       | format_compliance        | structural_integrity           | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 70.0% (7/10)          | 85.7% (6/7)                                         |
| 检查项13      | outline.json的Schema验证                          | format_compliance        | structural_integrity           | 90.0% (9/10)                         | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 60.0% (6/10)          | 85.7% (6/7)                                         |
| 检查项14      | X轴模式ID必须匹配^[A-G]\d{1,2}$格式                     | business_rule_compliance | enum_validity                  | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (3/3)                           | 62.5% (5/8)                      | 70.0% (7/10)          | 40.0% (2/5)                                         |
| 检查项15      | Y轴标签必须在12种枚举中                                  | business_rule_compliance | enum_validity                  | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (3/3)                           | 62.5% (5/8)                      | 70.0% (7/10)          | 40.0% (2/5)                                         |
| 检查项16      | Y轴标签数量必须为2-3个                                  | business_rule_compliance | quantity_constraint            | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (3/3)                           | 62.5% (5/8)                      | 70.0% (7/10)          | 40.0% (2/5)                                         |
| 检查项17      | forbidden_elements必须至少有1个                      | business_rule_compliance | quantity_constraint            | 100.0% (10/10)                       | 100.0% (7/7)                | 66.7% (2/3)                            | 62.5% (5/8)                      | 70.0% (7/10)          | 40.0% (2/5)                                         |
| 检查项18      | 配方选择阶段HITL调用                                   | business_rule_compliance | sop_compliance                 | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 90.0% (9/10)          | 85.7% (6/7)                                         |
| 检查项19      | 写作准备阶段HITL调用                                   | business_rule_compliance | sop_compliance                 | 40.0% (4/10)                         | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 42.9% (3/7)                                         |
| 检查项20      | 故事主题一致                                         | content_quality          | theme_consistency              | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| 检查项21      | 主要角色一致性                                        | content_quality          | main_character_consistency     | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 42.9% (3/7)                                         |
| 检查项22      | 人物设定一致性                                        | content_quality          | character_trait_consistency    | 90.0% (9/10)                         | 100.0% (7/7)                | 50.0% (2/4)                            | 100.0% (8/8)                     | 80.0% (8/10)          | 57.1% (4/7)                                         |
| 检查项23      | 实际表现符合设计文档                                     | content_quality          | character_design_adherence     | 90.0% (9/10)                         | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 60.0% (6/10)          | 85.7% (6/7)                                         |
| 检查项24      | 无逻辑硬伤                                          | content_quality          | logical_contradiction          | 0.0% (0/10)                          | 14.3% (1/7)                 | 0.0% (0/4)                             | 12.5% (1/8)                      | 0.0% (0/10)           | 0.0% (0/7)                                          |
| 检查项25      | 无不合理的多语言混用                                     | content_quality          | language_purity                | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 87.5% (7/8)                      | 50.0% (5/10)          | 42.9% (3/7)                                         |
| 检查项26      | creative_intent.json必须存在                       | business_rule_compliance | output_completeness            | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 71.4% (5/7)                                         |
| 检查项27      | characters.json必须存在                            | business_rule_compliance | output_completeness            | 100.0% (10/10)                       | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 100.0% (10/10)        | 85.7% (6/7)                                         |
| 检查项28      | outline.json必须存在                               | business_rule_compliance | output_completeness            | 90.0% (9/10)                         | 100.0% (7/7)                | 100.0% (4/4)                           | 100.0% (8/8)                     | 100.0% (10/10)        | 85.7% (6/7)                                         |
| 检查项29      | chapters/目录必须存在且有章节文件                          | business_rule_compliance | output_completeness            | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| 检查项30      | 章节情节推进质量                                       | content_quality          | plot_progression               | 100.0% (10/10)                       | 100.0% (7/7)                | 75.0% (3/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 57.1% (4/7)                                         |
| 检查项31      | 章节内容必须是完整正文而非大纲                                | content_quality          | full_narrative_content         | 90.0% (9/10)                         | 100.0% (7/7)                | 25.0% (1/4)                            | 100.0% (8/8)                     | 70.0% (7/10)          | 42.9% (3/7)                                         |
| 检查项32      | 不能出现多次结局标记（全文完/全书完/后记）                         | content_quality          | repeated_endings               | 80.0% (8/10)                         | 71.4% (5/7)                 | 50.0% (2/4)                            | 87.5% (7/8)                      | 60.0% (6/10)          | 57.1% (4/7)                                         |
| 检查项33      | workspace中不能有白名单之外的文件                          | business_rule_compliance | workspace_file_compliance      | 0.0% (0/0)                           | 0.0% (0/0)                  | 0.0% (0/0)                             | 0.0% (0/0)                       | 0.0% (0/0)            | 0.0% (0/0)                                          |
| 检查项34      | 后期章节不能跑偏写非正文内容（作者感想、读者互动、番外预告等）                | content_quality          | late_stage_digression          | 80.0% (8/10)                         | 85.7% (6/7)                 | 0.0% (0/4)                             | 100.0% (8/8)                     | 50.0% (5/10)          | 28.6% (2/7)                                         |
| 检查项35      | 设计的主要角色必须在大纲中规划                                | content_quality          | character_presence_in_outline  | 88.9% (8/9)                          | 100.0% (7/7)                | 50.0% (2/4)                            | 25.0% (2/8)                      | 28.6% (2/7)           | 16.7% (1/6)                                         |
| 检查项36      | 设计的主要角色必须在正文中出现                                | content_quality          | character_presence_in_chapters | 90.0% (9/10)                         | 85.7% (6/7)                 | 33.3% (1/3)                            | 25.0% (2/8)                      | 28.6% (2/7)           | 16.7% (1/6)                                         |
| 检查项37      | 必须创建writing_log.md记录创作进度                       | memory_management        | log_file_creation              | 100.0% (10/10)                       | 100.0% (7/7)                | 50.0% (2/4)                            | 100.0% (8/8)                     | 100.0% (10/10)        | 71.4% (5/7)                                         |
| 检查项38      | 必须读取writing_log.md了解前文内容                       | memory_management        | log_file_usage                 | 90.0% (9/10)                         | 85.7% (6/7)                 | 25.0% (1/4)                            | 62.5% (5/8)                      | 40.0% (4/10)          | 14.3% (1/7)                                         |
| 检查项39      | 总字数应在108000-132000之间（基于query要求120000，±10%浮动）   | business_rule_compliance | range_constraint               | 40.0% (4/10)                         | 42.9% (3/7)                 | 25.0% (1/4)                            | 0.0% (0/8)                       | 0.0% (0/10)           | 0.0% (0/7)                                          |
| 检查项40      | 实际内容必须是热血冒险向                                   | content_quality          | emotional_delivery_match       | 90.0% (9/10)                         | 71.4% (5/7)                 | 25.0% (1/4)                            | 62.5% (5/8)                      | 60.0% (6/10)          | 28.6% (2/7)                                         |
| 检查项41      | 核心关系线不能是恋爱                                     | content_quality          | emotional_delivery_match       | 44.4% (4/9)                          | 83.3% (5/6)                 | 50.0% (2/4)                            | 50.0% (4/8)                      | 44.4% (4/9)           | 33.3% (2/6)                                         |
| 检查项42      | 文笔风格必须与题材类型匹配                                  | content_quality          | narrative_tone_match           | 55.6% (5/9)                          | 83.3% (5/6)                 | 50.0% (2/4)                            | 75.0% (6/8)                      | 22.2% (2/9)           | 33.3% (2/6)                                         |
| 检查项43      | 文笔风格必须与题材类型匹配                                  | content_quality          | narrative_tone_match           | 100.0% (1/1)                         | 100.0% (1/1)                | 100.0% (1/1)                           | 0.0% (0/0)                       | 100.0% (1/1)          | 0.0% (0/1)                                          |


## 5. 逻辑硬伤细分分析 (logical_contradiction)

**说明**：从 check_result 的 `flaws` 结构化字段提取。需要使用新版 judge prompt + checker 的评测数据才有此数据。

### 5.1 各模型逻辑硬伤总览

| model                                   |   fail_samples |   total_flaws |   avg_flaws_per_fail | has_structured_data   |
|:----------------------------------------|---------------:|--------------:|---------------------:|:----------------------|
| claude-opus-4-5-20251101                |             10 |            33 |                  3.7 | 9/10                  |
| claude-opus-4-6                         |              6 |             8 |                  2.7 | 3/6                   |
| ernie-5.0-thinking-preview              |              4 |             7 |                  3.5 | 2/4                   |
| gemini-3-pro-preview                    |              7 |            15 |                  3   | 5/7                   |
| kimi-k2.5                               |             10 |            46 |                  5.1 | 9/10                  |
| openai_EB5-0209-A35B-midtrain-128k-chat |              7 |            16 |                  4   | 4/7                   |


### 5.2 硬伤类型分布

| model                                   | 客观事实矛盾   | 世界观不自洽   | 时空转换断链   |
|:----------------------------------------|:---------|:---------|:---------|
| claude-opus-4-5-20251101                | 21 (64%) | 6 (18%)  | 6 (18%)  |
| claude-opus-4-6                         | 5 (62%)  | 1 (12%)  | 2 (25%)  |
| ernie-5.0-thinking-preview              | 3 (43%)  | 2 (29%)  | 2 (29%)  |
| gemini-3-pro-preview                    | 10 (67%) | 3 (20%)  | 2 (13%)  |
| kimi-k2.5                               | 33 (72%) | 7 (15%)  | 6 (13%)  |
| openai_EB5-0209-A35B-midtrain-128k-chat | 8 (50%)  | 5 (31%)  | 3 (19%)  |


### 5.3 严重程度分布

| model                                   | 致命(critical)   | 严重(major)   | 轻微(minor)   |
|:----------------------------------------|:---------------|:------------|:------------|
| claude-opus-4-5-20251101                | 8 (24%)        | 24 (73%)    | 1 (3%)      |
| claude-opus-4-6                         | 0 (0%)         | 6 (75%)     | 2 (25%)     |
| ernie-5.0-thinking-preview              | 1 (14%)        | 6 (86%)     | 0 (0%)      |
| gemini-3-pro-preview                    | 2 (13%)        | 12 (80%)    | 1 (7%)      |
| kimi-k2.5                               | 10 (22%)       | 35 (76%)    | 1 (2%)      |
| openai_EB5-0209-A35B-midtrain-128k-chat | 4 (25%)        | 12 (75%)    | 0 (0%)      |

