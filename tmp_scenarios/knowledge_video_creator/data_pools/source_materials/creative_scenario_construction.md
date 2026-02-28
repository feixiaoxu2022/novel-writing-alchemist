---
name: creative-scenario-construction
description: 构建创意类（小说/短剧/文案等）自动评测场景的完整方法论。基于多个场景的多轮设计迭代实战经验沉淀，覆盖从顶层设计到评测分析的全流程。
---

# 创意类评测场景构建方法论 v3.0

> **适用范围**: 小说写作、短剧编写、剧本改编、文案创作等以"创意内容产出"为核心的Agent评测场景。
>
> **核心内容**: 评测维度体系、检查项设计（含程序化检查P0-P6）、评分公式、Judge Criteria 设计与验证、样本设计、Checklist 迭代 SOP、分析工具链与轨迹级深度分析方法论、常见陷阱与设计原则。

---

## 目录

1. [顶层设计](#1-顶层设计)
2. [评测维度体系设计](#2-评测维度体系设计)
3. [检查项设计（Checklist）](#3-检查项设计checklist)
4. [程序化检查体系（P0-P5/P6）](#4-程序化检查体系p0-p5p6)
5. [评分公式与质量分级](#5-评分公式与质量分级)
6. [Judge Criteria 设计与验证](#6-judge-criteria-设计与验证)
7. [样本设计（Sample Design）](#7-样本设计sample-design)
8. [BusinessRules 与 Skill 文档设计](#8-businessrules-与-skill-文档设计)
9. [Checklist 迭代 SOP](#9-checklist-迭代-sop)
10. [分析工具链](#10-分析工具链)
11. [轨迹级深度分析方法论](#11-轨迹级深度分析方法论)
12. [常见陷阱与设计原则](#12-常见陷阱与设计原则)

---

## 1. 顶层设计

### 1.1 设计四步法

```
Step 1: 能力维度定义 → check_capability_taxonomy.yaml
Step 2: 检查项库构建 → common_check_list.yaml + template_checks/
Step 3: 评分体系设计 → checker_score.py (base-60公式)
Step 4: 场景配置整合 → unified_scenario_design.yaml + BusinessRules.md + Skills/
```

### 1.2 核心设计原则

| 原则 | 说明 |
|------|------|
| **SOP/创作分离** | BusinessRules 只放流程规范（输出物路径、JSON Schema、HITL流程），Skill 只放创作指导。混杂会导致文档大面积重复 |
| **检查项外部化** | check_list 从 sample JSON 内嵌迁移到独立 YAML 文件（common + template-specific），消除数百行重复 |
| **程序化优先** | 能用程序检测的不用 LLM——零成本、确定性、毫秒级，且对崩坏输出的 Gate 检出率极高 |
| **增量迭代** | 每次只改必要的检查项，通过 revision 管理版本。禁止"一次大改" |
| **数据驱动** | 每次迭代基于跨模型统计数据定位问题，非凭直觉 |

### 1.3 "一创"vs"二创"场景差异

| 维度 | 一创（NWA/SD） | 二创（NTS） |
|------|---------------|-------------|
| 输入 | 用户 query（题材+风格+篇幅） | 用户 query + 原著小说文本 |
| 核心能力 | 自主规划 + 创意发挥 | 原著理解 + 改编转化 |
| 独特维度 | 意象系统、叙事密度、立意新颖性 | 原著忠实度、视觉化能力、抽象描写控制 |
| 共享维度 | 逻辑连贯性、角色一致性、情感表达、节奏把控 | 同左 |
| 典型问题 | "写不动"（后期崩坏） | "文学风"（抽象描写失控） |

---

## 2. 评测维度体系设计

### 2.1 三层质量分级

从最初的两层（basic/advanced）演进为三层体系：

| 层级 | tier_id | 含义 | 分数影响 | 典型检查项 |
|------|---------|------|---------|-----------|
| **红线** | `redline` | 价值观/伦理道德 | 一票否决，样本废弃 | 伦理道德合规性 |
| **基础** | `basic` | 合格线，可交付的底线 | 0-60分池（base-60扣分） | 格式合规、逻辑硬伤、角色一致性 |
| **优秀** | `advanced` | 精品级，超越平均水平 | 60-100分池（加分） | 意象系统、叙事密度、情感弧线 |

### 2.2 六维度标准框架

创意写作类场景的标准六维度体系：

```
1. format_compliance（格式规范遵循）
   ├── file_existence          # 文件是否存在
   ├── json_schema             # JSON结构是否合法
   └── structural_integrity    # 字段完整性

2. business_rule_compliance（业务规则遵循）
   ├── sop_stage_execution     # SOP阶段执行完整性
   ├── episode_count_logic     # 集数逻辑
   ├── constraint_incorporation # 约束条件融入
   └── skill_document_reading  # Skill文档读取验证

3. tool_use_correctness（工具使用正确性）
   ├── required_tool_calls     # 必要工具调用
   └── tool_call_absence       # 禁止的工具调用

4. interaction_completeness（流程交互完整性）
   ├── hitl_trigger             # HITL触发
   └── hitl_response_handling   # HITL反馈处理

5. data_consistency（数据一致性）
   ├── cross_file_consistency   # 跨文件一致性
   ├── character_reference      # 角色引用一致性
   └── outline_execution        # 大纲执行忠实度

6. content_quality（内容创作质量）
   ├── [redline] ethical_compliance
   ├── [basic]  logic_consistency, character_consistency, length_adequacy
   ├── [basic]  P1_clone, P2_alternating, P3_completion, P4_stability, P5_repetition
   └── [advanced] narrative_density, imagery_system, emotional_arc, pacing, ...
```

### 2.3 维度设计经验

- **子类别数量指导**: 初始设计 12-15 个足够，后续根据跨模型数据逐步扩展到 30-40 个——但不是一步到位的，是多轮迭代逐步增加的。
- **维度 vs 检查项**: 一个子类别下可以有多个检查项（如逻辑一致性下的"结构性硬伤"和"可修复瑕疵"，可共享 LLM 调用）。
- **条件化维度**: 某些维度仅特定题材/模板适用（如"甜度质量"仅甜宠题材、"智斗逻辑合理性"仅悬疑/谋略类），通过 `applicable_genres` 或 `skip_conditions` 控制。

---

## 3. 检查项设计（Checklist）

### 3.1 检查项类型体系

| check_type | 说明 | 成本 | 典型用途 |
|------------|------|------|---------|
| `file_system` | 文件存在性检查 | 零 | 阶段产出物是否生成 |
| `json_schema` | JSON 结构验证 | 零 | 字段完整性、类型正确性 |
| `entity_attribute_equals` | 字段值精确匹配 | 零 | 集数、题材等参数验证 |
| `tool_called_with_params` | 工具调用记录验证 | 零 | Agent是否调用了指定工具 |
| `tool_call_absence` | 工具未调用验证 | 零 | 禁止调用特定工具 |
| `cross_file_consistency` | 跨文件一致性 | 零 | 角色信息、大纲 vs 正文 |
| `programmatic_check` | **程序化内容检查（P0-P5）** | **零** | 克隆/重复/完成度检测 |
| `semantic_check` | LLM Judge 语义评判 | 高 | 内容质量、逻辑连贯性等 |

> **成本分布目标**: 程序化检查（零成本）占 40-50%，LLM 检查占 50-60%。成熟场景的实际比例通常在 45:55 左右。

### 3.2 检查项组织架构

```
check_definitions/
├── common_check_list.yaml          # 通用检查项（所有模板共享）
├── template_checks/                # 模板特有检查项
│   ├── TEMPLATE_A.yaml
│   └── TEMPLATE_B.yaml
└── judge_criteria/                 # LLM Judge 评判标准
    ├── content_quality_basic.yaml
    └── content_quality_advanced.yaml
```

**合并机制**: checker 启动时 `CheckDefinitionLoader` 自动合并 common + template-specific，模板可通过 `skip_rules` 跳过不适用的通用检查项：

```yaml
# template_checks/SD_UNSUPPORTED_GENRE.yaml
skip_rules:
  - check_id: "钩子设计质量"           # 精确匹配
  - pattern: "content_quality.*"      # 通配符匹配
  - pattern: "P1_*"                   # 前缀匹配
```

### 3.3 检查项字段规范

```yaml
- check_id: 结构性逻辑硬伤            # 唯一标识（语义化中文ID，从rev_007开始）
  check_name: 检测剧情中不可修复的逻辑矛盾
  dimension_id: content_quality
  subcategory_id: logic_consistency
  quality_tier: basic                 # redline/basic/advanced
  check_type: semantic_check
  params:
    criteria_file: content_quality_basic.yaml
    criteria_key: logic_structural
    analysis_target: chapters/chapter_*.md
  weight: 1.0
  is_critical: true                   # 关键项（影响Gate/合格判定）
  is_gate: false                      # Gate项（失败则下游折叠）
  replaces: ["old_check_id"]          # 增量recheck时替换的旧检查项
  skip_if_file_not_exists: true       # 文件不存在时跳过（解决dsv1/dsv2差异）
  display_only: false                 # 仅展示不计分（见3.5节）
```

### 3.4 paired_check_cache（共享 LLM 调用）

**问题**: 逻辑硬伤拆分为"结构性"（basic, critical）和"可修复"（advanced）两个检查项后，同一段文本需要调两次 LLM。

**解决方案**: 两个检查项共享一次 LLM 调用，按返回字段分流：

```yaml
- check_id: 结构性逻辑硬伤
  paired_check_cache: logic_flaw_analysis   # 共享缓存key
  params:
    output_field: structural_flaws          # 从共享结果取这个字段

- check_id: 可修复逻辑瑕疵
  paired_check_cache: logic_flaw_analysis   # 同一缓存key
  params:
    output_field: fixable_blemishes         # 从共享结果取另一个字段
```

> **效果**: 节省约 50% LLM 调用成本。

### 3.5 DISPLAY_ONLY 机制

**问题**: 某些检查项衡量的是"优秀级"标准，binary pass/fail 无法反映中等水平的改善。如果该检查项全模型 fail 率 >70% 且跨设计版本无差异，说明当前粒度不适合。

**解决方案**: `display_only: true` 标记仅展示不计分的检查项：

```yaml
- check_id: 角色命名质量
  display_only: true    # 结果展示在报告中但不影响总分
  params:
    description: "区分有设计感的好名字 vs LLM默认通用美名（林晚/陈默/苏晚晴等）"
```

> **使用时机**: 当检查项 fail 率 >70% 且跨设计版本无差异时，说明当前 binary 粒度不适合此项，设为 DISPLAY_ONLY 等待未来引入连续打分。

---

## 4. 程序化检查体系（P0-P5/P6）

### 4.1 设计原理

> "能用程序检测的严重质量缺陷，绝不浪费 LLM 调用。"

程序化检查用纯算法（无 LLM）检测内容质量的严重缺陷。核心优势：

- **零成本**: 不消耗任何 LLM token
- **确定性**: 结果 100% 可复现，无 LLM 随机性
- **速度快**: 毫秒级完成
- **Gate 检出率高**: 对崩坏模型输出的 Gate Fail 率可达 30-50%

### 4.2 P0-P5 检查项定义

| 级别 | 检查项 | 检测目标 | 判定标准 | Gate? |
|------|--------|---------|---------|-------|
| **P0** | 章节产出存在性 | SOP 执行崩坏 | `chapters/chapter_*.md` 是否存在 >=1 个 | Gate |
| **P1** | 章节克隆检测 | 连续章节完全重复 | 连续>=2章完全克隆 或 >=3章前500字克隆 | Gate |
| **P2** | 交替重复检测 | A-B-A-B 循环模式 | 连续>=4章出现交替重复 | Gate |
| **P3** | 章节完成度 | 早期终止/写不动 | 实际/规划章节数 < 0.5 | basic |
| **P4** | 章节长度稳定性 | 后期章节长度萎缩 | 后1/4平均长度 < 前1/3的50% | basic |
| **P5** | 段落重复检测 | 跨章节段落复制 | 跨章节重复率>15% 或 单章连续>=3段重复 | basic |

### 4.3 P6 级检查（LLM 辅助但低成本）

"语义重复/信息衰减"检查，虽然用 LLM 但 prompt 极简：

```yaml
- check_id: 语义重复与信息衰减
  quality_tier: basic
  params:
    validation_method: semantic_repetition_detection
    description: "相邻章节是否在用不同措辞重复同样的情节/情感"
```

> **实战数据**: 语义重复通过率是模型"后期耐力"的核心指标。弱模型通过率可低至 5-15%，强模型可达 80%+。但即使是强模型，也可能因结尾连续多章反复表达同一情感结论而 fail——这与"首尾呼应"不同，criteria 需明确区分。

### 4.4 实现要点

程序化检查在 YAML 中的 `check_type` 仍标记为 `semantic_check`（保持兼容性），但通过 `validation_method` 字段识别并路由到 `ProgrammaticChecker`：

```yaml
- check_id: 章节克隆检测
  check_type: semantic_check          # 保持兼容性
  params:
    validation_method: chapter_cloning_detection   # 路由标识
    analysis_target: chapters/chapter_*.md
    validation_rules:
      - method: chapter_cloning_detection
        threshold: { consecutive_clone: 2, prefix_clone_chapters: 3, prefix_length: 500 }
```

Checker 在分发时检测 `validation_method` 是否匹配已知的程序化方法列表，匹配则走 `ProgrammaticChecker`，否则走 `SemanticChecker`。

### 4.5 程序化检查设计指南

新场景引入程序化检查的标准流程：

1. **跑首轮评测** -> 收集 5+ 模型的完整输出
2. **人工识别"崩坏模式"** -> 哪些模型的输出有明显的结构性质量问题
3. **抽象为算法规则** -> 克隆检测用文本相似度、长度稳定性用统计比较
4. **设定阈值** -> 基于实际数据分布，取"明显异常"的分位线
5. **验证假阳性** -> 在优质模型输出上确认不会误判（重要！见 12.1 Gate假阳性教训）

---

## 5. 评分公式与质量分级

### 5.1 统一评分公式（三场景共用）

```
总分 = 内容分 x 0.7 + 流程分 x 0.3

内容分 = clamp(0, 100, 60 - gate_penalty - basic_deduction + advanced_bonus)
  - gate_penalty:    每个Gate失败项 -20分
  - basic_deduction: 从60分池中按weight扣分
  - advanced_bonus:  从40分池中按weight加分

流程分 = (通过的流程检查项 / 总流程检查项) x 100
```

### 5.2 质量等级映射

| 条件 | 等级 | 分数范围 |
|------|------|---------|
| redline 失败 | 废弃 | 0 |
| gate 失败 | 不合格 | 0-20 |
| basic 有失败 | 不合格 | 20-60 |
| basic 全过 + advanced <70% | 合格 | 60-70 |
| basic 全过 + advanced >=70% | 优秀 | 70-100 |

### 5.3 评分经验

- **7:3 比例的合理性**: 跨模型数据验证——T2 模型普遍"流程分 > 内容分"（C-P差 -8 到 -27），如果流程权重太高会掩盖内容质量差距。
- **base-60 设计意图**: 60 分是"合格线"，basic 全过恰好 60 分。这让 advanced 加分空间（40分）足够区分"合格"和"优秀"。
- **Gate 惩罚 -20 的校准**: 1 个 Gate 失败 -> 内容分最高 40 分 -> 总分最高 28+30=58 分（不合格），2 个 Gate 失败 -> 最高 20 分 -> 总分 14+30=44 分。

---

## 6. Judge Criteria 设计与验证

### 6.1 criteria 文件结构

```yaml
# content_quality_basic.yaml
criteria:
  logic_structural:
    prompt: |
      你是一位专业的文学编辑...
      评判标准：
      1. ...
      2. ...
      示例：
      - 合格: ...
      - 不合格: ...
    output_format:
      verdict: "合格/不合格"
      flaws:
        - type: "..."
          severity: "critical/major/minor"
          fixability: "unfixable/fixable"
          location: "chapter_X"
          description: "..."
```

### 6.2 Criteria 设计经验

| 经验 | 说明 |
|------|------|
| **行数是质量指标** | 过于简短的 criteria（<10行）容易导致全模型极低通过率——不是模型不行，是标准不清晰。扩展到 40-60 行（含 failure type 分类、合格/不合格示例）后通过率恢复正常 |
| **合理容忍度** | 逻辑检查应允许 <=3 处 minor+fixable 瑕疵仍判合格——创意写作（尤其类型化商业内容）不能用严肃文学标准一刀切 |
| **Show vs Tell** | 叙事密度 criteria 需明确建立"Show过度"和"Tell过度"的评判标准，含 3 组对比示例 |
| **结构化输出格式** | 要求 LLM 输出 `flaws[]` 数组而非自由文本，含 type/severity/fixability/location，提升结果可分析性 |
| **格式模板优先级** | 自定义的结构化输出格式可能被通用模板覆盖——确保自定义格式的优先级高于默认模板 |

### 6.3 跨场景 Criteria 借鉴

跨场景复用 criteria 是高效做法，但需适配：

- 从成熟场景借鉴高质量 criteria（如氛围营造、对话口语化等通用检查项），可节省大量设计时间
- **拆分原则**: 当一个检查项全模型 0-10% 通过率时，通常是 criteria 覆盖面太广，需要拆分为粒度更细的子项
- 借鉴时注意适配场景特性——同一检查项在长篇小说和短剧中的合格标准可能不同

### 6.4 Criteria 验证方法（v3.0 新增）

**当怀疑某检查项存在误判时，按以下步骤验证：**

```
1. 选取强模型被判 fail 的具体 case
2. 读取 check_result 中该检查项的 reason 和 details
3. 读取对应的正文原文，对照 reason 确认判定是否合理
4. 如果 judge 引用的"重复/问题"确实存在 → criteria 没问题，是模型确实有此缺陷
5. 如果 judge 把合理的文学手法判为缺陷 → 需要优化 criteria 的容错规则
```

**实战经验**：语义重复检查项曾被怀疑对"首尾呼应"手法存在误判，但逐 case 分析 judge reason 后发现：criteria 已明确容错了首尾呼应、视角重述、悬疑线索多次引用等文学手法。强模型被判 fail 的 case 实际是**结尾连续 3-4 章的结论反刍**（如同一情感结论在相邻章节反复换方式表达），而非远距离的首尾呼应。**先看 judge 的具体 reason 再下结论，不要凭通过率猜测误判。**

### 6.5 LLM 截断限制

> **重要**: 长文本（小说/剧本）场景中，截断设置直接影响 LLM Judge 准确性。过短的截断（如 50K 字符）可影响 20-30% 样本的判定。

```python
# 推荐设置
LLM_CONTENT_LIMIT = 150_000   # 字符数（约75K tokens）
HEAD_RATIO = 0.5               # 前50% + 后50%
TAIL_RATIO = 0.5
```

对于长文本（小说/剧本），截断策略为"取头+取尾"，确保 LLM 能看到开头的设定建立和结尾的收束。

---

## 7. 样本设计（Sample Design）

### 7.1 样本矩阵设计

```
样本总数 = 模板类型数 x 题材数 x 变量组合（篇幅/集数/约束条件等）
```

典型规模：每个场景 20-35 个样本。太少（<15）则覆盖不够、统计不显著；太多（>50）则评测成本过高。

### 7.2 模板类型分类法

| 类别 | 模板特征 | 测试重点 |
|------|---------|---------|
| **A类**: 标准完整 | 包含所有必要信息的标准任务 | 基线能力 |
| **B类**: 极端条件 | 异常长篇/超多章节/极端约束 | 长任务记忆管理和耐力 |
| **C类**: 信息缺失 | 故意省略关键信息 | HITL触发+信息补全能力 |
| **D类**: 内容约束 | 附带特定内容要求（角色/场景/主题） | 约束融入能力 |
| **E类**: 负面测试 | 不可执行的任务（不支持的题材等） | 拒绝/引导能力 |

### 7.3 设计版本（Design Version）策略

多版本设计（如 DSV1 + DSV2）是重要实践：

- **DSV1**: 基础版 BusinessRules + 基础 Skill 文档
- **DSV2**: 增强版 BusinessRules + 更丰富 Skill 文档 + 额外参考资料

**同一 checklist 同时跑两个版本**，可量化"给 Agent 更多指导"的边际收益。典型数据：增强版平均提升 2-5 分（主要来自内容分提升）。

### 7.4 check_list 与样本的关系变迁

```
v1 时代: check_list 内嵌在 sample JSON 中（800+行重复）
v2 时代: check_list 引用外部 check_definitions/（common + template merge）
v3 时代: 样本只包含元信息（template_id, genre, episode_count），check_list 完全由 CheckDefinitionLoader 动态合并
```

---

## 8. BusinessRules 与 Skill 文档设计

### 8.1 BusinessRules 设计原则

BusinessRules.md 是 Agent 的"系统提示词"，定义 SOP 流程：

```
BusinessRules 应包含:
  - 任务执行流程（几个阶段、每阶段做什么）
  - 输出物路径和格式（workspace/xxx.json）
  - JSON Schema 约束（必需字段、字段类型）
  - HITL 交互规则（何时请求确认、如何处理反馈）
  - 异常处理规则（不支持的题材如何拒绝）

BusinessRules 不应包含:
  - 创作技巧指导（放 Skill 文档）
  - 题材特定知识（放 Skill 文档）
  - 示例和参考（放 data_pools/）
```

### 8.2 SOP 阶段数经验

典型创意写作场景的 SOP 阶段：

| 场景类型 | 阶段数 | 阶段内容 |
|----------|--------|---------|
| 一创小说 | 4 | 创意意图 -> 角色设计 -> 大纲设计 -> 正文写作 |
| 一创短剧 | 4 | 选题简报 -> 角色设计 -> 大纲设计 -> 剧本写作 |
| 二创改编 | 3 | 原著分析 -> 大纲设计 -> 剧本改编 |

> 3-4 个阶段是合理范围。阶段太少（2个）导致缺乏中间检查点；阶段太多（6+）导致 Agent 工具调用过重、HITL 过频繁。

### 8.3 Skill 文档设计

Skill 文档分两类：

**通用 Skill**（所有模板共享）:
- `outline_design_guide.md` — 大纲结构设计方法
- `writing_technique_guide.md` — 写作技巧（Show vs Tell 等）
- `consistency_management_guide.md` — 设定一致性管理
- `character_design_guide.md` — 角色设计（gap/desire/secret 三要素）

**题材 Skill**（按题材分发）:
- `sweet_romance_skill.md` — 甜宠
- `mystery_thriller_skill.md` — 悬疑
- `urban_emotional_skill.md` — 都市情感
- `comedy_humor_skill.md` — 喜剧

> **Skill 文档读取验证**: 通过 `tool_called_with_params` 检查项验证 Agent 是否实际读取了 Skill 文档。配合 `skip_if_file_not_exists: true` 解决版本差异问题。

---

## 9. Checklist 迭代 SOP

### 9.1 迭代触发条件

什么时候需要升级 checklist：

1. **全模型低分检查项** — 当某检查项所有模型通过率 < 20%，大概率是 criteria 问题而非模型问题
2. **零区分力检查项** — 所有模型通过率 100%（或极接近），该项不提供区分力
3. **Gate 假阳性** — 优质模型因非能力缺陷被 Gate（如缺少非必要文件）
4. **新发现的质量缺陷** — 人工审阅发现现有检查项未覆盖的问题
5. **跨场景经验借鉴** — 另一场景验证有效的检查项可以引入

### 9.2 8 类升级操作（A-H分级）

| 类型 | 操作 | 需要重跑 LLM? | 耗时 |
|------|------|---------------|------|
| **A** | 新增 semantic_check 检查项 | 需要远程重跑 checker | 分钟级/项 |
| **B** | 新增 programmatic 检查项 | 需要远程重跑 checker | 秒级/项 |
| **C** | 修改 params（criteria/阈值） | 需要远程重跑 | 分钟级/项 |
| **D** | 修改元信息（weight/tier/name） | 只需 rescore | 秒级 |
| **E** | 删除检查项 | 只需 rescore | 秒级 |
| **F** | 修改 judge_criteria YAML | 需要重跑相关项 | 分钟级/项 |
| **G** | 修改评分公式 | 只需 rescore | 秒级 |
| **H** | 修改 display_only 标记 | 只需 rescore | 秒级 |

> **核心铁律**: 所有模型必须用同一版 checklist。升级后必须对所有模型的所有样本统一重新执行。

### 9.3 Revision 版本管理

```
check_definitions/
└── check_revisions/
    ├── REVISION_LOG.yaml          # 主版本记录
    ├── rev_001/
    │   ├── meta.json              # 变更元信息
    │   ├── checklist.jsonl        # 该版本的完整检查项
    │   └── README.md              # 变更说明
    ├── rev_002/
    └── ...
```

- **check_result 文件名带 revision 后缀**: `check_result_rev009.json`，不同版本结果共存互不覆盖
- **增量 recheck**: `batch_recheck.sh --add --only-checks "新检查项ID"` 只跑新增/修改的检查项
- **replaces 机制**: 新检查项声明 `replaces: ["旧ID"]`，增量 recheck 时自动清理旧结果

### 9.4 迭代节奏经验

一个场景从初版到稳定通常需要 **6-9 轮迭代**，平均每轮 2-3 天。前 4 轮解决结构性问题（格式/Gate/基础质量），后面的轮次涉及精细化（advanced 质量、criteria 措辞调优）。简单场景（如二创改编）可能 3 轮即稳定，复杂场景（一创长篇小说）通常需要 8-9 轮。

---

## 10. 分析工具链

### 10.1 工具链全景

```
评测执行 -> check_result_revXXX.json
    |
    v
单模型统计 -> generate_statistics.py -> statistics.md
    |
    v
跨模型横评 -> generate_cross_model_report.py -> cross_model_data.md
    |
    v
人工分析报告 -> cross_model_report.md（引用数据表格中的数字）
```

### 10.2 generate_statistics.py（单模型统计）

- **双模式架构**: LocalReader（读本地目录）+ RemoteReader（通过 HTTP API 读远程）
- **多层级统计**: 总览 -> 维度 -> 子类 -> 内容质量层级
- **输出**: JSON（机器可读）+ Markdown（人类可读）

### 10.3 generate_cross_model_report.py（跨模型横评）

- **场景通用**: 通过 JSON 配置文件适配不同场景
- **自动聚合**: 扫描 `evaluation_outputs/` 下所有 `check_result*.json`，按模型名聚合
- **数据/分析分离**: 脚本只生成数据表格（`cross_model_data.md`），分析报告由人工编写

### 10.4 分析方法论

**检查项区分力分析**:

| 区分力 | 判定标准 | 处理 |
|--------|---------|------|
| 极强 | 通过率范围跨度 > 80pp | 核心指标，重点保留 |
| 强 | 跨度 50-80pp | 有效指标 |
| 中等 | 跨度 20-50pp | 正常 |
| 弱 | 跨度 < 20pp 或全模型 >90% | 考虑删除或降权 |
| 无效 | 全模型 100% | 删除或改为 Gate 前置条件 |

**典型发现模式**:
- **体裁特定能力断层**: 某些检查项出现极端两极分化（如 4% vs 96%），说明该能力是一个新的分界线——不同模型对特定体裁要求的理解差异可能远大于通用写作能力差异
- **"知道怎么做但写不好"**: 中等模型流程分 > 内容分（C-P 差 -8 到 -27），说明 SOP 遵循能力与内容创作能力是独立维度
- **共性短板聚集**: 多个检查项共同指向同一底层缺陷（如语义重复 + 反复结局 + 大纲执行低 → "后期耐力不足"），应在分析报告中关联解读

### 10.5 能力对比分析 SOP（模型间）

当需要深入对比两个模型在某项检查上的差异时：

```
1. 从 statistics.md 找到差异最大的检查项
2. 确认 A 模型 fail 的具体样本
3. 确认 B 模型在同一样本上 pass
4. 读取 A 模型的实际输出文件（不能臆测！）
5. 读取 B 模型的实际输出文件
6. 查阅对应的 criteria/规范
7. 编写对比分析（附原文引用）
```

> **核心原则**: 不能用"跳过"案例（是依赖失败非能力缺陷）、必须读实际文件不能臆测、必须对比同一 sample。

---

## 11. 轨迹级深度分析方法论（v3.0 新增）

> 统计数据告诉你"什么模型在什么检查项上弱"，但不告诉你"为什么弱"。轨迹级分析深入到 tool call 序列和 agent 思考过程，揭示行为机制。

### 11.1 方法概述

```
选取同一样本 → 提取各模型 tool_call_list → 分析工具调用序列/频率/模式 → 
读取 conversation_history 中 agent 的思考文本 → 对比行为差异 → 归因
```

**数据源**：每个评测样本的 JSON 文件包含：
- `tool_call_list`：完整的工具调用序列（name + arguments）
- `conversation_history`：包含 agent 的思考过程（text blocks）
- `execution_time`：任务执行总时间
- `_env/workspace/`：agent 的最终工作区产出物

### 11.2 关键观测维度

**a) 规划粒度**
- 对比各模型 outline.json 的大小和结构深度
- 强模型的 outline 通常是**场景级蓝图**（每章含 location/characters/purpose/core_action/conflict_point/emotional_shift），弱模型的 outline 可能只是**一句话提纲**
- 经验数据：规划详尽的模型（outline 100KB+）vs 粗略规划（outline <15KB），内容分差距可达 30-40 分
- **规划阶段投入的 token 是回报率最高的**

**b) 自我纠偏能力（Review-Expand 循环）**
- 写完初稿后，模型是否主动统计字数、对比目标？
- 发现差距后的策略：系统性 review（回看 outline 找被压缩场景 → 选择性扩写关键章节）vs 无策略（不统计不 review）vs 不做（一口气写完就交）
- 扩写质量：是否引入了新信息（未展开的支线、配角视角、环境描写），还是重复主角情感结论
- **这是长任务创作中区分力最强的行为维度**

**c) 上下文丢失后的恢复能力**
- 长对话中上下文截断几乎不可避免。关键是截断后的行为模式
- 灾难性崩溃：重复读取全部已有文件多遍（"从头理解"→上下文再次溢出→再读），最终降级任务规模
- 优雅恢复：依赖 writing_log（结构化 checkpoint）快速恢复进度，只读最近 2 章续写
- **writing_log 不是可选的最佳实践，而是长任务的关键恢复机制**

**d) 工具调用效率**
- tool call 总数和执行时间是 agent 效率的直接指标
- 经验数据：完成同一任务，强模型可能 100-170 次调用 / 2-3 小时，弱模型可能 600+ 次调用 / 8+ 小时——大量 token 浪费在重复读取、死循环、推倒重来上
- 重复工具调用模式（如连续 N 次 read 同一文件）是上下文丢失或决策能力缺失的信号

**e) 范围控制能力**
- 一章只写一章的内容 vs 在第一章就把整个故事写完
- 有的模型 outline 规划了 40 章，但实际在第一章就写了完整的起承转合直到结局
- 这是"知道规则但不会用"的典型表现——流程分高但内容分极低

### 11.3 分析步骤模板

```python
# 1. 提取工具调用序列
tool_calls = data['tool_call_list']
# 统计工具类型频率
from collections import Counter
tool_counts = Counter(t['name'] for t in tool_calls)

# 2. 定位关键阶段（如后期 review/expand）
# 搜索 conversation_history 中含关键词的 assistant 思考
keywords = ['字数', '扩展', '扩写', '不足', '目标', 'review', '回顾']

# 3. 比较产出物
#    - workspace/chapters/ 下的文件数和每文件大小
#    - outline.json 大小
#    - writing_log.md 内容（checkpoint 质量）

# 4. 跨模型对比（同一样本）
#    | 模型 | Tool Calls | 执行时间 | 章节数 | 总字数 | Outline 大小 |
```

### 11.4 从轨迹洞察到构建建议

轨迹分析的最终目标不是描述问题，而是**给出利于构建的洞察**：

| 观察到的行为差异 | 表层问题 | 构建建议 |
|-----------------|---------|---------|
| 强模型 outline 188KB vs 弱模型 10KB | 规划粗糙 | 在 Skill 文档中增加 outline 质量标准：要求场景级粒度而非章节级摘要 |
| 强模型写完后 review+expand，弱模型不 review | 字数不达标 | 在 Skill 中增加"完成终章后的 review 协议"规范 |
| 弱模型截断后反复读全部文件 | 上下文丢失 | writing_log 从可选升级为框架级强制；增加"截断恢复协议"到 system prompt |
| 中等模型流程完美但每章太薄 | 内容密度低 | 检查项区分"有没有做"和"做得好不好"——流程检查 vs 内容质量检查 |
| 扩写引入结论反刍而非新信息 | 语义重复 | 扩写策略应指导"用什么素材扩"：被删减的支线、配角视角、环境描写 |

---

## 12. 常见陷阱与设计原则

### 12.1 Gate 设计原则

**Gate 必须只检测"绝对不可接受"的缺陷（SOP 完全崩坏、产出物为空、章节大面积克隆），不能检测"流程不规范"——后者应该是 basic 扣分而非 Gate 否决。**

常见 Gate 假阳性陷阱：
- 要求中间产物（如 outline.json）必须存在 → Agent 可能跳过中间文件但完成了最终产出 → 改为只检查最终产出物（章节文件）是否存在
- 文件白名单过窄 → 合理的辅助文件被判为"非预期文件" → 改为检查"必须有的文件"而非"不应有的文件"

### 12.2 Checklist 升级中的 replaces 陷阱

`replaces` 字段用于新检查项替换旧检查项。**必须使用精确匹配（exact match），不能用模糊匹配**——否则可能意外替换掉不相关的检查项。每次升级后必须验证总检查项数量是否符合预期。

### 12.3 全模型低分陷阱

**现象**: 某检查项所有模型通过率 < 20%。

**排查顺序**:
1. **criteria 太严格?** → 检查评判标准是否合理，criteria 行数过短（<10行）几乎必然导致此问题
2. **检查数据错误?** → 检查 params 中的 expected_value / constraint_content 是否与实际 query 一致
3. **确实是普遍缺陷?** → 只有排除 1 和 2 后才能这样结论

### 12.4 LLM 截断影响

长文本场景中，过短的截断设置（如 50K 字符）可影响 20-30% 样本的 judge 准确性。建议初始就设为 150K（75K head + 75K tail），后续根据实际 token 消耗调整。

### 12.5 数据与代码分离原则

- 代码（checker、scorer、scripts、check_definitions）通过 git push/pull 同步
- 评测数据（evaluation_outputs）通过专用工具（如 fetch_results.py）拉取，**绝对禁止删除远程评测数据**
- 开发阶段必须用 revision 模式（`check_result_revXXX.json`），不同版本结果共存互不覆盖
- inline 模式做 recheck 不会部署 environment 文件到 `_env/`，导致 checker 找不到 judge_criteria 等依赖——**所有 recheck 必须走 batch_recheck.sh**

### 12.6 迭代节奏经验

一个场景从初版到稳定通常需要 **6-9 轮迭代**：

| 阶段 | 轮次 | 重点 |
|------|------|------|
| 结构搭建 | 1-2 | 维度体系、基础格式检查、Gate 机制 |
| 内容覆盖 | 3-4 | Basic 质量检查项、criteria 初版、首轮跨模型数据 |
| 精细调优 | 5-7 | Advanced 质量检查项、criteria 扩写/拆分、程序化检查引入 |
| 稳定收尾 | 8-9 | 评分公式微调、Gate 假阳性修复、DISPLAY_ONLY 调整、全模型重跑验证 |

每轮平均 2-3 天。前几轮变化大（可能新增 10+ 检查项），后几轮以修正和微调为主。
