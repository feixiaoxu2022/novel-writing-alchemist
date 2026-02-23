# Novel Writing Alchemist 评测统计报告

- **模型**: `doubao-seed-2-0-pro-260215`
- **生成时间**: 2026-02-23T12:03:45.719857
- **评测目录**: `eval_dsv1_20260215_110700_doubao-seed-2-0-pro-260215`
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
| 加权总分 | 73.45 | 58.03 | 89.15 | 14 |
| 内容分(x0.7) | 71.93 | 55.29 | 84.50 | 14 |
| 过程分(x0.3) | 77.01 | 62.50 | 100.00 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| qualified | 1 | 7.1% |
| unqualified | 13 | 92.9% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 53 | 3 | 0 | 94.6% |
| 业务规则遵循 | 187 | 164 | 23 | 91 | 87.7% |
| 记忆管理 | 18 | 4 | 14 | 0 | 22.2% |

### 2.2 内容创作质量

- **平均内容分**: 71.93 (范围: 55.29 ~ 84.50)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 49 | 49 | 0 | 0 | 100.0% |
| Basic(基础) | 224 | 184 | 40 | 0 | 82.1% |
| Advanced(优秀) | 140 | 79 | 61 | 14 | 56.4% |

- **Gate触发率**: 0.0% (0/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 14 | 13 | 1 | 0 | 92.9% |
| structural_integrity | 42 | 40 | 2 | 0 | 95.2% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 3 | 11 | 0 | 21.4% |
| required_skill_reading | 124 | 35 | 8 | 81 | 81.4% |
| enum_validity | 28 | 26 | 2 | 0 | 92.9% |
| quantity_constraint | 28 | 26 | 2 | 0 | 92.9% |
| sop_compliance | 28 | 18 | 0 | 10 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 0 | 9 | 5 | 0.0% |
| log_file_creation | 14 | 4 | 5 | 5 | 44.4% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 14 | 0 | 14 | 0 | 0.0% |
| fixable_logic_inconsistency | 14 | 0 | 14 | 0 | 0.0% |
| character_naming_quality | 14 | 1 | 13 | 0 | 7.1% |
| genre_fit | 14 | 2 | 12 | 0 | 14.3% |
| semantic_redundancy | 14 | 4 | 10 | 0 | 28.6% |
| narrative_tone_match | 14 | 7 | 7 | 0 | 50.0% |
| narrative_density | 14 | 7 | 7 | 0 | 50.0% |
| outline_execution_fidelity | 14 | 9 | 5 | 0 | 64.3% |
| puzzle_logic_validity | 14 | 9 | 5 | 0 | 64.3% |
| pacing_rationality_advanced | 14 | 9 | 5 | 0 | 64.3% |
| structural_logic_defect | 14 | 9 | 5 | 0 | 64.3% |
| late_stage_digression | 14 | 10 | 4 | 0 | 71.4% |
| hook_design | 14 | 11 | 3 | 0 | 78.6% |
| main_character_consistency | 14 | 12 | 2 | 0 | 85.7% |
| character_design_adherence | 14 | 12 | 2 | 0 | 85.7% |
| language_purity | 14 | 12 | 2 | 0 | 85.7% |
| emotional_delivery_match | 14 | 12 | 2 | 0 | 85.7% |
| structural_design | 14 | 13 | 1 | 0 | 92.9% |
| repeated_endings | 14 | 13 | 1 | 0 | 92.9% |
| chapter_cloning | 14 | 14 | 0 | 0 | 100.0% |
| alternating_repetition | 14 | 7 | 0 | 7 | 100.0% |
| chapter_completion | 14 | 14 | 0 | 0 | 100.0% |
| paragraph_repetition | 14 | 14 | 0 | 0 | 100.0% |
| theme_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_trait_consistency | 14 | 14 | 0 | 0 | 100.0% |
| plot_progression | 14 | 14 | 0 | 0 | 100.0% |
| full_narrative_content | 28 | 28 | 0 | 0 | 100.0% |
| imagery_system | 14 | 14 | 0 | 0 | 100.0% |
| emotional_gradient | 14 | 14 | 0 | 0 | 100.0% |
| chapter_output_existence | 14 | 14 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 68.32 | 58.03 | 77.72 |
| IP | 1 | 71.93 | 71.93 | 71.93 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 81.98 | 75.51 | 89.15 |
| SHORT | 5 | 71.63 | 64.12 | 77.72 |
| MEDIUM | 4 | 65.08 | 58.03 | 71.93 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 76.78 | 59.00 | 89.15 |
| NEUTRAL | 1 | 71.93 | 71.93 | 71.93 |
| SUSPENSE | 1 | 58.03 | 58.03 | 58.03 |
| SWEET | 3 | 69.12 | 64.12 | 71.88 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

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

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项46`
  - 子类: narrative_density, 层级: advanced
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

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

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

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项18`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

### 格式规范遵循 (3个失败检查)

- **NW_CLEAR_SHORT_SWEET_002** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_ULTRA_SHORT_ANGSTY_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_002** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整
