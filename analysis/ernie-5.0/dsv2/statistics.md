# Novel Writing Alchemist 评测统计报告

- **模型**: `ernie-5.0-thinking-preview`
- **生成时间**: 2026-02-23T12:03:47.309497
- **评测目录**: `eval_dsv2_20260211_103353_ernie-5.0-thinking-preview`
- **Revision**: `rev008` (实际: check_result_rev008.json)

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
| 加权总分 | 46.71 | 13.82 | 79.09 | 14 |
| 内容分(x0.7) | 46.06 | 0.00 | 88.47 | 14 |
| 过程分(x0.3) | 48.24 | 0.00 | 94.45 | 14 |

### 1.2 质量等级分布

| 等级 | 数量 | 占比 |
|------|------|------|
| qualified | 2 | 14.3% |
| unqualified | 10 | 71.4% |

## 2. 能力维度统计

### 2.1 过程维度

| 维度 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| 格式规范遵循 | 40 | 32 | 8 | 0 | 80.0% |
| 业务规则遵循 | 182 | 142 | 40 | 15 | 78.0% |
| 记忆管理 | 18 | 7 | 11 | 0 | 38.9% |

### 2.2 内容创作质量

- **平均内容分**: 46.06 (范围: 0.00 ~ 88.47)

#### 质量层级通过率

| 层级 | 总检查数 | 通过 | 失败 | 跳过 | 通过率 |
|------|----------|------|------|------|--------|
| Gate(门控) | 40 | 36 | 4 | 0 | 90.0% |
| Basic(基础) | 174 | 93 | 81 | 0 | 53.4% |
| Advanced(优秀) | 104 | 41 | 63 | 14 | 39.4% |

- **Gate触发率**: 14.3% (2/14)

## 3. 子类维度统计

### 格式规范遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| naming_convention | 10 | 5 | 5 | 0 | 50.0% |
| structural_integrity | 30 | 27 | 3 | 0 | 90.0% |

### 业务规则遵循

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| range_constraint | 10 | 0 | 10 | 0 | 0.0% |
| quantity_constraint | 20 | 12 | 6 | 2 | 66.7% |
| enum_validity | 20 | 13 | 5 | 2 | 72.2% |
| required_skill_reading | 86 | 61 | 16 | 9 | 79.2% |
| sop_compliance | 21 | 17 | 2 | 2 | 89.5% |
| output_completeness | 40 | 39 | 1 | 0 | 97.5% |

### 记忆管理

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| log_file_usage | 10 | 3 | 6 | 1 | 33.3% |
| log_file_creation | 10 | 4 | 5 | 1 | 44.4% |

### 内容创作质量

| 子类 | 总检查 | 通过 | 失败 | 跳过 | 通过率 |
|------|--------|------|------|------|--------|
| fixable_logic_inconsistency | 14 | 1 | 13 | 0 | 7.1% |
| character_naming_quality | 14 | 1 | 13 | 0 | 7.1% |
| outline_execution_fidelity | 10 | 1 | 9 | 0 | 10.0% |
| genre_fit | 10 | 1 | 9 | 0 | 10.0% |
| semantic_redundancy | 10 | 1 | 9 | 0 | 10.0% |
| dialogue_character_distinction | 10 | 2 | 8 | 0 | 20.0% |
| narrative_density | 10 | 2 | 8 | 0 | 20.0% |
| pacing_rationality_advanced | 10 | 2 | 8 | 0 | 20.0% |
| character_design_adherence | 11 | 3 | 8 | 0 | 27.3% |
| narrative_tone_match | 10 | 3 | 7 | 0 | 30.0% |
| puzzle_logic_validity | 10 | 4 | 6 | 0 | 40.0% |
| structural_logic_defect | 14 | 6 | 8 | 0 | 42.9% |
| main_character_consistency | 10 | 5 | 5 | 0 | 50.0% |
| late_stage_digression | 10 | 5 | 5 | 0 | 50.0% |
| structural_design | 10 | 5 | 5 | 0 | 50.0% |
| paragraph_repetition | 10 | 6 | 4 | 0 | 60.0% |
| language_purity | 10 | 6 | 4 | 0 | 60.0% |
| full_narrative_content | 24 | 15 | 9 | 0 | 62.5% |
| repeated_endings | 14 | 9 | 5 | 0 | 64.3% |
| character_trait_consistency | 10 | 7 | 3 | 0 | 70.0% |
| imagery_system | 10 | 7 | 3 | 0 | 70.0% |
| chapter_cloning | 10 | 7 | 2 | 1 | 77.8% |
| theme_consistency | 10 | 8 | 2 | 0 | 80.0% |
| hook_design | 10 | 8 | 2 | 0 | 80.0% |
| emotional_delivery_match | 11 | 9 | 2 | 0 | 81.8% |
| alternating_repetition | 10 | 6 | 1 | 3 | 85.7% |
| chapter_completion | 10 | 9 | 1 | 0 | 90.0% |
| plot_progression | 10 | 9 | 1 | 0 | 90.0% |
| emotional_gradient | 10 | 9 | 1 | 0 | 90.0% |
| chapter_output_existence | 14 | 14 | 0 | 0 | 100.0% |

## 4. 按写作参数统计

### 创作模式

| 创作模式 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| CLEAR | 7 | 52.39 | 20.68 | 78.60 |
| IP | 1 | 13.82 | 13.82 | 13.82 |
| VAGUE | 1 | 54.34 | 54.34 | 54.34 |

### 篇幅

| 篇幅 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ULTRA_SHORT | 5 | 43.82 | 28.00 | 79.09 |
| SHORT | 2 | 58.56 | 57.25 | 59.88 |
| MEDIUM | 7 | 45.40 | 13.82 | 78.60 |

### 基调/题材

| 基调/题材 | 样本数 | 平均总分 | 最低分 | 最高分 |
|------|--------|----------|--------|--------|
| ADVENTURE | 1 | 78.60 | 78.60 | 78.60 |
| ANGSTY | 7 | 47.53 | 28.00 | 79.09 |
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

- **NW_CLEAR_MEDIUM_SUSPENSE_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

- **NW_CLEAR_MEDIUM_SWEET_001** / `检查项14`
  - 子类: naming_convention, 层级: 
  - 原因: 部分文件命名不符合规范

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
