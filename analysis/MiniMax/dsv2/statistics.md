# Novel Writing Alchemist 评测统计报告

- **模型**: `MiniMax-M2.5`
- **生成时间**: 2026-02-25T15:27:11.112162
- **评测目录**: `evaluation_outputs/eval_dsv2_20260224_194949_MiniMax-M2.5`
- **Revision**: `latest` (实际: check_result_rev008.json)

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
| 加权总分 | 52.00 | 7.00 | 81.79 | 15 |
| 内容分(x0.7) | 49.47 | 0.00 | 87.56 | 15 |
| 过程分(x0.3) | 57.90 | 23.35 | 90.62 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 11 | 73.3% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 36 | 24 | 0 | 60.0% |
| 业务规则遵循 | 273 | 206 | 67 | 38 | 75.5% |
| 记忆管理 | 20 | 12 | 8 | 0 | 60.0% |

### 2.2 内容创作质量

- **平均内容分**: 49.47 (范围: 0.00 ~ 87.56)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 37 | 29 | 8 | 0 | 78.4% |
| Basic(基础) | 239 | 142 | 97 | 4 | 59.4% |
| Advanced(优秀) | 135 | 57 | 78 | 0 | 42.2% |

- **Gate触发率**: 26.7% (4/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| structural_integrity | 45 | 24 | 21 | 0 | 53.3% |
| naming_convention | 15 | 12 | 3 | 0 | 80.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 2 | 13 | 0 | 13.3% |
| sop_compliance | 31 | 13 | 8 | 10 | 61.9% |
| enum_validity | 30 | 11 | 5 | 14 | 68.8% |
| quantity_constraint | 30 | 12 | 4 | 14 | 75.0% |
| output_completeness | 60 | 45 | 15 | 0 | 75.0% |
| required_skill_reading | 130 | 108 | 22 | 0 | 83.1% |
| workspace_file_compliance | 15 | 15 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 5 | 5 | 5 | 50.0% |
| log_file_creation | 15 | 7 | 3 | 5 | 70.0% |

### 数据一致性

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_presence_in_chapters | 15 | 2 | 8 | 5 | 20.0% |
| character_presence_in_outline | 15 | 6 | 4 | 5 | 60.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| logical_contradiction | 15 | 1 | 14 | 0 | 6.7% |
| outline_execution_fidelity | 15 | 2 | 13 | 0 | 13.3% |
| dialogue_character_distinction | 15 | 3 | 12 | 0 | 20.0% |
| genre_fit | 15 | 3 | 12 | 0 | 20.0% |
| pacing_rationality_advanced | 15 | 3 | 12 | 0 | 20.0% |
| narrative_density | 15 | 4 | 11 | 0 | 26.7% |
| narrative_tone_match | 15 | 5 | 10 | 0 | 33.3% |
| semantic_redundancy | 15 | 5 | 10 | 0 | 33.3% |
| late_stage_digression | 15 | 6 | 9 | 0 | 40.0% |
| puzzle_logic_validity | 15 | 6 | 9 | 0 | 40.0% |
| structural_design | 15 | 8 | 7 | 0 | 53.3% |
| character_design_adherence | 17 | 10 | 7 | 0 | 58.8% |
| full_narrative_content | 15 | 9 | 6 | 0 | 60.0% |
| emotional_gradient | 15 | 9 | 6 | 0 | 60.0% |
| language_purity | 15 | 10 | 5 | 0 | 66.7% |
| hook_design | 15 | 10 | 5 | 0 | 66.7% |
| chapter_length_stability | 15 | 8 | 3 | 4 | 72.7% |
| chapter_completion | 15 | 11 | 4 | 0 | 73.3% |
| repeated_endings | 15 | 11 | 4 | 0 | 73.3% |
| imagery_system | 15 | 11 | 4 | 0 | 73.3% |
| emotional_delivery_match | 16 | 12 | 4 | 0 | 75.0% |
| alternating_repetition | 15 | 7 | 2 | 6 | 77.8% |
| paragraph_repetition | 15 | 12 | 3 | 0 | 80.0% |
| character_trait_consistency | 15 | 12 | 3 | 0 | 80.0% |
| chapter_cloning | 15 | 11 | 2 | 2 | 84.6% |
| theme_consistency | 15 | 13 | 2 | 0 | 86.7% |
| main_character_consistency | 15 | 13 | 2 | 0 | 86.7% |
| plot_progression | 15 | 13 | 2 | 0 | 86.7% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 52.44 | 20.71 | 67.84 |
| IP | 1 | 48.56 | 48.56 | 48.56 |
| VAGUE | 1 | 42.79 | 42.79 | 42.79 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 53.83 | 7.00 | 81.79 |
| SHORT | 2 | 51.94 | 51.46 | 52.42 |
| MEDIUM | 8 | 50.87 | 20.71 | 67.84 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 66.72 | 66.72 | 66.72 |
| ANGSTY | 7 | 55.41 | 7.00 | 81.79 |
| BRAINY_ACTION | 1 | 51.88 | 51.88 | 51.88 |
| HEROINE | 1 | 42.18 | 42.18 | 42.18 |
| NEUTRAL | 1 | 48.56 | 48.56 | 48.56 |
| SUSPENSE | 1 | 67.84 | 67.84 | 67.84 |
| SWEET | 2 | 36.09 | 20.71 | 51.46 |
| SWEET_DRAMA | 1 | 42.79 | 42.79 | 42.79 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_22`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_23`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_30`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_32`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_17`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `check_17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `check_15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_28`
  - 子类: logical_contradiction, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_38`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_47`
  - 子类: puzzle_logic_validity, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_48`
  - 子类: genre_fit, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 数据一致性 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `check_41`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 孙海）

- **NW_CLEAR_SHORT_ANGSTY_001** / `check_41`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 陈老师）

- **NW_CLEAR_SHORT_SWEET_001** / `check_40`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（配角: 零号, 副本BOSS-镜）

- **NW_CLEAR_SHORT_SWEET_001** / `check_41`
  - 子类: character_presence_in_chapters, 层级: 
  - 原因: 部分设计角色未在正文中出现（配角: 零号, 玩家老K, 副本BOSS-镜）

- **NW_IP_MEDIUM_NEUTRAL_001** / `check_40`
  - 子类: character_presence_in_outline, 层级: 
  - 原因: 部分设计角色未在大纲中规划（主角: 约翰·马斯顿（张麻子））

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_HEROINE_001** / `check_42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `check_43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `check_43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_001** / `check_42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_SHORT_ANGSTY_001** / `check_43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
