# Novel Writing Alchemist 评测统计报告

- **模型**: `glm-5`
- **生成时间**: 2026-02-23T12:16:41.486919
- **评测目录**: `evaluation_outputs/eval_dsv2_20260222_114444_glm-5`
- **Revision**: `rev008` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 11 |
| 执行错误 | 4 |
| 有checker结果 | 15 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 61.56 | 11.88 | 83.53 | 15 |
| 内容分(x0.7) | 50.62 | 0.00 | 76.47 | 15 |
| 过程分(x0.3) | 87.08 | 39.60 | 100.00 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| unqualified | 11 | 73.3% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 60 | 53 | 7 | 0 | 88.3% |
| 业务规则遵循 | 252 | 217 | 35 | 59 | 86.1% |
| 记忆管理 | 20 | 16 | 4 | 0 | 80.0% |

### 2.2 内容创作质量

- **平均内容分**: 50.62 (范围: 0.00 ~ 76.47)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 48 | 38 | 10 | 0 | 79.2% |
| Basic(基础) | 260 | 183 | 77 | 13 | 70.4% |
| Advanced(优秀) | 150 | 46 | 104 | 15 | 30.7% |

- **Gate触发率**: 26.7% (4/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 15 | 13 | 2 | 0 | 86.7% |
| structural_integrity | 45 | 40 | 5 | 0 | 88.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 15 | 6 | 9 | 0 | 40.0% |
| sop_compliance | 31 | 16 | 5 | 10 | 76.2% |
| quantity_constraint | 30 | 23 | 5 | 2 | 82.1% |
| workspace_file_compliance | 15 | 13 | 2 | 0 | 86.7% |
| enum_validity | 30 | 25 | 3 | 2 | 89.3% |
| required_skill_reading | 130 | 78 | 7 | 45 | 91.8% |
| output_completeness | 60 | 56 | 4 | 0 | 93.3% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 15 | 7 | 3 | 5 | 70.0% |
| log_file_creation | 15 | 9 | 1 | 5 | 90.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| dialogue_character_distinction | 15 | 0 | 15 | 0 | 0.0% |
| narrative_density | 15 | 0 | 15 | 0 | 0.0% |
| genre_fit | 15 | 1 | 14 | 0 | 6.7% |
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| fixable_logic_inconsistency | 15 | 2 | 13 | 0 | 13.3% |
| semantic_redundancy | 15 | 2 | 13 | 0 | 13.3% |
| pacing_rationality_advanced | 15 | 3 | 12 | 0 | 20.0% |
| puzzle_logic_validity | 15 | 5 | 10 | 0 | 33.3% |
| hook_design | 15 | 6 | 9 | 0 | 40.0% |
| structural_logic_defect | 15 | 7 | 8 | 0 | 46.7% |
| outline_execution_fidelity | 15 | 7 | 8 | 0 | 46.7% |
| structural_design | 15 | 8 | 7 | 0 | 53.3% |
| paragraph_repetition | 15 | 9 | 6 | 0 | 60.0% |
| narrative_tone_match | 15 | 9 | 6 | 0 | 60.0% |
| emotional_delivery_match | 16 | 10 | 6 | 0 | 62.5% |
| character_presence_in_chapters | 15 | 8 | 4 | 3 | 66.7% |
| imagery_system | 15 | 10 | 5 | 0 | 66.7% |
| alternating_repetition | 15 | 5 | 2 | 8 | 71.4% |
| chapter_length_stability | 15 | 5 | 2 | 8 | 71.4% |
| chapter_completion | 15 | 11 | 4 | 0 | 73.3% |
| emotional_gradient | 15 | 11 | 4 | 0 | 73.3% |
| character_presence_in_outline | 15 | 10 | 3 | 2 | 76.9% |
| main_character_consistency | 15 | 12 | 3 | 0 | 80.0% |
| full_narrative_content | 15 | 12 | 3 | 0 | 80.0% |
| late_stage_digression | 15 | 12 | 3 | 0 | 80.0% |
| chapter_cloning | 15 | 9 | 2 | 4 | 81.8% |
| chapter_output_existence | 15 | 13 | 2 | 0 | 86.7% |
| theme_consistency | 15 | 13 | 2 | 0 | 86.7% |
| character_trait_consistency | 15 | 13 | 2 | 0 | 86.7% |
| language_purity | 15 | 13 | 2 | 0 | 86.7% |
| plot_progression | 15 | 13 | 2 | 0 | 86.7% |
| repeated_endings | 15 | 13 | 2 | 0 | 86.7% |
| character_design_adherence | 17 | 15 | 2 | 0 | 88.2% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 50.39 | 11.88 | 72.45 |
| IP | 1 | 63.24 | 63.24 | 63.24 |
| VAGUE | 1 | 69.69 | 69.69 | 69.69 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 77.47 | 74.84 | 83.53 |
| SHORT | 2 | 71.52 | 70.59 | 72.45 |
| MEDIUM | 8 | 49.13 | 11.88 | 69.69 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 63.46 | 63.46 | 63.46 |
| ANGSTY | 7 | 73.98 | 58.04 | 83.53 |
| BRAINY_ACTION | 1 | 21.50 | 21.50 | 21.50 |
| HEROINE | 1 | 11.88 | 11.88 | 11.88 |
| NEUTRAL | 1 | 63.24 | 63.24 | 63.24 |
| SUSPENSE | 1 | 41.27 | 41.27 | 41.27 |
| SWEET | 2 | 67.27 | 63.94 | 70.59 |
| SWEET_DRAMA | 1 | 69.69 | 69.69 | 69.69 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `读取creative_intent的schema`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `X轴模式ID格式`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `Y轴标签枚举`
  - 子类: enum_validity, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `Y轴标签数量`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `forbidden_elements存在性`
  - 子类: quantity_constraint, 层级: 
  - 原因: 属性值不符合预期

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `章节命名格式`
  - 子类: naming_convention, 层级: 
  - 原因: 目录不存在

- **NW_CLEAR_MEDIUM_HEROINE_001** / `creative_intent格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_HEROINE_001** / `outline格式`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现3处fixable类型逻辑问题: chapter_04出现关键引导者“阿木”（例如“沈书：是……是阿木说的那拨人？”“阿木说龙脊脚下就是古城的入口”），但在已提供的chapter_01与chapter_02中并未出现或交代此人及其信息来源，导致信息链断裂：读者无法在当前文本集合内建立“阿木→龙脊

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色正文出场完整性`
  - 子类: character_presence_in_chapters, 层级: basic
  - 原因: 部分设计角色未在正文中出现（配角: 老黑, 张父, 沈父）

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `大纲执行忠实度`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色语言辨识度`
  - 子类: dialogue_character_distinction, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `叙事密度`
  - 子类: narrative_density, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

### 记忆管理 (4个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_HEROINE_001** / `writing_log文件创建`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `writing_log文件读取`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配
