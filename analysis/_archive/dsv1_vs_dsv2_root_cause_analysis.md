# DSV1 vs DSV2 评测结果差异根因分析报告

生成时间: 2026-02-12
最后更新: 2026-02-13（修正handoff根因分析、character_presence checker修复后数据更新）

## 概述

本报告分析小说写作炼金术师场景从DSV1（设计v1 + rev_003 checklist）升级到DSV2（设计v2 + rev_004 checklist）后，各模型评测指标变化的根本原因。

**核心问题**：DSV1→DSV2同时变更了两个变量——场景设计和checklist版本。因此观察到的指标变化需要区分三类归因：
1. **场景设计变化**导致Agent行为变化（真实能力差异）
2. **Checklist变化**导致评分标准变化（度量尺度差异）
3. **样本池变化**导致统计口径变化（人群差异）

## 评测条件对照

| 条件 | DSV1 | DSV2 |
|------|------|------|
| 场景设计 | design_v1 | design_v2 |
| Checklist版本 | rev_003 | rev_004 |
| 样本数 | 14 | 10 |
| 共有data_id | 6个 | 6个 |
| DSV1独有 | 5个ultra_short + 3个short | — |
| DSV2新增 | — | 4个medium（全新模板） |

---

## 调查一：sop_compliance（检查项19：写作准备阶段HITL调用）

### 数据

| 模型 | DSV1 (rev_003) | DSV2 (rev_004) | 变化 |
|------|---------------|----------------|------|
| Claude 4.5 | 100% (14/14) | **40% (4/10)** | -60pp |
| Claude 4.6 | — | 100% (7/7) | 基线 |
| Gemini | 100% (14/14) | 100% (8/8) | 不变 |
| kimi-k2.5 | 100% (14/14) | 100% (10/10) | 不变 |
| Ernie-5.0 | 100% (14/14) | 75% (3/4) | 样本不足 |
| EB5 | 93% (13/14) | 43% (3/7) | -50pp |

### check定义对比

rev_003和rev_004中check_19的定义**逐字相同**：
```json
{
  "check_type": "tool_called_with_params",
  "params": {
    "tool_name": "novel_writing_service__request_human_review",
    "expected_params": {"stage": "写作准备确认", "type": "confirmation"}
  }
}
```
**结论：指标变化不是check定义变化导致的。**

### Stage 3工作量对比

| 维度 | DSV1 | DSV2 | 倍数 |
|------|------|------|------|
| 必读skill文件 | 2个（命名指南+姓名库） | 4个（+人物设计指南+大纲设计指南） | 2x |
| 大纲层次 | 1层（core_event） | 3层（story_synopsis + chapter_synopsis + scene_sequence） | 3x |
| 每章大纲数据量 | ~260字符 | ~2,252字符 | ~8.7x |
| 完整大纲总量 | ~10,375字符 | ~56,316字符 | ~5.4x |
| 工具调用次数 | ~6个 | ~20-50个 | 3-8x |

### 失败样本证据

Claude 4.5在DSV2中6个失败样本的共同模式——**Agent Handoff打断了HITL流程**：

| 失败样本 | 跳过机制 |
|---------|---------|
| NW_CLEAR_MEDIUM_ANGSTY_001 | 写完outline后发生Agent Handoff，新Agent跳过确认 |
| NW_CLEAR_MEDIUM_BRAINY_ACTION_001 | Turn 17写完大纲→Turn 18 Handoff→Turn 26新Agent直接开始阶段4 |
| NW_CLEAR_MEDIUM_HEROINE_001 | 多次Handoff丢失流程状态 |
| NW_CLEAR_MEDIUM_SWEET_001 | 写完大纲后Handoff，新Agent未恢复流程 |
| NW_CLEAR_SHORT_SWEET_001 | Handoff后跳过确认 |
| NW_IP_MEDIUM_NEUTRAL_001 | Handoff后跳过确认 |

**具体证据**（NW_CLEAR_MEDIUM_BRAINY_ACTION_001）：
- Turn 10-17：Agent完成characters.json和三幕大纲，消耗大量token
- Turn 18：`[Agent Handoff: Context compressed to continue task]`
- Turn 26：新Agent说"创作意图、角色和大纲已完成...我需要开始阶段4——章节创作"，**直接跳过了写作准备确认HITL**

### 根因结论

**归因：Agent上下文管理能力问题（DSV2成功暴露）**

因果链：DSV2 stage 3工作量增加5-8倍 → 产出大量token → 触发上下文窗口限制 → Agent Handoff/上下文压缩 → 新Agent接管时**丢失了"需要执行HITL确认"这个流程状态** → HITL被跳过。

DSV1不受影响的原因：stage 3工作量小（~6个工具调用），在同一个上下文窗口内就能完成全部stage 3工作+HITL确认，Handoff发生在stage 4，此时HITL已执行完毕。

通过的4个样本同样有Handoff，但Handoff恰好发生在HITL确认之后。**失败与否取决于Handoff发生的时间点是否恰好在"大纲完成-HITL确认"这个间隙**。

**这不是简单的"能力不足"，而是SOP流程在上下文断裂时的脆弱性**。Claude 4.6在同样条件下100%通过，说明更强的模型能更好地在Handoff后恢复流程状态。

### Handoff机制的深层分析（2026-02-13修正）

**之前的错误认知**：Handoff后system prompt丢失导致新Agent不知道流程要求。

**修正后的认知**：经过代码验证（agent.py:1791-1795），system prompt在Handoff后**始终被保留**。新Agent的messages列表首先附加system prompt，然后附加handoff_prompt。因此新Agent有完整的任务规则定义。

**真正的根因是handoff_prompt的内容质量**：
1. **Step 1 summary缺失**（已修复）：旧版handoff只传递`model_answers`（Step 3的Q&A回答），不传递`summary_response`（Step 1的工作总结）。修复后handoff_prompt同时包含工作总结和补充问答。
2. **Step 2问题缺乏flow-state引导**（已修复）：旧版Step 2让新Agent"提问"，但问题没有引导旧Agent明确说出"当前进行到哪个阶段、哪些步骤已完成、哪些尚未执行"。修复后handoff_prompt末尾明确提示："请仔细检查上述交接信息中提到的流程进度，确认哪些步骤已完成、哪些尚未执行（特别是需要与用户交互确认的步骤），然后从正确的位置继续工作。"

**修复效果评估**：handoff修复已部署到agent.py，但目前缺乏修复后的Claude 4.5重跑数据来验证改善程度。DSV2 Claude 4.5的re-run样本完成后可对比。

---

## 调查二：character_presence（检查项35/36：主角在大纲和正文中的存在性）

### 数据（原始，checker修复前）

**character_presence_in_outline**:

| 模型 | DSV1 (rev_003) | DSV2 (rev_004) | 变化 |
|------|---------------|----------------|------|
| Gemini | 84.6% (11/13) | **25.0% (2/8)** | -60pp |
| kimi-k2.5 | 90.9% (10/11) | **28.6% (2/7)** | -62pp |
| Claude 4.5 | 78.6% (11/14) | 88.9% (8/9) | +10pp |
| EB5 | 83.3% (10/12) | 16.7% (1/6) | -67pp |

### Checker修复说明（2026-02-13）

上述数据中，DSV2的大幅下降存在**checker统计污染**：当模型未读取schema、使用了错误字段名（如`protagonists`而非`main_characters`）时，checker会因找不到`main_characters`字段而直接判定`fail`。这把两类不同的问题混为一体：
- A. **schema合规性问题**：模型没读schema导致字段名错误（→应为skip，不计入pass_rate）
- B. **真正的角色存在性问题**：模型读了schema、字段名正确，但角色未出现在大纲/正文中（→应为fail）

**修复内容**：check_35/36的checker逻辑新增了前置类型检查——当`characters.json`的`main_characters`字段不存在时，返回`skip`（非pass非fail）并标记`schema_violation=True`。这样schema合规性问题不会污染character_presence的通过率统计。

### 修复后数据（rev_004，2026-02-13）

| 版本 | 模型 | 总样本 | 35(outline) pass/eval | 35 skip(sv) | 36(chapters) pass/eval | 36 skip(sv) |
|------|------|--------|----------------------|-------------|------------------------|-------------|
| DSV1 | Claude 4.5 | 8 | 6/8=75% | 0 | 8/8=100% | 0 |
| DSV1 | Ernie-5.0 | 8 | 3/7=43% | 1(0) | 3/7=43% | 1(0) |
| DSV1 | Gemini | 8 | 5/6=83% | 2(1sv) | 5/6=83% | 2(1sv) |
| DSV1 | EB5 | 14 | 10/12=83% | 2(0) | 9/11=82% | 3(0) |
| DSV1 | kimi | 14 | 10/11=91% | 3(0) | 10/11=91% | 3(0) |
| DSV1 | glm-4.7 | 3 | 2/2=100% | 1(0) | 1/1=100% | 2(0) |
| DSV2 | kimi-171439 | 8 | 1/1=100% | 7(5sv) | 1/1=100% | 7(5sv) |
| DSV2 | Ernie-5.0 | 6 | 4/4=100% | 2(2sv) | 4/4=100% | 2(2sv) |
| DSV2 | Claude 4.5 | 6 | 6/6=100% | 0 | 6/6=100% | 0 |
| DSV2 | kimi-131949 | 10 | 0/1=0% | 9(5sv) | 0/1=0% | 9(5sv) |
| DSV2 | EB5 | 7 | 1/1=100% | 6(5sv) | 1/1=100% | 6(5sv) |
| DSV2 | Claude 4.6 | 7 | 7/7=100% | 0 | 6/7=86% | 0 |
| DSV2 | Gemini | 10 | 2/2=100% | 8(8sv) | 2/2=100% | 8(8sv) |
| DSV2 | glm-4.7 | 3 | 1/1=100% | 2(0) | 1/1=100% | 2(0) |

**关键解读**：
- DSV2中大量`schema_violation skip`（sv列）证实了根因——模型未读schema导致字段名错误
- 排除schema_violation后，有效评估的样本数极少（Gemini仅2/10，kimi-171439仅1/8，EB5仅1/7），无法对pass_rate做有统计意义的判断
- **kimi-131949的唯一有效样本fail了（0/1=0%）**，说明即使字段名正确也不保证通过
- **DSV2的character_presence"暴跌"的主因是schema合规性问题**，但由于有效样本过少，无法确定排除schema问题后character_presence的真实水平
- DSV2中，Gemini 10个样本中8个因schema_violation而skip——只有2个样本读了schema
- 强模型（Claude 4.5/4.6）不受影响——100%读schema，100%或接近100%通过

### schema reading遵从率验证（硬数据）

| 模型 | DSV1读取characters.schema | DSV2读取characters.schema | 下降幅度 |
|------|--------------------------|--------------------------|---------|
| Gemini | **100% (14/14)** | **20% (2/10)** | -80pp |
| kimi-k2.5 | 100% (14/14) | 40% (4/10) | -60pp |
| Claude 4.5 | 100% (14/14) | 100% (10/10) | 不变 |
| EB5-midtrain | 79% (11/14) | 20% (2/10) | -59pp |
| Ernie-5.0 | — | 67% (4/6) | — |
| Claude 4.6 | — | 100% (7/7) | — |

### check定义对比

rev_003的check_34/35和rev_004的check_35/36定义**完全相同**，都检查`main_characters`字段。check编号偏移1是因为rev_004新增了check_33(workspace_file_compliance)，但检查逻辑不变。

### 核心发现：BusinessRules中schema引导的结构性差异

**DSV1**——schema reading作为**强制前置条件**，在3处反复强调：

| 位置 | 原文 |
|------|------|
| 阶段3准备工作 | "**验证JSON格式**：读取 data_pools/schemas/characters.schema.json 确认人物JSON格式" |
| 关键约束 | "**在输出每个JSON文件前，必须先读取对应schema验证格式** characters.json → 读取 characters.schema.json" |
| 核心原则 | "任务开始时必须阅读" |

**DSV2**——schema reading被**降级为"交付前验证"**，仅出现1次：

| 位置 | 原文 |
|------|------|
| 阶段3末尾 | "读取 characters.schema.json 和 outline.schema.json，确认输出格式正确"（放在"交付前验证"环节） |

### schema reading遵从率验证

| 模型 | DSV1读取characters.schema | DSV2读取characters.schema |
|------|--------------------------|--------------------------|
| Gemini | **100% (14/14)** | **37.5% (3/8)** |
| kimi-k2.5 | 100% (14/14) | 40% (4/10) |
| Claude 4.5 | 100% (14/14) | 100% (10/10) |

### Gemini错误字段名证据

Schema要求的正确字段名：`main_characters`（数组）

Gemini在DSV2中实际使用的字段名：

| data_id | 实际字段 | 是否正确 |
|---------|---------|---------|
| ADVENTURE_001 | `protagonists` | 错 |
| BRAINY_ACTION_001 | `protagonist` | 错 |
| HEROINE_001 | `protagonist` | 错 |
| SUSPENSE_001 | `protagonist` | 错 |
| SWEET_001 | `main_characters` | 对 |
| ANGSTY_001 | `main_characters` | 对 |
| SHORT_ANGSTY_001 | `characters` | 错 |
| SHORT_SWEET_001 | `protagonist` | 错 |
| IP_NEUTRAL_001 | `protagonist` | 错 |
| SWEET_DRAMA_001 | `protagonists` | 错 |

**80%的样本使用了错误字段名**（protagonist/protagonists/characters），都是语义正确但不符合schema规定。

### 同一data_id对比

| data_id | DSV1 Gemini字段 | DSV1结果 | DSV2 Gemini字段 | DSV2结果 |
|---------|---------------|---------|---------------|---------|
| SUSPENSE_001 | main_characters | pass | protagonist | **fail** |
| SWEET_001 | main_characters | pass | main_characters | pass |
| SHORT_SWEET_001 | main_characters | pass | protagonist | **fail** |

同一模型、同一data_id，差异只在于是否正确使用了`main_characters`字段名。

### 根因结论（2026-02-13修正）

**归因：样本设计问题（DSV2 prompt结构弱化了schema引导）+ Checker统计方法问题（已修复）**

因果链：DSV2将schema reading从"创作前强制前置"改为"交付后可选验证" → Gemini/kimi/EB5的schema reading遵从率从100%骤降至20-40% → 不读schema时模型使用先验认知中的`protagonist`/`protagonists`而非schema规定的`main_characters` → character_presence checker找不到`main_characters`字段。

**修复前**：checker直接判定fail → 污染了pass_rate统计，造成"character_presence暴跌"的假象。
**修复后**：checker返回skip(schema_violation) → 不计入pass_rate分母。修复后数据显示：正确使用`main_characters`字段的样本，角色存在性几乎100%通过。

**关键点**：
1. DSV2的character_presence"暴跌"的主因是schema合规性问题，而非角色描写能力下降
2. 但由于修复后有效评估样本极少（弱模型仅1-2个），无法确定真实的character_presence水平
3. 强模型（Claude 4.5/4.6）在任何prompt结构下都主动读schema，不受影响
4. 弱模型（Gemini/kimi/EB5）在schema引导弱化后就不读了，暴露出**指令遵从度**的差异

**改进建议**：在DSV2的BusinessRules中恢复schema reading的前置要求（已执行），至少在阶段3开始时明确要求"在创建characters.json前必须先读取characters.schema.json确认字段名"。

---

## 调查三：late_stage_digression（后期章节跑偏）

### 数据

| 模型 | DSV1 (rev_003) | DSV2 (rev_004) | 变化 |
|------|---------------|----------------|------|
| kimi-k2.5 | 0% (0/14) | **50% (5/10)** | +50pp |
| EB5 | 0% (0/14) | 28.6% (2/7) | +29pp |
| Claude 4.5 | 92.9% (13/14) | 80% (8/10) | -13pp |
| Gemini | 50% (7/14) | 100% (8/8) | +50pp |

### check定义变化

**rev_003 check_33**（late_stage_digression）：
- check_type: `semantic_check`
- analysis_target: `workspace/`（整个workspace目录）
- **复合检查**：judge criteria同时要求检查两件事：
  1. workspace中是否有白名单外的无关文件（"情况A：创建白名单之外的无关文件" → 不合格）
  2. chapters中章节是否跑偏（"情况B：chapters中的章节内容跑偏" → 不合格）
- 任一不合格即判定fail

**rev_004 拆分为两个独立检查**：

1. **check_33** (workspace_file_compliance)：
   - check_type: `file_whitelist_check`（新类型）
   - 纯规则检查，只验证workspace中是否有白名单外文件

2. **check_34** (late_stage_digression)：
   - check_type: `semantic_check`
   - analysis_target: `chapters/`（从workspace缩小到chapters目录）
   - judge criteria明确排除workspace文件检查："❌ 不检查：workspace中是否有额外文件"

### 关键发现：workspace_file_compliance从未执行

checker_execute.py的check_type分发逻辑（第2700-2717行）**不支持`file_whitelist_check`类型**，只支持：file_existence、json_schema、cross_file_consistency、tool_called_with_params、tool_call_absence、semantic_check。

所以check_33(workspace_file_compliance)在所有评测中结果都是`skip`（统计报告中显示0/0）。**拆分后workspace白名单检查实际完全消失了。**

### 根因结论

**归因：Checker设计变更导致数据不可比**

rev_003的late_stage_digression是复合检查（workspace文件合规 + 章节语义），rev_004将其拆分后late_stage_digression只检查章节语义。由于judge criteria中不再包含"创建无关文件=不合格"的判定标准，纯语义检查的通过率自然高于复合检查。

kimi从0%→50%的原因是：rev_003中LLM Judge在评估late_stage_digression时，judge criteria要求同时检查workspace文件合规性和内容语义，即使章节内容合格，如果有额外文件也会判fail；rev_004中judge criteria明确排除了文件检查，只看章节内容。

**附带发现**：rev_004新增的workspace_file_compliance(check_33)因为checker不支持`file_whitelist_check`类型而全部skip，这是一个**系统bug**——应该实现该check_type或改用已支持的类型。

---

## 调查四：logical_contradiction（检查项24：逻辑硬伤）

### 数据

| 模型 | DSV1 (rev_003) | DSV2 (rev_004) | 变化 |
|------|---------------|----------------|------|
| Claude 4.5 | **42.9% (6/14)** | **0% (0/10)** | -43pp |
| Claude 4.6 | — | 14.3% (1/7) | 基线 |
| Gemini | 21.4% (3/14) | 12.5% (1/8) | -9pp |
| kimi-k2.5 | 7.1% (1/14) | 0% (0/10) | -7pp |
| EB5 | 7.1% (1/14) | 0% (0/7) | -7pp |
| Ernie-5.0 | 7.1% (1/14) | 0% (0/4) | -7pp |

**注意**：之前context中记录DSV1 Claude 4.5为35.7%(5/14)，实际数据为42.9%(6/14)——已修正。

### judge_criteria差异

**rev_003** (content_quality_basic.yaml v1.4)：
- 输出格式：`{"matched": true/false, "reason": "..."}`
- 纯文本描述式评判

**rev_004** (content_quality_basic.yaml v1.6)：
- 输出格式：`{"matched": false, "flaw_count": 3, "flaws": [{"type": "factual_consistency/worldbuilding_coherence/spatiotemporal_continuity", "severity": "critical/major/minor", "location": "...", "description": "..."}], "reason": "..."}`
- **新增结构化硬伤清单**：要求对每个flaw标注类型和严重度

结构化输出要求迫使Judge逐条列举问题，而非笼统评判"整体无明显硬伤"就给pass。

### 小说复杂度对比

| 指标 | DSV1 | DSV2 | 倍数 |
|------|------|------|------|
| 平均字数 | 28,704字 | 77,757字 | 2.7x |
| 字数范围 | 6,469-81,768 | 29,765-117,145 | — |
| DSV2新增模板平均字数 | — | 95,936字 | — |

### 共有data_id交叉验证

| data_id | DSV1字数 | DSV2字数 | rev_003结果 | rev_004(DSV2)结果 |
|---------|---------|---------|-----------|----------------|
| MEDIUM_ANGSTY_001 | 63,577 | 104,516 | FAIL | FAIL |
| MEDIUM_SUSPENSE_001 | 66,413 | 75,618 | **PASS** | FAIL |
| MEDIUM_SWEET_001 | 81,768 | 117,145 | FAIL | FAIL |
| SHORT_ANGSTY_001 | 8,874 | 34,402 | **PASS** | FAIL |
| SHORT_SWEET_001 | 31,566 | 29,765 | **PASS** | FAIL |
| IP_NEUTRAL_001 | 14,330 | 32,385 | FAIL | FAIL |

6个共有data_id中，3个从PASS翻转为FAIL。其中SHORT_SWEET_001字数从31,566→29,765反而减少，仍从PASS翻转为FAIL——说明字数增长不是逻辑失败的充分条件。

### 两因素分解

**因素1：Judge criteria变严（贡献约50%，~21pp）**

用同批DSV1小说在v4中间版本（无结构化flaw输出但其他条件相同）重新评判：42.9% → 21.4%，3个边缘PASS被翻转。这个降幅纯粹来自评判标准变化。

**因素2：DSV2小说全新创作（贡献约45%，~19pp）**

共有data_id在v4标准下：DSV1小说约33.3%通过 → DSV2小说0%通过。DSV2中Agent为每个data_id重新创作的小说内容不同于DSV1，新创作的小说引入了新的逻辑问题。字数增长是附带现象而非独立原因——SHORT_SWEET_001字数减少仍fail证明了这一点。

**因素3：样本池构成变化（贡献约5%，~2pp）**

DSV2移除了5个ultra_short模板（DSV1中这些模板因篇幅短容易通过），新增4个medium模板（全部fail）。但样本池效应在v4标准下只贡献约2个百分点。

### 根因结论

**归因：Judge criteria变更（~50%）+ 小说内容差异（~45%）+ 样本池变化（~5%）**

42.9%→0%的下降是三因素叠加。最大的单因素是judge_criteria引入结构化flaw输出格式后评判标准变严。其次是DSV2下Agent创作的小说内容本身不同（不同的创作实例产生不同的逻辑问题）。样本池变化影响最小。

**缺失的控制实验**：目前没有"DSV1小说 + 正式rev_004 criteria"的cross-check数据。如果补做此实验（对DSV1评测结果用rev_004 checker重新跑），可以精确分离criteria和小说内容各自的贡献比例。

**附带发现**：REVISION_LOG.yaml中rev_004的变更记录**遗漏了judge_criteria结构化输出格式这一重大变更**，需要补充。

---

## 四大调查汇总：各指标变化的归因分类

| 指标 | 变化 | 归因类型 | 根因 |
|------|------|---------|------|
| sop_compliance (check_19) | Claude 4.5: 100%→40% | **Agent能力问题（DSV2成功暴露）+ Handoff机制缺陷（已修复）** | 工作量增加→Agent Handoff→handoff_prompt缺失summary+flow-state→流程状态丢失 |
| character_presence | Gemini: 85%→25%, kimi: 91%→29% | **样本设计问题 + Checker统计污染（已修复）** | DSV2 prompt弱化schema引导 + 旧checker把schema不合规误判为fail |
| late_stage_digression | kimi: 0%→50%, EB5: 0%→29% | **Checker设计变更（不可比）** | rev_004拆分复合检查为独立语义检查 |
| logical_contradiction | Claude 4.5: 43%→0% | **混合因素** | Judge criteria变严(50%) + 小说内容差异(45%) + 样本池变化(5%) |

---

## 五、DSV2设计升级的总体评价

### 核心问题：DSV1→DSV2升级整体是正向还是负向？

**结论：DSV2设计升级方向正确，但产生了"成本先到、收益后到"的错位效应。**

- 成本（过程复杂度增加）已经在当前checklist中体现为分数下降
- 收益（写作质量提升）在当前checklist中基本测不到

### 5.1 DSV2设计升级的核心内容备忘

#### 场景复杂度升级（增加过程负担）

| 升级项 | DSV1 | DSV2 | 影响 |
|--------|------|------|------|
| Skill文件数量 | 2个（SKILL.md + CHARACTER_NAMING_GUIDE.md） | 6个（拆分为按阶段组织的专项文件） | Agent需要更多读取操作 |
| 大纲结构 | 2层（act → core_event） | 3层（act → chapter_synopsis → scene_sequence，每场景8必填字段） | 大纲工作量增加5-8倍 |
| 每章大纲数据量 | ~260字符 | ~2,252字符 | 8.7倍 |
| 完整大纲总量 | ~10,375字符 | ~56,316字符 | 5.4倍 |
| 配方选择 | "灵感模糊时必需" | "必需（生成后必须让用户选择）" | 更严格的HITL要求 |
| BusinessRules结构 | 松散规则清单（163行） | 结构化操作手册（189行），每阶段有输入→过程→输出→验证闭环 | Agent更易遵循但也更长 |

#### 写作方法论升级（提升内容质量，当前测不到）

| 新增Guide | 所属阶段 | 教什么 |
|-----------|---------|--------|
| RECIPE_KNOWLEDGE.md | 阶段2 | 从SKILL.md拆出的配方知识（X轴+Y轴+反应规则+禁忌表） |
| CHARACTER_DESIGN_GUIDE.md | 阶段3 | 人物设计方法论（traits三步法、动机设计、秘密恐惧、配角、关系网） |
| OUTLINE_DESIGN_GUIDE.md | 阶段3 | 大纲设计方法论（三层结构设计、synopsis写法、scene_sequence设计） |
| WRITING_TECHNIQUE_GUIDE.md | 阶段4 | 写作实战技巧（场景构造、对话、叙事、情感渲染、冲突、节奏6大技法） |
| ROMANCE_WRITING_GUIDE.md | 阶段4 | 感情线写作技巧（含蓄表达、糖点类型学、双男主/男女CP差异化） |
| CONSISTENCY_MANAGEMENT_GUIDE.md | 阶段4(长篇) | 设定一致性管理（登记簿机制、一致性检查清单、高频漏洞点） |

#### 样本模板变化

| 类别 | DSV1 | DSV2 |
|------|------|------|
| 总样本数 | 14 | 10 |
| DSV1独有 | 5个ultra_short + CLEAR_SHORT_ANGSTY_002/003 + CLEAR_SHORT_SWEET_002 | — |
| DSV2新增 | — | VAGUE_MEDIUM_SWEET_DRAMA、CLEAR_MEDIUM_BRAINY_ACTION、CLEAR_MEDIUM_ADVENTURE、CLEAR_MEDIUM_HEROINE |
| 共有 | 6个（MEDIUM_ANGSTY/SUSPENSE/SWEET、SHORT_ANGSTY/SWEET、IP_NEUTRAL） | 同左 |
| 特点变化 | 含ultra_short/short/medium/long/ultra_long全谱系 | 集中在medium，砍掉极端长度，新增vague类型 |
| user_simulator_prompt | 部分非常简略（一行话） | 全部统一结构：核心诉求→配方选择偏好→写作准备确认关注点 |

### 5.2 全维度对比表（以可比的4个模型为准）

#### 可直接对比的维度（check定义未变）

| subcategory | Claude 4.5 DSV1→DSV2 | Gemini DSV1→DSV2 | kimi DSV1→DSV2 | EB5 DSV1→DSV2 | 趋势判断 |
|---|---|---|---|---|---|
| naming_convention | 100→100 (=) | 79→100 (+21) | 100→100 (=) | 79→57 (-22) | 中性 |
| structural_integrity | 83→87 (+4) | 79→100 (+21) | 81→73 (-8) | 81→76 (-5) | 中性偏正（Gemini提升明显） |
| output_completeness | 100→98 (-2) | 95→100 (+5) | 100→100 (=) | 86→75 (-11) | 中性（EB5下降） |
| log_file_creation | 100→100 (=) | 86→100 (+14) | 100→100 (=) | 86→71 (-15) | 中性 |
| log_file_usage | 57→90 (**+33**) | 57→63 (+6) | 86→40 (**-46**) | 14→14 (=) | **分化严重**：Claude 4.5大幅提升，kimi大幅下降 |
| theme_consistency | 100→100 (=) | 100→100 (=) | 93→100 (+7) | 79→57 (-22) | 中性（EB5下降） |
| main_character_consistency | 100→100 (=) | 100→100 (=) | 100→100 (=) | 79→43 (**-36**) | 中性（EB5崩塌） |
| plot_progression | 100→100 (=) | 100→100 (=) | 100→100 (=) | 64→57 (-7) | 几乎不变 |
| character_design_adherence | 100→83 (-17) | 93→80 (-13) | 93→50 (**-43**) | 64→75 (+11) | **整体下降**（kimi跌幅最大） |
| character_trait_consistency | 100→90 (-10) | 100→100 (=) | 86→80 (-6) | 71→57 (-14) | 轻微下降 |
| emotional_delivery_match | 77→82 (+5) | 62→60 (-2) | 64→73 (+9) | 58→14 (**-44**) | 中性（EB5崩塌） |
| full_narrative_content | 100→90 (-10) | 86→100 (+14) | 79→70 (-9) | 79→43 (-36) | 偏负（弱模型大幅下降） |
| repeated_endings | 93→80 (-13) | 86→88 (+2) | 79→60 (-19) | 57→57 (=) | 偏负 |

#### 有干扰因素的维度（不能直接归因于设计升级）

| subcategory | 变化方向 | 不可比原因 |
|---|---|---|
| sop_compliance | Claude 4.5: 100→40, EB5: 82→43 | check定义相同，但DSV2工作量增加导致Agent Handoff在关键间隙断裂（**Agent能力问题 + Handoff机制缺陷，DSV2成功暴露，Handoff已修复**） |
| character_presence | Gemini: 85→25, kimi: 91→29 | check定义相同，但DSV2 prompt弱化了schema reading引导（**样本设计bug + checker统计污染，均已修复**。修复后DSV2弱模型的大量样本变为schema_violation skip，有效评估样本极少，无法得出可靠的pass_rate结论） |
| late_stage_digression | kimi: 0→50, EB5: 0→29 | rev_004拆分了复合检查，语义检查独立运行后分数自然上升（**度量尺度变了**） |
| logical_contradiction | 全模型暴跌→0-14% | judge_criteria变严(~50%) + 小说内容差异(~45%) + 样本池变化(~5%)（**多因素混杂**） |
| range_constraint | 各模型普遍低 | DSV2目标字数120k vs DSV1的30k，难度完全不同 |
| enum_validity | Gemini: 96→63, kimi: 93→70 | DSV2配方结构更复杂 |
| quantity_constraint | Gemini: 100→63, kimi: 93→70 | 同上 |

#### DSV2新增但当前体系测不到的维度

| DSV2提供的方法论 | 当前有无对应check | 评价体系缺口 |
|---|---|---|
| WRITING_TECHNIQUE_GUIDE（场景构造、对话、叙事6大技法） | **无** | 完全测不到场景描写生动度、对话自然度、叙事节奏 |
| CHARACTER_DESIGN_GUIDE（人物立体度方法论） | character_design_adherence（只检查"是否符合设计文档"） | **只测"一致"不测"设计本身好不好"**——人物是否有内在冲突、动机层次、成长弧线都不测 |
| OUTLINE_DESIGN_GUIDE（三层大纲设计） | structural_integrity（只测JSON能否解析） | **只测格式不测内容质量**——scene_sequence是否有具体可视化行为、冲突点、情感转折都不测 |
| ROMANCE_WRITING_GUIDE（感情线技巧） | emotional_delivery_match（只测"是不是甜/虐"的大方向） | **只测方向不测细腻度**——"含蓄胜于直白、动作胜于语言、张力来自克制"这些技法是否应用了不测 |
| CONSISTENCY_MANAGEMENT_GUIDE（设定一致性管理） | character_trait_consistency + logical_contradiction | 部分覆盖，但logical_contradiction因judge变严反而全军覆没 |

### 5.3 对不同模型的影响分析

| 模型 | 整体avg_pass_rate变化 | 影响方向 | 原因 |
|------|---------------------|---------|------|
| **Claude 4.6** | —（DSV2新增，93.03%） | **正向基线** | DSV2的复杂度没压垮它（sop_compliance 100%），narrative_tone_match等维度表现好 |
| **Claude 4.5** | 89.72→86.97 (-2.75pp) | **表面微降，实际分化** | 流程管理退步（sop 100→40），但log_file_usage大幅提升（57→90）；DSV2任务更复杂但总分仅降2.75pp，说明核心能力仍强 |
| **Gemini** | 79.25→79.88 (+0.63pp) | **中性** | structural_integrity和log_file_creation提升，但character_presence暴跌（prompt bug导致，非真实下降） |
| **kimi-k2.5** | 71.34→70.08 (-1.26pp) | **表面微降，实际退步** | character_design_adherence 93→50, log_file_usage 86→40, 配方相关维度下降20+pp。DSV2的复杂度超过其能力阈值 |
| **EB5-midtrain** | 58.94→52.24 (-6.70pp) | **明显负向** | 多维度崩塌——main_character_consistency 79→43, emotional_delivery_match 58→14, full_narrative_content 79→43。DSV2任务复杂度远超其能力 |
| **Ernie-5.0** | 76.29→65.42 (-10.87pp) | **负向（但仅4样本）** | 样本不足，数据不可靠 |

**规律**：DSV2对模型的影响与模型能力呈正相关——**强模型基本不受影响甚至微升，弱模型明显被压垮**。这说明DSV2成功地拉大了模型间的区分度。

### 5.4 两个假设的验证

**假设A："context工程负担更重，导致中弱模型表现不如DSV1"**

**成立。** 证据：
1. DSV2 stage 3工作量增加5-8倍，直接导致Claude 4.5 sop_compliance从100%→40%（Agent Handoff在关键间隙断裂）
2. 配方结构更复杂，Gemini/kimi/EB5的enum_validity和quantity_constraint下降20-30pp
3. EB5的多个内容维度崩塌（main_character_consistency -36pp, emotional_delivery_match -44pp），说明任务复杂度远超其处理能力
4. 但Claude 4.6完全不受影响——说明这是模型能力的真实分水岭

**假设B："核心价值在于内容质量提升，但当前评价体系测不到"**

**成立。** 证据：
1. DSV2的5个写作方法论guide没有任何对应的check维度——WRITING_TECHNIQUE_GUIDE教的场景构造/对话技巧/叙事节奏，checklist完全不测
2. 已有的quality check只测"规范性"不测"艺术性"——character_design_adherence只测"一致"不测"立体"；structural_integrity只测"JSON格式"不测"大纲质量"
3. 唯一沾边的emotional_delivery_match只测"甜/虐/烧脑的大方向"，不测写作技法是否被应用

### 5.5 一句话总结

> DSV2的设计升级从"流程正确性"走向"创作质量"。但当前评价体系还停留在测"流程正确性"的阶段，所以DSV2的核心价值（写作方法论→更好的小说）完全体现不出来。观察到的负面效果来自两个原因：(1)复杂度增加确实压垮了中弱模型的流程执行能力（但成功拉大了模型间区分度）；(2)有一个prompt设计bug（schema引导弱化）制造了character_presence的虚假下降——checker修复后（schema_violation skip机制），大量弱模型样本变为skip状态，有效评估样本过少无法得出可靠结论，但至少证实了"暴跌"的主因是schema合规性问题而非角色描写能力退化。

---

## 六、行动建议

### 高优先级
1. ✅ **修复DSV2 BusinessRules**：恢复schema reading的前置要求，解决character_presence的系统性下降（已执行）
2. ✅ **实现file_whitelist_check类型**：checker_execute.py中实现了`_check_file_whitelist()`方法（已执行）
3. ✅ **补充REVISION_LOG**：rev_004补充了变更3记录（已执行）
4. ✅ **修复character_presence checker**：check_35/36在`main_characters`字段缺失时返回skip+schema_violation标记，不再污染pass_rate（已执行）
5. ✅ **修复Agent Handoff机制**：handoff_prompt加入summary_response + flow-state提示（已执行于agent.py）

### 中优先级（让DSV2价值显现）
6. **增加内容质量评判维度**：
   - `narrative_craftsmanship`：叙事技巧水平（场景构造、"展示而非告知"、节奏控制）
   - `character_depth`：人物立体度（是否有内在冲突、动机层次、成长弧线）
   - `emotional_subtlety`：情感表达含蓄度（vs 直白"我爱你"式写法）
   - `outline_quality`：大纲质量（scene_sequence是否有具体可视化行为、冲突点、情感转变）
7. **补做控制实验**：用rev_004 checker对DSV1评测结果重新跑check，精确分离criteria vs 小说内容的贡献（**DSV1 rev003→rev004转换已完成，可直接对比**）
8. **DSV2统计数据待补全**：多个模型的re-run正在进行中（见下方附录）

### 低优先级
9. **验证Handoff修复效果**：等Claude 4.5 DSV2 re-run完成后，对比修复前后sop_compliance指标
10. ✅ **修复checker_execute.py类型检查bug**：`_check_main_characters_in_outline`新增`isinstance(characters_data, dict)`检查，防止characters.json顶层为list时崩溃（已执行）

---

## 附录A：已执行的修复措施清单（截至2026-02-13）

| 修复项 | 修改文件 | 说明 |
|--------|---------|------|
| Handoff summary缺失 | `agent.py:1649-1657` | handoff_prompt加入`summary_response` + flow-state继续提示 |
| Handoff flow-state引导 | `agent.py:1649-1657` | 末尾加"请仔细检查交接信息中提到的流程进度" |
| check_35/36 schema_violation | `checker_execute.py:729-748, 821-840` | `main_characters`缺失时返回skip+schema_violation标记 |
| check_35/36 类型检查 | `checker_execute.py:729, 829` | 新增`isinstance(characters_data, dict)`防止list类型崩溃 |
| file_whitelist_check实现 | `checker_execute.py:2652` | `_check_file_whitelist()`方法实现 |
| checker增量模式 | `checker.py` | 新增`--existing-result`和`--only-checks`参数 |
| DSV2 BusinessRules | `design_v2/BusinessRules.md` | 恢复schema reading为阶段3前置要求 |
| REVISION_LOG | `check_definitions/check_revisions/REVISION_LOG.yaml` | 补充rev_004变更3 |
| rev003→rev004转换 | `scripts/convert_rev003_to_rev004.py` | 新脚本，完成DSV1全部目录转换 |

## 附录B：当前评测样本完成度（截至2026-02-13）

| 版本 | 模型 | 完成/目标 | rev004 | 缺失样本 |
|------|------|----------|--------|---------|
| DSV1 | Claude 4.5 | 10/14 | 8/8 | 4 re-running |
| DSV1 | Ernie-5.0 | 9/14 | 8/8 | 5 re-running |
| DSV1 | Gemini | 11/14 | 8/8 | 3 re-running |
| DSV1 | EB5-midtrain | **14/14** | **14/14** | — |
| DSV1 | kimi-k2.5 | **14/14** | **14/14** | — |
| DSV1 | glm-4.7 | 3/14 | 3/3 | 11 re-running |
| DSV2 | kimi-171439 | 8/10 | 8/8 | 2 re-running |
| DSV2 | Ernie-5.0 | 6/10 | 6/6 | 4 re-running |
| DSV2 | Claude 4.5 | 6/10 | 6/6 | 4 re-running |
| DSV2 | kimi-131949 | **10/10** | **10/10** | — |
| DSV2 | EB5-midtrain | 7/10 | 7/7 | 3 re-running |
| DSV2 | Claude 4.6 | 7/10 | 7/7 | 3 re-running |
| DSV2 | Gemini | **10/10** | **10/10** | — |
| DSV2 | glm-4.7 | 3/10 | 3/3 | 7 re-running |
| DSV1 | qwen3-max | 1/14 | 0 | 新模型，运行中 |
| DSV2 | qwen3-max | 0/10 | 0 | 新模型，运行中 |
