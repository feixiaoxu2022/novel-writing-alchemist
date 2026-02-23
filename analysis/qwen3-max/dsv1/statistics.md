# Novel Writing Alchemist 评测统计报告

- **模型**: `qwen3-max-2026-01-23`
- **生成时间**: 2026-02-23T12:03:46.263381
- **评测目录**: `eval_dsv1_20260213_143137_qwen3-max-2026-01-23`
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
| 加权总分 | 68.62 | 60.50 | 75.10 | 14 |
| 内容分(x0.7) | 72.85 | 61.41 | 84.25 | 14 |
| 过程分(x0.3) | 58.75 | 50.00 | 64.43 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 13 | 92.9% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 56 | 0 | 0 | 100.0% |
| 业务规则遵循 | 222 | 169 | 53 | 56 | 76.1% |
| 记忆管理 | 28 | 0 | 28 | 0 | 0.0% |

### 2.2 内容创作质量

- **平均内容分**: 72.85 (范围: 61.41 ~ 84.25)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 50 | 49 | 1 | 0 | 98.0% |
| Basic(基础) | 224 | 191 | 33 | 0 | 85.3% |
| Advanced(优秀) | 140 | 81 | 59 | 14 | 57.9% |

- **Gate触发率**: 7.1% (1/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 14 | 14 | 0 | 0 | 100.0% |
| structural_integrity | 42 | 42 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 4 | 10 | 0 | 28.6% |
| required_skill_reading | 124 | 36 | 32 | 56 | 52.9% |
| sop_compliance | 28 | 18 | 10 | 0 | 64.3% |
| enum_validity | 28 | 27 | 1 | 0 | 96.4% |
| quantity_constraint | 28 | 28 | 0 | 0 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_creation | 14 | 0 | 14 | 0 | 0.0% |
| log_file_usage | 14 | 0 | 14 | 0 | 0.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 14 | 0 | 14 | 0 | 0.0% |
| genre_fit | 14 | 1 | 13 | 0 | 7.1% |
| semantic_redundancy | 14 | 1 | 13 | 0 | 7.1% |
| character_naming_quality | 14 | 1 | 13 | 0 | 7.1% |
| fixable_logic_inconsistency | 14 | 2 | 12 | 0 | 14.3% |
| narrative_density | 14 | 4 | 10 | 0 | 28.6% |
| narrative_tone_match | 14 | 8 | 6 | 0 | 57.1% |
| outline_execution_fidelity | 14 | 8 | 6 | 0 | 57.1% |
| structural_logic_defect | 14 | 9 | 5 | 0 | 64.3% |
| pacing_rationality_advanced | 14 | 11 | 3 | 0 | 78.6% |
| emotional_delivery_match | 14 | 11 | 3 | 0 | 78.6% |
| puzzle_logic_validity | 14 | 12 | 2 | 0 | 85.7% |
| hook_design | 14 | 12 | 2 | 0 | 85.7% |
| structural_design | 14 | 12 | 2 | 0 | 85.7% |
| chapter_completion | 14 | 13 | 1 | 0 | 92.9% |
| emotional_gradient | 14 | 13 | 1 | 0 | 92.9% |
| chapter_cloning | 14 | 13 | 0 | 1 | 100.0% |
| alternating_repetition | 14 | 9 | 0 | 5 | 100.0% |
| paragraph_repetition | 14 | 14 | 0 | 0 | 100.0% |
| theme_consistency | 14 | 14 | 0 | 0 | 100.0% |
| main_character_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_trait_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_design_adherence | 14 | 14 | 0 | 0 | 100.0% |
| language_purity | 14 | 14 | 0 | 0 | 100.0% |
| plot_progression | 14 | 14 | 0 | 0 | 100.0% |
| full_narrative_content | 28 | 28 | 0 | 0 | 100.0% |
| late_stage_digression | 14 | 14 | 0 | 0 | 100.0% |
| imagery_system | 14 | 14 | 0 | 0 | 100.0% |
| chapter_output_existence | 14 | 14 | 0 | 0 | 100.0% |
| repeated_endings | 14 | 14 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 69.59 | 62.32 | 75.10 |
| IP | 1 | 66.93 | 66.93 | 66.93 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 67.40 | 60.50 | 74.59 |
| SHORT | 5 | 73.38 | 69.67 | 75.10 |
| MEDIUM | 4 | 64.19 | 62.32 | 66.93 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 68.66 | 60.50 | 74.92 |
| NEUTRAL | 1 | 66.93 | 66.93 | 66.93 |
| SUSPENSE | 1 | 62.32 | 62.32 | 62.32 |
| SWEET | 3 | 71.16 | 63.27 | 75.10 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项46`
  - 子类: narrative_density, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项47`
  - 子类: puzzle_logic_validity, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

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

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项19`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求
