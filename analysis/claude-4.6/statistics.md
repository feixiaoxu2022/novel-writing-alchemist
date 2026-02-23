# Novel Writing Alchemist 评测统计报告

- **模型**: `claude-opus-4-6`
- **生成时间**: 2026-02-23T17:13:57.730506
- **评测目录**: `evaluation_outputs/eval_dsv2_20260211_204123_claude-opus-4-6`
- **Revision**: `latest` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 14 |
| 执行错误 | 1 |
| 有checker结果 | 14 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 91.46 | 85.78 | 97.20 | 14 |
| 内容分(x0.7) | 90.08 | 84.50 | 96.00 | 14 |
| 过程分(x0.3) | 94.67 | 80.00 | 100.00 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| excellent | 3 | 21.4% |
| unqualified | 11 | 78.6% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 54 | 2 | 0 | 96.4% |
| 业务规则遵循 | 222 | 209 | 13 | 55 | 94.1% |
| 记忆管理 | 18 | 17 | 1 | 0 | 94.4% |

### 2.2 内容创作质量

- **平均内容分**: 90.08 (范围: 84.50 ~ 96.00)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 51 | 51 | 0 | 0 | 100.0% |
| Basic(基础) | 226 | 208 | 18 | 0 | 92.0% |
| Advanced(优秀) | 140 | 122 | 18 | 14 | 87.1% |

- **Gate触发率**: 0.0% (0/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 42 | 40 | 2 | 0 | 95.2% |
| naming_convention | 14 | 14 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 5 | 9 | 0 | 35.7% |
| sop_compliance | 29 | 18 | 1 | 10 | 94.7% |
| required_skill_reading | 122 | 74 | 3 | 45 | 96.1% |
| enum_validity | 28 | 28 | 0 | 0 | 100.0% |
| quantity_constraint | 28 | 28 | 0 | 0 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 8 | 1 | 5 | 88.9% |
| log_file_creation | 14 | 9 | 0 | 5 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 14 | 2 | 12 | 0 | 14.3% |
| dialogue_character_distinction | 14 | 8 | 6 | 0 | 57.1% |
| character_naming_quality | 14 | 8 | 6 | 0 | 57.1% |
| semantic_redundancy | 14 | 9 | 5 | 0 | 64.3% |
| narrative_tone_match | 14 | 10 | 4 | 0 | 71.4% |
| structural_logic_defect | 14 | 10 | 4 | 0 | 71.4% |
| late_stage_digression | 14 | 12 | 2 | 0 | 85.7% |
| emotional_delivery_match | 15 | 13 | 2 | 0 | 86.7% |
| outline_execution_fidelity | 14 | 13 | 1 | 0 | 92.9% |
| chapter_cloning | 14 | 14 | 0 | 0 | 100.0% |
| alternating_repetition | 14 | 9 | 0 | 5 | 100.0% |
| chapter_completion | 14 | 14 | 0 | 0 | 100.0% |
| paragraph_repetition | 14 | 14 | 0 | 0 | 100.0% |
| theme_consistency | 14 | 14 | 0 | 0 | 100.0% |
| main_character_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_trait_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_design_adherence | 15 | 15 | 0 | 0 | 100.0% |
| language_purity | 14 | 14 | 0 | 0 | 100.0% |
| plot_progression | 14 | 14 | 0 | 0 | 100.0% |
| full_narrative_content | 28 | 28 | 0 | 0 | 100.0% |
| narrative_density | 14 | 14 | 0 | 0 | 100.0% |
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
| CLEAR | 7 | 91.69 | 85.78 | 97.20 |
| IP | 1 | 93.87 | 93.87 | 93.87 |
| VAGUE | 1 | 87.89 | 87.89 | 87.89 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 91.37 | 87.48 | 94.58 |
| SHORT | 2 | 89.77 | 85.78 | 93.75 |
| MEDIUM | 7 | 92.00 | 87.89 | 97.20 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 97.20 | 97.20 | 97.20 |
| ANGSTY | 7 | 90.26 | 85.78 | 94.58 |
| BRAINY_ACTION | 1 | 89.79 | 89.79 | 89.79 |
| NEUTRAL | 1 | 93.87 | 93.87 | 93.87 |
| SUSPENSE | 1 | 92.23 | 92.23 | 92.23 |
| SWEET | 2 | 93.83 | 93.75 | 93.90 |
| SWEET_DRAMA | 1 | 87.89 | 87.89 | 87.89 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现4处fixable类型逻辑问题: 父亲论文时间线冲突：第1章称《南诏秘密军事据点"苍墟城"方位考证初探》发表/存档年份为“二十二年前”; 父辈失踪时长前后不一致：多处写“二十年”（如第1章贺铮“二十年了”、第21章遗骸处“二十年”），但第; 主角年龄与父亲失踪时间不闭合：第2章明说贺铮“我二十八

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项45`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项53`
  - 子类: semantic_redundancy, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现5处fixable类型逻辑问题: 陆沉从警年限与系统绑定时长出现前后不一致：chapter_01称“从警八年、三十一岁、系统绑定九十二; 系统显示“剩余时间/倒计时”的一致性冲突：chapter_02中系统记录了多起预告存在时间偏差（最大; AX-7浓度数据链存在不自洽：chapter_31外部

### 格式规范遵循 (2个失败检查)

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_ULTRA_SHORT_ANGSTY_004** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_SHORT_SWEET_001** / `检查项57`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 记忆管理 (1个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
