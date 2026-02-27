# Novel Writing Alchemist 评测统计报告

- **模型**: `kimi-k2.5`
- **生成时间**: 2026-02-27T11:42:26.097806
- **评测目录**: `eval_dsv2_20260211_131949_kimi-k2.5`
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
| 加权总分 | 77.28 | 58.76 | 90.15 | 15 |
| 内容分(x0.7) | 75.82 | 54.18 | 92.73 | 15 |
| 过程分(x0.3) | 80.68 | 52.50 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 1 | 6.7% |
| unqualified | 14 | 93.3% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 48 | 12 | 0 | 80.0% |
| 业务规则遵循 | 167 | 143 | 24 | 144 | 85.6% |
| 记忆管理 | 20 | 17 | 3 | 10 | 85.0% |

### 2.2 内容创作质量

- **平均内容分**: 75.82 (范围: 54.18 ~ 92.73)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 0 | 0 | 0 | 0 | 100.0% |
| Basic(基础) | 297 | 229 | 68 | 6 | 77.1% |
| Advanced(优秀) | 165 | 121 | 44 | 15 | 73.3% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 33 | 12 | 0 | 73.3% |
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| required_skill_reading | 130 | 0 | 0 | 130 | 0.0% |
| range_constraint | 15 | 3 | 12 | 0 | 20.0% |
| sop_compliance | 31 | 17 | 4 | 10 | 81.0% |
| workspace_file_compliance | 15 | 13 | 2 | 0 | 86.7% |
| quantity_constraint | 30 | 25 | 3 | 2 | 89.3% |
| enum_validity | 30 | 26 | 2 | 2 | 92.9% |
| output_completeness | 60 | 59 | 1 | 0 | 98.3% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 7 | 3 | 5 | 70.0% |
| log_file_creation | 15 | 10 | 0 | 5 | 100.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 2 | 3 | 10 | 40.0% |
| character_presence_in_outline | 15 | 4 | 1 | 10 | 80.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 15 | 0 | 15 | 0 | 0.0% |
| fixable_logic_inconsistency | 15 | 1 | 14 | 0 | 6.7% |
| character_naming_quality | 15 | 2 | 13 | 0 | 13.3% |
| chapter_length_stability | 15 | 3 | 6 | 6 | 33.3% |
| structural_logic_defect | 15 | 6 | 9 | 0 | 40.0% |
| semantic_redundancy | 15 | 6 | 9 | 0 | 40.0% |
| language_purity | 15 | 7 | 8 | 0 | 46.7% |
| outline_structure_completeness | 15 | 7 | 8 | 0 | 46.7% |
| outline_execution_fidelity | 15 | 8 | 7 | 0 | 53.3% |
| genre_fit | 15 | 8 | 7 | 0 | 53.3% |
| puzzle_logic_validity | 15 | 10 | 5 | 0 | 66.7% |
| narrative_tone_match | 15 | 11 | 4 | 0 | 73.3% |
| late_stage_digression | 15 | 11 | 4 | 0 | 73.3% |
| pacing_rationality_advanced | 15 | 12 | 3 | 0 | 80.0% |
| character_motivation_design | 15 | 13 | 2 | 0 | 86.7% |
| character_arc_design | 15 | 13 | 2 | 0 | 86.7% |
| emotional_delivery_match | 16 | 14 | 2 | 0 | 87.5% |
| character_trait_consistency | 15 | 14 | 1 | 0 | 93.3% |
| full_narrative_content | 15 | 14 | 1 | 0 | 93.3% |
| narrative_density | 15 | 14 | 1 | 0 | 93.3% |
| imagery_system | 15 | 14 | 1 | 0 | 93.3% |
| structural_design | 15 | 14 | 1 | 0 | 93.3% |
| character_relationship_design | 15 | 14 | 1 | 0 | 93.3% |
| character_design_adherence | 17 | 16 | 1 | 0 | 94.1% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| chapter_cloning | 15 | 11 | 0 | 4 | 100.0% |
| alternating_repetition | 15 | 9 | 0 | 6 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| repeated_endings | 15 | 15 | 0 | 0 | 100.0% |
| hook_design | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| outline_narrative_tension | 15 | 15 | 0 | 0 | 100.0% |

## 3b. 逐检查项通过率

### 格式规范遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 章节命名格式 | naming_convention | - | 15 | 0 | 0 | 100% (15/15) |
| characters格式 | structural_integrity | - | 10 | 5 | 0 | 67% (10/15) |
| creative_intent格式 | structural_integrity | - | 12 | 3 | 0 | 80% (12/15) |
| outline格式 | structural_integrity | - | 11 | 4 | 0 | 73% (11/15) |

### 业务规则遵循

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| X轴模式ID格式 | enum_validity | - | 13 | 1 | 1 | 93% (13/14) |
| Y轴标签枚举 | enum_validity | - | 13 | 1 | 1 | 93% (13/14) |
| chapters目录存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| characters文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| creative_intent文件存在性 | output_completeness | - | 14 | 1 | 0 | 93% (14/15) |
| outline文件存在性 | output_completeness | - | 15 | 0 | 0 | 100% (15/15) |
| Y轴标签数量 | quantity_constraint | - | 12 | 2 | 1 | 86% (12/14) |
| forbidden_elements存在性 | quantity_constraint | - | 13 | 1 | 1 | 93% (13/14) |
| 中篇字数 | range_constraint | - | 0 | 5 | 0 | 0% (0/5) |
| 中篇字数_冒险 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_大女主 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 中篇字数_智斗 | range_constraint | - | 0 | 1 | 0 | 0% (0/1) |
| 短篇字数 | range_constraint | - | 0 | 2 | 0 | 0% (0/2) |
| 超短篇字数 | range_constraint | - | 3 | 2 | 0 | 60% (3/5) |
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
| 配方选择交互 | sop_compliance | - | 8 | 2 | 5 | 80% (8/10) |
| workspace文件规范 | workspace_file_compliance | basic | 13 | 2 | 0 | 87% (13/15) |

### 记忆管理

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| writing_log文件创建 | log_file_creation | - | 10 | 0 | 5 | 100% (10/10) |
| writing_log文件读取 | log_file_usage | - | 7 | 3 | 5 | 70% (7/10) |

### 数据一致性

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 角色正文出场完整性 | character_presence_in_chapters | - | 2 | 3 | 10 | 40% (2/5) |
| 角色大纲规划完整性 | character_presence_in_outline | - | 4 | 1 | 10 | 80% (4/5) |

### 内容创作质量

| 检查项 | 子类 | 层级 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|------|------|--------|
| 交替重复检测 | alternating_repetition | gate | 9 | 0 | 6 | 100% (9/9) |
| 章节克隆检测 | chapter_cloning | gate | 11 | 0 | 4 | 100% (11/11) |
| 章节完成度 | chapter_completion | gate | 15 | 0 | 0 | 100% (15/15) |
| 章节长度稳定性 | chapter_length_stability | basic | 3 | 6 | 6 | 33% (3/9) |
| 章节产出存在性 | chapter_output_existence | gate | 15 | 0 | 0 | 100% (15/15) |
| 角色成长弧线设计 | character_arc_design | advanced | 13 | 2 | 0 | 87% (13/15) |
| 人物设计遵循度 | character_design_adherence | basic | 15 | 0 | 0 | 100% (15/15) |
| 反套路检查 | character_design_adherence | basic | 0 | 1 | 0 | 0% (0/1) |
| 女主独立性检查 | character_design_adherence | basic | 1 | 0 | 0 | 100% (1/1) |
| 角色动机设计深度 | character_motivation_design | basic | 13 | 2 | 0 | 87% (13/15) |
| 角色命名质量 | character_naming_quality | advanced | 2 | 13 | 0 | 13% (2/15) |
| 角色关系设计张力 | character_relationship_design | basic | 14 | 1 | 0 | 93% (14/15) |
| 人物设定一致性 | character_trait_consistency | basic | 14 | 1 | 0 | 93% (14/15) |
| 角色语言辨识度 | dialogue_character_distinction | advanced | 0 | 15 | 0 | 0% (0/15) |
| 伏笔回收检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付冒险 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付大女主 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付智斗 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付烧脑 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜宠外虐 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感交付甜爽 | emotional_delivery_match | basic | 0 | 2 | 0 | 0% (0/2) |
| 情感交付虐心 | emotional_delivery_match | basic | 7 | 0 | 0 | 100% (7/7) |
| 非恋爱主线检查 | emotional_delivery_match | basic | 1 | 0 | 0 | 100% (1/1) |
| 情感弧线层次 | emotional_gradient | advanced | 15 | 0 | 0 | 100% (15/15) |
| 可修复逻辑瑕疵 | fixable_logic_inconsistency | advanced | 1 | 14 | 0 | 7% (1/15) |
| 完整叙事文本 | full_narrative_content | basic | 14 | 1 | 0 | 93% (14/15) |
| 题材契合度 | genre_fit | advanced | 8 | 7 | 0 | 53% (8/15) |
| 钩子设计 | hook_design | advanced | 15 | 0 | 0 | 100% (15/15) |
| 意象系统 | imagery_system | advanced | 14 | 1 | 0 | 93% (14/15) |
| 语言纯净性 | language_purity | basic | 7 | 8 | 0 | 47% (7/15) |
| 后期章节跑偏 | late_stage_digression | basic | 11 | 4 | 0 | 73% (11/15) |
| 主要角色一致性 | main_character_consistency | basic | 15 | 0 | 0 | 100% (15/15) |
| 叙事密度 | narrative_density | advanced | 14 | 1 | 0 | 93% (14/15) |
| 叙事调性匹配 | narrative_tone_match | basic | 11 | 4 | 0 | 73% (11/15) |
| 大纲执行忠实度 | outline_execution_fidelity | basic | 8 | 7 | 0 | 53% (8/15) |
| outline叙事张力 | outline_narrative_tension | advanced | 15 | 0 | 0 | 100% (15/15) |
| outline结构完整性 | outline_structure_completeness | basic | 7 | 8 | 0 | 47% (7/15) |
| 剧情节奏合理性 | pacing_rationality_advanced | advanced | 12 | 3 | 0 | 80% (12/15) |
| 段落重复检测 | paragraph_repetition | basic | 15 | 0 | 0 | 100% (15/15) |
| 情节推进 | plot_progression | basic | 15 | 0 | 0 | 100% (15/15) |
| 智斗逻辑合理性 | puzzle_logic_validity | basic | 10 | 5 | 0 | 67% (10/15) |
| 反复结局 | repeated_endings | basic | 15 | 0 | 0 | 100% (15/15) |
| 语义重复检测 | semantic_redundancy | basic | 6 | 9 | 0 | 40% (6/15) |
| 结构功能性 | structural_design | advanced | 14 | 1 | 0 | 93% (14/15) |
| 结构性逻辑硬伤 | structural_logic_defect | basic | 6 | 9 | 0 | 40% (6/15) |
| 主题一致性 | theme_consistency | basic | 15 | 0 | 0 | 100% (15/15) |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 73.96 | 58.76 | 83.78 |
| IP | 1 | 67.22 | 67.22 | 67.22 |
| VAGUE | 1 | 85.41 | 85.41 | 85.41 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 82.97 | 79.73 | 90.15 |
| SHORT | 2 | 78.14 | 72.68 | 83.60 |
| MEDIUM | 8 | 73.51 | 58.76 | 85.41 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 80.70 | 80.70 | 80.70 |
| ANGSTY | 7 | 83.17 | 79.73 | 90.15 |
| BRAINY_ACTION | 1 | 66.58 | 66.58 | 66.58 |
| HEROINE | 1 | 74.91 | 74.91 | 74.91 |
| NEUTRAL | 1 | 67.22 | 67.22 | 67.22 |
| SUSPENSE | 1 | 70.70 | 70.70 | 70.70 |
| SWEET | 2 | 65.72 | 58.76 | 72.68 |
| SWEET_DRAMA | 1 | 85.41 | 85.41 | 85.41 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `章节长度稳定性`
  - 子类: chapter_length_stability, 层级: basic
  - 原因: 章节长度严重萎缩(后期仅为前期37%)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现2处structural类型逻辑问题: 第15章结尾两人已到“天门”且洞口外出现阿普；但第16章又写两人还在为“撑不到天门”找食物，像尚未抵达天门；第19章又再次“终于到达天门”。同一关键地点被重复抵达，且第15章出现的阿普并未承接解释。; 第25章称古城将“限制游客进入，只供学术研究使用/建立

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现4处fixable类型逻辑问题: 第15章进入山洞使用“手电筒”；第19章同一段进入洞内却写“把火把点燃”，照明设备从手电筒变为火把，缺少丢失/损坏/替换的交代。; 第20-21章阿普拿出“布包”称其一直保存父辈的笔记和信件并交给两人；但第13章两人在“废弃营地”已自行挖出父辈的照片/信件/残页

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `语言纯净性`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事调性匹配`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `workspace文件规范`
  - 子类: workspace_file_compliance, 层级: basic
  - 原因: workspace中存在白名单外的文件: ['outline_adjusted.json']

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `中篇字数_冒险`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `X轴模式ID格式`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `Y轴标签枚举`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `Y轴标签数量`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `characters格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_HEROINE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_SWEET_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SWEET_001** / `characters格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SWEET_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (3个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_IP_MEDIUM_NEUTRAL_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 数据一致性 (4个失败检查)

- **NW_IP_MEDIUM_NEUTRAL_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（主角: 约翰·马斯顿（John Marston）; 配角: 安德鲁·米尔顿（Andrew Milton）, 亚瑟·摩根（Arthur Morgan））

- **NW_IP_MEDIUM_NEUTRAL_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（主角: 约翰·马斯顿（John Marston）; 配角: 马邦德（师爷）, 安德鲁·米尔顿（Andrew Milton）, 亚瑟·摩根（Arthur Morgan））

- **NW_ULTRA_SHORT_ANGSTY_002** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 护士长）

- **NW_ULTRA_SHORT_ANGSTY_003** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（主角: 零号（顾临））
