# Novel Writing Alchemist 评测统计报告

- **模型**: `openai_EB5-0209-A35B-midtrain-128k-chat`
- **生成时间**: 2026-02-27T11:42:26.349475
- **评测目录**: `eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat`
- **Revision**: `rev009` (实际: check_result_rev009.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 10 |
| 成功执行 | 9 |
| 执行错误 | 1 |
| 有checker结果 | 10 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 37.45 | 3.66 | 77.37 | 10 |
| 内容分(x0.7) | 32.05 | 3.64 | 74.81 | 10 |
| 过程分(x0.3) | 50.02 | 3.70 | 83.33 | 10 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 10 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 40 | 25 | 15 | 0 | 62.5% |
| 业务规则遵循 | 105 | 51 | 54 | 101 | 48.6% |
| 记忆管理 | 20 | 8 | 12 | 0 | 40.0% |

### 2.2 内容创作质量

- **平均内容分**: 32.05 (范围: 3.64 ~ 74.81)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 203 | 69 | 134 | 0 | 34.0% |
| Advanced(优秀) | 110 | 32 | 78 | 10 | 29.1% |

- **Gate触发率**: 0.0% (0/10)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 10 | 5 | 5 | 0 | 50.0% |
| structural_integrity | 30 | 20 | 10 | 0 | 66.7% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| required_skill_reading | 85 | 0 | 0 | 85 | 0.0% |
| range_constraint | 10 | 0 | 10 | 0 | 0.0% |
| enum_validity | 20 | 4 | 8 | 8 | 33.3% |
| quantity_constraint | 20 | 4 | 8 | 8 | 33.3% |
| sop_compliance | 21 | 10 | 11 | 0 | 47.6% |
| workspace_file_compliance | 10 | 6 | 4 | 0 | 60.0% |
| output_completeness | 40 | 27 | 13 | 0 | 67.5% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 10 | 1 | 9 | 0 | 10.0% |
| log_file_creation | 10 | 7 | 3 | 0 | 70.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 10 | 1 | 1 | 8 | 50.0% |
| character_presence_in_outline | 10 | 2 | 1 | 7 | 66.7% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 10 | 0 | 10 | 0 | 0.0% |
| puzzle_logic_validity | 10 | 0 | 10 | 0 | 0.0% |
| genre_fit | 10 | 0 | 10 | 0 | 0.0% |
| semantic_redundancy | 10 | 0 | 10 | 0 | 0.0% |
| structural_logic_defect | 10 | 1 | 9 | 0 | 10.0% |
| narrative_density | 10 | 1 | 9 | 0 | 10.0% |
| pacing_rationality_advanced | 10 | 1 | 9 | 0 | 10.0% |
| hook_design | 10 | 1 | 9 | 0 | 10.0% |
| emotional_delivery_match | 11 | 2 | 9 | 0 | 18.2% |
| paragraph_repetition | 10 | 2 | 8 | 0 | 20.0% |
| late_stage_digression | 10 | 2 | 8 | 0 | 20.0% |
| emotional_gradient | 10 | 2 | 8 | 0 | 20.0% |
| character_naming_quality | 10 | 2 | 8 | 0 | 20.0% |
| main_character_consistency | 10 | 3 | 7 | 0 | 30.0% |
| language_purity | 10 | 3 | 7 | 0 | 30.0% |
| full_narrative_content | 10 | 3 | 7 | 0 | 30.0% |
| outline_execution_fidelity | 10 | 3 | 7 | 0 | 30.0% |
| imagery_system | 10 | 3 | 7 | 0 | 30.0% |
| structural_design | 10 | 3 | 7 | 0 | 30.0% |
| chapter_cloning | 10 | 4 | 6 | 0 | 40.0% |
| chapter_length_stability | 10 | 4 | 6 | 0 | 40.0% |
| plot_progression | 10 | 4 | 6 | 0 | 40.0% |
| repeated_endings | 10 | 4 | 6 | 0 | 40.0% |
| character_design_adherence | 12 | 5 | 7 | 0 | 41.7% |
| chapter_output_existence | 10 | 5 | 5 | 0 | 50.0% |
| alternating_repetition | 10 | 5 | 5 | 0 | 50.0% |
| chapter_completion | 10 | 5 | 5 | 0 | 50.0% |
| theme_consistency | 10 | 5 | 5 | 0 | 50.0% |
| character_trait_consistency | 10 | 5 | 5 | 0 | 50.0% |
| fixable_logic_inconsistency | 10 | 5 | 5 | 0 | 50.0% |
| narrative_tone_match | 10 | 5 | 5 | 0 | 50.0% |
| character_relationship_design | 10 | 5 | 5 | 0 | 50.0% |
| outline_structure_completeness | 10 | 6 | 4 | 0 | 60.0% |
| character_motivation_design | 10 | 7 | 3 | 0 | 70.0% |
| character_arc_design | 10 | 8 | 2 | 0 | 80.0% |
| outline_narrative_tension | 10 | 8 | 2 | 0 | 80.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 5 | 5 | 0 | 50% (5/10) |
| characters格式 | structural_integrity | - | 8 | 2 | 0 | 80% (8/10) |
| creative_intent格式 | structural_integrity | - | 5 | 5 | 0 | 50% (5/10) |
| outline格式 | structural_integrity | - | 7 | 3 | 0 | 70% (7/10) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 2 | 4 | 4 | 33% (2/6) |
| Y轴标签枚举 | enum_validity | - | 2 | 4 | 4 | 33% (2/6) |
| chapters目录存在性 | output_completeness | - | 5 | 5 | 0 | 50% (5/10) |
| characters文件存在性 | output_completeness | - | 8 | 2 | 0 | 80% (8/10) |
| creative_intent文件存在性 | output_completeness | - | 6 | 4 | 0 | 60% (6/10) |
| outline文件存在性 | output_completeness | - | 8 | 2 | 0 | 80% (8/10) |
| Y轴标签数量 | quantity_constraint | - | 2 | 4 | 4 | 33% (2/6) |
| forbidden_elements存在性 | quantity_constraint | - | 2 | 4 | 4 | 33% (2/6) |
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
| 写作准备确认 | sop_compliance | - | 3 | 7 | 0 | 30% (3/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 7 | 3 | 0 | 70% (7/10) |
| workspace文件规范 | workspace_file_compliance | basic | 6 | 4 | 0 | 60% (6/10) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 7 | 3 | 0 | 70% (7/10) |
| writing_log文件读取 | log_file_usage | - | 1 | 9 | 0 | 10% (1/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 1 | 1 | 8 | 50% (1/2) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 2 | 1 | 7 | 67% (2/3) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 5 | 5 | 0 | 50% (5/10) |
| 章节克隆检测 | chapter_cloning | gate | 4 | 6 | 0 | 40% (4/10) |
| 章节完成度 | chapter_completion | gate | 5 | 5 | 0 | 50% (5/10) |
| 章节长度稳定性 | chapter_length_stability | basic | 4 | 6 | 0 | 40% (4/10) |
| 章节产出存在性 | chapter_output_existence | gate | 5 | 5 | 0 | 50% (5/10) |
| 角色成长弧线设计 | character_arc_design | advanced | 8 | 2 | 0 | 80% (8/10) |
| 人物设计遵循度 | character_design_adherence | basic | 5 | 5 | 0 | 50% (5/10) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 7 | 3 | 0 | 70% (7/10) |
| 角色命名质量 | character_naming_quality | advanced | 2 | 8 | 0 | 20% (2/10) |
| 角色关系设计张力 | character_relationship_design | basic | 5 | 5 | 0 | 50% (5/10) |
| 人物设定一致性 | character_trait_consistency | basic | 5 | 5 | 0 | 50% (5/10) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 0 | 10 | 0 | 0% (0/10) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 0 | 2 | 0 | 0% (0/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 1 | 1 | 0 | 50% (1/2) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 2 | 8 | 0 | 20% (2/10) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 5 | 5 | 0 | 50% (5/10) |
| 完整叙事文本 | full_narrative_content | basic | 3 | 7 | 0 | 30% (3/10) |
| 题材契合度 | genre_fit | advanced | 0 | 10 | 0 | 0% (0/10) |
| 钩子设计 | hook_design | advanced | 1 | 9 | 0 | 10% (1/10) |
| 意象系统 | imagery_system | advanced | 3 | 7 | 0 | 30% (3/10) |
| 语言纯净性 | language_purity | basic | 3 | 7 | 0 | 30% (3/10) |
| 后期章节跑偏 | late_stage_digression | basic | 2 | 8 | 0 | 20% (2/10) |
| 主要角色一致性 | main_character_consistency | basic | 3 | 7 | 0 | 30% (3/10) |
| 叙事密度 | narrative_density | advanced | 1 | 9 | 0 | 10% (1/10) |
| 叙事调性匹配 | narrative_tone_match | basic | 5 | 5 | 0 | 50% (5/10) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 3 | 7 | 0 | 30% (3/10) |
| outline叙事张力 | outline_narrative_tension | advanced | 8 | 2 | 0 | 80% (8/10) |
| outline结构完整性 | outline_structure_completeness | basic | 6 | 4 | 0 | 60% (6/10) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 1 | 9 | 0 | 10% (1/10) |
| 段落重复检测 | paragraph_repetition | basic | 2 | 8 | 0 | 20% (2/10) |
| 情节推进 | plot_progression | basic | 4 | 6 | 0 | 40% (4/10) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 0 | 10 | 0 | 0% (0/10) |
| 反复结局 | repeated_endings | basic | 4 | 6 | 0 | 40% (4/10) |
| 语义重复检测 | semantic_redundancy | basic | 0 | 10 | 0 | 0% (0/10) |
| 结构功能性 | structural_design | advanced | 3 | 7 | 0 | 30% (3/10) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 1 | 9 | 0 | 10% (1/10) |
| 主题一致性 | theme_consistency | basic | 5 | 5 | 0 | 50% (5/10) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 40.49 | 3.80 | 77.37 |
| IP | 1 | 46.91 | 46.91 | 46.91 |
| VAGUE | 1 | 3.66 | 3.66 | 3.66 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| SHORT | 2 | 56.88 | 56.22 | 57.53 |
| MEDIUM | 8 | 32.59 | 3.66 | 77.37 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 37.09 | 37.09 | 37.09 |
| ANGSTY | 2 | 39.23 | 22.24 | 56.22 |
| BRAINY_ACTION | 1 | 32.51 | 32.51 | 32.51 |
| HEROINE | 1 | 37.13 | 37.13 | 37.13 |
| NEUTRAL | 1 | 46.91 | 46.91 | 46.91 |
| SUSPENSE | 1 | 77.37 | 77.37 | 77.37 |
| SWEET | 2 | 30.66 | 3.80 | 57.53 |
| SWEET_DRAMA | 1 | 3.66 | 3.66 | 3.66 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `章节克隆检测`
  - 子类: chapter_cloning, 层级: gate
  - 原因: 检测到21章近似克隆

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `章节长度稳定性`
  - 子类: chapter_length_stability, 层级: basic
  - 原因: 章节长度严重萎缩(后期仅为前期45%)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `段落重复检测`
  - 子类: paragraph_repetition, 层级: basic
  - 原因: 同章内段落重复21处

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `主要角色一致性`
  - 子类: main_character_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `人物设计遵循度`
  - 子类: character_design_adherence, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_HEROINE_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

### 业务规则遵循 (5个失败检查)

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

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `写作准备确认`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 数据一致性 (2个失败检查)

- **NW_CLEAR_SHORT_SWEET_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 其他玩家（群像））

- **NW_CLEAR_SHORT_SWEET_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 其他玩家（群像））
