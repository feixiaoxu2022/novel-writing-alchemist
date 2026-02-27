# Novel Writing Alchemist 评测统计报告

- **模型**: `doubao-seed-2-0-pro-260215`
- **生成时间**: 2026-02-27T11:42:25.349696
- **评测目录**: `eval_dsv2_20260215_110711_doubao-seed-2-0-pro-260215`
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
| 加权总分 | 74.44 | 50.32 | 88.70 | 15 |
| 内容分(x0.7) | 71.74 | 48.31 | 89.57 | 15 |
| 过程分(x0.3) | 80.75 | 55.00 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 56 | 4 | 0 | 93.3% |
| 业务规则遵循 | 256 | 183 | 73 | 55 | 71.5% |
| 记忆管理 | 20 | 16 | 4 | 10 | 80.0% |

### 2.2 内容创作质量

- **平均内容分**: 71.74 (范围: 48.31 ~ 89.57)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 298 | 230 | 68 | 5 | 77.2% |
| Advanced(优秀) | 165 | 104 | 61 | 15 | 63.0% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 41 | 4 | 0 | 91.1% |
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| enum_validity | 30 | 6 | 24 | 0 | 20.0% |
| quantity_constraint | 30 | 6 | 24 | 0 | 20.0% |
| range_constraint | 15 | 5 | 10 | 0 | 33.3% |
| required_skill_reading | 130 | 74 | 11 | 45 | 87.1% |
| sop_compliance | 31 | 19 | 2 | 10 | 90.5% |
| output_completeness | 60 | 58 | 2 | 0 | 96.7% |
| workspace_file_compliance | 15 | 15 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 6 | 4 | 5 | 60.0% |
| log_file_creation | 15 | 10 | 0 | 5 | 100.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_outline | 15 | 8 | 4 | 3 | 66.7% |
| character_presence_in_chapters | 15 | 11 | 3 | 1 | 78.6% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 0 | 15 | 0 | 0.0% |
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| outline_structure_completeness | 15 | 1 | 14 | 0 | 6.7% |
| dialogue_character_distinction | 15 | 2 | 13 | 0 | 13.3% |
| genre_fit | 15 | 5 | 10 | 0 | 33.3% |
| structural_logic_defect | 15 | 6 | 9 | 0 | 40.0% |
| outline_execution_fidelity | 15 | 7 | 8 | 0 | 46.7% |
| semantic_redundancy | 15 | 8 | 7 | 0 | 53.3% |
| narrative_tone_match | 15 | 9 | 6 | 0 | 60.0% |
| character_arc_design | 15 | 9 | 6 | 0 | 60.0% |
| puzzle_logic_validity | 15 | 10 | 5 | 0 | 66.7% |
| pacing_rationality_advanced | 15 | 10 | 5 | 0 | 66.7% |
| late_stage_digression | 15 | 11 | 4 | 0 | 73.3% |
| hook_design | 15 | 11 | 4 | 0 | 73.3% |
| emotional_delivery_match | 16 | 12 | 4 | 0 | 75.0% |
| character_design_adherence | 17 | 13 | 4 | 0 | 76.5% |
| narrative_density | 15 | 12 | 3 | 0 | 80.0% |
| structural_design | 15 | 12 | 3 | 0 | 80.0% |
| outline_narrative_tension | 15 | 13 | 2 | 0 | 86.7% |
| chapter_length_stability | 15 | 9 | 1 | 5 | 90.0% |
| theme_consistency | 15 | 14 | 1 | 0 | 93.3% |
| main_character_consistency | 15 | 14 | 1 | 0 | 93.3% |
| character_trait_consistency | 15 | 14 | 1 | 0 | 93.3% |
| full_narrative_content | 15 | 14 | 1 | 0 | 93.3% |
| repeated_endings | 15 | 14 | 1 | 0 | 93.3% |
| character_relationship_design | 15 | 14 | 1 | 0 | 93.3% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| chapter_cloning | 15 | 10 | 0 | 5 | 100.0% |
| alternating_repetition | 15 | 10 | 0 | 5 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| language_purity | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| character_motivation_design | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 15 | 0 | 0 | 100% (15/15) |
| characters格式 | structural_integrity | - | 14 | 1 | 0 | 93% (14/15) |
| creative_intent格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
| outline格式 | structural_integrity | - | 12 | 3 | 0 | 80% (12/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 3 | 12 | 0 | 20% (3/15) |
| Y轴标签枚举 | enum_validity | - | 3 | 12 | 0 | 20% (3/15) |
| chapters目录存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| outline文件存在性 | output_completeness | - | 13 | 2 | 0 | 87% (13/15) |
| Y轴标签数量 | quantity_constraint | - | 3 | 12 | 0 | 20% (3/15) |
| forbidden_elements存在性 | quantity_constraint | - | 3 | 12 | 0 | 20% (3/15) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 0 | 2 | 0 | 0% (0/2) |
| 超短篇字数 | range_constraint | - | 5 | 0 | 0 | 100% (5/5) |
| 读取characters的schema | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取creative_intent的schema | required_skill_reading | - | 1 | 9 | 5 | 10% (1/10) |
| 读取outline的schema | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取写作技巧指南 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取命名skill | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取大纲设计指南 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取感情线写作指南 | required_skill_reading | - | 3 | 2 | 0 | 60% (3/5) |
| 读取短篇skill | required_skill_reading | - | 0 | 0 | 5 | skip(5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取配方知识库 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 写作准备确认 | sop_compliance | - | 9 | 1 | 5 | 90% (9/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| workspace文件规范 | workspace_file_compliance | basic | 15 | 0 | 0 | 100% (15/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 10 | 0 | 5 | 100% (10/10) |
| writing_log文件读取 | log_file_usage | - | 6 | 4 | 5 | 60% (6/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 11 | 3 | 1 | 79% (11/14) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 8 | 4 | 3 | 67% (8/12) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 10 | 0 | 5 | 100% (10/10) |
| 章节克隆检测 | chapter_cloning | gate | 10 | 0 | 5 | 100% (10/10) |
| 章节完成度 | chapter_completion | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 9 | 1 | 5 | 90% (9/10) |
| 章节产出存在性 | chapter_output_existence | gate | 15 | 0 | 0 | 100% (15/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 9 | 6 | 0 | 60% (9/15) |
| 人物设计遵循度 | character_design_adherence | basic | 13 | 2 | 0 | 87% (13/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 15 | 0 | 0 | 100% (15/15) |
| 角色命名质量 | character_naming_quality | advanced | 1 | 14 | 0 | 7% (1/15) |
| 角色关系设计张力 | character_relationship_design | basic | 14 | 1 | 0 | 93% (14/15) |
| 人物设定一致性 | character_trait_consistency | basic | 14 | 1 | 0 | 93% (14/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 2 | 13 | 0 | 13% (2/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 1 | 1 | 0 | 50% (1/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 6 | 1 | 0 | 86% (6/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感弧线层次 | emotional_gradient | advanced | 15 | 0 | 0 | 100% (15/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 0 | 15 | 0 | 0% (0/15) |
| 完整叙事文本 | full_narrative_content | basic | 14 | 1 | 0 | 93% (14/15) |
| 题材契合度 | genre_fit | advanced | 5 | 10 | 0 | 33% (5/15) |
| 钩子设计 | hook_design | advanced | 11 | 4 | 0 | 73% (11/15) |
| 意象系统 | imagery_system | advanced | 15 | 0 | 0 | 100% (15/15) |
| 语言纯净性 | language_purity | basic | 15 | 0 | 0 | 100% (15/15) |
| 后期章节跑偏 | late_stage_digression | basic | 11 | 4 | 0 | 73% (11/15) |
| 主要角色一致性 | main_character_consistency | basic | 14 | 1 | 0 | 93% (14/15) |
| 叙事密度 | narrative_density | advanced | 12 | 3 | 0 | 80% (12/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 9 | 6 | 0 | 60% (9/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 7 | 8 | 0 | 47% (7/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 13 | 2 | 0 | 87% (13/15) |
| outline结构完整性 | outline_structure_completeness | basic | 1 | 14 | 0 | 7% (1/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 10 | 5 | 0 | 67% (10/15) |
| 段落重复检测 | paragraph_repetition | basic | 15 | 0 | 0 | 100% (15/15) |
| 情节推进 | plot_progression | basic | 15 | 0 | 0 | 100% (15/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 10 | 5 | 0 | 67% (10/15) |
| 反复结局 | repeated_endings | basic | 14 | 1 | 0 | 93% (14/15) |
| 语义重复检测 | semantic_redundancy | basic | 8 | 7 | 0 | 53% (8/15) |
| 结构功能性 | structural_design | advanced | 12 | 3 | 0 | 80% (12/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 6 | 9 | 0 | 40% (6/15) |
| 主题一致性 | theme_consistency | basic | 14 | 1 | 0 | 93% (14/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 71.46 | 50.32 | 80.62 |
| IP | 1 | 63.59 | 63.59 | 63.59 |
| VAGUE | 1 | 73.60 | 73.60 | 73.60 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 81.56 | 75.35 | 88.70 |
| SHORT | 2 | 76.78 | 72.93 | 80.62 |
| MEDIUM | 8 | 69.41 | 50.32 | 80.12 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 69.02 | 69.02 | 69.02 |
| ANGSTY | 7 | 78.86 | 71.32 | 88.70 |
| BRAINY_ACTION | 1 | 71.41 | 71.41 | 71.41 |
| HEROINE | 1 | 80.12 | 80.12 | 80.12 |
| NEUTRAL | 1 | 63.59 | 63.59 | 63.59 |
| SUSPENSE | 1 | 50.32 | 50.32 | 50.32 |
| SWEET | 2 | 78.28 | 75.93 | 80.62 |
| SWEET_DRAMA | 1 | 73.60 | 73.60 | 73.60 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `读取creative_intent的schema`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `X轴模式ID格式`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `Y轴标签枚举`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `Y轴标签数量`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `forbidden_elements存在性`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现1处structural类型逻辑问题: 遗骨/遗体处理形态前后矛盾：第12章在议事厅发现“两具遗骨”，第13章已将遗骨“包好放进专门的收纳袋里背走”，但第17章追悼会后又写“陈峰把父亲的骨灰葬在公墓里…并把铜牌放在骨灰盒旁边”“林砚把父亲的骨灰带回了家”。此前未交代遗骨如何被合法火化、何时火化、

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现2处fixable类型逻辑问题: 高原反应相关海拔数值前后冲突：第6章明确“这里海拔3600”，第9章又写“海拔已经升到了三千二百米”，但叙事上第9章发生在之后的行进过程中，海拔应大致不降反升或需解释为何下降（如绕行下切到河谷）。; 队伍人数在连续章节中不一致：第11章进入溶洞队伍为4人（陈峰、

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `完整叙事文本`
  - 子类: full_narrative_content, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事调性匹配`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `后期章节跑偏`
  - 子类: late_stage_digression, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 张正国）

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 王磊（王胖子））

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 王磊（王胖子））

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 乔治·史密斯）

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 乔治·史密斯）

### 记忆管理 (4个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 格式规范遵循 (4个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_003** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_004** / `characters格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_005** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整
