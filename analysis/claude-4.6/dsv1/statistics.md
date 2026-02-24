# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-6`
- **生成时间**: 2026-02-24T00:33:27.589006
- **评测目录**: `evaluation_outputs/eval_dsv1_20260214_014809_claude-opus-4-6`
- **Revision**: `latest` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 14 |
| 成功执行 | 13 |
| 执行错误 | 1 |
| 有checker结果 | 14 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 70.58 | 42.00 | 91.53 | 14 |
| 内容分(x0.7) | 78.83 | 60.00 | 96.25 | 14 |
| 过程分(x0.3) | 51.32 | 0.00 | 95.83 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 3 | 21.4% |
| unqualified | 6 | 42.9% |
| unknown | 5 | 35.7% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 36 | 32 | 4 | 0 | 88.9% |
| 业务规则遵循 | 142 | 127 | 15 | 36 | 89.4% |
| 记忆管理 | 18 | 11 | 7 | 0 | 61.1% |

### 2.2 内容创作质量

- **平均内容分**: 89.30 (范围: 81.41 ~ 96.25)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 34 | 34 | 0 | 0 | 100.0% |
| Basic(基础) | 144 | 132 | 12 | 0 | 91.7% |
| Advanced(优秀) | 90 | 77 | 13 | 9 | 85.6% |

- **Gate触发率**: 0.0% (0/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 14 | 13 | 1 | 0 | 92.9% |
| structural_integrity | 42 | 39 | 3 | 0 | 92.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 1 | 13 | 0 | 7.1% |
| sop_compliance | 28 | 18 | 10 | 0 | 64.3% |
| required_skill_reading | 124 | 61 | 7 | 56 | 89.7% |
| enum_validity | 28 | 28 | 0 | 0 | 100.0% |
| quantity_constraint | 28 | 28 | 0 | 0 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 2 | 12 | 0 | 14.3% |
| log_file_creation | 14 | 14 | 0 | 0 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 14 | 2 | 12 | 0 | 14.3% |
| dialogue_character_distinction | 14 | 7 | 7 | 0 | 50.0% |
| character_naming_quality | 14 | 9 | 5 | 0 | 64.3% |
| narrative_tone_match | 14 | 11 | 3 | 0 | 78.6% |
| structural_logic_defect | 14 | 11 | 3 | 0 | 78.6% |
| outline_execution_fidelity | 14 | 12 | 2 | 0 | 85.7% |
| semantic_redundancy | 14 | 12 | 2 | 0 | 85.7% |
| emotional_delivery_match | 14 | 12 | 2 | 0 | 85.7% |
| full_narrative_content | 28 | 26 | 2 | 0 | 92.9% |
| late_stage_digression | 14 | 13 | 1 | 0 | 92.9% |
| narrative_density | 14 | 13 | 1 | 0 | 92.9% |
| chapter_cloning | 14 | 13 | 0 | 1 | 100.0% |
| alternating_repetition | 14 | 7 | 0 | 7 | 100.0% |
| chapter_completion | 14 | 14 | 0 | 0 | 100.0% |
| paragraph_repetition | 14 | 14 | 0 | 0 | 100.0% |
| theme_consistency | 14 | 14 | 0 | 0 | 100.0% |
| main_character_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_trait_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_design_adherence | 14 | 14 | 0 | 0 | 100.0% |
| language_purity | 14 | 14 | 0 | 0 | 100.0% |
| plot_progression | 14 | 14 | 0 | 0 | 100.0% |
| puzzle_logic_validity | 14 | 14 | 0 | 0 | 100.0% |
| genre_fit | 14 | 14 | 0 | 0 | 100.0% |
| pacing_rationality_advanced | 14 | 14 | 0 | 0 | 100.0% |
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
| CLEAR | 8 | 85.82 | 76.32 | 91.12 |
| IP | 1 | 91.53 | 91.53 | 91.53 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 42.00 | 42.00 | 42.00 |
| SHORT | 5 | 87.33 | 82.90 | 91.12 |
| MEDIUM | 4 | 85.36 | 76.32 | 91.53 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 62.00 | 42.00 | 90.70 |
| NEUTRAL | 1 | 91.53 | 91.53 | 91.53 |
| SUSPENSE | 1 | 76.32 | 76.32 | 76.32 |
| SWEET | 3 | 87.41 | 82.90 | 91.12 |

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

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

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

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项43`
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
