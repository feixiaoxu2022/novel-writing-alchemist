# Novel Writing Alchemist 评测统计报告

- **模型**: `glm-5`
- **生成时间**: 2026-02-23T12:03:46.594746
- **评测目录**: `eval_dsv1_20260222_014523_glm-5`
- **Revision**: `rev008` (实际: check_result_rev008.json)

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
| 加权总分 | 66.79 | 50.54 | 79.24 | 14 |
| 内容分(x0.7) | 55.91 | 35.76 | 70.67 | 14 |
| 过程分(x0.3) | 92.19 | 79.40 | 100.00 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 14 | 100.0% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 56 | 56 | 0 | 0 | 100.0% |
| 业务规则遵循 | 201 | 184 | 17 | 91 | 91.5% |
| 记忆管理 | 18 | 14 | 4 | 0 | 77.8% |

### 2.2 内容创作质量

- **平均内容分**: 55.91 (范围: 35.76 ~ 70.67)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 54 | 54 | 0 | 0 | 100.0% |
| Basic(基础) | 251 | 174 | 77 | 1 | 69.3% |
| Advanced(优秀) | 140 | 50 | 90 | 14 | 35.7% |

- **Gate触发率**: 0.0% (0/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 14 | 14 | 0 | 0 | 100.0% |
| structural_integrity | 42 | 42 | 0 | 0 | 100.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 14 | 4 | 10 | 0 | 28.6% |
| required_skill_reading | 124 | 36 | 7 | 81 | 83.7% |
| enum_validity | 28 | 28 | 0 | 0 | 100.0% |
| quantity_constraint | 28 | 28 | 0 | 0 | 100.0% |
| sop_compliance | 28 | 18 | 0 | 10 | 100.0% |
| output_completeness | 56 | 56 | 0 | 0 | 100.0% |
| workspace_file_compliance | 14 | 14 | 0 | 0 | 100.0% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 14 | 5 | 4 | 5 | 55.6% |
| log_file_creation | 14 | 9 | 0 | 5 | 100.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 14 | 0 | 14 | 0 | 0.0% |
| dialogue_character_distinction | 14 | 0 | 14 | 0 | 0.0% |
| narrative_density | 14 | 0 | 14 | 0 | 0.0% |
| genre_fit | 14 | 1 | 13 | 0 | 7.1% |
| semantic_redundancy | 14 | 1 | 13 | 0 | 7.1% |
| character_naming_quality | 14 | 1 | 13 | 0 | 7.1% |
| pacing_rationality_advanced | 14 | 3 | 11 | 0 | 21.4% |
| structural_logic_defect | 14 | 6 | 8 | 0 | 42.9% |
| narrative_tone_match | 14 | 6 | 8 | 0 | 42.9% |
| late_stage_digression | 14 | 6 | 8 | 0 | 42.9% |
| character_presence_in_outline | 14 | 6 | 8 | 0 | 42.9% |
| outline_execution_fidelity | 14 | 7 | 7 | 0 | 50.0% |
| puzzle_logic_validity | 14 | 7 | 7 | 0 | 50.0% |
| hook_design | 14 | 7 | 7 | 0 | 50.0% |
| paragraph_repetition | 14 | 8 | 6 | 0 | 57.1% |
| character_presence_in_chapters | 14 | 8 | 6 | 0 | 57.1% |
| emotional_gradient | 14 | 8 | 6 | 0 | 57.1% |
| character_design_adherence | 14 | 10 | 4 | 0 | 71.4% |
| chapter_length_stability | 14 | 11 | 2 | 1 | 84.6% |
| full_narrative_content | 14 | 12 | 2 | 0 | 85.7% |
| imagery_system | 14 | 12 | 2 | 0 | 85.7% |
| structural_design | 14 | 12 | 2 | 0 | 85.7% |
| emotional_delivery_match | 14 | 12 | 2 | 0 | 85.7% |
| language_purity | 14 | 13 | 1 | 0 | 92.9% |
| plot_progression | 14 | 13 | 1 | 0 | 92.9% |
| repeated_endings | 14 | 13 | 1 | 0 | 92.9% |
| chapter_output_existence | 14 | 14 | 0 | 0 | 100.0% |
| chapter_cloning | 14 | 14 | 0 | 0 | 100.0% |
| alternating_repetition | 14 | 12 | 0 | 2 | 100.0% |
| chapter_completion | 14 | 14 | 0 | 0 | 100.0% |
| theme_consistency | 14 | 14 | 0 | 0 | 100.0% |
| main_character_consistency | 14 | 14 | 0 | 0 | 100.0% |
| character_trait_consistency | 14 | 14 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 62.52 | 50.54 | 78.29 |
| IP | 1 | 54.41 | 54.41 | 54.41 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 76.10 | 72.37 | 79.24 |
| SHORT | 5 | 64.44 | 50.54 | 78.29 |
| MEDIUM | 4 | 58.09 | 54.41 | 62.42 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ANGSTY | 9 | 71.93 | 55.55 | 79.24 |
| NEUTRAL | 1 | 54.41 | 54.41 | 54.41 |
| SUSPENSE | 1 | 55.46 | 55.46 | 55.46 |
| SWEET | 3 | 59.28 | 50.54 | 64.89 |

## 5. 失败案例索引

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `章节长度稳定性`
  - 子类: chapter_length_stability, 层级: basic
  - 原因: 章节长度严重萎缩(后期仅为前期47%)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `段落重复检测`
  - 子类: paragraph_repetition, 层级: basic
  - 原因: 同章内段落重复12处

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `结构性逻辑硬伤`
  - 子类: structural_logic_defect, 层级: basic
  - 原因: 发现1处structural类型逻辑问题: 同一“关押/突袭地点”在多章中出现互斥：第7章收到定位为“废弃化工厂（西城区郊区）”，第8/9章直接变为“废弃船厂”，第3章又铺垫为“城东旧港口废弃船厂”。若不解释化工厂与船厂的关系/二次转移/误导定位，将导致追踪线索与行动部署的因果链崩塌，且后续多章均依

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现3处fixable类型逻辑问题: 同一事件“林清将在今晚23:00杀害你”的倒计时数值前后冲突：第1章早晨提示约11小时58分/11小时15分；第5章深夜又出现【倒计时：11小时28分】并继续到【10小时15分】，与“同一晚23:00”不一致，等于把同一倒计时重置或跳时未解释。; 第2章明确“今

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `叙事调性匹配`
  - 子类: narrative_tone_match, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `读取感情线写作指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SWEET_001** / `中篇字数`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

- **NW_CLEAR_MEDIUM_SWEET_001** / `读取感情线写作指南`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 记忆管理 (4个失败检查)

- **NW_CLEAR_SHORT_ANGSTY_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_ANGSTY_002** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_SHORT_SWEET_002** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
