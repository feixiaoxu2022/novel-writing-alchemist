# Novel Writing Alchemist 评测统计报告

- **模型**: `openai_EB5-0209-A35B-midtrain-128k-chat`
- **生成时间**: 2026-02-23T17:14:16.772325
- **评测目录**: `evaluation_outputs/eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat`
- **Revision**: `latest` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 10 |
| 成功执行 | 9 |
| 执行错误 | 1 |
| 有checker结果 | 10 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 30.32 | 1.76 | 75.56 | 10 |
| 内容分(x0.7) | 21.06 | 0.00 | 70.35 | 10 |
| 过程分(x0.3) | 51.93 | 5.87 | 87.73 | 10 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 4 | 40.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 40 | 25 | 15 | 0 | 62.5% |
| 业务规则遵循 | 180 | 98 | 82 | 16 | 54.4% |
| 记忆管理 | 20 | 8 | 12 | 0 | 40.0% |

### 2.2 内容创作质量

- **平均内容分**: 21.06 (范围: 0.00 ~ 70.35)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 40 | 19 | 21 | 0 | 47.5% |
| Basic(基础) | 163 | 53 | 110 | 0 | 32.5% |
| Advanced(优秀) | 100 | 20 | 80 | 10 | 20.0% |

- **Gate触发率**: 60.0% (6/10)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 10 | 5 | 5 | 0 | 50.0% |
| structural_integrity | 30 | 20 | 10 | 0 | 66.7% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 10 | 0 | 10 | 0 | 0.0% |
| enum_validity | 20 | 4 | 8 | 8 | 33.3% |
| quantity_constraint | 20 | 4 | 8 | 8 | 33.3% |
| sop_compliance | 21 | 10 | 11 | 0 | 47.6% |
| required_skill_reading | 85 | 53 | 32 | 0 | 62.4% |
| output_completeness | 40 | 27 | 13 | 0 | 67.5% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 10 | 1 | 9 | 0 | 10.0% |
| log_file_creation | 10 | 7 | 3 | 0 | 70.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 10 | 0 | 10 | 0 | 0.0% |
| puzzle_logic_validity | 10 | 0 | 10 | 0 | 0.0% |
| semantic_redundancy | 10 | 0 | 10 | 0 | 0.0% |
| structural_logic_defect | 10 | 0 | 10 | 0 | 0.0% |
| narrative_density | 10 | 1 | 9 | 0 | 10.0% |
| genre_fit | 10 | 1 | 9 | 0 | 10.0% |
| character_naming_quality | 10 | 1 | 9 | 0 | 10.0% |
| paragraph_repetition | 10 | 2 | 8 | 0 | 20.0% |
| late_stage_digression | 10 | 2 | 8 | 0 | 20.0% |
| outline_execution_fidelity | 10 | 2 | 8 | 0 | 20.0% |
| pacing_rationality_advanced | 10 | 2 | 8 | 0 | 20.0% |
| hook_design | 10 | 2 | 8 | 0 | 20.0% |
| emotional_delivery_match | 11 | 3 | 8 | 0 | 27.3% |
| full_narrative_content | 20 | 6 | 14 | 0 | 30.0% |
| imagery_system | 10 | 3 | 7 | 0 | 30.0% |
| emotional_gradient | 10 | 3 | 7 | 0 | 30.0% |
| structural_design | 10 | 3 | 7 | 0 | 30.0% |
| chapter_cloning | 10 | 4 | 6 | 0 | 40.0% |
| main_character_consistency | 10 | 4 | 6 | 0 | 40.0% |
| language_purity | 10 | 4 | 6 | 0 | 40.0% |
| plot_progression | 10 | 4 | 6 | 0 | 40.0% |
| narrative_tone_match | 10 | 4 | 6 | 0 | 40.0% |
| repeated_endings | 10 | 4 | 6 | 0 | 40.0% |
| alternating_repetition | 10 | 5 | 5 | 0 | 50.0% |
| chapter_completion | 10 | 5 | 5 | 0 | 50.0% |
| theme_consistency | 10 | 5 | 5 | 0 | 50.0% |
| character_trait_consistency | 10 | 5 | 5 | 0 | 50.0% |
| fixable_logic_inconsistency | 10 | 5 | 5 | 0 | 50.0% |
| chapter_output_existence | 10 | 5 | 5 | 0 | 50.0% |
| character_design_adherence | 12 | 8 | 4 | 0 | 66.7% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 32.38 | 1.88 | 75.56 |
| IP | 1 | 42.37 | 42.37 | 42.37 |
| VAGUE | 1 | 1.76 | 1.76 | 1.76 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| SHORT | 2 | 56.83 | 53.70 | 59.95 |
| MEDIUM | 8 | 23.69 | 1.76 | 75.56 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 22.12 | 22.12 | 22.12 |
| ANGSTY | 2 | 33.35 | 13.00 | 53.70 |
| BRAINY_ACTION | 1 | 16.00 | 16.00 | 16.00 |
| HEROINE | 1 | 16.84 | 16.84 | 16.84 |
| NEUTRAL | 1 | 42.37 | 42.37 | 42.37 |
| SUSPENSE | 1 | 75.56 | 75.56 | 75.56 |
| SWEET | 2 | 30.92 | 1.88 | 59.95 |
| SWEET_DRAMA | 1 | 1.76 | 1.76 | 1.76 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项2`
  - 子类: chapter_cloning, 层级: basic
  - 原因: 检测到3章近似克隆

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项6`
  - 子类: paragraph_repetition, 层级: basic
  - 原因: 同章内段落重复21处

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项34`
  - 子类: plot_progression, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项35`
  - 子类: full_narrative_content, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项18`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项19`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项20`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项21`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

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

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

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
