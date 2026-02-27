# Novel Writing Alchemist 评测统计报告

- **模型**: `MiniMax-M2.5`
- **生成时间**: 2026-02-25T15:27:10.964288
- **评测目录**: `evaluation_outputs/eval_dsv1_20260224_194650_MiniMax-M2.5`
- **Revision**: `latest` (实际: check_result_rev008.json)

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
| 加权总分 | 44.82 | 0.83 | 76.25 | 14 |
| 内容分(x0.7) | 47.16 | 0.00 | 83.56 | 14 |
| 过程分(x0.3) | 39.38 | 2.77 | 71.65 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 10 | 71.4% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 21 | 35 | 0 | 37.5% |
| 业务规则遵循 | 206 | 118 | 88 | 86 | 57.3% |
| 记忆管理 | 18 | 4 | 14 | 0 | 22.2% |

### 2.2 内容创作质量

- **平均内容分**: 47.16 (范围: 0.00 ~ 83.56)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 26 | 16 | 10 | 0 | 61.5% |
| Basic(基础) | 217 | 118 | 99 | 7 | 54.4% |
| Advanced(优秀) | 126 | 51 | 75 | 0 | 40.5% |

- **Gate触发率**: 28.6% (4/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 42 | 10 | 32 | 0 | 23.8% |
| naming_convention | 14 | 11 | 3 | 0 | 78.6% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 3 | 11 | 0 | 21.4% |
| sop_compliance | 28 | 8 | 10 | 10 | 44.4% |
| required_skill_reading | 124 | 41 | 39 | 44 | 51.2% |
| output_completeness | 56 | 29 | 27 | 0 | 51.8% |
| enum_validity | 28 | 11 | 1 | 16 | 91.7% |
| quantity_constraint | 28 | 12 | 0 | 16 | 100.0% |
| workspace_file_compliance | 14 | 14 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 1 | 8 | 5 | 11.1% |
| log_file_creation | 14 | 3 | 6 | 5 | 33.3% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_outline | 14 | 0 | 2 | 12 | 0.0% |
| character_presence_in_chapters | 14 | 0 | 2 | 12 | 0.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 14 | 0 | 14 | 0 | 0.0% |
| logical_contradiction | 14 | 2 | 12 | 0 | 14.3% |
| genre_fit | 14 | 2 | 12 | 0 | 14.3% |
| character_design_adherence | 14 | 3 | 11 | 0 | 21.4% |
| outline_execution_fidelity | 14 | 3 | 11 | 0 | 21.4% |
| hook_design | 14 | 4 | 10 | 0 | 28.6% |
| semantic_redundancy | 14 | 5 | 9 | 0 | 35.7% |
| alternating_repetition | 14 | 2 | 3 | 9 | 40.0% |
| late_stage_digression | 14 | 6 | 8 | 0 | 42.9% |
| narrative_density | 14 | 6 | 8 | 0 | 42.9% |
| pacing_rationality_advanced | 14 | 6 | 8 | 0 | 42.9% |
| structural_design | 14 | 6 | 8 | 0 | 42.9% |
| narrative_tone_match | 14 | 7 | 7 | 0 | 50.0% |
| chapter_cloning | 14 | 4 | 3 | 7 | 57.1% |
| chapter_length_stability | 14 | 4 | 3 | 7 | 57.1% |
| emotional_gradient | 14 | 8 | 6 | 0 | 57.1% |
| character_trait_consistency | 14 | 9 | 5 | 0 | 64.3% |
| language_purity | 14 | 9 | 5 | 0 | 64.3% |
| repeated_endings | 14 | 9 | 5 | 0 | 64.3% |
| imagery_system | 14 | 9 | 5 | 0 | 64.3% |
| emotional_delivery_match | 14 | 9 | 5 | 0 | 64.3% |
| chapter_completion | 14 | 10 | 4 | 0 | 71.4% |
| paragraph_repetition | 14 | 10 | 4 | 0 | 71.4% |
| main_character_consistency | 14 | 10 | 4 | 0 | 71.4% |
| full_narrative_content | 14 | 10 | 4 | 0 | 71.4% |
| puzzle_logic_validity | 14 | 10 | 4 | 0 | 71.4% |
| theme_consistency | 14 | 11 | 3 | 0 | 78.6% |
| plot_progression | 14 | 11 | 3 | 0 | 78.6% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 39.25 | 1.25 | 70.37 |
| IP | 1 | 0.83 | 0.83 | 0.83 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 62.55 | 47.23 | 76.25 |
| SHORT | 5 | 50.86 | 41.45 | 70.37 |
| MEDIUM | 4 | 15.12 | 0.83 | 43.67 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 53.88 | 14.73 | 76.25 |
| NEUTRAL | 1 | 0.83 | 0.83 | 0.83 |
| SUSPENSE | 1 | 1.25 | 1.25 | 1.25 |
| SWEET | 3 | 46.86 | 43.67 | 52.63 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_01`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_07`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_08`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_09`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_55`
  - 子类: range_constraint, 层级: 
  - 原因: 未找到匹配文件

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_02`
  - 子类: chapter_cloning, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_03`
  - 子类: alternating_repetition, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_04`
  - 子类: chapter_completion, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_05`
  - 子类: chapter_length_stability, 层级: basic
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_06`
  - 子类: paragraph_repetition, 层级: basic
  - 原因: 未找到匹配文件

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录为空

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `check_14`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `check_15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `check_16`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `check_17`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 数据一致性 (4个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_40`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 林小满, 陈建国）

- **NW_CLEAR_SHORT_ANGSTY_002** / `check_40`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 系统AI（假象））

- **NW_CLEAR_SHORT_ANGSTY_002** / `check_41`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 系统AI（假象））

- **NW_ULTRA_SHORT_ANGSTY_004** / `check_41`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 岗哨士兵）

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `check_42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `check_43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `check_43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `check_42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在
