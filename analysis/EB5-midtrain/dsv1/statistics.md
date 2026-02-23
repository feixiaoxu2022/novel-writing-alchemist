# Novel Writing Alchemist 评测统计报告

- **模型**: `openai_EB5-0209-A35B-midtrain-128k-chat`
- **生成时间**: 2026-02-23T12:03:47.465886
- **评测目录**: `eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat`
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
| 加权总分 | 47.20 | 0.00 | 76.17 | 14 |
| 内容分(x0.7) | 41.48 | 0.00 | 80.25 | 14 |
| 过程分(x0.3) | 60.55 | 0.00 | 81.27 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 8 | 57.1% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 45 | 11 | 0 | 80.4% |
| 业务规则遵循 | 206 | 124 | 82 | 72 | 60.2% |
| 记忆管理 | 28 | 12 | 16 | 0 | 42.9% |

### 2.2 内容创作质量

- **平均内容分**: 41.48 (范围: 0.00 ~ 80.25)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 54 | 42 | 12 | 0 | 77.8% |
| Basic(基础) | 224 | 137 | 87 | 0 | 61.2% |
| Advanced(优秀) | 140 | 38 | 102 | 14 | 27.1% |

- **Gate触发率**: 42.9% (6/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 14 | 11 | 3 | 0 | 78.6% |
| structural_integrity | 42 | 34 | 8 | 0 | 81.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 1 | 13 | 0 | 7.1% |
| required_skill_reading | 124 | 26 | 42 | 56 | 38.2% |
| sop_compliance | 28 | 15 | 13 | 0 | 53.6% |
| quantity_constraint | 28 | 16 | 4 | 8 | 80.0% |
| output_completeness | 56 | 48 | 8 | 0 | 85.7% |
| enum_validity | 28 | 18 | 2 | 8 | 90.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 0 | 14 | 0 | 0.0% |
| log_file_creation | 14 | 12 | 2 | 0 | 85.7% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| genre_fit | 14 | 0 | 14 | 0 | 0.0% |
| dialogue_character_distinction | 14 | 1 | 13 | 0 | 7.1% |
| semantic_redundancy | 14 | 1 | 13 | 0 | 7.1% |
| character_naming_quality | 14 | 1 | 13 | 0 | 7.1% |
| narrative_density | 14 | 2 | 12 | 0 | 14.3% |
| pacing_rationality_advanced | 14 | 2 | 12 | 0 | 14.3% |
| fixable_logic_inconsistency | 14 | 3 | 11 | 0 | 21.4% |
| hook_design | 14 | 4 | 10 | 0 | 28.6% |
| structural_logic_defect | 14 | 4 | 10 | 0 | 28.6% |
| puzzle_logic_validity | 14 | 5 | 9 | 0 | 35.7% |
| outline_execution_fidelity | 14 | 6 | 8 | 0 | 42.9% |
| emotional_gradient | 14 | 6 | 8 | 0 | 42.9% |
| paragraph_repetition | 14 | 7 | 7 | 0 | 50.0% |
| narrative_tone_match | 14 | 7 | 7 | 0 | 50.0% |
| late_stage_digression | 14 | 7 | 7 | 0 | 50.0% |
| structural_design | 14 | 7 | 7 | 0 | 50.0% |
| imagery_system | 14 | 8 | 6 | 0 | 57.1% |
| emotional_delivery_match | 14 | 8 | 6 | 0 | 57.1% |
| chapter_cloning | 14 | 9 | 4 | 1 | 69.2% |
| character_trait_consistency | 14 | 10 | 4 | 0 | 71.4% |
| character_design_adherence | 14 | 10 | 4 | 0 | 71.4% |
| plot_progression | 14 | 10 | 4 | 0 | 71.4% |
| full_narrative_content | 28 | 21 | 7 | 0 | 75.0% |
| alternating_repetition | 14 | 10 | 3 | 1 | 76.9% |
| chapter_completion | 14 | 11 | 3 | 0 | 78.6% |
| theme_consistency | 14 | 11 | 3 | 0 | 78.6% |
| main_character_consistency | 14 | 11 | 3 | 0 | 78.6% |
| language_purity | 14 | 12 | 2 | 0 | 85.7% |
| chapter_output_existence | 14 | 12 | 2 | 0 | 85.7% |
| repeated_endings | 14 | 12 | 2 | 0 | 85.7% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 40.45 | 0.00 | 73.87 |
| IP | 1 | 57.93 | 57.93 | 57.93 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 55.85 | 21.31 | 76.17 |
| SHORT | 5 | 50.97 | 30.58 | 73.87 |
| MEDIUM | 4 | 31.67 | 0.00 | 57.93 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 47.60 | 0.00 | 76.17 |
| NEUTRAL | 1 | 57.93 | 57.93 | 57.93 |
| SUSPENSE | 1 | 13.50 | 13.50 | 13.50 |
| SWEET | 3 | 53.67 | 41.49 | 64.28 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项2`
  - 子类: chapter_cloning, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项3`
  - 子类: alternating_repetition, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项4`
  - 子类: chapter_completion, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项6`
  - 子类: paragraph_repetition, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项24`
  - 子类: theme_consistency, 层级: basic
  - 原因: 未找到匹配文件

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项10`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项12`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项13`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项22`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

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
