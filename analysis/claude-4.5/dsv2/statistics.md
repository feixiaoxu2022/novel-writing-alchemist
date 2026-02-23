# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-5-20251101`
- **生成时间**: 2026-02-23T12:03:45.609397
- **评测目录**: `eval_dsv2_20260211_122519_claude-opus-4-5-20251101`
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
| 加权总分 | 84.16 | 69.50 | 95.53 | 15 |
| 内容分(x0.7) | 80.31 | 60.00 | 96.00 | 15 |
| 过程分(x0.3) | 93.14 | 80.00 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 1 | 6.7% |
| unqualified | 14 | 93.3% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 55 | 5 | 0 | 91.7% |
| 业务规则遵循 | 241 | 224 | 17 | 55 | 93.0% |
| 记忆管理 | 20 | 19 | 1 | 0 | 95.0% |

### 2.2 内容创作质量

- **平均内容分**: 80.31 (范围: 60.00 ~ 96.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 55 | 55 | 0 | 0 | 100.0% |
| Basic(基础) | 243 | 197 | 46 | 0 | 81.1% |
| Advanced(优秀) | 150 | 119 | 31 | 15 | 79.3% |

- **Gate触发率**: 0.0% (0/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 40 | 5 | 0 | 88.9% |
| naming_convention | 15 | 15 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 9 | 6 | 0 | 60.0% |
| sop_compliance | 31 | 17 | 4 | 10 | 81.0% |
| required_skill_reading | 130 | 78 | 7 | 45 | 91.8% |
| enum_validity | 30 | 30 | 0 | 0 | 100.0% |
| quantity_constraint | 30 | 30 | 0 | 0 | 100.0% |
| output_completeness | 60 | 60 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 9 | 1 | 5 | 90.0% |
| log_file_creation | 15 | 10 | 0 | 5 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 15 | 0 | 15 | 0 | 0.0% |
| semantic_redundancy | 15 | 4 | 11 | 0 | 26.7% |
| structural_logic_defect | 15 | 5 | 10 | 0 | 33.3% |
| dialogue_character_distinction | 15 | 6 | 9 | 0 | 40.0% |
| narrative_tone_match | 15 | 7 | 8 | 0 | 46.7% |
| outline_execution_fidelity | 15 | 7 | 8 | 0 | 46.7% |
| character_naming_quality | 15 | 7 | 8 | 0 | 46.7% |
| puzzle_logic_validity | 15 | 11 | 4 | 0 | 73.3% |
| character_design_adherence | 17 | 13 | 4 | 0 | 76.5% |
| late_stage_digression | 15 | 12 | 3 | 0 | 80.0% |
| genre_fit | 15 | 13 | 2 | 0 | 86.7% |
| narrative_density | 15 | 14 | 1 | 0 | 93.3% |
| repeated_endings | 15 | 14 | 1 | 0 | 93.3% |
| full_narrative_content | 30 | 29 | 1 | 0 | 96.7% |
| chapter_cloning | 15 | 15 | 0 | 0 | 100.0% |
| alternating_repetition | 15 | 10 | 0 | 5 | 100.0% |
| chapter_completion | 15 | 15 | 0 | 0 | 100.0% |
| paragraph_repetition | 15 | 15 | 0 | 0 | 100.0% |
| theme_consistency | 15 | 15 | 0 | 0 | 100.0% |
| main_character_consistency | 15 | 15 | 0 | 0 | 100.0% |
| character_trait_consistency | 15 | 15 | 0 | 0 | 100.0% |
| language_purity | 15 | 15 | 0 | 0 | 100.0% |
| plot_progression | 15 | 15 | 0 | 0 | 100.0% |
| pacing_rationality_advanced | 15 | 15 | 0 | 0 | 100.0% |
| hook_design | 15 | 15 | 0 | 0 | 100.0% |
| imagery_system | 15 | 15 | 0 | 0 | 100.0% |
| emotional_gradient | 15 | 15 | 0 | 0 | 100.0% |
| structural_design | 15 | 15 | 0 | 0 | 100.0% |
| emotional_delivery_match | 16 | 16 | 0 | 0 | 100.0% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 83.81 | 75.47 | 91.73 |
| IP | 1 | 69.50 | 69.50 | 69.50 |
| VAGUE | 1 | 80.15 | 80.15 | 80.15 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 88.45 | 79.26 | 95.53 |
| SHORT | 2 | 82.78 | 80.53 | 85.03 |
| MEDIUM | 8 | 81.82 | 69.50 | 91.73 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 91.73 | 91.73 | 91.73 |
| ANGSTY | 7 | 85.46 | 75.47 | 95.53 |
| BRAINY_ACTION | 1 | 86.24 | 86.24 | 86.24 |
| HEROINE | 1 | 85.41 | 85.41 | 85.41 |
| NEUTRAL | 1 | 69.50 | 69.50 | 69.50 |
| SUSPENSE | 1 | 82.34 | 82.34 | 82.34 |
| SWEET | 2 | 84.38 | 83.72 | 85.03 |
| SWEET_DRAMA | 1 | 80.15 | 80.15 | 80.15 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项9`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项9`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项23`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `检查项9`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现1处structural类型逻辑问题: 沈屿森年龄/时间线自相矛盾：多处称父亲失踪时他“六岁”（chapter_11、chapter_14）

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现3处fixable类型逻辑问题: 玉佩归属与性质前后不一致：chapter_08中阿依莫认定玉佩是“村寨圣物、失踪的第三件”；chap; 空间连续性断裂：chapter_11结尾写“阿依莫已离开、两人并肩走向龙口洞穴”；但chapter_; 父辈遗骨状态前后矛盾：chapter_14明确发现两具

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项27`
  - 子类: character_design_adherence, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_IP_MEDIUM_NEUTRAL_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_002** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 记忆管理 (1个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
