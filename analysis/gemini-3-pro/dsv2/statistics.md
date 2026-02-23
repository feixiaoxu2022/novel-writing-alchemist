# Novel Writing Alchemist 评测统计报告

- **模型**: `gemini-3-pro-preview`
- **生成时间**: 2026-02-23T12:03:45.088527
- **评测目录**: `eval_dsv2_20260215_002829_gemini-3-pro-preview`
- **Revision**: `rev008` (实际: check_result_rev008.json)

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
| 加权总分 | 85.21 | 72.52 | 98.34 | 15 |
| 内容分(x0.7) | 84.80 | 69.25 | 100.00 | 15 |
| 过程分(x0.3) | 86.17 | 65.00 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 4 | 26.7% |
| unqualified | 11 | 73.3% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 60 | 0 | 0 | 100.0% |
| 业务规则遵循 | 241 | 229 | 12 | 55 | 95.0% |
| 记忆管理 | 20 | 9 | 11 | 0 | 45.0% |

### 2.2 内容创作质量

- **平均内容分**: 84.80 (范围: 69.25 ~ 100.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 50 | 50 | 0 | 0 | 100.0% |
| Basic(基础) | 243 | 216 | 27 | 0 | 88.9% |
| Advanced(优秀) | 150 | 118 | 32 | 15 | 78.7% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |
| structural_integrity | 45 | 45 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 5 | 10 | 0 | 33.3% |
| sop_compliance | 31 | 20 | 1 | 10 | 95.2% |
| quantity_constraint | 30 | 29 | 1 | 0 | 96.7% |
| required_skill_reading | 130 | 85 | 0 | 45 | 100.0% |
| enum_validity | 30 | 30 | 0 | 0 | 100.0% |
| output_completeness | 60 | 60 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 0 | 10 | 5 | 0.0% |
| log_file_creation | 15 | 9 | 1 | 5 | 90.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 2 | 13 | 0 | 13.3% |
| character_naming_quality | 15 | 2 | 13 | 0 | 13.3% |
| outline_execution_fidelity | 15 | 8 | 7 | 0 | 53.3% |
| dialogue_character_distinction | 15 | 8 | 7 | 0 | 53.3% |
| genre_fit | 15 | 8 | 7 | 0 | 53.3% |
| structural_logic_defect | 15 | 8 | 7 | 0 | 53.3% |
| narrative_tone_match | 15 | 10 | 5 | 0 | 66.7% |
| puzzle_logic_validity | 15 | 12 | 3 | 0 | 80.0% |
| character_design_adherence | 17 | 14 | 3 | 0 | 82.3% |
| semantic_redundancy | 15 | 13 | 2 | 0 | 86.7% |
| character_trait_consistency | 15 | 14 | 1 | 0 | 93.3% |
| late_stage_digression | 15 | 14 | 1 | 0 | 93.3% |
| pacing_rationality_advanced | 15 | 14 | 1 | 0 | 93.3% |
| structural_design | 15 | 14 | 1 | 0 | 93.3% |
| emotional_delivery_match | 16 | 15 | 1 | 0 | 93.8% |
| chapter_cloning | 15 | 14 | 0 | 1 | 100.0% |
| alternating_repetition | 15 | 6 | 0 | 9 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| language_purity | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| full_narrative_content | 30 | 30 | 0 | 0 | 100.0% |
| narrative_density | 15 | 15 | 0 | 0 | 100.0% |
| hook_design | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |
| repeated_endings | 15 | 15 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 83.14 | 80.80 | 86.73 |
| IP | 1 | 83.27 | 83.27 | 83.27 |
| VAGUE | 1 | 72.52 | 72.52 | 72.52 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 91.44 | 86.35 | 98.34 |
| SHORT | 2 | 83.86 | 83.82 | 83.90 |
| MEDIUM | 8 | 81.65 | 72.52 | 86.73 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 80.80 | 80.80 | 80.80 |
| ANGSTY | 7 | 89.24 | 83.65 | 98.34 |
| BRAINY_ACTION | 1 | 86.73 | 86.73 | 86.73 |
| HEROINE | 1 | 81.46 | 81.46 | 81.46 |
| NEUTRAL | 1 | 83.27 | 83.27 | 83.27 |
| SUSPENSE | 1 | 83.93 | 83.93 | 83.93 |
| SWEET | 2 | 82.38 | 80.85 | 83.90 |
| SWEET_DRAMA | 1 | 72.52 | 72.52 | 72.52 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项47`
  - 子类: puzzle_logic_validity, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项48`
  - 子类: genre_fit, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项54`
  - 子类: structural_design, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现2处fixable类型逻辑问题: 第2章明确写“帐篷、发电机、精密仪器，全没了”，只剩“两个幸存的战术背包、三天口粮”。但第5章进入倒; 第2章交代向导阿木称“林教授死在鬼哭谷”。但第5章又在倒悬城内确认“林砚也认出了旁边的一具尸体，那是

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求
