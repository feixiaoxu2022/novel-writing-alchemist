# Novel Writing Alchemist 评测统计报告

- **模型**: `qwen3-max-2026-01-23`
- **生成时间**: 2026-02-23T12:03:46.444755
- **评测目录**: `eval_dsv2_20260213_143908_qwen3-max-2026-01-23`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 10 |
| 执行错误 | 5 |
| 有checker结果 | 10 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 70.41 | 60.27 | 77.62 | 10 |
| 内容分(x0.7) | 61.43 | 44.00 | 72.50 | 10 |
| 过程分(x0.3) | 91.37 | 65.20 | 98.33 | 10 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 8 | 80.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 40 | 38 | 2 | 0 | 95.0% |
| 业务规则遵循 | 188 | 168 | 20 | 8 | 89.4% |
| 记忆管理 | 20 | 18 | 2 | 0 | 90.0% |

### 2.2 内容创作质量

- **平均内容分**: 61.43 (范围: 44.00 ~ 72.50)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 31 | 29 | 2 | 0 | 93.5% |
| Basic(基础) | 163 | 129 | 34 | 0 | 79.1% |
| Advanced(优秀) | 100 | 45 | 55 | 10 | 45.0% |

- **Gate触发率**: 20.0% (2/10)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 30 | 28 | 2 | 0 | 93.3% |
| naming_convention | 10 | 10 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 10 | 0 | 10 | 0 | 0.0% |
| enum_validity | 20 | 15 | 1 | 4 | 93.8% |
| quantity_constraint | 20 | 15 | 1 | 4 | 93.8% |
| required_skill_reading | 85 | 80 | 5 | 0 | 94.1% |
| output_completeness | 40 | 38 | 2 | 0 | 95.0% |
| sop_compliance | 21 | 20 | 1 | 0 | 95.2% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 10 | 8 | 2 | 0 | 80.0% |
| log_file_creation | 10 | 10 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| genre_fit | 10 | 0 | 10 | 0 | 0.0% |
| dialogue_character_distinction | 10 | 1 | 9 | 0 | 10.0% |
| semantic_redundancy | 10 | 2 | 8 | 0 | 20.0% |
| structural_logic_defect | 10 | 2 | 8 | 0 | 20.0% |
| fixable_logic_inconsistency | 10 | 2 | 8 | 0 | 20.0% |
| character_naming_quality | 10 | 2 | 8 | 0 | 20.0% |
| narrative_tone_match | 10 | 3 | 7 | 0 | 30.0% |
| narrative_density | 10 | 4 | 6 | 0 | 40.0% |
| puzzle_logic_validity | 10 | 4 | 6 | 0 | 40.0% |
| pacing_rationality_advanced | 10 | 4 | 6 | 0 | 40.0% |
| outline_execution_fidelity | 10 | 7 | 3 | 0 | 70.0% |
| emotional_gradient | 10 | 7 | 3 | 0 | 70.0% |
| structural_design | 10 | 7 | 3 | 0 | 70.0% |
| chapter_completion | 10 | 8 | 2 | 0 | 80.0% |
| paragraph_repetition | 10 | 8 | 2 | 0 | 80.0% |
| hook_design | 10 | 8 | 2 | 0 | 80.0% |
| imagery_system | 10 | 8 | 2 | 0 | 80.0% |
| character_design_adherence | 12 | 10 | 2 | 0 | 83.3% |
| language_purity | 10 | 9 | 1 | 0 | 90.0% |
| full_narrative_content | 20 | 18 | 2 | 0 | 90.0% |
| emotional_delivery_match | 11 | 10 | 1 | 0 | 90.9% |
| chapter_cloning | 10 | 8 | 0 | 2 | 100.0% |
| alternating_repetition | 10 | 3 | 0 | 7 | 100.0% |
| theme_consistency | 10 | 10 | 0 | 0 | 100.0% |
| main_character_consistency | 10 | 10 | 0 | 0 | 100.0% |
| character_trait_consistency | 10 | 10 | 0 | 0 | 100.0% |
| plot_progression | 10 | 10 | 0 | 0 | 100.0% |
| late_stage_digression | 10 | 10 | 0 | 0 | 100.0% |
| chapter_output_existence | 10 | 10 | 0 | 0 | 100.0% |
| repeated_endings | 10 | 10 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 71.69 | 66.47 | 77.62 |
| IP | 1 | 60.27 | 60.27 | 60.27 |
| VAGUE | 1 | 70.31 | 70.31 | 70.31 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| SHORT | 2 | 77.46 | 77.30 | 77.62 |
| MEDIUM | 8 | 68.65 | 60.27 | 73.44 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 69.49 | 69.49 | 69.49 |
| ANGSTY | 2 | 74.06 | 70.50 | 77.62 |
| BRAINY_ACTION | 1 | 73.44 | 73.44 | 73.44 |
| HEROINE | 1 | 66.47 | 66.47 | 66.47 |
| NEUTRAL | 1 | 60.27 | 60.27 | 60.27 |
| SUSPENSE | 1 | 67.52 | 67.52 | 67.52 |
| SWEET | 2 | 74.25 | 71.20 | 77.30 |
| SWEET_DRAMA | 1 | 70.31 | 70.31 | 70.31 |

## 5. 失败案例索引

### 格式规范遵循 (2个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_VAGUE_MEDIUM_SWEET_DRAMA_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项29`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项46`
  - 子类: narrative_density, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项47`
  - 子类: puzzle_logic_validity, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项30`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项21`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 记忆管理 (2个失败检查)

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_VAGUE_MEDIUM_SWEET_DRAMA_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
