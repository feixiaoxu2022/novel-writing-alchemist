# Novel Writing Alchemist 评测统计报告

- **模型**: `ernie-5.0-thinking-preview`
- **生成时间**: 2026-02-23T17:14:02.727153
- **评测目录**: `evaluation_outputs/eval_dsv2_20260211_103353_ernie-5.0-thinking-preview`
- **Revision**: `latest` (实际: check_result_rev008.json)

## 1. 总览

| 指标 | 值 |
|------|-----|
| 总样本数 | 15 |
| 成功执行 | 14 |
| 执行错误 | 1 |
| 有checker结果 | 15 |

### 1.1 总分统计

| 分数类型 | 平均分 | 最低分 | 最高分 | 样本数 |
|----------|--------|--------|--------|--------|
| 加权总分 | 47.30 | 13.82 | 79.09 | 15 |
| 内容分(x0.7) | 46.21 | 0.00 | 88.47 | 15 |
| 过程分(x0.3) | 49.84 | 0.00 | 94.45 | 15 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| qualified | 2 | 13.3% |
| unqualified | 11 | 73.3% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 44 | 34 | 10 | 0 | 77.3% |
| 业务规则遵循 | 197 | 152 | 45 | 19 | 77.2% |
| 记忆管理 | 20 | 9 | 11 | 0 | 45.0% |

### 2.2 内容创作质量

- **平均内容分**: 46.21 (范围: 0.00 ~ 88.47)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 44 | 40 | 4 | 0 | 90.9% |
| Basic(基础) | 191 | 101 | 90 | 0 | 52.9% |
| Advanced(优秀) | 114 | 46 | 68 | 15 | 40.4% |

- **Gate触发率**: 13.3% (2/15)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 11 | 5 | 6 | 0 | 45.5% |
| structural_integrity | 33 | 29 | 4 | 0 | 87.9% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 11 | 0 | 11 | 0 | 0.0% |
| quantity_constraint | 22 | 12 | 6 | 4 | 66.7% |
| enum_validity | 22 | 13 | 5 | 4 | 72.2% |
| required_skill_reading | 94 | 66 | 19 | 9 | 77.6% |
| sop_compliance | 23 | 19 | 2 | 2 | 90.5% |
| output_completeness | 44 | 42 | 2 | 0 | 95.5% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 11 | 4 | 6 | 1 | 40.0% |
| log_file_creation | 11 | 5 | 5 | 1 | 50.0% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| character_naming_quality | 15 | 1 | 14 | 0 | 6.7% |
| outline_execution_fidelity | 11 | 1 | 10 | 0 | 9.1% |
| genre_fit | 11 | 1 | 10 | 0 | 9.1% |
| semantic_redundancy | 11 | 1 | 10 | 0 | 9.1% |
| fixable_logic_inconsistency | 15 | 2 | 13 | 0 | 13.3% |
| dialogue_character_distinction | 11 | 2 | 9 | 0 | 18.2% |
| pacing_rationality_advanced | 11 | 2 | 9 | 0 | 18.2% |
| narrative_tone_match | 11 | 3 | 8 | 0 | 27.3% |
| narrative_density | 11 | 3 | 8 | 0 | 27.3% |
| character_design_adherence | 13 | 4 | 9 | 0 | 30.8% |
| puzzle_logic_validity | 11 | 4 | 7 | 0 | 36.4% |
| structural_logic_defect | 15 | 6 | 9 | 0 | 40.0% |
| late_stage_digression | 11 | 5 | 6 | 0 | 45.5% |
| main_character_consistency | 11 | 6 | 5 | 0 | 54.5% |
| language_purity | 11 | 6 | 5 | 0 | 54.5% |
| structural_design | 11 | 6 | 5 | 0 | 54.5% |
| paragraph_repetition | 11 | 7 | 4 | 0 | 63.6% |
| character_trait_consistency | 11 | 7 | 4 | 0 | 63.6% |
| imagery_system | 11 | 7 | 4 | 0 | 63.6% |
| full_narrative_content | 26 | 17 | 9 | 0 | 65.4% |
| repeated_endings | 15 | 10 | 5 | 0 | 66.7% |
| emotional_delivery_match | 12 | 9 | 3 | 0 | 75.0% |
| chapter_cloning | 11 | 8 | 2 | 1 | 80.0% |
| theme_consistency | 11 | 9 | 2 | 0 | 81.8% |
| hook_design | 11 | 9 | 2 | 0 | 81.8% |
| alternating_repetition | 11 | 7 | 1 | 3 | 87.5% |
| chapter_completion | 11 | 10 | 1 | 0 | 90.9% |
| plot_progression | 11 | 10 | 1 | 0 | 90.9% |
| emotional_gradient | 11 | 10 | 1 | 0 | 90.9% |
| chapter_output_existence | 15 | 15 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 8 | 52.77 | 20.68 | 78.60 |
| IP | 1 | 13.82 | 13.82 | 13.82 |
| VAGUE | 1 | 54.34 | 54.34 | 54.34 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 43.82 | 28.00 | 79.09 |
| SHORT | 2 | 58.56 | 57.25 | 59.88 |
| MEDIUM | 8 | 46.65 | 13.82 | 78.60 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 78.60 | 78.60 | 78.60 |
| ANGSTY | 7 | 47.53 | 28.00 | 79.09 |
| BRAINY_ACTION | 1 | 55.44 | 55.44 | 55.44 |
| HEROINE | 1 | 47.08 | 47.08 | 47.08 |
| NEUTRAL | 1 | 13.82 | 13.82 | 13.82 |
| SUSPENSE | 1 | 46.89 | 46.89 | 46.89 |
| SWEET | 2 | 40.28 | 20.68 | 59.88 |
| SWEET_DRAMA | 1 | 54.34 | 54.34 | 54.34 |

## 5. 失败案例索引

### 业务规则遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项9`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项11`
  - 子类: required_skill_reading, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项23`
  - 子类: sop_compliance, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项30`
  - 子类: output_completeness, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项55`
  - 子类: range_constraint, 层级: 
  - 原因: 字数不符合要求

### 格式规范遵循 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项17`
  - 子类: structural_integrity, 层级: 
  - 原因: 部分文件结构不完整

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_CLEAR_MEDIUM_BRAINY_ACTION_001** / `检查项15`
  - 子类: structural_integrity, 层级: 
  - 原因: 未找到匹配文件

### 记忆管理 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项42`
  - 子类: log_file_creation, 层级: 
  - 原因: 文件不存在

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项43`
  - 子类: log_file_usage, 层级: 
  - 原因: 工具未被调用或参数不匹配

### 内容创作质量 (5个失败检查)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项44`
  - 子类: outline_execution_fidelity, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `检查项54`
  - 子类: structural_design, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `可修复逻辑瑕疵`
  - 子类: fixable_logic_inconsistency, 层级: advanced
  - 原因: 发现2处fixable类型逻辑问题: 出现“手指无意识地推了推眼镜——虽然他没戴眼镜”。同一时间同一人物在叙述层面被同时设定为“戴/没戴眼; 前文写“阿旺的马受惊，前蹄踏空，连人带马摔向深渊”，随后又写“林墨和阿旺（他幸运地抓住了崖壁的藤蔓爬

- **NW_CLEAR_MEDIUM_ADVENTURE_001** / `角色命名质量`
  - 子类: character_naming_quality, 层级: advanced
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)

- **NW_CLEAR_MEDIUM_ANGSTY_001** / `检查项25`
  - 子类: main_character_consistency, 层级: basic
  - 原因: 内容不符合标准 (LLM语义判断-解耦模式)
