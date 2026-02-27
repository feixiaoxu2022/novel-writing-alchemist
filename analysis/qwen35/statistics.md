# Novel Writing Alchemist 评测统计报告

- **模型**: `qwen3.5-plus-2026-02-15`
- **生成时间**: 2026-02-27T11:42:27.435827
- **评测目录**: `eval_dsv2_20260224_194934_qwen3.5-plus-2026-02-15`
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
| 加权总分 | 72.06 | 58.59 | 83.04 | 15 |
| 内容分(x0.7) | 67.39 | 43.91 | 80.10 | 15 |
| 过程分(x0.3) | 82.96 | 56.58 | 96.59 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 52 | 8 | 0 | 86.7% |
| 业务规则遵循 | 297 | 271 | 26 | 14 | 91.2% |
| 记忆管理 | 20 | 19 | 1 | 10 | 95.0% |

### 2.2 内容创作质量

- **平均内容分**: 67.39 (范围: 43.91 ~ 80.10)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 298 | 208 | 90 | 5 | 69.8% |
| Advanced(优秀) | 165 | 105 | 60 | 15 | 63.6% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 37 | 8 | 0 | 82.2% |
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 4 | 11 | 0 | 26.7% |
| sop_compliance | 31 | 17 | 4 | 10 | 81.0% |
| enum_validity | 30 | 26 | 2 | 2 | 92.9% |
| quantity_constraint | 30 | 26 | 2 | 2 | 92.9% |
| workspace_file_compliance | 15 | 14 | 1 | 0 | 93.3% |
| output_completeness | 60 | 58 | 2 | 0 | 96.7% |
| required_skill_reading | 130 | 126 | 4 | 0 | 96.9% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 9 | 1 | 5 | 90.0% |
| log_file_creation | 15 | 10 | 0 | 5 | 100.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 9 | 6 | 0 | 60.0% |
| character_presence_in_outline | 15 | 10 | 4 | 1 | 71.4% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 0 | 15 | 0 | 0.0% |
| dialogue_character_distinction | 15 | 1 | 14 | 0 | 6.7% |
| semantic_redundancy | 15 | 1 | 14 | 0 | 6.7% |
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| structural_logic_defect | 15 | 4 | 11 | 0 | 26.7% |
| narrative_tone_match | 15 | 6 | 9 | 0 | 40.0% |
| genre_fit | 15 | 6 | 9 | 0 | 40.0% |
| outline_execution_fidelity | 15 | 7 | 8 | 0 | 46.7% |
| puzzle_logic_validity | 15 | 7 | 8 | 0 | 46.7% |
| pacing_rationality_advanced | 15 | 7 | 8 | 0 | 46.7% |
| outline_structure_completeness | 15 | 8 | 7 | 0 | 53.3% |
| language_purity | 15 | 9 | 6 | 0 | 60.0% |
| late_stage_digression | 15 | 9 | 6 | 0 | 60.0% |
| narrative_density | 15 | 9 | 6 | 0 | 60.0% |
| character_design_adherence | 17 | 11 | 6 | 0 | 64.7% |
| full_narrative_content | 15 | 10 | 5 | 0 | 66.7% |
| character_trait_consistency | 15 | 12 | 3 | 0 | 80.0% |
| character_arc_design | 15 | 12 | 3 | 0 | 80.0% |
| paragraph_repetition | 15 | 13 | 2 | 0 | 86.7% |
| hook_design | 15 | 13 | 2 | 0 | 86.7% |
| character_relationship_design | 15 | 13 | 2 | 0 | 86.7% |
| outline_narrative_tension | 15 | 13 | 2 | 0 | 86.7% |
| emotional_delivery_match | 16 | 14 | 2 | 0 | 87.5% |
| repeated_endings | 15 | 14 | 1 | 0 | 93.3% |
| emotional_gradient | 15 | 14 | 1 | 0 | 93.3% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| chapter_cloning | 15 | 15 | 0 | 0 | 100.0% |
| alternating_repetition | 15 | 10 | 0 | 5 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| chapter_length_stability | 15 | 10 | 0 | 5 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| structural_design | 15 | 15 | 0 | 0 | 100.0% |
| character_motivation_design | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 15 | 0 | 0 | 100% (15/15) |
| characters格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent格式 | structural_integrity | - | 8 | 7 | 0 | 53% (8/15) |
| outline格式 | structural_integrity | - | 14 | 1 | 0 | 93% (14/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 13 | 1 | 1 | 93% (13/14) |
| Y轴标签枚举 | enum_validity | - | 13 | 1 | 1 | 93% (13/14) |
| chapters目录存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| outline文件存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| Y轴标签数量 | quantity_constraint | - | 13 | 1 | 1 | 93% (13/14) |
| forbidden_elements存在性 | quantity_constraint | - | 13 | 1 | 1 | 93% (13/14) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 1 | 0 | 0 | 100% (1/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 1 | 1 | 0 | 50% (1/2) |
| 超短篇字数 | range_constraint | - | 2 | 3 | 0 | 40% (2/5) |
| 读取characters的schema | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取creative_intent的schema | required_skill_reading | - | 14 | 1 | 0 | 93% (14/15) |
| 读取outline的schema | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取写作技巧指南 | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取命名skill | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取大纲设计指南 | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取感情线写作指南 | required_skill_reading | - | 4 | 1 | 0 | 80% (4/5) |
| 读取短篇skill | required_skill_reading | - | 5 | 0 | 0 | 100% (5/5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 13 | 2 | 0 | 87% (13/15) |
| 读取配方知识库 | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 写作准备确认 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 7 | 3 | 5 | 70% (7/10) |
| workspace文件规范 | workspace_file_compliance | basic | 14 | 1 | 0 | 93% (14/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 10 | 0 | 5 | 100% (10/10) |
| writing_log文件读取 | log_file_usage | - | 9 | 1 | 5 | 90% (9/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 9 | 6 | 0 | 60% (9/15) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 10 | 4 | 1 | 71% (10/14) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 10 | 0 | 5 | 100% (10/10) |
| 章节克隆检测 | chapter_cloning | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节完成度 | chapter_completion | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 10 | 0 | 5 | 100% (10/10) |
| 章节产出存在性 | chapter_output_existence | gate | 15 | 0 | 0 | 100% (15/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 12 | 3 | 0 | 80% (12/15) |
| 人物设计遵循度 | character_design_adherence | basic | 10 | 5 | 0 | 67% (10/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 1 | 0 | 0 | 100% (1/1) |
| 角色动机设计深度 | character_motivation_design | basic | 15 | 0 | 0 | 100% (15/15) |
| 角色命名质量 | character_naming_quality | advanced | 1 | 14 | 0 | 7% (1/15) |
| 角色关系设计张力 | character_relationship_design | basic | 13 | 2 | 0 | 87% (13/15) |
| 人物设定一致性 | character_trait_consistency | basic | 12 | 3 | 0 | 80% (12/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 1 | 14 | 0 | 7% (1/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 1 | 1 | 0 | 50% (1/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 7 | 0 | 0 | 100% (7/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 14 | 1 | 0 | 93% (14/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 0 | 15 | 0 | 0% (0/15) |
| 完整叙事文本 | full_narrative_content | basic | 10 | 5 | 0 | 67% (10/15) |
| 题材契合度 | genre_fit | advanced | 6 | 9 | 0 | 40% (6/15) |
| 钩子设计 | hook_design | advanced | 13 | 2 | 0 | 87% (13/15) |
| 意象系统 | imagery_system | advanced | 15 | 0 | 0 | 100% (15/15) |
| 语言纯净性 | language_purity | basic | 9 | 6 | 0 | 60% (9/15) |
| 后期章节跑偏 | late_stage_digression | basic | 9 | 6 | 0 | 60% (9/15) |
| 主要角色一致性 | main_character_consistency | basic | 15 | 0 | 0 | 100% (15/15) |
| 叙事密度 | narrative_density | advanced | 9 | 6 | 0 | 60% (9/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 6 | 9 | 0 | 40% (6/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 7 | 8 | 0 | 47% (7/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 13 | 2 | 0 | 87% (13/15) |
| outline结构完整性 | outline_structure_completeness | basic | 8 | 7 | 0 | 53% (8/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 7 | 8 | 0 | 47% (7/15) |
| 段落重复检测 | paragraph_repetition | basic | 13 | 2 | 0 | 87% (13/15) |
| 情节推进 | plot_progression | basic | 15 | 0 | 0 | 100% (15/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 7 | 8 | 0 | 47% (7/15) |
| 反复结局 | repeated_endings | basic | 14 | 1 | 0 | 93% (14/15) |
| 语义重复检测 | semantic_redundancy | basic | 1 | 14 | 0 | 7% (1/15) |
| 结构功能性 | structural_design | advanced | 15 | 0 | 0 | 100% (15/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 4 | 11 | 0 | 27% (4/15) |
| 主题一致性 | theme_consistency | basic | 15 | 0 | 0 | 100% (15/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 69.84 | 58.59 | 76.66 |
| IP | 1 | 63.25 | 63.25 | 63.25 |
| VAGUE | 1 | 76.19 | 76.19 | 76.19 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 76.53 | 67.61 | 83.04 |
| SHORT | 2 | 72.31 | 71.92 | 72.71 |
| MEDIUM | 8 | 69.19 | 58.59 | 76.66 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 66.32 | 66.32 | 66.32 |
| ANGSTY | 7 | 74.32 | 65.65 | 83.04 |
| BRAINY_ACTION | 1 | 74.41 | 74.41 | 74.41 |
| HEROINE | 1 | 72.48 | 72.48 | 72.48 |
| NEUTRAL | 1 | 63.25 | 63.25 | 63.25 |
| SUSPENSE | 1 | 76.66 | 76.66 | 76.66 |
| SWEET | 2 | 65.65 | 58.59 | 72.71 |
| SWEET_DRAMA | 1 | 76.19 | 76.19 | 76.19 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `人物设定一致性`
  - 子类: character_trait_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `人物设计遵循度`
  - 子类: character_design_adherence, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现3处structural类型逻辑问题: 第12章末尾明确“三天后，昆明”（已经出山回城），但第13章又写“进山第十五天，返程路上……到村寨入口”，把已经回到昆明的情节重新拉回山中，形成无法自洽的整体时间线/场景回跳。; 第12章已给出明确结局：山洞坍塌、三天后回到昆明、顾言回校、阿木回村寨；但第

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现5处fixable类型逻辑问题: 第8章明确“进山第六天，傍晚六点到达村寨并留宿”，第9章却直接写“进山第九天，上午八点在村寨醒来”，中间第7-8天发生了什么未交代，时间线出现断档。; 第11章结尾写“洞外天色渐渐亮了，第一缕阳光升起”，但第12章开头却标注“凌晨两点，后山山洞内”，同一连续事件

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `语言纯净性`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 周志远）

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 周志远）

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 老K）

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 老K）

- **NW_CLEAR_SHORT_SWEET_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 零号管理员）

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `配方选择交互`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取感情线写作指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `outline文件存在性`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['test.txt']

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_HEROINE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (1个失败检查)

- **NW_CLEAR_SHORT_SWEET_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
