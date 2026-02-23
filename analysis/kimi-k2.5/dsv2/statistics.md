# Novel Writing Alchemist 评测统计报告

- **模型**: `kimi-k2.5`
- **生成时间**: 2026-02-23T12:03:46.157055
- **评测目录**: `eval_dsv2_20260211_131949_kimi-k2.5`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 10 |
| 成功执行 | 10 |
| 执行错误 | 0 |
| 有checker结果 | 10 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 69.72 | 51.35 | 82.65 | 10 |
| 内容分(x0.7) | 64.52 | 45.50 | 84.50 | 10 |
| 过程分(x0.3) | 81.85 | 63.90 | 98.23 | 10 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 10 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 40 | 32 | 8 | 0 | 80.0% |
| 业务规则遵循 | 192 | 155 | 37 | 4 | 80.7% |
| 记忆管理 | 20 | 17 | 3 | 0 | 85.0% |

### 2.2 内容创作质量

- **平均内容分**: 64.52 (范围: 45.50 ~ 84.50)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 38 | 38 | 0 | 0 | 100.0% |
| Basic(基础) | 163 | 114 | 49 | 0 | 69.9% |
| Advanced(优秀) | 100 | 56 | 44 | 10 | 56.0% |

- **Gate触发率**: 0.0% (0/10)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 30 | 22 | 8 | 0 | 73.3% |
| naming_convention | 10 | 10 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 10 | 0 | 10 | 0 | 0.0% |
| required_skill_reading | 85 | 67 | 18 | 0 | 78.8% |
| sop_compliance | 21 | 17 | 4 | 0 | 81.0% |
| enum_validity | 20 | 16 | 2 | 2 | 88.9% |
| quantity_constraint | 20 | 16 | 2 | 2 | 88.9% |
| output_completeness | 40 | 39 | 1 | 0 | 97.5% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 10 | 7 | 3 | 0 | 70.0% |
| log_file_creation | 10 | 10 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 10 | 0 | 10 | 0 | 0.0% |
| fixable_logic_inconsistency | 10 | 0 | 10 | 0 | 0.0% |
| semantic_redundancy | 10 | 1 | 9 | 0 | 10.0% |
| character_naming_quality | 10 | 1 | 9 | 0 | 10.0% |
| language_purity | 10 | 3 | 7 | 0 | 30.0% |
| late_stage_digression | 10 | 3 | 7 | 0 | 30.0% |
| narrative_density | 10 | 3 | 7 | 0 | 30.0% |
| structural_logic_defect | 10 | 3 | 7 | 0 | 30.0% |
| outline_execution_fidelity | 10 | 4 | 6 | 0 | 40.0% |
| genre_fit | 10 | 4 | 6 | 0 | 40.0% |
| pacing_rationality_advanced | 10 | 5 | 5 | 0 | 50.0% |
| narrative_tone_match | 10 | 6 | 4 | 0 | 60.0% |
| puzzle_logic_validity | 10 | 7 | 3 | 0 | 70.0% |
| emotional_delivery_match | 11 | 8 | 3 | 0 | 72.7% |
| character_design_adherence | 12 | 9 | 3 | 0 | 75.0% |
| hook_design | 10 | 8 | 2 | 0 | 80.0% |
| character_trait_consistency | 10 | 9 | 1 | 0 | 90.0% |
| full_narrative_content | 20 | 18 | 2 | 0 | 90.0% |
| structural_design | 10 | 9 | 1 | 0 | 90.0% |
| chapter_cloning | 10 | 9 | 0 | 1 | 100.0% |
| alternating_repetition | 10 | 9 | 0 | 1 | 100.0% |
| chapter_completion | 10 | 10 | 0 | 0 | 100.0% |
| paragraph_repetition | 10 | 10 | 0 | 0 | 100.0% |
| theme_consistency | 10 | 10 | 0 | 0 | 100.0% |
| main_character_consistency | 10 | 10 | 0 | 0 | 100.0% |
| plot_progression | 10 | 10 | 0 | 0 | 100.0% |
| imagery_system | 10 | 10 | 0 | 0 | 100.0% |
| emotional_gradient | 10 | 10 | 0 | 0 | 100.0% |
| chapter_output_existence | 10 | 10 | 0 | 0 | 100.0% |
| repeated_endings | 10 | 10 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 68.32 | 51.35 | 82.65 |
| IP | 1 | 72.07 | 72.07 | 72.07 |
| VAGUE | 1 | 78.54 | 78.54 | 78.54 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| SHORT | 2 | 73.64 | 64.62 | 82.65 |
| MEDIUM | 8 | 68.74 | 51.35 | 82.35 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 70.64 | 70.64 | 70.64 |
| ANGSTY | 2 | 82.50 | 82.35 | 82.65 |
| BRAINY_ACTION | 1 | 57.15 | 57.15 | 57.15 |
| HEROINE | 1 | 76.16 | 76.16 | 76.16 |
| NEUTRAL | 1 | 72.07 | 72.07 | 72.07 |
| SUSPENSE | 1 | 61.66 | 61.66 | 61.66 |
| SWEET | 2 | 57.98 | 51.35 | 64.62 |
| SWEET_DRAMA | 1 | 78.54 | 78.54 | 78.54 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项29`
  - 子类: language_purity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项39`
  - 子类: late_stage_digression, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

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

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项16`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (3个失败检查)

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_IP_MEDIUM_NEUTRAL_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
