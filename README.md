# 小说创作Agent自动评测场景

## 1. 场景概述

### 1.1 评测目标

评估大模型在**复杂创意任务**中的Agent能力，核心考察：

| 能力维度 | 具体考察点 |
|---------|-----------|
| **Prompt遵循** | 能否严格按照System Prompt中的SOP和格式规范执行 |
| **Tool Use** | 能否正确调用工具（读取skill文档、HITL交互、文件读写） |
| **任务规划** | 能否将复杂创作任务分解为阶段性子任务 |
| **内容质量** | 生成的小说是否符合要求（主题一致、人物一致、情节推进、无逻辑硬伤） |
| **长程记忆** | 多章节创作中能否通过writing_log保持前后一致性 |

### 1.2 任务设定

Agent扮演"网文高手"，基于X-Y轴配方系统，完成从用户灵感到完整小说的创作流程：

```
用户灵感 → 配方选择 → 人物设计 → 大纲规划 → 章节写作 → 交付
```

**交付物**：
- `creative_intent.json` - 创作意图（配方、情感基调、禁忌元素）
- `characters.json` - 人物设计（主角、配角、traits、动机）
- `outline.json` - 三层大纲（story→chapter→scene）
- `chapters/*.md` - 正文章节
- `writing_log.md` - 创作日志（长篇续写用）

---

## 2. 版本演进：v1 → v2

### 2.1 为什么要升级

| 问题 | v1现状 | v2解决方案 |
|------|--------|-----------|
| **长篇成本过高** | 超长篇（50万字）需要几十轮对话，单样本评测耗时数小时，token成本不可接受 | 砍掉长篇和超长篇，聚焦短篇（1.5-4万字）和中篇（8-25万字） |
| **超短篇差异大** | 超短篇（6500-10000字）的query设计和评价体系与数万字篇幅有本质不同，混在一起难以统一评估 | 砍掉超短篇，单独设计超短篇评测场景 |
| **SOP不够清晰** | v1的System Prompt对创作流程描述较粗，Agent容易跳步或遗漏环节 | 重构System Prompt，明确4阶段SOP和每阶段的HITL交互要求 |
| **Skill支撑不足** | v1只有基础的配方知识库和写作指南 | 新增6份专业Skill文档：命名指南、大纲设计、一致性管理、感情线写作等 |
| **用户模拟器辅助不足** | v1的用户模拟器只模拟用户行为，不提供任何引导 | v2在用户模拟器prompt中加入提醒Agent查看skill的话术，辅助Agent及时读取相关指导文档 |

### 2.2 核心升级内容

#### 2.2.1 System Prompt重构

v2的System Prompt明确定义了4阶段SOP，每个阶段有明确的：
- **前置条件**：进入该阶段前必须完成什么
- **必读Skill**：该阶段需要读取哪些指导文档
- **HITL交互**：在什么时机、以什么方式与用户确认
- **交付物**：该阶段结束时必须产出什么

#### 2.2.2 Skill文档体系

| Skill文档 | 作用 | v1 | v2 |
|-----------|------|----|----|
| `RECIPE_KNOWLEDGE.md` | X轴36种剧情模式 + Y轴12种标签 | ✓ | ✓ |
| `CHARACTER_DESIGN_GUIDE.md` | 人物traits、动机、秘密恐惧设计 | ✓ | ✓ |
| `WRITING_TECHNIQUE_GUIDE.md` | 场景、对话、叙事等9大写作技法 | ✓ | ✓ |
| `CHARACTER_NAMING_GUIDE.md` | 角色命名方法（类型基调、文化合规） | - | ✓ |
| `OUTLINE_DESIGN_GUIDE.md` | 三层大纲结构设计方法 | - | ✓ |
| `CONSISTENCY_MANAGEMENT_GUIDE.md` | 设定登记簿、一致性检查清单 | - | ✓ |
| `ROMANCE_WRITING_GUIDE.md` | 感情线写作：含蓄胜于直白 | - | ✓ |
| `SHORT_STORY_GUIDE.md` | 短篇专用技巧 | ✓ | ✓ |

#### 2.2.3 用户模拟器升级

v2用户模拟器的核心改进是**在prompt中加入提醒Agent查看skill的话术**：

```yaml
# v2用户模拟器示例
user_simulator_prompt: |
  ...
  在配方选择阶段，如果Agent没有主动提到参考配方知识库，你可以说：
  "你可以看看你的配方知识库，里面有很多剧情模式可以参考"
  
  在人物设计阶段，如果Agent的人物设计比较单薄，你可以提醒：
  "你有没有专门的人物设计指南？可以参考一下让人物更立体"
  ...
```

**设计意图**：通过用户模拟器的引导话术，测试Agent是否能响应用户提示、主动查阅相关skill文档。这比单纯依赖System Prompt中的要求更贴近真实场景——真实用户也会给出类似的提示。

### 2.3 版本对比总结

| 维度 | v1 | v2 |
|------|----|----|
| **篇幅范围** | 超短篇(6.5k-1万) ~ 超长篇(50万) | 短篇(1.5-4万) ~ 中篇(8-25万) |
| **样本数** | 14个 | 10个 |
| **System Prompt** | 基础版SOP | 重构版4阶段SOP |
| **Skill文档** | 3份 | 8份 |
| **用户模拟器** | 仅模拟用户行为 | 加入提醒Agent查看skill的话术 |
| **评测成本** | 高（长篇耗时数小时） | 可控（中篇约30分钟） |

---

## 3. 检查能力体系

### 3.1 四大能力维度

| 维度 | 说明 | 检查方式 |
|------|------|----------|
| **format_compliance** | 输出文件格式规范（JSON Schema、命名规则） | 规则校验 |
| **business_rule_compliance** | 业务规则遵循（SOP流程、枚举约束、字数范围、Skill阅读） | 规则校验 |
| **content_quality** | 内容质量（主题一致、人物一致、情节推进、逻辑硬伤、情感交付） | LLM Judge |
| **memory_management** | 长程记忆（writing_log创建与读取） | 规则校验 |

### 3.2 检查项分布 (rev_003)

共40个检查项（通用37个 + 模板特有1-4个）：

| 维度 | 检查项数 | 典型检查项 |
|------|----------|-----------|
| business_rule_compliance | 21 | Skill阅读、HITL交互、枚举校验、字数范围 |
| content_quality | 13 | 主题一致、人物一致、逻辑硬伤、情感交付 |
| format_compliance | 4 | JSON Schema、文件命名 |
| memory_management | 2 | writing_log创建、writing_log读取 |

### 3.3 rev_003新增检查项

| 检查项 | 说明 | 发现的问题 |
|--------|------|-----------|
| `repeated_endings` | 检测多次出现"全文完/全书完/后记" | 模型写不动了硬撑，反复写结局 |
| `late_stage_digression` | 检测workspace无关文件、章节内容跑偏 | 模型写着写着跑题，写作者感想、番外预告 |
| `CONSISTENCY_MANAGEMENT_GUIDE` | 必须读取设定一致性管理指南 | 长篇创作缺乏一致性管理意识 |

---

## 4. 评测结果（v1样本 + rev_003检查项）

### 4.1 整体表现

| 模型 | 样本数 | 平均通过率 |
|------|--------|-----------|
| Claude Opus 4.5 | 14 | 89.72% |
| Gemini 3 Pro | 8* | 82.12% |
| ERNIE 5.0 | 14 | 76.29% |

> **平均通过率**：每个样本的通过率 = 通过的检查项数 / 总检查项数（排除skip），平均通过率为所有样本通过率的算术平均。
>
> **\*Gemini说明**：原始14个样本中有6个因tool call格式问题（重复tool name等低级错误）导致执行失败，未计入统计。

### 4.2 维度对比

| 维度 | Claude | Gemini | ERNIE |
|------|--------|--------|-------|
| format_compliance | 87.5% | 65.6% | 87.5% |
| business_rule_compliance | 92.4% | 87.7% | 84.3% |
| memory_management | 78.6% | 75.0% | 32.1% |
| content_quality | 81.8% | 73.9% | 66.8% |

### 4.3 关键发现

#### 4.3.1 共性难点（所有模型通过率低）

| 检查项 | Claude | Gemini | ERNIE | 分析 |
|--------|--------|--------|-------|------|
| **字数达标** | 28.6% | 12.5% | 35.7% | 短篇容易超字数，中篇容易不够 |
| **无逻辑硬伤** | 35.7% | 0% | 7.1% | 长篇创作极易出现前后矛盾 |
| **writing_log读取** | 57.1% | 62.5% | 21.4% | 续写时忘记先读log了解前文 |

#### 4.3.2 ERNIE特有短板

| 检查项 | ERNIE | Claude | 差距 | 问题 |
|--------|-------|--------|------|------|
| **writing_log创建** | 42.9% | 100% | -57.1% | 不主动创建创作日志 |
| **完整正文输出** | 50.0% | 100% | -50.0% | 部分章节是大纲式摘要而非正文 |
| **角色正文出场** | 64.3% | 92.9% | -28.6% | 设计的角色在正文中未出现 |

### 4.4 ERNIE 5.0改进建议

| 优先级 | 问题 | 建议 | 预期收益 |
|--------|------|------|----------|
| **P0** | 长程记忆缺失 | 强化writing_log机制：创建时机、内容格式、读取习惯 | memory_management +45% |
| **P1** | 章节质量不稳定 | 优化章节生成，避免输出大纲式摘要 | full_narrative_content +50% |
| **P1** | 角色追踪能力弱 | 加强设计→正文的角色追踪 | character_presence +28% |

---

## 5. 目录结构

```
novel_writing_alchemist/
├── check_definitions/           # 检查项定义（v1/v2共用）
│   ├── common_check_list.yaml   # 37个通用检查项
│   ├── template_checks/         # 14个模板特有检查项
│   ├── judge_criteria/          # LLM评判标准
│   └── check_revisions/         # 版本管理 (rev_001~003)
├── design_v1/                   # v1场景设计（超短篇~超长篇）
│   ├── unified_scenario_design.yaml
│   ├── BusinessRules_v2.md      # System Prompt
│   ├── data_pools/skills/       # Skill文档
│   └── samples/                 # 14个样本
├── design_v2/                   # v2场景设计（短篇~中篇）
│   ├── unified_scenario_design.yaml
│   ├── BusinessRules.md         # 重构版System Prompt
│   ├── data_pools/skills/       # 8份Skill文档
│   └── samples/                 # 10个样本
├── env/                         # Checker执行环境
├── scripts/                     # 工具脚本
│   └── recheck_with_new_checklist.sh
├── analysis/                    # 评测结果分析
│   └── model_comparison_statistics.md
└── evaluation_outputs/          # 评测结果
```

---

## 6. 相关文档

| 文档 | 说明 |
|------|------|
| `design_v2/BusinessRules.md` | Agent System Prompt（v2重构版） |
| `check_capability_taxonomy.yaml` | 检查能力体系定义 |
| `check_definitions/check_revisions/REVISION_LOG.yaml` | Checklist版本记录 |
| `analysis/model_comparison_statistics.md` | 详细评测指标统计 |
| `.claude/skills/creative_scenario_construction/SKILL.md` | 创意类场景构建方法论 |
