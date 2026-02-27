# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-5-20251101`
- **生成时间**: 2026-02-27T11:42:24.788049
- **评测目录**: `eval_dsv2_20260211_122519_claude-opus-4-5-20251101`
- **Revision**: `rev009` (实际: check_result_rev009.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 15 |
| 执行错误 | 0 |
| 有checker结果 | 15 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 82.71 | 71.98 | 90.53 | 15 |
| 内容分(x0.7) | 81.77 | 74.26 | 90.05 | 15 |
| 过程分(x0.3) | 84.91 | 64.58 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 55 | 5 | 0 | 91.7% |
| 业务规则遵循 | 171 | 152 | 19 | 140 | 88.9% |
| 记忆管理 | 20 | 19 | 1 | 10 | 95.0% |

### 2.2 内容创作质量

- **平均内容分**: 81.77 (范围: 74.26 ~ 90.05)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 298 | 252 | 46 | 5 | 84.6% |
| Advanced(优秀) | 165 | 128 | 37 | 15 | 77.6% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 40 | 5 | 0 | 88.9% |
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| required_skill_reading | 130 | 0 | 0 | 130 | 0.0% |
| workspace_file_compliance | 15 | 6 | 9 | 0 | 40.0% |
| range_constraint | 15 | 9 | 6 | 0 | 60.0% |
| sop_compliance | 31 | 17 | 4 | 10 | 81.0% |
| enum_validity | 30 | 30 | 0 | 0 | 100.0% |
| quantity_constraint | 30 | 30 | 0 | 0 | 100.0% |
| output_completeness | 60 | 60 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 9 | 1 | 5 | 90.0% |
| log_file_creation | 15 | 10 | 0 | 5 | 100.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_outline | 15 | 9 | 6 | 0 | 60.0% |
| character_presence_in_chapters | 15 | 10 | 5 | 0 | 66.7% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 1 | 14 | 0 | 6.7% |
| dialogue_character_distinction | 15 | 4 | 11 | 0 | 26.7% |
| semantic_redundancy | 15 | 5 | 10 | 0 | 33.3% |
| structural_logic_defect | 15 | 7 | 8 | 0 | 46.7% |
| character_naming_quality | 15 | 7 | 8 | 0 | 46.7% |
| outline_execution_fidelity | 15 | 8 | 7 | 0 | 53.3% |
| character_arc_design | 15 | 10 | 5 | 0 | 66.7% |
| outline_structure_completeness | 15 | 10 | 5 | 0 | 66.7% |
| narrative_tone_match | 15 | 11 | 4 | 0 | 73.3% |
| puzzle_logic_validity | 15 | 12 | 3 | 0 | 80.0% |
| genre_fit | 15 | 12 | 3 | 0 | 80.0% |
| pacing_rationality_advanced | 15 | 12 | 3 | 0 | 80.0% |
| repeated_endings | 15 | 13 | 2 | 0 | 86.7% |
| late_stage_digression | 15 | 13 | 2 | 0 | 86.7% |
| chapter_length_stability | 15 | 9 | 1 | 5 | 90.0% |
| full_narrative_content | 15 | 14 | 1 | 0 | 93.3% |
| structural_design | 15 | 14 | 1 | 0 | 93.3% |
| character_relationship_design | 15 | 14 | 1 | 0 | 93.3% |
| emotional_delivery_match | 16 | 15 | 1 | 0 | 93.8% |
| character_design_adherence | 17 | 16 | 1 | 0 | 94.1% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| chapter_cloning | 15 | 15 | 0 | 0 | 100.0% |
| alternating_repetition | 15 | 10 | 0 | 5 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| character_trait_consistency | 15 | 15 | 0 | 0 | 100.0% |
| language_purity | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| narrative_density | 15 | 15 | 0 | 0 | 100.0% |
| hook_design | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| character_motivation_design | 15 | 15 | 0 | 0 | 100.0% |
| outline_narrative_tension | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 15 | 0 | 0 | 100% (15/15) |
| characters格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent格式 | structural_integrity | - | 10 | 5 | 0 | 67% (10/15) |
| outline格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 15 | 0 | 0 | 100% (15/15) |
| Y轴标签枚举 | enum_validity | - | 15 | 0 | 0 | 100% (15/15) |
| chapters目录存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| outline文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| Y轴标签数量 | quantity_constraint | - | 15 | 0 | 0 | 100% (15/15) |
| forbidden_elements存在性 | quantity_constraint | - | 15 | 0 | 0 | 100% (15/15) |
| 中篇字数 | range_constraint | - | 4 | 1 | 0 | 80% (4/5) |
| 中篇字数_冒险 | range_constraint | - | 1 | 0 | 0 | 100% (1/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 1 | 0 | 0 | 100% (1/1) |
| 短篇字数 | range_constraint | - | 1 | 1 | 0 | 50% (1/2) |
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
| 写作准备确认 | sop_compliance | - | 7 | 3 | 5 | 70% (7/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| workspace文件规范 | workspace_file_compliance | basic | 6 | 9 | 0 | 40% (6/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 10 | 0 | 5 | 100% (10/10) |
| writing_log文件读取 | log_file_usage | - | 9 | 1 | 5 | 90% (9/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 10 | 5 | 0 | 67% (10/15) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 9 | 6 | 0 | 60% (9/15) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 10 | 0 | 5 | 100% (10/10) |
| 章节克隆检测 | chapter_cloning | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节完成度 | chapter_completion | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 9 | 1 | 5 | 90% (9/10) |
| 章节产出存在性 | chapter_output_existence | gate | 15 | 0 | 0 | 100% (15/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 10 | 5 | 0 | 67% (10/15) |
| 人物设计遵循度 | character_design_adherence | basic | 15 | 0 | 0 | 100% (15/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 1 | 0 | 0 | 100% (1/1) |
| 角色动机设计深度 | character_motivation_design | basic | 15 | 0 | 0 | 100% (15/15) |
| 角色命名质量 | character_naming_quality | advanced | 7 | 8 | 0 | 47% (7/15) |
| 角色关系设计张力 | character_relationship_design | basic | 14 | 1 | 0 | 93% (14/15) |
| 人物设定一致性 | character_trait_consistency | basic | 15 | 0 | 0 | 100% (15/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 4 | 11 | 0 | 27% (4/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 2 | 0 | 0 | 100% (2/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 6 | 1 | 0 | 86% (6/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 15 | 0 | 0 | 100% (15/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 1 | 14 | 0 | 7% (1/15) |
| 完整叙事文本 | full_narrative_content | basic | 14 | 1 | 0 | 93% (14/15) |
| 题材契合度 | genre_fit | advanced | 12 | 3 | 0 | 80% (12/15) |
| 钩子设计 | hook_design | advanced | 15 | 0 | 0 | 100% (15/15) |
| 意象系统 | imagery_system | advanced | 15 | 0 | 0 | 100% (15/15) |
| 语言纯净性 | language_purity | basic | 15 | 0 | 0 | 100% (15/15) |
| 后期章节跑偏 | late_stage_digression | basic | 13 | 2 | 0 | 87% (13/15) |
| 主要角色一致性 | main_character_consistency | basic | 15 | 0 | 0 | 100% (15/15) |
| 叙事密度 | narrative_density | advanced | 15 | 0 | 0 | 100% (15/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 11 | 4 | 0 | 73% (11/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 8 | 7 | 0 | 53% (8/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 15 | 0 | 0 | 100% (15/15) |
| outline结构完整性 | outline_structure_completeness | basic | 10 | 5 | 0 | 67% (10/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 12 | 3 | 0 | 80% (12/15) |
| 段落重复检测 | paragraph_repetition | basic | 15 | 0 | 0 | 100% (15/15) |
| 情节推进 | plot_progression | basic | 15 | 0 | 0 | 100% (15/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 12 | 3 | 0 | 80% (12/15) |
| 反复结局 | repeated_endings | basic | 13 | 2 | 0 | 87% (13/15) |
| 语义重复检测 | semantic_redundancy | basic | 5 | 10 | 0 | 33% (5/15) |
| 结构功能性 | structural_design | advanced | 14 | 1 | 0 | 93% (14/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 7 | 8 | 0 | 47% (7/15) |
| 主题一致性 | theme_consistency | basic | 15 | 0 | 0 | 100% (15/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 80.25 | 75.89 | 87.99 |
| IP | 1 | 71.98 | 71.98 | 71.98 |
| VAGUE | 1 | 89.56 | 89.56 | 89.56 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 87.42 | 82.19 | 90.53 |
| SHORT | 2 | 77.62 | 77.31 | 77.94 |
| MEDIUM | 8 | 81.04 | 71.98 | 89.56 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 81.99 | 81.99 | 81.99 |
| ANGSTY | 7 | 84.42 | 75.89 | 90.53 |
| BRAINY_ACTION | 1 | 80.03 | 80.03 | 80.03 |
| HEROINE | 1 | 84.49 | 84.49 | 84.49 |
| NEUTRAL | 1 | 71.98 | 71.98 | 71.98 |
| SUSPENSE | 1 | 76.36 | 76.36 | 76.36 |
| SWEET | 2 | 82.65 | 77.31 | 87.99 |
| SWEET_DRAMA | 1 | 89.56 | 89.56 | 89.56 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现5处fixable类型逻辑问题: 玉佩状态前后矛盾：第8章阿依莫将玉佩“拿走/收走”；第9章结尾却写“秦北望从口袋里掏出那枚玉佩，放在手心里看”，中间无任何归还/取回交代。; 玉佩去向前后矛盾：第10章老头人把玉佩“重新放到秦北望手里/还给他”，后续多章持续佩戴；但第17章第5节又写“从脖子上取

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `大纲执行忠实度`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `智斗逻辑合理性`
  - 子类: puzzle_logic_validity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `题材契合度`
  - 子类: genre_fit, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色成长弧线设计`
  - 子类: character_arc_design, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['temp_act_two.json', 'temp_act_three.json', 'outline_act_two_partial.json', 'build_outline.py', 'merge_all_outline.py', 'outline

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['outline_act2_ch21_22.json', 'outline_act3.json', 'outline_act2_ch15_16.json', 'outline_act2_ch19_20.json', 'outline_act2_ch13_1

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `写作准备确认`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['outline_act_three.json', 'outline_act_two.json']

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 阿依莫, 马崇山, 格桑）

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 陆沉母亲（陆雁））

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 陆沉母亲（陆雁）, 审判者组织）

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 陈焕, 赵砚青, 林幺幺）

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 英国领事馆档案员·霍华德）

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_IP_MEDIUM_NEUTRAL_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_002** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (1个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
