# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-6`
- **生成时间**: 2026-02-23T12:03:44.581504
- **评测目录**: `eval_dsv1_20260214_014809_claude-opus-4-6`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 14 |
| 成功执行 | 13 |
| 执行错误 | 1 |
| 有checker结果 | 13 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 85.98 | 76.32 | 91.53 | 13 |
| 内容分(x0.7) | 90.76 | 81.41 | 100.00 | 13 |
| 过程分(x0.3) | 74.82 | 64.43 | 95.83 | 13 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 6 | 46.2% |
| unqualified | 7 | 53.8% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 52 | 48 | 4 | 0 | 92.3% |
| 业务规则遵循 | 206 | 153 | 53 | 52 | 74.3% |
| 记忆管理 | 26 | 15 | 11 | 0 | 57.7% |

### 2.2 内容创作质量

- **平均内容分**: 90.76 (范围: 81.41 ~ 100.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 44 | 44 | 0 | 0 | 100.0% |
| Basic(基础) | 208 | 195 | 13 | 0 | 93.8% |
| Advanced(优秀) | 130 | 112 | 18 | 13 | 86.2% |

- **Gate触发率**: 0.0% (0/13)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 13 | 12 | 1 | 0 | 92.3% |
| structural_integrity | 39 | 36 | 3 | 0 | 92.3% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 13 | 1 | 12 | 0 | 7.7% |
| required_skill_reading | 115 | 32 | 31 | 52 | 50.8% |
| sop_compliance | 26 | 16 | 10 | 0 | 61.5% |
| enum_validity | 26 | 26 | 0 | 0 | 100.0% |
| quantity_constraint | 26 | 26 | 0 | 0 | 100.0% |
| output_completeness | 52 | 52 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 13 | 2 | 11 | 0 | 15.4% |
| log_file_creation | 13 | 13 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 13 | 2 | 11 | 0 | 15.4% |
| dialogue_character_distinction | 13 | 7 | 6 | 0 | 53.8% |
| character_naming_quality | 13 | 9 | 4 | 0 | 69.2% |
| narrative_tone_match | 13 | 10 | 3 | 0 | 76.9% |
| semantic_redundancy | 13 | 11 | 2 | 0 | 84.6% |
| emotional_delivery_match | 13 | 11 | 2 | 0 | 84.6% |
| structural_logic_defect | 13 | 11 | 2 | 0 | 84.6% |
| full_narrative_content | 26 | 24 | 2 | 0 | 92.3% |
| late_stage_digression | 13 | 12 | 1 | 0 | 92.3% |
| outline_execution_fidelity | 13 | 12 | 1 | 0 | 92.3% |
| narrative_density | 13 | 12 | 1 | 0 | 92.3% |
| chapter_cloning | 13 | 12 | 0 | 1 | 100.0% |
| alternating_repetition | 13 | 6 | 0 | 7 | 100.0% |
| chapter_completion | 13 | 13 | 0 | 0 | 100.0% |
| paragraph_repetition | 13 | 13 | 0 | 0 | 100.0% |
| theme_consistency | 13 | 13 | 0 | 0 | 100.0% |
| main_character_consistency | 13 | 13 | 0 | 0 | 100.0% |
| character_trait_consistency | 13 | 13 | 0 | 0 | 100.0% |
| character_design_adherence | 13 | 13 | 0 | 0 | 100.0% |
| language_purity | 13 | 13 | 0 | 0 | 100.0% |
| plot_progression | 13 | 13 | 0 | 0 | 100.0% |
| puzzle_logic_validity | 13 | 13 | 0 | 0 | 100.0% |
| genre_fit | 13 | 13 | 0 | 0 | 100.0% |
| pacing_rationality_advanced | 13 | 13 | 0 | 0 | 100.0% |
| hook_design | 13 | 13 | 0 | 0 | 100.0% |
| imagery_system | 13 | 13 | 0 | 0 | 100.0% |
| emotional_gradient | 13 | 13 | 0 | 0 | 100.0% |
| structural_design | 13 | 13 | 0 | 0 | 100.0% |
| chapter_output_existence | 13 | 13 | 0 | 0 | 100.0% |
| repeated_endings | 13 | 13 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 7 | 86.24 | 76.32 | 91.12 |
| IP | 1 | 91.53 | 91.53 | 91.53 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 84.51 | 81.78 | 90.00 |
| SHORT | 5 | 87.33 | 82.90 | 91.12 |
| MEDIUM | 3 | 86.18 | 76.32 | 91.53 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 85.62 | 81.78 | 90.70 |
| NEUTRAL | 1 | 91.53 | 91.53 | 91.53 |
| SUSPENSE | 1 | 76.32 | 76.32 | 76.32 |
| SWEET | 2 | 89.66 | 88.20 | 91.12 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现1处structural类型逻辑问题: 周淮死亡方式前后矛盾：第34章明确为许盈用15ml 10%氯化钾推注致死；第35章再次详细描写同一氯

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现5处fixable类型逻辑问题: 死亡时间自相矛盾：第34章方竹清邮件称22:45到达且“十五分钟内必须完成”，并在第36章出现“22; 时间显示错误：文中对话为“21:52”，随后叙述“仪表盘…22:52的倒计时——不，这不是倒计时。这; 致死概率数字前后不一致：第8章计算咪达唑仑方案“致死概

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项35`
  - 子类: full_narrative_content, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项39`
  - 子类: late_stage_digression, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

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

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

### 格式规范遵循 (4个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_ANGSTY_003** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_SHORT_SWEET_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_002** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_003** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_002** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
