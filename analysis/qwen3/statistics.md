# Novel Writing Alchemist 评测统计报告

- **模型**: `qwen3-max-2026-01-23`
- **生成时间**: 2026-02-27T11:25:02.352886
- **评测目录**: `eval_dsv2_20260213_143908_qwen3-max-2026-01-23`
- **Revision**: `rev009` (实际: check_result_rev009.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 10 |
| 执行错误 | 5 |
| 有checker结果 | 10 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 72.07 | 66.02 | 78.75 | 10 |
| 内容分(x0.7) | 64.91 | 52.35 | 74.00 | 10 |
| 过程分(x0.3) | 88.75 | 72.92 | 97.92 | 10 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 8 | 80.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 40 | 38 | 2 | 0 | 95.0% |
| 业务规则遵循 | 113 | 97 | 16 | 93 | 85.8% |
| 记忆管理 | 20 | 18 | 2 | 0 | 90.0% |

### 2.2 内容创作质量

- **平均内容分**: 64.91 (范围: 52.35 ~ 74.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 31 | 29 | 2 | 0 | 93.5% |
| Basic(基础) | 190 | 157 | 33 | 3 | 82.6% |
| Advanced(优秀) | 120 | 58 | 62 | 10 | 48.3% |

- **Gate触发率**: 20.0% (2/10)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 30 | 28 | 2 | 0 | 93.3% |
| naming_convention | 10 | 10 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| required_skill_reading | 85 | 0 | 0 | 85 | 0.0% |
| range_constraint | 10 | 0 | 10 | 0 | 0.0% |
| workspace_file_compliance | 10 | 9 | 1 | 0 | 90.0% |
| enum_validity | 20 | 15 | 1 | 4 | 93.8% |
| quantity_constraint | 20 | 15 | 1 | 4 | 93.8% |
| output_completeness | 40 | 38 | 2 | 0 | 95.0% |
| sop_compliance | 21 | 20 | 1 | 0 | 95.2% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 10 | 8 | 2 | 0 | 80.0% |
| log_file_creation | 10 | 10 | 0 | 0 | 100.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 10 | 7 | 3 | 0 | 70.0% |
| character_presence_in_outline | 10 | 10 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 10 | 0 | 10 | 0 | 0.0% |
| genre_fit | 10 | 0 | 10 | 0 | 0.0% |
| fixable_logic_inconsistency | 10 | 2 | 8 | 0 | 20.0% |
| character_naming_quality | 10 | 2 | 8 | 0 | 20.0% |
| narrative_density | 10 | 3 | 7 | 0 | 30.0% |
| pacing_rationality_advanced | 10 | 3 | 7 | 0 | 30.0% |
| narrative_tone_match | 10 | 4 | 6 | 0 | 40.0% |
| puzzle_logic_validity | 10 | 4 | 6 | 0 | 40.0% |
| semantic_redundancy | 10 | 4 | 6 | 0 | 40.0% |
| hook_design | 10 | 5 | 5 | 0 | 50.0% |
| structural_logic_defect | 10 | 6 | 4 | 0 | 60.0% |
| structural_design | 10 | 6 | 4 | 0 | 60.0% |
| outline_structure_completeness | 10 | 6 | 4 | 0 | 60.0% |
| imagery_system | 10 | 7 | 3 | 0 | 70.0% |
| chapter_length_stability | 10 | 5 | 2 | 3 | 71.4% |
| chapter_completion | 10 | 8 | 2 | 0 | 80.0% |
| paragraph_repetition | 10 | 8 | 2 | 0 | 80.0% |
| outline_execution_fidelity | 10 | 8 | 2 | 0 | 80.0% |
| emotional_gradient | 10 | 8 | 2 | 0 | 80.0% |
| character_motivation_design | 10 | 8 | 2 | 0 | 80.0% |
| emotional_delivery_match | 11 | 9 | 2 | 0 | 81.8% |
| character_design_adherence | 12 | 10 | 2 | 0 | 83.3% |
| character_trait_consistency | 10 | 9 | 1 | 0 | 90.0% |
| chapter_output_existence | 10 | 10 | 0 | 0 | 100.0% |
| chapter_cloning | 10 | 8 | 0 | 2 | 100.0% |
| alternating_repetition | 10 | 3 | 0 | 7 | 100.0% |
| theme_consistency | 10 | 10 | 0 | 0 | 100.0% |
| main_character_consistency | 10 | 10 | 0 | 0 | 100.0% |
| language_purity | 10 | 10 | 0 | 0 | 100.0% |
| plot_progression | 10 | 10 | 0 | 0 | 100.0% |
| full_narrative_content | 10 | 10 | 0 | 0 | 100.0% |
| repeated_endings | 10 | 10 | 0 | 0 | 100.0% |
| late_stage_digression | 10 | 10 | 0 | 0 | 100.0% |
| character_relationship_design | 10 | 10 | 0 | 0 | 100.0% |
| character_arc_design | 10 | 10 | 0 | 0 | 100.0% |
| outline_narrative_tension | 10 | 10 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 10 | 0 | 0 | 100% (10/10) |
| characters格式 | structural_integrity | - | 10 | 0 | 0 | 100% (10/10) |
| creative_intent格式 | structural_integrity | - | 8 | 2 | 0 | 80% (8/10) |
| outline格式 | structural_integrity | - | 10 | 0 | 0 | 100% (10/10) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 8 | 0 | 2 | 100% (8/8) |
| Y轴标签枚举 | enum_validity | - | 7 | 1 | 2 | 88% (7/8) |
| chapters目录存在性 | output_completeness | - | 10 | 0 | 0 | 100% (10/10) |
| characters文件存在性 | output_completeness | - | 10 | 0 | 0 | 100% (10/10) |
| creative_intent文件存在性 | output_completeness | - | 8 | 2 | 0 | 80% (8/10) |
| outline文件存在性 | output_completeness | - | 10 | 0 | 0 | 100% (10/10) |
| Y轴标签数量 | quantity_constraint | - | 8 | 0 | 2 | 100% (8/8) |
| forbidden_elements存在性 | quantity_constraint | - | 7 | 1 | 2 | 88% (7/8) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 0 | 2 | 0 | 0% (0/2) |
| 读取characters的schema | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取creative_intent的schema | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取outline的schema | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取写作技巧指南 | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取命名skill | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取大纲设计指南 | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取感情线写作指南 | required_skill_reading | - | 0 | 0 | 5 | skip(5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 读取配方知识库 | required_skill_reading | - | 0 | 0 | 10 | skip(10) |
| 写作准备确认 | sop_compliance | - | 10 | 0 | 0 | 100% (10/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 10 | 0 | 0 | 100% (10/10) |
| workspace文件规范 | workspace_file_compliance | basic | 9 | 1 | 0 | 90% (9/10) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 10 | 0 | 0 | 100% (10/10) |
| writing_log文件读取 | log_file_usage | - | 8 | 2 | 0 | 80% (8/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 7 | 3 | 0 | 70% (7/10) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 10 | 0 | 0 | 100% (10/10) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 3 | 0 | 7 | 100% (3/3) |
| 章节克隆检测 | chapter_cloning | gate | 8 | 0 | 2 | 100% (8/8) |
| 章节完成度 | chapter_completion | gate | 8 | 2 | 0 | 80% (8/10) |
| 章节长度稳定性 | chapter_length_stability | basic | 5 | 2 | 3 | 71% (5/7) |
| 章节产出存在性 | chapter_output_existence | gate | 10 | 0 | 0 | 100% (10/10) |
| 角色成长弧线设计 | character_arc_design | advanced | 10 | 0 | 0 | 100% (10/10) |
| 人物设计遵循度 | character_design_adherence | basic | 9 | 1 | 0 | 90% (9/10) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 1 | 0 | 0 | 100% (1/1) |
| 角色动机设计深度 | character_motivation_design | basic | 8 | 2 | 0 | 80% (8/10) |
| 角色命名质量 | character_naming_quality | advanced | 2 | 8 | 0 | 20% (2/10) |
| 角色关系设计张力 | character_relationship_design | basic | 10 | 0 | 0 | 100% (10/10) |
| 人物设定一致性 | character_trait_consistency | basic | 9 | 1 | 0 | 90% (9/10) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 0 | 10 | 0 | 0% (0/10) |
| 伏笔回收检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 1 | 1 | 0 | 50% (1/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 2 | 0 | 0 | 100% (2/2) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 8 | 2 | 0 | 80% (8/10) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 2 | 8 | 0 | 20% (2/10) |
| 完整叙事文本 | full_narrative_content | basic | 10 | 0 | 0 | 100% (10/10) |
| 题材契合度 | genre_fit | advanced | 0 | 10 | 0 | 0% (0/10) |
| 钩子设计 | hook_design | advanced | 5 | 5 | 0 | 50% (5/10) |
| 意象系统 | imagery_system | advanced | 7 | 3 | 0 | 70% (7/10) |
| 语言纯净性 | language_purity | basic | 10 | 0 | 0 | 100% (10/10) |
| 后期章节跑偏 | late_stage_digression | basic | 10 | 0 | 0 | 100% (10/10) |
| 主要角色一致性 | main_character_consistency | basic | 10 | 0 | 0 | 100% (10/10) |
| 叙事密度 | narrative_density | advanced | 3 | 7 | 0 | 30% (3/10) |
| 叙事调性匹配 | narrative_tone_match | basic | 4 | 6 | 0 | 40% (4/10) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 8 | 2 | 0 | 80% (8/10) |
| outline叙事张力 | outline_narrative_tension | advanced | 10 | 0 | 0 | 100% (10/10) |
| outline结构完整性 | outline_structure_completeness | basic | 6 | 4 | 0 | 60% (6/10) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 3 | 7 | 0 | 30% (3/10) |
| 段落重复检测 | paragraph_repetition | basic | 8 | 2 | 0 | 80% (8/10) |
| 情节推进 | plot_progression | basic | 10 | 0 | 0 | 100% (10/10) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 4 | 6 | 0 | 40% (4/10) |
| 反复结局 | repeated_endings | basic | 10 | 0 | 0 | 100% (10/10) |
| 语义重复检测 | semantic_redundancy | basic | 4 | 6 | 0 | 40% (4/10) |
| 结构功能性 | structural_design | advanced | 6 | 4 | 0 | 60% (6/10) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 6 | 4 | 0 | 60% (6/10) |
| 主题一致性 | theme_consistency | basic | 10 | 0 | 0 | 100% (10/10) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 72.66 | 66.45 | 78.75 |
| IP | 1 | 66.02 | 66.02 | 66.02 |
| VAGUE | 1 | 73.33 | 73.33 | 73.33 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| SHORT | 2 | 76.88 | 75.00 | 78.75 |
| MEDIUM | 8 | 70.86 | 66.02 | 78.05 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 78.05 | 78.05 | 78.05 |
| ANGSTY | 2 | 71.00 | 67.00 | 75.00 |
| BRAINY_ACTION | 1 | 76.98 | 76.98 | 76.98 |
| HEROINE | 1 | 66.45 | 66.45 | 66.45 |
| NEUTRAL | 1 | 66.02 | 66.02 | 66.02 |
| SUSPENSE | 1 | 68.35 | 68.35 | 68.35 |
| SWEET | 2 | 74.75 | 70.74 | 78.75 |
| SWEET_DRAMA | 1 | 73.33 | 73.33 | 73.33 |

## 5. 失败案例索引

### 格式规范遵循 (2个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_VAGUE_MEDIUM_SWEET_DRAMA_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现4处fixable类型逻辑问题: 陈峰与林清在电话中约定“明天中午，小镇茶馆见”，但紧接着场景三写为“夜色已深”，且林清称“从昆明到边境小镇坐了整整一天的车”，未交代时间跳转与当日/次日关系，导致会面时间连续性断裂。; 场景一当日从早上九点研究到晚上七点，且当晚决定“明天一早出发”；但场景三又称

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事调性匹配`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色语言辨识度`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事密度`
  - 子类: narrative_density, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `智斗逻辑合理性`
  - 子类: puzzle_logic_validity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `creative_intent文件存在性`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `中篇字数_冒险`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `forbidden_elements存在性`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `中篇字数_智斗`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

### 数据一致性 (3个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 林小雨, 赵天佑）

- **NW_CLEAR_MEDIUM_HEROINE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（主角: 陆砚; 配角: 周世昌, 林律师）

- **NW_CLEAR_SHORT_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 张老师）

### 记忆管理 (2个失败检查)

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_VAGUE_MEDIUM_SWEET_DRAMA_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
