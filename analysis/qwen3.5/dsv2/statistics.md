# Novel Writing Alchemist 评测统计报告

- **模型**: `qwen3.5-plus-2026-02-15`
- **生成时间**: 2026-02-25T16:33:05.199465
- **评测目录**: `evaluation_outputs/eval_dsv2_20260224_194934_qwen3.5-plus-2026-02-15`
- **Revision**: `rev008` (实际: check_result_rev008.json)

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
| 加权总分 | 71.91 | 57.70 | 88.26 | 15 |
| 内容分(x0.7) | 67.17 | 42.64 | 87.56 | 15 |
| 过程分(x0.3) | 82.96 | 56.57 | 96.60 | 15 |

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
| 记忆管理 | 20 | 19 | 1 | 0 | 95.0% |

### 2.2 内容创作质量

- **平均内容分**: 67.17 (范围: 42.64 ~ 87.56)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 40 | 40 | 0 | 0 | 100.0% |
| Basic(基础) | 238 | 165 | 73 | 5 | 69.3% |
| Advanced(优秀) | 135 | 86 | 49 | 0 | 63.7% |

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
| logical_contradiction | 15 | 0 | 15 | 0 | 0.0% |
| dialogue_character_distinction | 15 | 0 | 15 | 0 | 0.0% |
| semantic_redundancy | 15 | 0 | 15 | 0 | 0.0% |
| puzzle_logic_validity | 15 | 6 | 9 | 0 | 40.0% |
| genre_fit | 15 | 6 | 9 | 0 | 40.0% |
| outline_execution_fidelity | 15 | 7 | 8 | 0 | 46.7% |
| narrative_tone_match | 15 | 8 | 7 | 0 | 53.3% |
| pacing_rationality_advanced | 15 | 8 | 7 | 0 | 53.3% |
| late_stage_digression | 15 | 9 | 6 | 0 | 60.0% |
| language_purity | 15 | 10 | 5 | 0 | 66.7% |
| full_narrative_content | 15 | 10 | 5 | 0 | 66.7% |
| narrative_density | 15 | 10 | 5 | 0 | 66.7% |
| character_design_adherence | 17 | 13 | 4 | 0 | 76.5% |
| character_trait_consistency | 15 | 12 | 3 | 0 | 80.0% |
| hook_design | 15 | 12 | 3 | 0 | 80.0% |
| paragraph_repetition | 15 | 13 | 2 | 0 | 86.7% |
| emotional_delivery_match | 16 | 14 | 2 | 0 | 87.5% |
| repeated_endings | 15 | 14 | 1 | 0 | 93.3% |
| emotional_gradient | 15 | 14 | 1 | 0 | 93.3% |
| chapter_cloning | 15 | 15 | 0 | 0 | 100.0% |
| alternating_repetition | 15 | 10 | 0 | 5 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| chapter_length_stability | 15 | 10 | 0 | 5 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| structural_design | 15 | 15 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 68.11 | 57.70 | 76.70 |
| IP | 1 | 63.83 | 63.83 | 63.83 |
| VAGUE | 1 | 76.52 | 76.52 | 76.52 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 78.67 | 70.32 | 88.26 |
| SHORT | 2 | 71.63 | 68.13 | 75.14 |
| MEDIUM | 8 | 67.75 | 57.70 | 76.70 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 62.76 | 62.76 | 62.76 |
| ANGSTY | 7 | 74.68 | 61.25 | 88.26 |
| BRAINY_ACTION | 1 | 73.39 | 73.39 | 73.39 |
| HEROINE | 1 | 69.84 | 69.84 | 69.84 |
| NEUTRAL | 1 | 63.83 | 63.83 | 63.83 |
| SUSPENSE | 1 | 76.70 | 76.70 | 76.70 |
| SWEET | 2 | 66.42 | 57.70 | 75.14 |
| SWEET_DRAMA | 1 | 76.52 | 76.52 | 76.52 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `人物设定一致性`
  - 子类: character_trait_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `人物设计遵循度`
  - 子类: character_design_adherence, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构性逻辑硬伤`
  - 子类: logical_contradiction, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `语言纯净性`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事调性匹配`
  - 子类: narrative_tone_match, 层级: basic
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
