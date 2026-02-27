# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-6`
- **生成时间**: 2026-02-27T11:42:24.284303
- **评测目录**: `eval_dsv2_20260211_204123_claude-opus-4-6`
- **Revision**: `rev009` (实际: check_result_rev009.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 14 |
| 执行错误 | 1 |
| 有checker结果 | 15 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 85.09 | 17.38 | 96.83 | 15 |
| 内容分(x0.7) | 83.47 | 9.35 | 96.36 | 15 |
| 过程分(x0.3) | 88.86 | 36.11 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 2 | 13.3% |
| unqualified | 13 | 86.7% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 56 | 4 | 0 | 93.3% |
| 业务规则遵循 | 171 | 149 | 22 | 140 | 87.1% |
| 记忆管理 | 20 | 17 | 3 | 10 | 85.0% |

### 2.2 内容创作质量

- **平均内容分**: 83.47 (范围: 9.35 ~ 96.36)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 298 | 256 | 42 | 5 | 85.9% |
| Advanced(优秀) | 165 | 131 | 34 | 15 | 79.4% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 15 | 14 | 1 | 0 | 93.3% |
| structural_integrity | 45 | 42 | 3 | 0 | 93.3% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| required_skill_reading | 130 | 0 | 0 | 130 | 0.0% |
| workspace_file_compliance | 15 | 6 | 9 | 0 | 40.0% |
| range_constraint | 15 | 6 | 9 | 0 | 40.0% |
| sop_compliance | 31 | 19 | 2 | 10 | 90.5% |
| output_completeness | 60 | 58 | 2 | 0 | 96.7% |
| enum_validity | 30 | 30 | 0 | 0 | 100.0% |
| quantity_constraint | 30 | 30 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 8 | 2 | 5 | 80.0% |
| log_file_creation | 15 | 9 | 1 | 5 | 90.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 12 | 2 | 1 | 85.7% |
| character_presence_in_outline | 15 | 13 | 1 | 1 | 92.9% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 1 | 14 | 0 | 6.7% |
| structural_logic_defect | 15 | 9 | 6 | 0 | 60.0% |
| dialogue_character_distinction | 15 | 9 | 6 | 0 | 60.0% |
| character_naming_quality | 15 | 9 | 6 | 0 | 60.0% |
| semantic_redundancy | 15 | 10 | 5 | 0 | 66.7% |
| emotional_delivery_match | 16 | 11 | 5 | 0 | 68.8% |
| outline_structure_completeness | 15 | 11 | 4 | 0 | 73.3% |
| chapter_length_stability | 15 | 8 | 2 | 5 | 80.0% |
| narrative_tone_match | 15 | 12 | 3 | 0 | 80.0% |
| late_stage_digression | 15 | 12 | 3 | 0 | 80.0% |
| hook_design | 15 | 12 | 3 | 0 | 80.0% |
| character_arc_design | 15 | 12 | 3 | 0 | 80.0% |
| plot_progression | 15 | 13 | 2 | 0 | 86.7% |
| genre_fit | 15 | 13 | 2 | 0 | 86.7% |
| character_design_adherence | 17 | 15 | 2 | 0 | 88.2% |
| alternating_repetition | 15 | 9 | 1 | 5 | 90.0% |
| chapter_output_existence | 15 | 14 | 1 | 0 | 93.3% |
| chapter_cloning | 15 | 14 | 1 | 0 | 93.3% |
| chapter_completion | 15 | 14 | 1 | 0 | 93.3% |
| paragraph_repetition | 15 | 14 | 1 | 0 | 93.3% |
| theme_consistency | 15 | 14 | 1 | 0 | 93.3% |
| main_character_consistency | 15 | 14 | 1 | 0 | 93.3% |
| character_trait_consistency | 15 | 14 | 1 | 0 | 93.3% |
| language_purity | 15 | 14 | 1 | 0 | 93.3% |
| full_narrative_content | 15 | 14 | 1 | 0 | 93.3% |
| repeated_endings | 15 | 14 | 1 | 0 | 93.3% |
| outline_execution_fidelity | 15 | 14 | 1 | 0 | 93.3% |
| narrative_density | 15 | 14 | 1 | 0 | 93.3% |
| puzzle_logic_validity | 15 | 14 | 1 | 0 | 93.3% |
| pacing_rationality_advanced | 15 | 14 | 1 | 0 | 93.3% |
| imagery_system | 15 | 14 | 1 | 0 | 93.3% |
| emotional_gradient | 15 | 14 | 1 | 0 | 93.3% |
| structural_design | 15 | 14 | 1 | 0 | 93.3% |
| character_relationship_design | 15 | 14 | 1 | 0 | 93.3% |
| outline_narrative_tension | 15 | 14 | 1 | 0 | 93.3% |
| character_motivation_design | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 14 | 1 | 0 | 93% (14/15) |
| characters格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent格式 | structural_integrity | - | 13 | 2 | 0 | 87% (13/15) |
| outline格式 | structural_integrity | - | 14 | 1 | 0 | 93% (14/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 15 | 0 | 0 | 100% (15/15) |
| Y轴标签枚举 | enum_validity | - | 15 | 0 | 0 | 100% (15/15) |
| chapters目录存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| outline文件存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| Y轴标签数量 | quantity_constraint | - | 15 | 0 | 0 | 100% (15/15) |
| forbidden_elements存在性 | quantity_constraint | - | 15 | 0 | 0 | 100% (15/15) |
| 中篇字数 | range_constraint | - | 2 | 3 | 0 | 40% (2/5) |
| 中篇字数_冒险 | range_constraint | - | 1 | 0 | 0 | 100% (1/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 1 | 0 | 0 | 100% (1/1) |
| 短篇字数 | range_constraint | - | 0 | 2 | 0 | 0% (0/2) |
| 超短篇字数 | range_constraint | - | 2 | 3 | 0 | 40% (2/5) |
| 读取characters的schema | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取creative_intent的schema | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取outline的schema | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取写作技巧指南 | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取命名skill | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取大纲设计指南 | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取感情线写作指南 | required_skill_reading | - | 0 | 0 | 5 | skip(5) |
| 读取短篇skill | required_skill_reading | - | 0 | 0 | 5 | skip(5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 读取配方知识库 | required_skill_reading | - | 0 | 0 | 15 | skip(15) |
| 写作准备确认 | sop_compliance | - | 9 | 1 | 5 | 90% (9/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| workspace文件规范 | workspace_file_compliance | basic | 6 | 9 | 0 | 40% (6/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 9 | 1 | 5 | 90% (9/10) |
| writing_log文件读取 | log_file_usage | - | 8 | 2 | 5 | 80% (8/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 12 | 2 | 1 | 86% (12/14) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 13 | 1 | 1 | 93% (13/14) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 9 | 1 | 5 | 90% (9/10) |
| 章节克隆检测 | chapter_cloning | gate | 14 | 1 | 0 | 93% (14/15) |
| 章节完成度 | chapter_completion | gate | 14 | 1 | 0 | 93% (14/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 8 | 2 | 5 | 80% (8/10) |
| 章节产出存在性 | chapter_output_existence | gate | 14 | 1 | 0 | 93% (14/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 12 | 3 | 0 | 80% (12/15) |
| 人物设计遵循度 | character_design_adherence | basic | 14 | 1 | 0 | 93% (14/15) |
| 反套路检查 | character_design_adherence | basic | 1 | 0 | 0 | 100% (1/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 15 | 0 | 0 | 100% (15/15) |
| 角色命名质量 | character_naming_quality | advanced | 9 | 6 | 0 | 60% (9/15) |
| 角色关系设计张力 | character_relationship_design | basic | 14 | 1 | 0 | 93% (14/15) |
| 人物设定一致性 | character_trait_consistency | basic | 14 | 1 | 0 | 93% (14/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 9 | 6 | 0 | 60% (9/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 0 | 2 | 0 | 0% (0/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 6 | 1 | 0 | 86% (6/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 14 | 1 | 0 | 93% (14/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 1 | 14 | 0 | 7% (1/15) |
| 完整叙事文本 | full_narrative_content | basic | 14 | 1 | 0 | 93% (14/15) |
| 题材契合度 | genre_fit | advanced | 13 | 2 | 0 | 87% (13/15) |
| 钩子设计 | hook_design | advanced | 12 | 3 | 0 | 80% (12/15) |
| 意象系统 | imagery_system | advanced | 14 | 1 | 0 | 93% (14/15) |
| 语言纯净性 | language_purity | basic | 14 | 1 | 0 | 93% (14/15) |
| 后期章节跑偏 | late_stage_digression | basic | 12 | 3 | 0 | 80% (12/15) |
| 主要角色一致性 | main_character_consistency | basic | 14 | 1 | 0 | 93% (14/15) |
| 叙事密度 | narrative_density | advanced | 14 | 1 | 0 | 93% (14/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 12 | 3 | 0 | 80% (12/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 14 | 1 | 0 | 93% (14/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 14 | 1 | 0 | 93% (14/15) |
| outline结构完整性 | outline_structure_completeness | basic | 11 | 4 | 0 | 73% (11/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 14 | 1 | 0 | 93% (14/15) |
| 段落重复检测 | paragraph_repetition | basic | 14 | 1 | 0 | 93% (14/15) |
| 情节推进 | plot_progression | basic | 13 | 2 | 0 | 87% (13/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 14 | 1 | 0 | 93% (14/15) |
| 反复结局 | repeated_endings | basic | 14 | 1 | 0 | 93% (14/15) |
| 语义重复检测 | semantic_redundancy | basic | 10 | 5 | 0 | 67% (10/15) |
| 结构功能性 | structural_design | advanced | 14 | 1 | 0 | 93% (14/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 9 | 6 | 0 | 60% (9/15) |
| 主题一致性 | theme_consistency | basic | 14 | 1 | 0 | 93% (14/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 82.51 | 17.38 | 96.83 |
| IP | 1 | 90.25 | 90.25 | 90.25 |
| VAGUE | 1 | 87.32 | 87.32 | 87.32 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 87.73 | 80.35 | 91.70 |
| SHORT | 2 | 86.69 | 85.58 | 87.80 |
| MEDIUM | 8 | 83.04 | 17.38 | 96.83 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 96.83 | 96.83 | 96.83 |
| ANGSTY | 7 | 88.42 | 80.35 | 94.73 |
| BRAINY_ACTION | 1 | 94.83 | 94.83 | 94.83 |
| HEROINE | 1 | 17.38 | 17.38 | 17.38 |
| NEUTRAL | 1 | 90.25 | 90.25 | 90.25 |
| SUSPENSE | 1 | 90.96 | 90.96 | 90.96 |
| SWEET | 2 | 89.90 | 87.80 | 92.00 |
| SWEET_DRAMA | 1 | 87.32 | 87.32 | 87.32 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现4处fixable类型逻辑问题: 时间线/天数冲突：第6章开头写“进山第四天”，但第7章写“第五天下午三点左右”，第9章写“进山第六天/第七天中午到垭口”。若第6章确为第4天且洪水“退了六个小时”后应仍在第4天/第5天初，后续天数推进与叙述的具体事件顺序存在明显错位。; 犬只伤腿状态前后矛盾：第

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现3处fixable类型逻辑问题: 第8章结尾明确当晚尚未到23:00且两人上床“今晚不会”睡；第9章开头却直接写“现在是凌晨一点四十三分”，中间缺少任何时间推进交代，属于同一连续场景的时间跳跃断链。; 系统倒计时与现实时间线出现无法同时成立的冲突：按第1章07:08距23:00应约15:52；第

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `语义重复检测`
  - 子类: semantic_redundancy, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色命名质量`
  - 子类: character_naming_quality, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现2处structural类型逻辑问题: 同一人物（许芸）的“先驱者编号”前后互相矛盾：chapter_07 的“先驱者名单”中写“003，许芸”，而 chapter_17 的“先驱者转移计划·第一批”目标名单中写“003——许芸”。与此同时，chapter_07 的同表格示例还出现“001李岱山

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['outline_act3.json', 'outline_act2_part2.json', 'outline_act2_part1.json']

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['tmp_outline']

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['outline_act3_part2.json', 'outline_act2_part2.json', 'outline_act2_part1.json', 'outline_act2_part3.json', 'outline_act23_draft

- **NW_CLEAR_MEDIUM_HEROINE_001** / `写作准备确认`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `outline文件存在性`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

### 格式规范遵循 (4个失败检查)

- **NW_CLEAR_MEDIUM_HEROINE_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_004** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (3个失败检查)

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 数据一致性 (3个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 温既白的母亲（温母））

- **NW_CLEAR_SHORT_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 温既白的母亲（温母））

- **NW_IP_MEDIUM_NEUTRAL_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（主角: 张麻子（约翰·马斯顿）; 配角: 黄四郎替身）
