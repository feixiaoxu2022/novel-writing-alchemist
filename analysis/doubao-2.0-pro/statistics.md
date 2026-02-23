# Novel Writing Alchemist 评测统计报告

- **模型**: `doubao-seed-2-0-pro-260215`
- **生成时间**: 2026-02-23T17:14:01.006249
- **评测目录**: `evaluation_outputs/eval_dsv2_20260215_110711_doubao-seed-2-0-pro-260215`
- **Revision**: `latest` (实际: check_result_rev008.json)

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
| 加权总分 | 76.04 | 55.94 | 91.78 | 15 |
| 内容分(x0.7) | 74.10 | 48.71 | 92.00 | 15 |
| 过程分(x0.3) | 80.54 | 59.70 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 1 | 6.7% |
| qualified | 1 | 6.7% |
| unqualified | 13 | 86.7% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 56 | 4 | 0 | 93.3% |
| 业务规则遵循 | 241 | 167 | 74 | 55 | 69.3% |
| 记忆管理 | 20 | 16 | 4 | 0 | 80.0% |

### 2.2 内容创作质量

- **平均内容分**: 74.10 (范围: 48.71 ~ 92.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 50 | 50 | 0 | 0 | 100.0% |
| Basic(基础) | 243 | 197 | 46 | 0 | 81.1% |
| Advanced(优秀) | 150 | 95 | 55 | 15 | 63.3% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 41 | 4 | 0 | 91.1% |
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| enum_validity | 30 | 6 | 24 | 0 | 20.0% |
| quantity_constraint | 30 | 6 | 24 | 0 | 20.0% |
| range_constraint | 15 | 4 | 11 | 0 | 26.7% |
| required_skill_reading | 130 | 74 | 11 | 45 | 87.1% |
| sop_compliance | 31 | 19 | 2 | 10 | 90.5% |
| output_completeness | 60 | 58 | 2 | 0 | 96.7% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 6 | 4 | 5 | 60.0% |
| log_file_creation | 15 | 10 | 0 | 5 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 0 | 15 | 0 | 0.0% |
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| dialogue_character_distinction | 15 | 4 | 11 | 0 | 26.7% |
| genre_fit | 15 | 4 | 11 | 0 | 26.7% |
| narrative_tone_match | 15 | 7 | 8 | 0 | 46.7% |
| semantic_redundancy | 15 | 7 | 8 | 0 | 46.7% |
| outline_execution_fidelity | 15 | 8 | 7 | 0 | 53.3% |
| character_design_adherence | 17 | 10 | 7 | 0 | 58.8% |
| narrative_density | 15 | 10 | 5 | 0 | 66.7% |
| pacing_rationality_advanced | 15 | 10 | 5 | 0 | 66.7% |
| structural_logic_defect | 15 | 10 | 5 | 0 | 66.7% |
| emotional_delivery_match | 16 | 11 | 5 | 0 | 68.8% |
| puzzle_logic_validity | 15 | 11 | 4 | 0 | 73.3% |
| late_stage_digression | 15 | 13 | 2 | 0 | 86.7% |
| hook_design | 15 | 13 | 2 | 0 | 86.7% |
| structural_design | 15 | 13 | 2 | 0 | 86.7% |
| main_character_consistency | 15 | 14 | 1 | 0 | 93.3% |
| character_trait_consistency | 15 | 14 | 1 | 0 | 93.3% |
| language_purity | 15 | 14 | 1 | 0 | 93.3% |
| repeated_endings | 15 | 14 | 1 | 0 | 93.3% |
| chapter_cloning | 15 | 10 | 0 | 5 | 100.0% |
| alternating_repetition | 15 | 10 | 0 | 5 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| full_narrative_content | 30 | 30 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 71.33 | 55.94 | 77.92 |
| IP | 1 | 77.07 | 77.07 | 77.07 |
| VAGUE | 1 | 68.89 | 68.89 | 68.89 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 84.79 | 79.69 | 91.78 |
| SHORT | 2 | 72.75 | 67.85 | 77.65 |
| MEDIUM | 8 | 71.38 | 55.94 | 77.92 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 73.28 | 73.28 | 73.28 |
| ANGSTY | 7 | 82.79 | 77.65 | 91.78 |
| BRAINY_ACTION | 1 | 68.28 | 68.28 | 68.28 |
| HEROINE | 1 | 72.63 | 72.63 | 72.63 |
| NEUTRAL | 1 | 77.07 | 77.07 | 77.07 |
| SUSPENSE | 1 | 55.94 | 55.94 | 55.94 |
| SWEET | 2 | 72.46 | 67.85 | 77.07 |
| SWEET_DRAMA | 1 | 68.89 | 68.89 | 68.89 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项18`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项19`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项20`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项21`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项29`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项46`
  - 子类: narrative_density, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (4个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 格式规范遵循 (4个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_003** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_004** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_005** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整
