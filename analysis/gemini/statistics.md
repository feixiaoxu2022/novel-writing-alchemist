# Novel Writing Alchemist 评测统计报告

- **模型**: `gemini-3-pro-preview`
- **生成时间**: 2026-02-27T11:42:25.072309
- **评测目录**: `eval_dsv2_20260215_002829_gemini-3-pro-preview`
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
| 加权总分 | 81.89 | 73.83 | 94.25 | 15 |
| 内容分(x0.7) | 84.51 | 70.45 | 93.21 | 15 |
| 过程分(x0.3) | 75.76 | 61.25 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 15 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 60 | 0 | 0 | 100.0% |
| 业务规则遵循 | 256 | 243 | 13 | 55 | 94.9% |
| 记忆管理 | 20 | 9 | 11 | 10 | 45.0% |

### 2.2 内容创作质量

- **平均内容分**: 84.51 (范围: 70.45 ~ 93.21)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 298 | 258 | 40 | 5 | 86.6% |
| Advanced(优秀) | 165 | 134 | 31 | 15 | 81.2% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |
| structural_integrity | 45 | 45 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 5 | 10 | 0 | 33.3% |
| workspace_file_compliance | 15 | 14 | 1 | 0 | 93.3% |
| sop_compliance | 31 | 20 | 1 | 10 | 95.2% |
| quantity_constraint | 30 | 29 | 1 | 0 | 96.7% |
| required_skill_reading | 130 | 85 | 0 | 45 | 100.0% |
| enum_validity | 30 | 30 | 0 | 0 | 100.0% |
| output_completeness | 60 | 60 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 0 | 10 | 5 | 0.0% |
| log_file_creation | 15 | 9 | 1 | 5 | 90.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 6 | 9 | 0 | 40.0% |
| character_presence_in_outline | 15 | 9 | 6 | 0 | 60.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 3 | 12 | 0 | 20.0% |
| character_naming_quality | 15 | 3 | 12 | 0 | 20.0% |
| outline_structure_completeness | 15 | 4 | 11 | 0 | 26.7% |
| dialogue_character_distinction | 15 | 7 | 8 | 0 | 46.7% |
| outline_execution_fidelity | 15 | 8 | 7 | 0 | 53.3% |
| structural_logic_defect | 15 | 10 | 5 | 0 | 66.7% |
| genre_fit | 15 | 10 | 5 | 0 | 66.7% |
| puzzle_logic_validity | 15 | 12 | 3 | 0 | 80.0% |
| character_relationship_design | 15 | 12 | 3 | 0 | 80.0% |
| late_stage_digression | 15 | 13 | 2 | 0 | 86.7% |
| hook_design | 15 | 13 | 2 | 0 | 86.7% |
| semantic_redundancy | 15 | 13 | 2 | 0 | 86.7% |
| character_motivation_design | 15 | 13 | 2 | 0 | 86.7% |
| character_design_adherence | 17 | 15 | 2 | 0 | 88.2% |
| character_trait_consistency | 15 | 14 | 1 | 0 | 93.3% |
| narrative_tone_match | 15 | 14 | 1 | 0 | 93.3% |
| narrative_density | 15 | 14 | 1 | 0 | 93.3% |
| pacing_rationality_advanced | 15 | 14 | 1 | 0 | 93.3% |
| structural_design | 15 | 14 | 1 | 0 | 93.3% |
| character_arc_design | 15 | 14 | 1 | 0 | 93.3% |
| emotional_delivery_match | 16 | 15 | 1 | 0 | 93.8% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| chapter_cloning | 15 | 14 | 0 | 1 | 100.0% |
| alternating_repetition | 15 | 6 | 0 | 9 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| chapter_length_stability | 15 | 10 | 0 | 5 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| language_purity | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| full_narrative_content | 15 | 15 | 0 | 0 | 100.0% |
| repeated_endings | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| outline_narrative_tension | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 15 | 0 | 0 | 100% (15/15) |
| characters格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent格式 | structural_integrity | - | 15 | 0 | 0 | 100% (15/15) |
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
| forbidden_elements存在性 | quantity_constraint | - | 14 | 1 | 0 | 93% (14/15) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 0 | 2 | 0 | 0% (0/2) |
| 超短篇字数 | range_constraint | - | 5 | 0 | 0 | 100% (5/5) |
| 读取characters的schema | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取creative_intent的schema | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取outline的schema | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取写作技巧指南 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取命名skill | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取大纲设计指南 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取感情线写作指南 | required_skill_reading | - | 5 | 0 | 0 | 100% (5/5) |
| 读取短篇skill | required_skill_reading | - | 0 | 0 | 5 | skip(5) |
| 读取设定一致性管理指南 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 读取配方知识库 | required_skill_reading | - | 10 | 0 | 5 | 100% (10/10) |
| 写作准备确认 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| 灵感激发交互 | sop_compliance | - | 0 | 1 | 0 | 0% (0/1) |
| 配方选择交互 | sop_compliance | - | 10 | 0 | 5 | 100% (10/10) |
| workspace文件规范 | workspace_file_compliance | basic | 14 | 1 | 0 | 93% (14/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 9 | 1 | 5 | 90% (9/10) |
| writing_log文件读取 | log_file_usage | - | 0 | 10 | 5 | 0% (0/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 6 | 9 | 0 | 40% (6/15) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 9 | 6 | 0 | 60% (9/15) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 6 | 0 | 9 | 100% (6/6) |
| 章节克隆检测 | chapter_cloning | gate | 14 | 0 | 1 | 100% (14/14) |
| 章节完成度 | chapter_completion | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 10 | 0 | 5 | 100% (10/10) |
| 章节产出存在性 | chapter_output_existence | gate | 15 | 0 | 0 | 100% (15/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 14 | 1 | 0 | 93% (14/15) |
| 人物设计遵循度 | character_design_adherence | basic | 15 | 0 | 0 | 100% (15/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 角色动机设计深度 | character_motivation_design | basic | 13 | 2 | 0 | 87% (13/15) |
| 角色命名质量 | character_naming_quality | advanced | 3 | 12 | 0 | 20% (3/15) |
| 角色关系设计张力 | character_relationship_design | basic | 12 | 3 | 0 | 80% (12/15) |
| 人物设定一致性 | character_trait_consistency | basic | 14 | 1 | 0 | 93% (14/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 7 | 8 | 0 | 47% (7/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 0 | 1 | 0 | 0% (0/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 2 | 0 | 0 | 100% (2/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 7 | 0 | 0 | 100% (7/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 15 | 0 | 0 | 100% (15/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 3 | 12 | 0 | 20% (3/15) |
| 完整叙事文本 | full_narrative_content | basic | 15 | 0 | 0 | 100% (15/15) |
| 题材契合度 | genre_fit | advanced | 10 | 5 | 0 | 67% (10/15) |
| 钩子设计 | hook_design | advanced | 13 | 2 | 0 | 87% (13/15) |
| 意象系统 | imagery_system | advanced | 15 | 0 | 0 | 100% (15/15) |
| 语言纯净性 | language_purity | basic | 15 | 0 | 0 | 100% (15/15) |
| 后期章节跑偏 | late_stage_digression | basic | 13 | 2 | 0 | 87% (13/15) |
| 主要角色一致性 | main_character_consistency | basic | 15 | 0 | 0 | 100% (15/15) |
| 叙事密度 | narrative_density | advanced | 14 | 1 | 0 | 93% (14/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 14 | 1 | 0 | 93% (14/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 8 | 7 | 0 | 53% (8/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 15 | 0 | 0 | 100% (15/15) |
| outline结构完整性 | outline_structure_completeness | basic | 4 | 11 | 0 | 27% (4/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 14 | 1 | 0 | 93% (14/15) |
| 段落重复检测 | paragraph_repetition | basic | 15 | 0 | 0 | 100% (15/15) |
| 情节推进 | plot_progression | basic | 15 | 0 | 0 | 100% (15/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 12 | 3 | 0 | 80% (12/15) |
| 反复结局 | repeated_endings | basic | 15 | 0 | 0 | 100% (15/15) |
| 语义重复检测 | semantic_redundancy | basic | 13 | 2 | 0 | 87% (13/15) |
| 结构功能性 | structural_design | advanced | 14 | 1 | 0 | 93% (14/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 10 | 5 | 0 | 67% (10/15) |
| 主题一致性 | theme_consistency | basic | 15 | 0 | 0 | 100% (15/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 80.42 | 73.83 | 84.60 |
| IP | 1 | 76.65 | 76.65 | 76.65 |
| VAGUE | 1 | 74.88 | 74.88 | 74.88 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 86.69 | 80.49 | 94.25 |
| SHORT | 2 | 81.85 | 79.10 | 84.60 |
| MEDIUM | 8 | 78.90 | 73.83 | 82.38 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 81.69 | 81.69 | 81.69 |
| ANGSTY | 7 | 84.75 | 79.10 | 94.25 |
| BRAINY_ACTION | 1 | 73.83 | 73.83 | 73.83 |
| HEROINE | 1 | 82.38 | 82.38 | 82.38 |
| NEUTRAL | 1 | 76.65 | 76.65 | 76.65 |
| SUSPENSE | 1 | 79.03 | 79.03 | 79.03 |
| SWEET | 2 | 83.28 | 81.96 | 84.60 |
| SWEET_DRAMA | 1 | 74.88 | 74.88 | 74.88 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现4处fixable类型逻辑问题: chapter_01明确写林砚父亲“在横断山脉失踪”“所有人都说遭遇泥石流”“连一点残骸都留不下”；但chapter_02阿木称其“死在鬼哭谷”，chapter_05又出现可辨认的林教授干尸。前文将状态设为“失踪且无残骸”，后文变为“已确认死亡且遗体可见”，缺少

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `后期章节跑偏`
  - 子类: late_stage_digression, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `智斗逻辑合理性`
  - 子类: puzzle_logic_validity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `题材契合度`
  - 子类: genre_fit, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `钩子设计`
  - 子类: hook_design, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `中篇字数_冒险`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `中篇字数_智斗`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_HEROINE_001** / `中篇字数_大女主`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 赵铁, 阿K）

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 王大彪）

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 馆长）

- **NW_CLEAR_MEDIUM_HEROINE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 林婉华（傅母））

- **NW_CLEAR_MEDIUM_HEROINE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 林婉华（傅母））
