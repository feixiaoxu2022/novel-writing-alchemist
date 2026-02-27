# Novel Writing Alchemist 评测统计报告

- **模型**: `glm-5`
- **生成时间**: 2026-02-27T11:42:26.789159
- **评测目录**: `eval_dsv2_20260222_114444_glm-5`
- **Revision**: `rev009` (实际: check_result_rev009.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 11 |
| 执行错误 | 4 |
| 有checker结果 | 15 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 63.68 | 19.99 | 80.64 | 15 |
| 内容分(x0.7) | 55.88 | 15.84 | 72.34 | 15 |
| 过程分(x0.3) | 81.90 | 29.69 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 53 | 7 | 0 | 88.3% |
| 业务规则遵循 | 297 | 261 | 36 | 14 | 87.9% |
| 记忆管理 | 20 | 16 | 4 | 10 | 80.0% |

### 2.2 内容创作质量

- **平均内容分**: 55.88 (范围: 15.84 ~ 72.34)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 295 | 198 | 97 | 8 | 67.1% |
| Advanced(优秀) | 165 | 63 | 102 | 15 | 38.2% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 15 | 13 | 2 | 0 | 86.7% |
| structural_integrity | 45 | 40 | 5 | 0 | 88.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 6 | 9 | 0 | 40.0% |
| sop_compliance | 31 | 16 | 5 | 10 | 76.2% |
| quantity_constraint | 30 | 23 | 5 | 2 | 82.1% |
| workspace_file_compliance | 15 | 13 | 2 | 0 | 86.7% |
| enum_validity | 30 | 25 | 3 | 2 | 89.3% |
| output_completeness | 60 | 56 | 4 | 0 | 93.3% |
| required_skill_reading | 130 | 122 | 8 | 0 | 93.8% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 7 | 3 | 5 | 70.0% |
| log_file_creation | 15 | 9 | 1 | 5 | 90.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 8 | 4 | 3 | 66.7% |
| character_presence_in_outline | 15 | 10 | 3 | 2 | 76.9% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 15 | 0 | 15 | 0 | 0.0% |
| narrative_density | 15 | 1 | 14 | 0 | 6.7% |
| genre_fit | 15 | 1 | 14 | 0 | 6.7% |
| semantic_redundancy | 15 | 1 | 14 | 0 | 6.7% |
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| fixable_logic_inconsistency | 15 | 2 | 13 | 0 | 13.3% |
| pacing_rationality_advanced | 15 | 3 | 12 | 0 | 20.0% |
| hook_design | 15 | 5 | 10 | 0 | 33.3% |
| structural_logic_defect | 15 | 6 | 9 | 0 | 40.0% |
| outline_structure_completeness | 15 | 6 | 9 | 0 | 40.0% |
| outline_execution_fidelity | 15 | 7 | 8 | 0 | 46.7% |
| puzzle_logic_validity | 15 | 7 | 8 | 0 | 46.7% |
| emotional_delivery_match | 16 | 9 | 7 | 0 | 56.2% |
| paragraph_repetition | 15 | 9 | 6 | 0 | 60.0% |
| narrative_tone_match | 15 | 9 | 6 | 0 | 60.0% |
| imagery_system | 15 | 9 | 6 | 0 | 60.0% |
| emotional_gradient | 15 | 9 | 6 | 0 | 60.0% |
| structural_design | 15 | 9 | 6 | 0 | 60.0% |
| character_arc_design | 15 | 10 | 5 | 0 | 66.7% |
| alternating_repetition | 15 | 5 | 2 | 8 | 71.4% |
| chapter_length_stability | 15 | 5 | 2 | 8 | 71.4% |
| chapter_completion | 15 | 11 | 4 | 0 | 73.3% |
| character_motivation_design | 15 | 11 | 4 | 0 | 73.3% |
| character_trait_consistency | 15 | 12 | 3 | 0 | 80.0% |
| plot_progression | 15 | 12 | 3 | 0 | 80.0% |
| repeated_endings | 15 | 12 | 3 | 0 | 80.0% |
| late_stage_digression | 15 | 12 | 3 | 0 | 80.0% |
| chapter_cloning | 15 | 9 | 2 | 4 | 81.8% |
| chapter_output_existence | 15 | 13 | 2 | 0 | 86.7% |
| theme_consistency | 15 | 13 | 2 | 0 | 86.7% |
| main_character_consistency | 15 | 13 | 2 | 0 | 86.7% |
| language_purity | 15 | 13 | 2 | 0 | 86.7% |
| full_narrative_content | 15 | 13 | 2 | 0 | 86.7% |
| character_relationship_design | 15 | 13 | 2 | 0 | 86.7% |
| character_design_adherence | 17 | 15 | 2 | 0 | 88.2% |
| outline_narrative_tension | 15 | 14 | 1 | 0 | 93.3% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 13 | 2 | 0 | 87% (13/15) |
| characters格式 | structural_integrity | - | 14 | 1 | 0 | 93% (14/15) |
| creative_intent格式 | structural_integrity | - | 14 | 1 | 0 | 93% (14/15) |
| outline格式 | structural_integrity | - | 12 | 3 | 0 | 80% (12/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 13 | 1 | 1 | 93% (13/14) |
| Y轴标签枚举 | enum_validity | - | 12 | 2 | 1 | 86% (12/14) |
| chapters目录存在性 | output_completeness | - | 13 | 2 | 0 | 87% (13/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| outline文件存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| Y轴标签数量 | quantity_constraint | - | 13 | 1 | 1 | 93% (13/14) |
| forbidden_elements存在性 | quantity_constraint | - | 10 | 4 | 1 | 71% (10/14) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 2 | 0 | 0 | 100% (2/2) |
| 超短篇字数 | range_constraint | - | 4 | 1 | 0 | 80% (4/5) |
| 读取characters的schema | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取creative_intent的schema | required_skill_reading | - | 13 | 2 | 0 | 87% (13/15) |
| 读取outline的schema | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取写作技巧指南 | required_skill_reading | - | 14 | 1 | 0 | 93% (14/15) |
| 读取命名skill | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取大纲设计指南 | required_skill_reading | - | 15 | 0 | 0 | 100% (15/15) |
| 读取感情线写作指南 | required_skill_reading | - | 3 | 2 | 0 | 60% (3/5) |
| 读取短篇skill | required_skill_reading | - | 4 | 1 | 0 | 80% (4/5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 14 | 1 | 0 | 93% (14/15) |
| 读取配方知识库 | required_skill_reading | - | 14 | 1 | 0 | 93% (14/15) |
| 写作准备确认 | sop_compliance | - | 8 | 2 | 5 | 80% (8/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 8 | 2 | 5 | 80% (8/10) |
| workspace文件规范 | workspace_file_compliance | basic | 13 | 2 | 0 | 87% (13/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 9 | 1 | 5 | 90% (9/10) |
| writing_log文件读取 | log_file_usage | - | 7 | 3 | 5 | 70% (7/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 8 | 4 | 3 | 67% (8/12) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 10 | 3 | 2 | 77% (10/13) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 5 | 2 | 8 | 71% (5/7) |
| 章节克隆检测 | chapter_cloning | gate | 9 | 2 | 4 | 82% (9/11) |
| 章节完成度 | chapter_completion | gate | 11 | 4 | 0 | 73% (11/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 5 | 2 | 8 | 71% (5/7) |
| 章节产出存在性 | chapter_output_existence | gate | 13 | 2 | 0 | 87% (13/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 10 | 5 | 0 | 67% (10/15) |
| 人物设计遵循度 | character_design_adherence | basic | 15 | 0 | 0 | 100% (15/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 11 | 4 | 0 | 73% (11/15) |
| 角色命名质量 | character_naming_quality | advanced | 1 | 14 | 0 | 7% (1/15) |
| 角色关系设计张力 | character_relationship_design | basic | 13 | 2 | 0 | 87% (13/15) |
| 人物设定一致性 | character_trait_consistency | basic | 12 | 3 | 0 | 80% (12/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 0 | 15 | 0 | 0% (0/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 1 | 1 | 0 | 50% (1/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 5 | 2 | 0 | 71% (5/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 9 | 6 | 0 | 60% (9/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 2 | 13 | 0 | 13% (2/15) |
| 完整叙事文本 | full_narrative_content | basic | 13 | 2 | 0 | 87% (13/15) |
| 题材契合度 | genre_fit | advanced | 1 | 14 | 0 | 7% (1/15) |
| 钩子设计 | hook_design | advanced | 5 | 10 | 0 | 33% (5/15) |
| 意象系统 | imagery_system | advanced | 9 | 6 | 0 | 60% (9/15) |
| 语言纯净性 | language_purity | basic | 13 | 2 | 0 | 87% (13/15) |
| 后期章节跑偏 | late_stage_digression | basic | 12 | 3 | 0 | 80% (12/15) |
| 主要角色一致性 | main_character_consistency | basic | 13 | 2 | 0 | 87% (13/15) |
| 叙事密度 | narrative_density | advanced | 1 | 14 | 0 | 7% (1/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 9 | 6 | 0 | 60% (9/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 7 | 8 | 0 | 47% (7/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 14 | 1 | 0 | 93% (14/15) |
| outline结构完整性 | outline_structure_completeness | basic | 6 | 9 | 0 | 40% (6/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 3 | 12 | 0 | 20% (3/15) |
| 段落重复检测 | paragraph_repetition | basic | 9 | 6 | 0 | 60% (9/15) |
| 情节推进 | plot_progression | basic | 12 | 3 | 0 | 80% (12/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 7 | 8 | 0 | 47% (7/15) |
| 反复结局 | repeated_endings | basic | 12 | 3 | 0 | 80% (12/15) |
| 语义重复检测 | semantic_redundancy | basic | 1 | 14 | 0 | 7% (1/15) |
| 结构功能性 | structural_design | advanced | 9 | 6 | 0 | 60% (9/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 6 | 9 | 0 | 40% (6/15) |
| 主题一致性 | theme_consistency | basic | 13 | 2 | 0 | 87% (13/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 56.11 | 19.99 | 72.96 |
| IP | 1 | 67.42 | 67.42 | 67.42 |
| VAGUE | 1 | 72.66 | 72.66 | 72.66 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 73.26 | 68.34 | 80.64 |
| SHORT | 2 | 67.55 | 66.32 | 68.78 |
| MEDIUM | 8 | 56.73 | 19.99 | 72.96 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 56.84 | 56.84 | 56.84 |
| ANGSTY | 7 | 72.23 | 66.32 | 80.64 |
| BRAINY_ACTION | 1 | 39.81 | 39.81 | 39.81 |
| HEROINE | 1 | 19.99 | 19.99 | 19.99 |
| NEUTRAL | 1 | 67.42 | 67.42 | 67.42 |
| SUSPENSE | 1 | 62.23 | 62.23 | 62.23 |
| SWEET | 2 | 65.37 | 61.96 | 68.78 |
| SWEET_DRAMA | 1 | 72.66 | 72.66 | 72.66 |

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

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_HEROINE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现4处fixable类型逻辑问题: chapter_02 结尾两人因黑水寨排斥而在树林扎营等待；chapter_04 直接出现“第三天清晨”且由“阿木”提供关键信息（龙脊入口、‘那拨人’），但中间缺失与阿木相遇/建立信任/获取情报的关键事实交代，导致事实链断裂。; chapter_04 直接从清晨

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `大纲执行忠实度`
  - 子类: outline_execution_fidelity, 层级: basic
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

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 老黑, 张父, 沈父）

- **NW_CLEAR_MEDIUM_HEROINE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 赵老, 陈母）

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 沈渊（曾祖父））

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 沈渊（曾祖父）, 何文渊, 林素心）

- **NW_ULTRA_SHORT_ANGSTY_004** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 小陈）

### 记忆管理 (4个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
