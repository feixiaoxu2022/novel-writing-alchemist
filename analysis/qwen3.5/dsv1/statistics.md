# Novel Writing Alchemist 评测统计报告

- **模型**: `qwen3.5-plus-2026-02-15`
- **生成时间**: 2026-02-25T16:32:50.606393
- **评测目录**: `evaluation_outputs/eval_dsv1_20260224_194821_qwen3.5-plus-2026-02-15`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 14 |
| 成功执行 | 13 |
| 执行错误 | 1 |
| 有checker结果 | 14 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 61.67 | 24.33 | 76.51 | 14 |
| 内容分(x0.7) | 56.81 | 0.00 | 79.86 | 14 |
| 过程分(x0.3) | 72.99 | 56.10 | 89.43 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 13 | 92.9% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 45 | 11 | 0 | 80.4% |
| 业务规则遵循 | 238 | 212 | 26 | 54 | 89.1% |
| 记忆管理 | 18 | 12 | 6 | 0 | 66.7% |

### 2.2 内容创作质量

- **平均内容分**: 56.81 (范围: 0.00 ~ 79.86)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 38 | 35 | 3 | 0 | 92.1% |
| Basic(基础) | 222 | 138 | 84 | 2 | 62.2% |
| Advanced(优秀) | 126 | 62 | 64 | 0 | 49.2% |

- **Gate触发率**: 7.1% (1/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 42 | 32 | 10 | 0 | 76.2% |
| naming_convention | 14 | 13 | 1 | 0 | 92.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 8 | 6 | 0 | 57.1% |
| required_skill_reading | 124 | 61 | 19 | 44 | 76.2% |
| sop_compliance | 28 | 17 | 1 | 10 | 94.4% |
| enum_validity | 28 | 28 | 0 | 0 | 100.0% |
| quantity_constraint | 28 | 28 | 0 | 0 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |
| workspace_file_compliance | 14 | 14 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 3 | 6 | 5 | 33.3% |
| log_file_creation | 14 | 9 | 0 | 5 | 100.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_outline | 14 | 6 | 8 | 0 | 42.9% |
| character_presence_in_chapters | 14 | 8 | 5 | 1 | 61.5% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| logical_contradiction | 14 | 0 | 14 | 0 | 0.0% |
| dialogue_character_distinction | 14 | 0 | 14 | 0 | 0.0% |
| semantic_redundancy | 14 | 0 | 14 | 0 | 0.0% |
| genre_fit | 14 | 3 | 11 | 0 | 21.4% |
| narrative_density | 14 | 4 | 10 | 0 | 28.6% |
| pacing_rationality_advanced | 14 | 4 | 10 | 0 | 28.6% |
| outline_execution_fidelity | 14 | 5 | 9 | 0 | 35.7% |
| narrative_tone_match | 14 | 6 | 8 | 0 | 42.9% |
| late_stage_digression | 14 | 6 | 8 | 0 | 42.9% |
| puzzle_logic_validity | 14 | 6 | 8 | 0 | 42.9% |
| language_purity | 14 | 7 | 7 | 0 | 50.0% |
| emotional_gradient | 14 | 9 | 5 | 0 | 64.3% |
| character_design_adherence | 14 | 10 | 4 | 0 | 71.4% |
| repeated_endings | 14 | 10 | 4 | 0 | 71.4% |
| chapter_length_stability | 14 | 9 | 3 | 2 | 75.0% |
| full_narrative_content | 14 | 11 | 3 | 0 | 78.6% |
| hook_design | 14 | 11 | 3 | 0 | 78.6% |
| main_character_consistency | 14 | 12 | 2 | 0 | 85.7% |
| character_trait_consistency | 14 | 12 | 2 | 0 | 85.7% |
| plot_progression | 14 | 12 | 2 | 0 | 85.7% |
| structural_design | 14 | 12 | 2 | 0 | 85.7% |
| emotional_delivery_match | 14 | 12 | 2 | 0 | 85.7% |
| alternating_repetition | 14 | 9 | 1 | 4 | 90.0% |
| chapter_cloning | 14 | 13 | 1 | 0 | 92.9% |
| chapter_completion | 14 | 13 | 1 | 0 | 92.9% |
| paragraph_repetition | 14 | 13 | 1 | 0 | 92.9% |
| theme_consistency | 14 | 13 | 1 | 0 | 92.9% |
| imagery_system | 14 | 13 | 1 | 0 | 92.9% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 60.67 | 48.33 | 73.84 |
| IP | 1 | 62.95 | 62.95 | 62.95 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 62.99 | 24.33 | 76.51 |
| SHORT | 5 | 64.79 | 58.68 | 73.84 |
| MEDIUM | 4 | 56.09 | 48.33 | 62.95 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 62.06 | 24.33 | 76.51 |
| NEUTRAL | 1 | 62.95 | 62.95 | 62.95 |
| SUSPENSE | 1 | 60.93 | 60.93 | 60.93 |
| SWEET | 3 | 60.28 | 48.33 | 72.82 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取配方知识库`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取大纲设计指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取写作技巧指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取设定一致性管理指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取感情线写作指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `主要角色一致性`
  - 子类: main_character_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `人物设计遵循度`
  - 子类: character_design_adherence, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `结构性逻辑硬伤`
  - 子类: logical_contradiction, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `语言纯净性`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `反复结局`
  - 子类: repeated_endings, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_002** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_003** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SWEET_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_002** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_003** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 托马斯·哈特利）

- **NW_CLEAR_MEDIUM_SWEET_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 陈建国, 周明宇）

- **NW_CLEAR_MEDIUM_SWEET_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 陈建国）

- **NW_CLEAR_SHORT_ANGSTY_001** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 王老师）

- **NW_CLEAR_SHORT_ANGSTY_002** / `角色大纲规划完整性`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 老周, 电台声音（回忆））
