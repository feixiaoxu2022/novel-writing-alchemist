# Novel Writing Alchemist 评测统计报告

- **模型**: `kimi-k2.5`
- **生成时间**: 2026-02-23T12:03:46.010194
- **评测目录**: `eval_dsv1_20260211_202557_kimi-k2.5`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 14 |
| 成功执行 | 14 |
| 执行错误 | 0 |
| 有checker结果 | 14 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 71.23 | 57.80 | 85.91 | 14 |
| 内容分(x0.7) | 67.39 | 41.75 | 88.25 | 14 |
| 过程分(x0.3) | 80.17 | 58.33 | 97.93 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 14 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 48 | 8 | 0 | 85.7% |
| 业务规则遵循 | 222 | 161 | 61 | 56 | 72.5% |
| 记忆管理 | 28 | 23 | 5 | 0 | 82.1% |

### 2.2 内容创作质量

- **平均内容分**: 67.39 (范围: 41.75 ~ 88.25)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 51 | 51 | 0 | 0 | 100.0% |
| Basic(基础) | 224 | 164 | 60 | 0 | 73.2% |
| Advanced(优秀) | 140 | 82 | 58 | 14 | 58.6% |

- **Gate触发率**: 0.0% (0/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 42 | 34 | 8 | 0 | 81.0% |
| naming_convention | 14 | 14 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 2 | 12 | 0 | 14.3% |
| required_skill_reading | 124 | 35 | 33 | 56 | 51.5% |
| sop_compliance | 28 | 16 | 12 | 0 | 57.1% |
| enum_validity | 28 | 26 | 2 | 0 | 92.9% |
| quantity_constraint | 28 | 26 | 2 | 0 | 92.9% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 9 | 5 | 0 | 64.3% |
| log_file_creation | 14 | 14 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 14 | 0 | 14 | 0 | 0.0% |
| fixable_logic_inconsistency | 14 | 0 | 14 | 0 | 0.0% |
| semantic_redundancy | 14 | 1 | 13 | 0 | 7.1% |
| character_naming_quality | 14 | 3 | 11 | 0 | 21.4% |
| genre_fit | 14 | 5 | 9 | 0 | 35.7% |
| late_stage_digression | 14 | 6 | 8 | 0 | 42.9% |
| structural_logic_defect | 14 | 6 | 8 | 0 | 42.9% |
| language_purity | 14 | 7 | 7 | 0 | 50.0% |
| outline_execution_fidelity | 14 | 7 | 7 | 0 | 50.0% |
| narrative_density | 14 | 7 | 7 | 0 | 50.0% |
| narrative_tone_match | 14 | 8 | 6 | 0 | 57.1% |
| puzzle_logic_validity | 14 | 8 | 6 | 0 | 57.1% |
| pacing_rationality_advanced | 14 | 8 | 6 | 0 | 57.1% |
| emotional_delivery_match | 14 | 11 | 3 | 0 | 78.6% |
| character_trait_consistency | 14 | 12 | 2 | 0 | 85.7% |
| full_narrative_content | 28 | 25 | 3 | 0 | 89.3% |
| theme_consistency | 14 | 13 | 1 | 0 | 92.9% |
| character_design_adherence | 14 | 13 | 1 | 0 | 92.9% |
| emotional_gradient | 14 | 13 | 1 | 0 | 92.9% |
| structural_design | 14 | 13 | 1 | 0 | 92.9% |
| repeated_endings | 14 | 13 | 1 | 0 | 92.9% |
| chapter_cloning | 14 | 14 | 0 | 0 | 100.0% |
| alternating_repetition | 14 | 9 | 0 | 5 | 100.0% |
| chapter_completion | 14 | 14 | 0 | 0 | 100.0% |
| paragraph_repetition | 14 | 14 | 0 | 0 | 100.0% |
| main_character_consistency | 14 | 14 | 0 | 0 | 100.0% |
| plot_progression | 14 | 14 | 0 | 0 | 100.0% |
| hook_design | 14 | 14 | 0 | 0 | 100.0% |
| imagery_system | 14 | 14 | 0 | 0 | 100.0% |
| chapter_output_existence | 14 | 14 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 70.66 | 57.80 | 85.91 |
| IP | 1 | 65.07 | 65.07 | 65.07 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 73.36 | 65.62 | 82.39 |
| SHORT | 5 | 76.66 | 68.92 | 85.91 |
| MEDIUM | 4 | 61.76 | 57.80 | 66.20 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 73.90 | 65.62 | 85.91 |
| NEUTRAL | 1 | 65.07 | 65.07 | 65.07 |
| SUSPENSE | 1 | 57.80 | 57.80 | 57.80 |
| SWEET | 3 | 69.75 | 57.97 | 79.85 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项26`
  - 子类: character_trait_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项39`
  - 子类: late_stage_digression, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_003** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_003** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_003** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_SWEET_001** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (5个失败检查)

- **NW_ULTRA_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_ULTRA_SHORT_ANGSTY_002** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_ULTRA_SHORT_ANGSTY_003** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_ULTRA_SHORT_ANGSTY_004** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_ULTRA_SHORT_ANGSTY_005** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
