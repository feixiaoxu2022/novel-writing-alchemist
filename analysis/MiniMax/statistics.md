# Novel Writing Alchemist 评测统计报告

- **模型**: `MiniMax-M2.5`
- **生成时间**: 2026-02-27T11:42:27.059961
- **评测目录**: `eval_dsv2_20260224_194949_MiniMax-M2.5`
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
| 加权总分 | 55.48 | 9.55 | 80.99 | 15 |
| 内容分(x0.7) | 54.44 | 3.64 | 86.41 | 15 |
| 过程分(x0.3) | 57.90 | 23.34 | 90.62 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 36 | 24 | 0 | 60.0% |
| 业务规则遵循 | 273 | 206 | 67 | 38 | 75.5% |
| 记忆管理 | 20 | 12 | 8 | 10 | 60.0% |

### 2.2 内容创作质量

- **平均内容分**: 54.44 (范围: 3.64 ~ 86.41)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 299 | 181 | 118 | 4 | 60.5% |
| Advanced(优秀) | 165 | 74 | 91 | 15 | 44.9% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 24 | 21 | 0 | 53.3% |
| naming_convention | 15 | 12 | 3 | 0 | 80.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 2 | 13 | 0 | 13.3% |
| sop_compliance | 31 | 13 | 8 | 10 | 61.9% |
| enum_validity | 30 | 11 | 5 | 14 | 68.8% |
| quantity_constraint | 30 | 12 | 4 | 14 | 75.0% |
| output_completeness | 60 | 45 | 15 | 0 | 75.0% |
| required_skill_reading | 130 | 108 | 22 | 0 | 83.1% |
| workspace_file_compliance | 15 | 15 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 5 | 5 | 5 | 50.0% |
| log_file_creation | 15 | 7 | 3 | 5 | 70.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 2 | 8 | 5 | 20.0% |
| character_presence_in_outline | 15 | 6 | 4 | 5 | 60.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| outline_execution_fidelity | 15 | 2 | 13 | 0 | 13.3% |
| dialogue_character_distinction | 15 | 2 | 13 | 0 | 13.3% |
| genre_fit | 15 | 2 | 13 | 0 | 13.3% |
| character_naming_quality | 15 | 2 | 13 | 0 | 13.3% |
| fixable_logic_inconsistency | 15 | 3 | 12 | 0 | 20.0% |
| structural_logic_defect | 15 | 4 | 11 | 0 | 26.7% |
| narrative_density | 15 | 4 | 11 | 0 | 26.7% |
| pacing_rationality_advanced | 15 | 5 | 10 | 0 | 33.3% |
| semantic_redundancy | 15 | 5 | 10 | 0 | 33.3% |
| narrative_tone_match | 15 | 7 | 8 | 0 | 46.7% |
| puzzle_logic_validity | 15 | 7 | 8 | 0 | 46.7% |
| character_design_adherence | 17 | 8 | 9 | 0 | 47.1% |
| language_purity | 15 | 8 | 7 | 0 | 53.3% |
| late_stage_digression | 15 | 8 | 7 | 0 | 53.3% |
| character_arc_design | 15 | 8 | 7 | 0 | 53.3% |
| full_narrative_content | 15 | 9 | 6 | 0 | 60.0% |
| hook_design | 15 | 9 | 6 | 0 | 60.0% |
| structural_design | 15 | 9 | 6 | 0 | 60.0% |
| emotional_delivery_match | 16 | 10 | 6 | 0 | 62.5% |
| character_trait_consistency | 15 | 10 | 5 | 0 | 66.7% |
| imagery_system | 15 | 10 | 5 | 0 | 66.7% |
| outline_structure_completeness | 15 | 10 | 5 | 0 | 66.7% |
| chapter_length_stability | 15 | 8 | 3 | 4 | 72.7% |
| chapter_completion | 15 | 11 | 4 | 0 | 73.3% |
| repeated_endings | 15 | 11 | 4 | 0 | 73.3% |
| emotional_gradient | 15 | 11 | 4 | 0 | 73.3% |
| outline_narrative_tension | 15 | 11 | 4 | 0 | 73.3% |
| alternating_repetition | 15 | 7 | 2 | 6 | 77.8% |
| paragraph_repetition | 15 | 12 | 3 | 0 | 80.0% |
| main_character_consistency | 15 | 12 | 3 | 0 | 80.0% |
| character_relationship_design | 15 | 12 | 3 | 0 | 80.0% |
| character_motivation_design | 15 | 12 | 3 | 0 | 80.0% |
| chapter_cloning | 15 | 11 | 2 | 2 | 84.6% |
| chapter_output_existence | 15 | 13 | 2 | 0 | 86.7% |
| theme_consistency | 15 | 13 | 2 | 0 | 86.7% |
| plot_progression | 15 | 13 | 2 | 0 | 86.7% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 12 | 3 | 0 | 80% (12/15) |
| characters格式 | structural_integrity | - | 11 | 4 | 0 | 73% (11/15) |
| creative_intent格式 | structural_integrity | - | 7 | 8 | 0 | 47% (7/15) |
| outline格式 | structural_integrity | - | 6 | 9 | 0 | 40% (6/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 5 | 3 | 7 | 62% (5/8) |
| Y轴标签枚举 | enum_validity | - | 6 | 2 | 7 | 75% (6/8) |
| chapters目录存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| characters文件存在性 | output_completeness | - | 12 | 3 | 0 | 80% (12/15) |
| creative_intent文件存在性 | output_completeness | - | 8 | 7 | 0 | 53% (8/15) |
| outline文件存在性 | output_completeness | - | 11 | 4 | 0 | 73% (11/15) |
| Y轴标签数量 | quantity_constraint | - | 6 | 2 | 7 | 75% (6/8) |
| forbidden_elements存在性 | quantity_constraint | - | 6 | 2 | 7 | 75% (6/8) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 1 | 1 | 0 | 50% (1/2) |
| 超短篇字数 | range_constraint | - | 1 | 4 | 0 | 20% (1/5) |
| 读取characters的schema | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取creative_intent的schema | required_skill_reading | - | 7 | 8 | 0 | 47% (7/15) |
| 读取outline的schema | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取写作技巧指南 | required_skill_reading | - | 13 | 2 | 0 | 87% (13/15) |
| 读取命名skill | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取大纲设计指南 | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取感情线写作指南 | required_skill_reading | - | 1 | 4 | 0 | 20% (1/5) |
| 读取短篇skill | required_skill_reading | - | 1 | 4 | 0 | 20% (1/5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 11 | 4 | 0 | 73% (11/15) |
| 读取配方知识库 | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 写作准备确认 | sop_compliance | - | 6 | 4 | 5 | 60% (6/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 7 | 3 | 5 | 70% (7/10) |
| workspace文件规范 | workspace_file_compliance | basic | 15 | 0 | 0 | 100% (15/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 7 | 3 | 5 | 70% (7/10) |
| writing_log文件读取 | log_file_usage | - | 5 | 5 | 5 | 50% (5/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 2 | 8 | 5 | 20% (2/10) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 6 | 4 | 5 | 60% (6/10) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 7 | 2 | 6 | 78% (7/9) |
| 章节克隆检测 | chapter_cloning | gate | 11 | 2 | 2 | 85% (11/13) |
| 章节完成度 | chapter_completion | gate | 11 | 4 | 0 | 73% (11/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 8 | 3 | 4 | 73% (8/11) |
| 章节产出存在性 | chapter_output_existence | gate | 13 | 2 | 0 | 87% (13/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 8 | 7 | 0 | 53% (8/15) |
| 人物设计遵循度 | character_design_adherence | basic | 8 | 7 | 0 | 53% (8/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 12 | 3 | 0 | 80% (12/15) |
| 角色命名质量 | character_naming_quality | advanced | 2 | 13 | 0 | 13% (2/15) |
| 角色关系设计张力 | character_relationship_design | basic | 12 | 3 | 0 | 80% (12/15) |
| 人物设定一致性 | character_trait_consistency | basic | 10 | 5 | 0 | 67% (10/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 2 | 13 | 0 | 13% (2/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 0 | 2 | 0 | 0% (0/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 6 | 1 | 0 | 86% (6/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 11 | 4 | 0 | 73% (11/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 3 | 12 | 0 | 20% (3/15) |
| 完整叙事文本 | full_narrative_content | basic | 9 | 6 | 0 | 60% (9/15) |
| 题材契合度 | genre_fit | advanced | 2 | 13 | 0 | 13% (2/15) |
| 钩子设计 | hook_design | advanced | 9 | 6 | 0 | 60% (9/15) |
| 意象系统 | imagery_system | advanced | 10 | 5 | 0 | 67% (10/15) |
| 语言纯净性 | language_purity | basic | 8 | 7 | 0 | 53% (8/15) |
| 后期章节跑偏 | late_stage_digression | basic | 8 | 7 | 0 | 53% (8/15) |
| 主要角色一致性 | main_character_consistency | basic | 12 | 3 | 0 | 80% (12/15) |
| 叙事密度 | narrative_density | advanced | 4 | 11 | 0 | 27% (4/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 7 | 8 | 0 | 47% (7/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 2 | 13 | 0 | 13% (2/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 11 | 4 | 0 | 73% (11/15) |
| outline结构完整性 | outline_structure_completeness | basic | 10 | 5 | 0 | 67% (10/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 5 | 10 | 0 | 33% (5/15) |
| 段落重复检测 | paragraph_repetition | basic | 12 | 3 | 0 | 80% (12/15) |
| 情节推进 | plot_progression | basic | 13 | 2 | 0 | 87% (13/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 7 | 8 | 0 | 47% (7/15) |
| 反复结局 | repeated_endings | basic | 11 | 4 | 0 | 73% (11/15) |
| 语义重复检测 | semantic_redundancy | basic | 5 | 10 | 0 | 33% (5/15) |
| 结构功能性 | structural_design | advanced | 9 | 6 | 0 | 60% (9/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 4 | 11 | 0 | 27% (4/15) |
| 主题一致性 | theme_consistency | basic | 13 | 2 | 0 | 87% (13/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 55.18 | 31.68 | 69.76 |
| IP | 1 | 54.41 | 54.41 | 54.41 |
| VAGUE | 1 | 62.78 | 62.78 | 62.78 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 54.71 | 9.55 | 80.99 |
| SHORT | 2 | 55.90 | 50.69 | 61.11 |
| MEDIUM | 8 | 55.85 | 31.68 | 69.76 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 63.21 | 63.21 | 63.21 |
| ANGSTY | 7 | 57.39 | 9.55 | 80.99 |
| BRAINY_ACTION | 1 | 69.76 | 69.76 | 69.76 |
| HEROINE | 1 | 31.68 | 31.68 | 31.68 |
| NEUTRAL | 1 | 54.41 | 54.41 | 54.41 |
| SUSPENSE | 1 | 63.27 | 63.27 | 63.27 |
| SWEET | 2 | 42.67 | 34.65 | 50.69 |
| SWEET_DRAMA | 1 | 62.78 | 62.78 | 62.78 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `读取creative_intent的schema`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `配方选择交互`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `写作准备确认`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `creative_intent文件存在性`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `outline文件存在性`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现1处structural类型逻辑问题: 第8章仍在“村寨/狼牙口”一线推进，下一出现的章节直接变为“地道/地下洞穴/墓室”探险，但缺失从村寨如何进入地下遗址（入口、触发事件、被抓/迷路/机关开启等）的关键过渡，导致场景与行动链条断裂。

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现3处fixable类型逻辑问题: 当日上午行程描述为“中午到铜矿、下午两小时到第一个正式营地”，但后文又改为“今晚就住这儿吧（废弃铜矿）”，并继续写“傍晚时分，他们终于到达了阿都所说的第一个营地”。同一日内‘是否在铜矿过夜/第一个营地位置’出现自相矛盾。; 第1章确定‘失踪20年’，父亲陆维山在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事调性匹配`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `大纲执行忠实度`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `智斗逻辑合理性`
  - 子类: puzzle_logic_validity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 孙海）

- **NW_CLEAR_SHORT_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 陈老师）

- **NW_CLEAR_SHORT_SWEET_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 零号, 副本BOSS-镜）

- **NW_CLEAR_SHORT_SWEET_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 零号, 玩家老K, 副本BOSS-镜）

- **NW_IP_MEDIUM_NEUTRAL_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（主角: 约翰·马斯顿（张麻子））

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
