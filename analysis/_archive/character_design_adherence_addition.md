# 新增检查维度：人物设计遵循度（character_design_adherence）

生成时间: 2026-02-06

## 📋 概述

为内容质量维度（content_quality）的基础层（basic tier）新增了 `character_design_adherence`（人物设计遵循度）检查项，用于验证正式章节中角色的实际表现是否符合 `characters.json` 设计文档中定义的人物特点。

## 🎯 核心目标

**检查Plan阶段（设计）vs Execute阶段（执行）的一致性**

- **Plan阶段**: `characters.json` 中对角色的traits（性格特质）、motivation（动机）、background（背景）、relationships（关系）的设计
- **Execute阶段**: `chapters/*.md` 中角色在实际剧情中的表现（对话、行动、心理活动）

## 🔍 与现有检查项的区分

| 检查项 | 检查内容 | 对比基准 |
|--------|---------|---------|
| **检查项17 - 主要角色一致性** | 主角是否换人/消失 | 主角列表的存在性 |
| **检查项18 - 人物设定一致性** | 章节间性格/行为是否前后一致 | Execute内部（chapter_01 vs chapter_02） |
| **新增项 - 人物设计遵循度** | 实际表现是否符合设计文档 | Plan vs Execute（设计 vs 实际） |
| **检查项19 - 逻辑硬伤** | 客观事实/世界观是否矛盾 | 事实层面的前后一致性 |

**关键区分**：
- 检查项17关注"人还在不在"（最基础）
- 检查项18关注"执行阶段内部前后是否一致"
- 新增项关注"执行是否遵循设计"（Plan → Execute）
- 检查项19关注"客观事实是否矛盾"

## 📝 判断标准要点

### 不合格标准（matched: false）

1. **性格特质不符**：设计说"沉默寡言"，实际表现为话痨
2. **核心能力不符**：设计说"聪明绝顶"，实际表现为愚钝
3. **核心动机偏离**：设计说"复仇"，实际完全不提复仇
4. **背景设定未体现**：设计说"江湖经验丰富"，实际表现为江湖小白
5. **关系设定未遵循**：设计说"多年老友"，实际表现为初次相识

### 合格标准（matched: true）

- characters.json中定义的traits在chapters中得到体现
- motivation持续驱动角色行为
- background影响角色的判断和选择
- relationships在互动中得到呈现
- 允许合理发挥和细节补充，只要不违背核心设定

### 容错范围

- ✅ **合理发挥**：设计未明确的细节可以补充
- ✅ **合理深化**：在设计基础上的深化演绎
- ❌ **方向偏离**：实际表现与设计核心方向相反
- ❌ **核心缺失**：设计的核心特质完全未体现

## 🔄 判断流程

```
1. 读取characters.json
   ↓ 提取每个main_character的核心设定

2. 扫描所有chapters/*.md
   ↓ 提取角色的实际表现

3. 逐项对比
   ↓ traits是否体现？motivation是否驱动？
   ↓ background是否影响？relationships是否呈现？

4. 判定结果
   ↓ 核心设定（至少2-3项）得到体现 → matched=true
   ↓ 核心设定严重不符（方向相反或完全缺失） → matched=false
```

## 📂 修改的文件

### 1. `/tmp_scenarios/novel_writing_alchemist/check_capability_taxonomy.yaml`

在 `content_quality` 维度的 `subcategories` 中添加：

```yaml
- subcategory_id: "character_design_adherence"
  subcategory_name: "人物设计遵循度"
  tier_level: "basic"
  description: "正式章节中角色的实际表现必须符合characters.json中设计的人物特点（traits、motivation、background等）。这是检查plan阶段设计与execute阶段实际表现的一致性"
  check_types: ["semantic_check", "cross_file_consistency"]
  applicable_scenarios: ["original_creation", "adaptation"]
  note: "与character_trait_consistency区分：本项检查plan vs execute（设计文档 vs 实际表现），character_trait_consistency检查execute内部（chapter_01 vs chapter_02）"
```

### 2. `/design_v1/judge_criteria/content_quality_basic.yaml`

- 更新版本号为v1.2
- 在文件末尾添加完整的 `character_design_adherence` LLM判断标准
- 包含详细的范围约束、判断标准、验证要点、判断流程、示例分析

### 3. `/design_v1/unified_scenario_design.yaml`

在 `common_check_list` 中添加新的检查项（位于"人物设定一致性"和"逻辑硬伤"之间）：

```yaml
- check_id: 人物设计遵循度
  check_name: 实际表现符合设计文档
  dimension_id: content_quality
  subcategory_id: character_design_adherence
  quality_tier: basic
  check_type: semantic_check
  params:
    analysis_target: chapters/ + characters.json
    validation_rules:
    - rule_id: character_design_adherence
      description: 正式章节中角色的实际表现必须符合characters.json中设计的人物特点（traits、motivation、background等）
      validation_method: llm_semantic_analysis
      evaluation_criteria:
        scoring_rubric: 根据人物设计遵循度标准评估内容质量：1分=完全不符合，3分=基本符合，5分=完全符合
        pass_threshold: 3.0
        validation_prompt: 请评估角色实际表现是否符合characters.json中的设计文档
  weight: 1.0
  is_critical: true
```

**关键特性**：
- `analysis_target: chapters/ + characters.json` - 明确需要同时分析章节内容和设计文档
- `is_critical: true` - 作为basic层检查项，失败会导致整体不合格
- 位于检查项序列的合理位置（在character_trait_consistency之后，logical_contradiction之前）

### 4. `/analysis/character_design_adherence_addition.md`

- 创建了完整的说明文档，记录了设计思路和应用场景

## 💡 应用场景

### 典型问题检测

**问题1：设计与执行的人物特质反差**
- 设计：角色A是"理性克制、深思熟虑"
- 实际：角色A在各章节中表现为"冲动冒进、不计后果"
- 判定：不合格（matched=false）

**问题2：核心动机在执行中缺失**
- 设计：角色B的核心动机是"为父报仇"
- 实际：整部作品中角色B从未提及父亲，完全围绕事业发展展开
- 判定：不合格（matched=false）

**问题3：背景设定未影响行为**
- 设计：角色C是"退伍军人，战斗经验丰富"
- 实际：遇到危险时表现为慌乱无措，完全不像有战斗经验
- 判定：不合格（matched=false）

### 正确的案例

**案例：程远山与苏小满（NW_ULTRA_SHORT_ANGSTY_005）**
- 设计：程远山"沉默寡言、外冷内热、对苏小满有愧疚感"
- 实际：
  - 第1章：话很少，递烟时没多说话（体现"沉默寡言"）
  - 第2章：暴雨中默默买红丝巾（体现"外冷内热"）
  - 第4章：告白时说"欠你的"（体现"愧疚感"）
- 判定：合格（matched=true）

## 🎯 评估价值

1. **测试Agent的全局规划能力**：是否能在Plan阶段就明确人物特征，并在Execute阶段持续遵循
2. **测试长程记忆管理能力**：是否能在多章节写作中记住并遵循初始设计
3. **测试一致性维护能力**：是否能在自由创作中保持对设计文档的遵循
4. **区分不同层次的问题**：
   - 设计阶段理解不足（Plan问题）
   - 执行阶段遗忘设计（Execute问题）
   - 设计与执行缺乏桥接（Plan-Execute衔接问题）

## 📊 后续工作

1. **创建Checker实现**：编写检查脚本，调用LLM judge进行评估
2. **添加测试样本**：在现有样本中标注expected结果，验证判断标准
3. **统计分析**：评估不同模型在该维度上的表现差异
4. **归因分析**：失败案例是设计问题还是执行问题？是能力不足还是记忆丢失？

---

**版本**: v1.0
**创建时间**: 2026-02-06
**相关Issue**: 解决Ernie 5.0在人物设定一致性上的0%通过率问题，通过更细粒度的检查项区分不同类型的一致性问题
