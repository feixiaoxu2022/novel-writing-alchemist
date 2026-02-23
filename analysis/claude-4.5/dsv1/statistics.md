# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-5-20251101`
- **生成时间**: 2026-02-23T12:03:45.230173
- **评测目录**: `eval_dsv1_20260205_132400_claude-opus-4-5-20251101`
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
| 加权总分 | 77.91 | 63.70 | 85.35 | 14 |
| 内容分(x0.7) | 77.00 | 53.50 | 92.00 | 14 |
| 过程分(x0.3) | 80.03 | 58.33 | 97.93 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 2 | 14.3% |
| unqualified | 12 | 85.7% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 48 | 8 | 0 | 85.7% |
| 业务规则遵循 | 222 | 168 | 54 | 56 | 75.7% |
| 记忆管理 | 28 | 22 | 6 | 0 | 78.6% |

### 2.2 内容创作质量

- **平均内容分**: 77.00 (范围: 53.50 ~ 92.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 49 | 49 | 0 | 0 | 100.0% |
| Basic(基础) | 224 | 185 | 39 | 0 | 82.6% |
| Advanced(优秀) | 140 | 96 | 44 | 14 | 68.6% |

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
| range_constraint | 14 | 3 | 11 | 0 | 21.4% |
| required_skill_reading | 124 | 36 | 32 | 56 | 52.9% |
| sop_compliance | 28 | 18 | 10 | 0 | 64.3% |
| enum_validity | 28 | 27 | 1 | 0 | 96.4% |
| quantity_constraint | 28 | 28 | 0 | 0 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 8 | 6 | 0 | 57.1% |
| log_file_creation | 14 | 14 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 14 | 0 | 14 | 0 | 0.0% |
| dialogue_character_distinction | 14 | 2 | 12 | 0 | 14.3% |
| semantic_redundancy | 14 | 3 | 11 | 0 | 21.4% |
| character_naming_quality | 14 | 5 | 9 | 0 | 35.7% |
| outline_execution_fidelity | 14 | 6 | 8 | 0 | 42.9% |
| genre_fit | 14 | 7 | 7 | 0 | 50.0% |
| structural_logic_defect | 14 | 8 | 6 | 0 | 57.1% |
| narrative_tone_match | 14 | 9 | 5 | 0 | 64.3% |
| late_stage_digression | 14 | 9 | 5 | 0 | 64.3% |
| narrative_density | 14 | 9 | 5 | 0 | 64.3% |
| puzzle_logic_validity | 14 | 10 | 4 | 0 | 71.4% |
| pacing_rationality_advanced | 14 | 12 | 2 | 0 | 85.7% |
| emotional_delivery_match | 14 | 12 | 2 | 0 | 85.7% |
| character_trait_consistency | 14 | 13 | 1 | 0 | 92.9% |
| character_design_adherence | 14 | 13 | 1 | 0 | 92.9% |
| chapter_cloning | 14 | 13 | 0 | 1 | 100.0% |
| alternating_repetition | 14 | 8 | 0 | 6 | 100.0% |
| chapter_completion | 14 | 14 | 0 | 0 | 100.0% |
| paragraph_repetition | 14 | 14 | 0 | 0 | 100.0% |
| theme_consistency | 14 | 14 | 0 | 0 | 100.0% |
| main_character_consistency | 14 | 14 | 0 | 0 | 100.0% |
| language_purity | 14 | 14 | 0 | 0 | 100.0% |
| plot_progression | 14 | 14 | 0 | 0 | 100.0% |
| full_narrative_content | 28 | 28 | 0 | 0 | 100.0% |
| hook_design | 14 | 14 | 0 | 0 | 100.0% |
| imagery_system | 14 | 14 | 0 | 0 | 100.0% |
| emotional_gradient | 14 | 14 | 0 | 0 | 100.0% |
| structural_design | 14 | 14 | 0 | 0 | 100.0% |
| chapter_output_existence | 14 | 14 | 0 | 0 | 100.0% |
| repeated_endings | 14 | 14 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 77.47 | 63.70 | 85.35 |
| IP | 1 | 82.53 | 82.53 | 82.53 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 77.71 | 71.55 | 84.40 |
| SHORT | 5 | 78.28 | 63.70 | 85.35 |
| MEDIUM | 4 | 77.72 | 73.60 | 82.53 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 79.10 | 71.55 | 85.35 |
| NEUTRAL | 1 | 82.53 | 82.53 | 82.53 |
| SUSPENSE | 1 | 73.60 | 73.60 | 73.60 |
| SWEET | 3 | 74.24 | 63.70 | 84.77 |

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

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项47`
  - 子类: puzzle_logic_validity, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项53`
  - 子类: semantic_redundancy, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

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

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项15`
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

### 记忆管理 (5个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

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
