# Novel Writing Alchemist 评测统计报告

- **模型**: `ernie-5.0-thinking-preview`
- **生成时间**: 2026-02-23T12:03:46.956098
- **评测目录**: `eval_dsv1_20260205_140957_ernie-5.0-thinking-preview`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 14 |
| 成功执行 | 9 |
| 执行错误 | 5 |
| 有checker结果 | 9 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 61.06 | 40.60 | 70.20 | 9 |
| 内容分(x0.7) | 60.53 | 44.00 | 84.25 | 9 |
| 过程分(x0.3) | 62.33 | 29.17 | 97.77 | 9 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 9 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 36 | 31 | 5 | 0 | 86.1% |
| 业务规则遵循 | 135 | 86 | 49 | 44 | 63.7% |
| 记忆管理 | 18 | 7 | 11 | 0 | 38.9% |

### 2.2 内容创作质量

- **平均内容分**: 60.53 (范围: 44.00 ~ 84.25)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 33 | 33 | 0 | 0 | 100.0% |
| Basic(基础) | 143 | 99 | 44 | 0 | 69.2% |
| Advanced(优秀) | 90 | 43 | 47 | 9 | 47.8% |

- **Gate触发率**: 0.0% (0/9)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 27 | 23 | 4 | 0 | 85.2% |
| naming_convention | 9 | 8 | 1 | 0 | 88.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 9 | 2 | 7 | 0 | 22.2% |
| required_skill_reading | 80 | 14 | 30 | 36 | 31.8% |
| sop_compliance | 18 | 10 | 8 | 0 | 55.6% |
| output_completeness | 36 | 32 | 4 | 0 | 88.9% |
| enum_validity | 18 | 14 | 0 | 4 | 100.0% |
| quantity_constraint | 18 | 14 | 0 | 4 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 9 | 2 | 7 | 0 | 22.2% |
| log_file_creation | 9 | 5 | 4 | 0 | 55.6% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 9 | 0 | 9 | 0 | 0.0% |
| semantic_redundancy | 9 | 0 | 9 | 0 | 0.0% |
| genre_fit | 9 | 1 | 8 | 0 | 11.1% |
| fixable_logic_inconsistency | 9 | 1 | 8 | 0 | 11.1% |
| character_naming_quality | 9 | 1 | 8 | 0 | 11.1% |
| narrative_tone_match | 9 | 2 | 7 | 0 | 22.2% |
| pacing_rationality_advanced | 9 | 2 | 7 | 0 | 22.2% |
| structural_logic_defect | 9 | 2 | 7 | 0 | 22.2% |
| puzzle_logic_validity | 9 | 3 | 6 | 0 | 33.3% |
| narrative_density | 9 | 4 | 5 | 0 | 44.4% |
| outline_execution_fidelity | 9 | 5 | 4 | 0 | 55.6% |
| character_design_adherence | 9 | 6 | 3 | 0 | 66.7% |
| late_stage_digression | 9 | 6 | 3 | 0 | 66.7% |
| hook_design | 9 | 6 | 3 | 0 | 66.7% |
| paragraph_repetition | 9 | 7 | 2 | 0 | 77.8% |
| character_trait_consistency | 9 | 7 | 2 | 0 | 77.8% |
| full_narrative_content | 18 | 14 | 4 | 0 | 77.8% |
| emotional_delivery_match | 8 | 7 | 1 | 0 | 87.5% |
| language_purity | 9 | 8 | 1 | 0 | 88.9% |
| emotional_gradient | 9 | 8 | 1 | 0 | 88.9% |
| repeated_endings | 9 | 8 | 1 | 0 | 88.9% |
| chapter_cloning | 9 | 8 | 0 | 1 | 100.0% |
| alternating_repetition | 9 | 7 | 0 | 2 | 100.0% |
| chapter_completion | 9 | 9 | 0 | 0 | 100.0% |
| theme_consistency | 9 | 9 | 0 | 0 | 100.0% |
| main_character_consistency | 9 | 9 | 0 | 0 | 100.0% |
| plot_progression | 9 | 9 | 0 | 0 | 100.0% |
| imagery_system | 9 | 9 | 0 | 0 | 100.0% |
| structural_design | 9 | 9 | 0 | 0 | 100.0% |
| chapter_output_existence | 9 | 9 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 4 | 63.20 | 56.32 | 70.20 |
| IP | 1 | 60.13 | 60.13 | 60.13 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 4 | 59.16 | 40.60 | 68.97 |
| SHORT | 4 | 63.20 | 56.32 | 70.20 |
| MEDIUM | 1 | 60.13 | 60.13 | 60.13 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 7 | 61.68 | 40.60 | 70.20 |
| NEUTRAL | 1 | 60.13 | 60.13 | 60.13 |
| SWEET | 1 | 57.67 | 57.67 | 57.67 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项12`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项13`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项26`
  - 子类: character_trait_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项47`
  - 子类: puzzle_logic_validity, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项48`
  - 子类: genre_fit, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (5个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_ULTRA_SHORT_ANGSTY_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_ULTRA_SHORT_ANGSTY_001** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_003** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_ULTRA_SHORT_ANGSTY_005** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件
