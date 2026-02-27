# Novel Writing Alchemist 评测统计报告

- **模型**: `ernie-5.0-thinking-preview`
- **生成时间**: 2026-02-27T11:42:25.812113
- **评测目录**: `eval_dsv2_20260211_103353_ernie-5.0-thinking-preview`
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
| 加权总分 | 59.48 | 34.52 | 79.95 | 15 |
| 内容分(x0.7) | 52.59 | 26.70 | 86.09 | 15 |
| 过程分(x0.3) | 75.55 | 52.78 | 94.44 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 47 | 13 | 0 | 78.3% |
| 业务规则遵循 | 159 | 115 | 44 | 152 | 72.3% |
| 记忆管理 | 20 | 9 | 11 | 10 | 45.0% |

### 2.2 内容创作质量

- **平均内容分**: 52.59 (范围: 26.70 ~ 86.09)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 298 | 174 | 124 | 5 | 58.4% |
| Advanced(优秀) | 165 | 72 | 93 | 15 | 43.6% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 15 | 7 | 8 | 0 | 46.7% |
| structural_integrity | 45 | 40 | 5 | 0 | 88.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| required_skill_reading | 130 | 0 | 0 | 130 | 0.0% |
| range_constraint | 15 | 2 | 13 | 0 | 13.3% |
| workspace_file_compliance | 15 | 4 | 11 | 0 | 26.7% |
| quantity_constraint | 30 | 16 | 8 | 6 | 66.7% |
| enum_validity | 30 | 17 | 7 | 6 | 70.8% |
| sop_compliance | 31 | 19 | 2 | 10 | 90.5% |
| output_completeness | 60 | 57 | 3 | 0 | 95.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 4 | 6 | 5 | 40.0% |
| log_file_creation | 15 | 5 | 5 | 5 | 50.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_outline | 15 | 11 | 0 | 4 | 100.0% |
| character_presence_in_chapters | 15 | 11 | 0 | 4 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 1 | 14 | 0 | 6.7% |
| dialogue_character_distinction | 15 | 1 | 14 | 0 | 6.7% |
| genre_fit | 15 | 1 | 14 | 0 | 6.7% |
| pacing_rationality_advanced | 15 | 1 | 14 | 0 | 6.7% |
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| semantic_redundancy | 15 | 2 | 13 | 0 | 13.3% |
| outline_execution_fidelity | 15 | 3 | 12 | 0 | 20.0% |
| narrative_density | 15 | 3 | 12 | 0 | 20.0% |
| narrative_tone_match | 15 | 4 | 11 | 0 | 26.7% |
| structural_logic_defect | 15 | 5 | 10 | 0 | 33.3% |
| late_stage_digression | 15 | 6 | 9 | 0 | 40.0% |
| puzzle_logic_validity | 15 | 7 | 8 | 0 | 46.7% |
| structural_design | 15 | 7 | 8 | 0 | 46.7% |
| character_design_adherence | 17 | 8 | 9 | 0 | 47.1% |
| hook_design | 15 | 8 | 7 | 0 | 53.3% |
| paragraph_repetition | 15 | 9 | 6 | 0 | 60.0% |
| main_character_consistency | 15 | 9 | 6 | 0 | 60.0% |
| character_trait_consistency | 15 | 9 | 6 | 0 | 60.0% |
| language_purity | 15 | 10 | 5 | 0 | 66.7% |
| full_narrative_content | 15 | 10 | 5 | 0 | 66.7% |
| repeated_endings | 15 | 10 | 5 | 0 | 66.7% |
| imagery_system | 15 | 11 | 4 | 0 | 73.3% |
| emotional_gradient | 15 | 11 | 4 | 0 | 73.3% |
| character_motivation_design | 15 | 11 | 4 | 0 | 73.3% |
| outline_structure_completeness | 15 | 11 | 4 | 0 | 73.3% |
| chapter_length_stability | 15 | 8 | 2 | 5 | 80.0% |
| theme_consistency | 15 | 12 | 3 | 0 | 80.0% |
| emotional_delivery_match | 16 | 13 | 3 | 0 | 81.2% |
| chapter_cloning | 15 | 12 | 2 | 1 | 85.7% |
| character_relationship_design | 15 | 13 | 2 | 0 | 86.7% |
| character_arc_design | 15 | 13 | 2 | 0 | 86.7% |
| alternating_repetition | 15 | 8 | 1 | 6 | 88.9% |
| chapter_completion | 15 | 14 | 1 | 0 | 93.3% |
| plot_progression | 15 | 14 | 1 | 0 | 93.3% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| outline_narrative_tension | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 7 | 8 | 0 | 47% (7/15) |
| characters格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent格式 | structural_integrity | - | 12 | 3 | 0 | 80% (12/15) |
| outline格式 | structural_integrity | - | 13 | 2 | 0 | 87% (13/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 9 | 3 | 3 | 75% (9/12) |
| Y轴标签枚举 | enum_validity | - | 8 | 4 | 3 | 67% (8/12) |
| chapters目录存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 12 | 3 | 0 | 80% (12/15) |
| outline文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| Y轴标签数量 | quantity_constraint | - | 9 | 3 | 3 | 75% (9/12) |
| forbidden_elements存在性 | quantity_constraint | - | 7 | 5 | 3 | 58% (7/12) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
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
| 写作准备确认 | sop_compliance | - | 8 | 2 | 5 | 80% (8/10) |
| 灵感激发交互 | sop_compliance | - | 1 | 0 | 0 | 100% (1/1) |
| 配方选择交互 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| workspace文件规范 | workspace_file_compliance | basic | 4 | 11 | 0 | 27% (4/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 5 | 5 | 5 | 50% (5/10) |
| writing_log文件读取 | log_file_usage | - | 4 | 6 | 5 | 40% (4/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 11 | 0 | 4 | 100% (11/11) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 11 | 0 | 4 | 100% (11/11) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 8 | 1 | 6 | 89% (8/9) |
| 章节克隆检测 | chapter_cloning | gate | 12 | 2 | 1 | 86% (12/14) |
| 章节完成度 | chapter_completion | gate | 14 | 1 | 0 | 93% (14/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 8 | 2 | 5 | 80% (8/10) |
| 章节产出存在性 | chapter_output_existence | gate | 15 | 0 | 0 | 100% (15/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 13 | 2 | 0 | 87% (13/15) |
| 人物设计遵循度 | character_design_adherence | basic | 8 | 7 | 0 | 53% (8/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 11 | 4 | 0 | 73% (11/15) |
| 角色命名质量 | character_naming_quality | advanced | 1 | 14 | 0 | 7% (1/15) |
| 角色关系设计张力 | character_relationship_design | basic | 13 | 2 | 0 | 87% (13/15) |
| 人物设定一致性 | character_trait_consistency | basic | 9 | 6 | 0 | 60% (9/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 1 | 14 | 0 | 7% (1/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 2 | 0 | 0 | 100% (2/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 6 | 1 | 0 | 86% (6/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 11 | 4 | 0 | 73% (11/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 1 | 14 | 0 | 7% (1/15) |
| 完整叙事文本 | full_narrative_content | basic | 10 | 5 | 0 | 67% (10/15) |
| 题材契合度 | genre_fit | advanced | 1 | 14 | 0 | 7% (1/15) |
| 钩子设计 | hook_design | advanced | 8 | 7 | 0 | 53% (8/15) |
| 意象系统 | imagery_system | advanced | 11 | 4 | 0 | 73% (11/15) |
| 语言纯净性 | language_purity | basic | 10 | 5 | 0 | 67% (10/15) |
| 后期章节跑偏 | late_stage_digression | basic | 6 | 9 | 0 | 40% (6/15) |
| 主要角色一致性 | main_character_consistency | basic | 9 | 6 | 0 | 60% (9/15) |
| 叙事密度 | narrative_density | advanced | 3 | 12 | 0 | 20% (3/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 4 | 11 | 0 | 27% (4/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 3 | 12 | 0 | 20% (3/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 15 | 0 | 0 | 100% (15/15) |
| outline结构完整性 | outline_structure_completeness | basic | 11 | 4 | 0 | 73% (11/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 1 | 14 | 0 | 7% (1/15) |
| 段落重复检测 | paragraph_repetition | basic | 9 | 6 | 0 | 60% (9/15) |
| 情节推进 | plot_progression | basic | 14 | 1 | 0 | 93% (14/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 7 | 8 | 0 | 47% (7/15) |
| 反复结局 | repeated_endings | basic | 10 | 5 | 0 | 67% (10/15) |
| 语义重复检测 | semantic_redundancy | basic | 2 | 13 | 0 | 13% (2/15) |
| 结构功能性 | structural_design | advanced | 7 | 8 | 0 | 47% (7/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 5 | 10 | 0 | 33% (5/15) |
| 主题一致性 | theme_consistency | basic | 12 | 3 | 0 | 80% (12/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 57.67 | 41.31 | 79.95 |
| IP | 1 | 34.52 | 34.52 | 34.52 |
| VAGUE | 1 | 50.75 | 50.75 | 50.75 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 69.10 | 63.87 | 78.64 |
| SHORT | 2 | 61.18 | 55.65 | 66.71 |
| MEDIUM | 8 | 53.04 | 34.52 | 79.95 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 79.95 | 79.95 | 79.95 |
| ANGSTY | 7 | 64.98 | 53.68 | 78.64 |
| BRAINY_ACTION | 1 | 60.17 | 60.17 | 60.17 |
| HEROINE | 1 | 47.34 | 47.34 | 47.34 |
| NEUTRAL | 1 | 34.52 | 34.52 | 34.52 |
| SUSPENSE | 1 | 56.57 | 56.57 | 56.57 |
| SWEET | 2 | 54.01 | 41.31 | 66.71 |
| SWEET_DRAMA | 1 | 50.75 | 50.75 | 50.75 |

## 5. 失败案例索引

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `写作准备确认`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `creative_intent文件存在性`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `中篇字数_冒险`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `X轴模式ID格式`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `Y轴标签枚举`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现2处fixable类型逻辑问题: 林墨被描写为“手指无意识地推了推眼镜——虽然他没戴眼镜”，但第1章已明确其“戴着金丝眼镜”，且第2章后文与第3章又多次出现“眼镜歪了/眼镜片”等描写，导致同一时间段内眼镜佩戴状态自相矛盾。; 蜂群来袭时写“栈道太窄，三个人加两匹马根本跑不快”，但紧接着描写“阿旺

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `大纲执行忠实度`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `题材契合度`
  - 子类: genre_fit, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构功能性`
  - 子类: structural_design, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色命名质量`
  - 子类: character_naming_quality, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SWEET_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
