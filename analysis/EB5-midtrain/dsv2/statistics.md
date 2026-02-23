# Novel Writing Alchemist 评测统计报告

- **模型**: `openai_EB5-0209-A35B-midtrain-128k-chat`
- **生成时间**: 2026-02-23T12:03:47.613225
- **评测目录**: `eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 10 |
| 成功执行 | 9 |
| 执行错误 | 1 |
| 有checker结果 | 9 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 31.23 | 1.76 | 75.56 | 9 |
| 内容分(x0.7) | 22.87 | 0.00 | 70.35 | 9 |
| 过程分(x0.3) | 50.73 | 5.87 | 87.73 | 9 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 4 | 44.4% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 36 | 22 | 14 | 0 | 61.1% |
| 业务规则遵循 | 161 | 86 | 75 | 16 | 53.4% |
| 记忆管理 | 18 | 7 | 11 | 0 | 38.9% |

### 2.2 内容创作质量

- **平均内容分**: 22.87 (范围: 0.00 ~ 70.35)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 36 | 16 | 20 | 0 | 44.4% |
| Basic(基础) | 146 | 46 | 100 | 0 | 31.5% |
| Advanced(优秀) | 90 | 20 | 70 | 9 | 22.2% |

- **Gate触发率**: 55.6% (5/9)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 9 | 4 | 5 | 0 | 44.4% |
| structural_integrity | 27 | 18 | 9 | 0 | 66.7% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 9 | 0 | 9 | 0 | 0.0% |
| enum_validity | 18 | 4 | 6 | 8 | 40.0% |
| quantity_constraint | 18 | 4 | 6 | 8 | 40.0% |
| sop_compliance | 19 | 9 | 10 | 0 | 47.4% |
| required_skill_reading | 77 | 46 | 31 | 0 | 59.7% |
| output_completeness | 36 | 23 | 13 | 0 | 63.9% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 9 | 1 | 8 | 0 | 11.1% |
| log_file_creation | 9 | 6 | 3 | 0 | 66.7% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 9 | 0 | 9 | 0 | 0.0% |
| puzzle_logic_validity | 9 | 0 | 9 | 0 | 0.0% |
| semantic_redundancy | 9 | 0 | 9 | 0 | 0.0% |
| structural_logic_defect | 9 | 0 | 9 | 0 | 0.0% |
| narrative_density | 9 | 1 | 8 | 0 | 11.1% |
| genre_fit | 9 | 1 | 8 | 0 | 11.1% |
| emotional_delivery_match | 9 | 1 | 8 | 0 | 11.1% |
| character_naming_quality | 9 | 1 | 8 | 0 | 11.1% |
| paragraph_repetition | 9 | 2 | 7 | 0 | 22.2% |
| late_stage_digression | 9 | 2 | 7 | 0 | 22.2% |
| outline_execution_fidelity | 9 | 2 | 7 | 0 | 22.2% |
| pacing_rationality_advanced | 9 | 2 | 7 | 0 | 22.2% |
| hook_design | 9 | 2 | 7 | 0 | 22.2% |
| main_character_consistency | 9 | 3 | 6 | 0 | 33.3% |
| language_purity | 9 | 3 | 6 | 0 | 33.3% |
| full_narrative_content | 18 | 6 | 12 | 0 | 33.3% |
| imagery_system | 9 | 3 | 6 | 0 | 33.3% |
| emotional_gradient | 9 | 3 | 6 | 0 | 33.3% |
| structural_design | 9 | 3 | 6 | 0 | 33.3% |
| chapter_cloning | 9 | 4 | 5 | 0 | 44.4% |
| alternating_repetition | 9 | 4 | 5 | 0 | 44.4% |
| chapter_completion | 9 | 4 | 5 | 0 | 44.4% |
| theme_consistency | 9 | 4 | 5 | 0 | 44.4% |
| character_trait_consistency | 9 | 4 | 5 | 0 | 44.4% |
| plot_progression | 9 | 4 | 5 | 0 | 44.4% |
| narrative_tone_match | 9 | 4 | 5 | 0 | 44.4% |
| chapter_output_existence | 9 | 4 | 5 | 0 | 44.4% |
| repeated_endings | 9 | 4 | 5 | 0 | 44.4% |
| fixable_logic_inconsistency | 9 | 5 | 4 | 0 | 55.6% |
| character_design_adherence | 11 | 7 | 4 | 0 | 63.6% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 7 | 33.85 | 1.88 | 75.56 |
| IP | 1 | 42.37 | 42.37 | 42.37 |
| VAGUE | 1 | 1.76 | 1.76 | 1.76 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| SHORT | 2 | 56.83 | 53.70 | 59.95 |
| MEDIUM | 7 | 23.92 | 1.76 | 75.56 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 2 | 33.35 | 13.00 | 53.70 |
| BRAINY_ACTION | 1 | 16.00 | 16.00 | 16.00 |
| HEROINE | 1 | 16.84 | 16.84 | 16.84 |
| NEUTRAL | 1 | 42.37 | 42.37 | 42.37 |
| SUSPENSE | 1 | 75.56 | 75.56 | 75.56 |
| SWEET | 2 | 30.92 | 1.88 | 59.95 |
| SWEET_DRAMA | 1 | 1.76 | 1.76 | 1.76 |

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

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项12`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项13`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项18`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项19`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在
