# DSV1 vs DSV2 Context Engineering 收益分析报告

> **2026-02-18 | rev008 统一度量 | 8 模型 × 11 共有 task | 排除 EB5 后 7 模型 65 组有效配对**
>
> 分析口径：仅分析 DSV1 和 DSV2 共有的 11 个 task（4 MEDIUM + 2 SHORT + 5 ULTRA_SHORT）上的配对数据。不涉及全量均值或非共有 task。
>
> rev008 变更：(1) sop_stage_coverage → chapter_output_existence（仅检查章节文件是否存在）; (2) 新增 character_naming_quality（角色命名质量 LLM 评审，**仅展示不计分**）; (3) 删除 workspace_file_compliance（噪音过大）

---

## Executive Summary

```
┌──────────────────────────────────────────────────────────────────────┐
│  Context Engineering 有效吗？—— 取决于模型能力                       │
│                                                                      │
│  核心发现：不同模型对 context engineering 的收益差异，               │
│  本身就是模型能力的试金石。                                          │
│                                                                      │
│  ● 强模型（claude×2 + gemini）：                                     │
│    Δcontent=+2.7, Δprocess=+14.7 —— 全面受益，能读懂并用好方法论   │
│  ● 中等偏上（doubao, kimi）：                                        │
│    内容正向（+5.4, +6.5），但流程收益分化                            │
│  ● 中等偏下（qwen3, ernie）：                                        │
│    ernie -15.3，qwen3 -10.4 —— 更复杂的场景设计反而拖累弱模型      │
│                                                                      │
│  全模型均值（Δtotal=+1.4, Δcontent=-0.8）因 ernie 大幅负向失真，   │
│  分层看才有意义。胜率 62%（40/65），6/7 模型总分正向。               │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 一、分析设计

> **一句话**：在 11 个共有 task 上做严格配对对比，控制 query、模型、checker 版本，仅改变场景设计版本（DSV1 vs DSV2）。

### 实验设计

- **自变量**：场景设计版本（DSV1 vs DSV2）
- **控制变量**：同模型、同 query 文本、同 checker（rev008）
- **因变量**：total_score = content×0.7 + process×0.3
- **11 个共有 task**：4 MEDIUM（含 IP）+ 2 SHORT + 5 ULTRA_SHORT
- **模型**：8 个模型。EB5-midtrain 因 gate fail 率 83%（5/6 配对至少一方 gate fail）自动排除出汇总，有效模型 7 个
- **配对数**：kimi/EB5 各 6 对（缺 DSV2 ultra_short），qwen3 6 对（缺 5 个），ernie 9 对（2 个 error 样本被排除），其余 11 对。排除 EB5 后共 65 组有效配对

### 术语：gate_triggered 与 execution_status=error

这是两个独立的概念，不要混淆：

- **gate_triggered**：Agent **跑完了**，但产出物质量触底。内容质量评分采用三层结构：Gate 层（底线）→ Basic 层 → Advanced 层。**Gate 层包含 4 个"一票否决"检查项**（chapter_output_existence、chapter_cloning、alternating_repetition、chapter_completion），任一 fail 则 `gate_triggered=True`，内容分被严重扣减（通常归零或接近零）。常见原因：Agent 不调用 write_file 工具（EB5）、SOP 阶段遗漏（qwen3/doubao）、看到用户 STOP 信号后自行停止（ernie）。这些都是 **Agent 能力问题**。
- **execution_status=error**：Agent **没跑完**，通常是 API 报错、proxy 超时等**外部系统问题**。这类样本不该进入分析。提取脚本已自动过滤（`error` 且工作目录中无 chapter 文件的样本跳过；有 chapter 文件的 error 样本保留，因其在超时前已产出实质内容）。

### 两种分析口径

| 口径                      | 含义                                                            | 适用场景                                              |
| ------------------------- | --------------------------------------------------------------- | ----------------------------------------------------- |
| **含 gate**（默认） | 包含所有配对，gate_triggered 样本以实际得分（通常极低）参与计算 | 反映真实全面表现（包含 Agent 能力不足导致的触底）     |
| **排 gate**         | 排除任一方 gate_triggered=True 的配对                           | 排除 Agent 能力触底的噪声，反映"正常完成时"的质量差异 |

---

## 二、配对汇总

> **一句话**：6/7 模型 DSV2 总分正向，收益高度分层——强模型全面受益（Δcontent=+2.7），中等模型分化严重（ernie -15.3 vs doubao +5.4），全模型均值被 ernie 拉偏，分层看更有意义。

### 2.1 含 gate 版（全配对）

| 模型           | 梯队 | n  | Δ总分         | Δ内容         | Δ流程          |
| -------------- | ---- | -- | -------------- | -------------- | --------------- |
| gemini-3-pro   | 强   | 11 | **+6.7** | **+4.3** | **+12.2** |
| claude-4.5     | 强   | 11 | **+6.4** | **+3.6** | **+12.9** |
| claude-4.6     | 强   | 11 | **+5.9** | +0.3           | **+18.9** |
| doubao-2.0-pro | 中   | 11 | **+3.4** | **+5.4** | -1.2            |
| qwen3-max      | 中   | 6  | **+2.9** | -10.4          | **+34.1** |
| kimi-k2.5      | 中   | 6  | +1.7           | **+6.5** | -9.5            |
| ernie-5.0      | 中   | 9  | -16.9          | -15.3          | **-20.5** |
| EB5-midtrain   | 弱   | 6  | +8.0 ⚠️      | +11.5          | -0.4            |

> 排 EB5 后 7 模型均值：**Δtotal=+1.4, Δcontent=-0.8, Δprocess=+6.7**
> 内容正向模型：5/7（gemini +4.3, kimi +6.5, doubao +5.4, claude-4.5 +3.6, claude-4.6 +0.3）
> Δcontent 均值为负主要因 ernie -15.3 拉低；排除 ernie 后 6 模型均值 +1.6

```
                    配对 Δ 总分（DSV2 - DSV1）
           -20   -15   -10    -5     0    +5   +10
             ├─────┼─────┼─────┼─────┼─────┼─────┤
gemini  (11) ·····································████████████▓    +6.7
claude45(11) ·····································████████████▓    +6.4
claude46(11) ·····································██████████▓      +5.9
doubao  (11) ·····································██████▓           +3.4
qwen3    (6) ·····································█████▓            +2.9
kimi     (6) ·····································███▓              +1.7
ernie    (9) ··████████████████████████████▓                      -16.9
             ├─────┼─────┼─────┼─────┼─────┼─────┤
           -20   -15   -10    -5     0    +5   +10

  排 EB5 后均值: +1.4    () 内为配对数
```

### 2.2 排 gate 版（排除 Agent 能力触底的噪声）

仅保留双方均非 gate_triggered 的配对，反映"正常完成时"的质量差异。

**n 的含义**：`总配对数 - gate排除数 = 有效配对数`。例如 ernie 有 9 组配对，其中 2 组至少一方 gate crash，排除后剩 7 组有效数据。

| 模型           | 梯队 | 总配对 | gate排除 | **有效n** | Δ总分                   | Δ内容         | Δ流程          |
| -------------- | ---- | ------ | -------- | --------------- | ------------------------ | -------------- | --------------- |
| gemini-3-pro   | 强   | 11     | 0        | **11**    | **+6.7**           | **+4.3** | **+12.2** |
| claude-4.5     | 强   | 11     | 0        | **11**    | **+6.4**           | **+3.6** | **+12.9** |
| claude-4.6     | 强   | 11     | 0        | **11**    | **+5.9**           | +0.3           | **+18.9** |
| doubao-2.0-pro | 中   | 11     | 0        | **11**    | **+3.4**           | **+5.4** | -1.2            |
| kimi-k2.5      | 中   | 6      | 0        | **6**     | +1.7                     | **+6.5** | -9.5            |
| qwen3-max      | 中   | 6      | 2        | **4**     | +1.5                     | -12.6          | **+34.6** |
| ernie-5.0      | 中   | 9      | 2        | **7**     | **-9.8**           | -8.9           | **-12.0** |
| EB5-midtrain   | 弱   | 6      | 5        | **1**     | ⚠️ 仅1对，不具统计意义 |                |                 |

> 排 EB5 后 7 模型均值（简单平均）：**Δtotal=+2.3, Δcontent=-0.2**
>
> 5/7 模型 Δcontent 正向。排 gate 后两个关键变化：
>
> - doubao 排 gate 后 Δcontent=+5.4（0 gate 排除，两种口径一致）
 > - ernie 从含gate -15.3 收窄至排gate **-8.9**（排除 gate crash 后负向差异略有收窄）
>
> **EB5 为什么排除**：6 组配对中 5 组至少一方 gate fail（83%），仅剩 1 对 clean 数据（SHORT_SWEET_001），无统计意义。根因是模型不会用 write_file 工具（详见附录 B）。

### 2.3 两种口径对比的启示

| 模型                            | Δcontent 含gate | Δcontent 排gate | 差异原因                           |
| ------------------------------- | ---------------- | ---------------- | ---------------------------------- |
| claude×2, gemini, doubao, kimi | 不变             | 不变             | 0 gate 排除，两种口径完全一致      |
| ernie                           | -15.3            | **-8.9**   | 2 个 gate 配对拉低了含gate均值 |
| qwen3                           | -10.4            | -12.6            | 2 个 gate 配对略缓解了负向差异     |

**ernie 是最值得注意的分化**：含 gate -15.3（大幅负向），排 gate 后收窄为 -8.9。ernie 在正常完成的 task 上，DSV2 内容质量确实不如 DSV1，且流程分也 -12.0。

---

## 三、按篇幅分层

> **一句话**：三种篇幅的内容均值均接近零或轻微负向（MEDIUM -1.9, SHORT -1.0, ULTRA_SHORT +0.7），ernie 大幅负向拉低各分组。排除 ernie 后强模型在三种篇幅上均为内容正向。

### 3.1 各篇幅 × 各模型 Δcontent

| 模型           | MEDIUM (4t)     | SHORT (2t)     | ULTRA_SHORT (5t) |
| -------------- | --------------- | -------------- | ---------------- |
| claude-4.6     | **+2.6**  | +0.1           | -1.5             |
| claude-4.5     | +0.9            | **+10.0** | **+3.2**   |
| gemini-3-pro   | **+2.1**  | **+7.6** | **+4.7**   |
| doubao-2.0-pro | +2.1            | -1.5           | **+10.8**  |
| kimi-k2.5      | **+12.7** | -5.8           | — (n=0)         |
| qwen3-max      | -9.9            | -11.5          | — (n=0)         |
| ernie-5.0      | -23.9           | -5.8           | -13.7            |

### 3.2 篇幅分组汇总（排 EB5 后 7 模型）

| 篇幅                  | tasks | Δcontent 均值 | 正/负 | Δtotal 均值   | 正/负 |
| --------------------- | ----- | -------------- | ----- | -------------- | ----- |
| **MEDIUM**      | 4     | -1.9           | 5/2   | -0.5           | 6/1   |
| **SHORT**       | 2     | -1.0           | 3/4   | -0.2           | 3/4   |
| **ULTRA_SHORT** | 5     | +0.7           | 3/2   | +3.8           | 4/1   |

### 3.3 篇幅分析

**MEDIUM（4 task，含 IP）**：内容均值为负（Δcontent=-1.9），主要因 ernie -23.9 极端拉低（ernie 仅 3 对 MEDIUM 配对，排除的 2 个 error 样本中 1 个是 MEDIUM）。排 ernie 后 6 模型均值 +1.8（5/1 正向），kimi +12.7 提升最大，claude-4.6 +2.6 和 gemini/doubao +2.1 也有实质性改善。

**SHORT（2 task）**：轻微负向（Δcontent=-1.0）。3/7 模型内容正向。claude-4.5 +10.0 是最突出的正向，但 ernie/kimi/qwen3 均为负向。短篇创作复杂度有限，DSV2 的 context engineering 发挥空间较小。

**ULTRA_SHORT（5 task）**：轻微正向（Δcontent=+0.7，3/5 有数据模型内容正向）。doubao +10.8 内容分提升突出，gemini +4.7、claude-4.5 +3.2 也正向；但 ernie -13.7 大幅拉低均值。DSV2 的 skill 文件和角色设计指南对多数模型有效。

---

## 三b、篇幅达标率（range_constraint）

> **一句话**：篇幅达标率整体很低（DSV1 20.9%，DSV2 28.6%），DSV2 略有改善但 SHORT 篇幅反而恶化。

### 配对口径（排 EB5 后 7 模型 × 11 task）

| 模型           | v1达标 | v1总 | v1率  | v2达标 | v2总 | v2率  | Δ(pp)          |
| -------------- | ------ | ---- | ----- | ------ | ---- | ----- | --------------- |
| claude-4.5     | 3      | 11   | 27.3% | 6      | 11   | 54.5% | **+27.3** |
| claude-4.6     | 1      | 11   | 9.1%  | 3      | 11   | 27.3% | **+18.2** |
| gemini-3-pro   | 3      | 11   | 27.3% | 5      | 11   | 45.5% | **+18.2** |
| doubao-2.0-pro | 3      | 11   | 27.3% | 4      | 11   | 36.4% | +9.1            |
| kimi-k2.5      | 1      | 6    | 16.7% | 0      | 6    | 0.0%  | -16.7           |
| ernie-5.0      | 3      | 9    | 33.3% | 0      | 6    | 0.0%  | -33.3           |
| qwen3-max      | 0      | 6    | 0.0%  | 0      | 6    | 0.0%  | 0.0             |

### 按长度分组（排 gate fail 模型）

| 篇幅        | v1达标率 | v2达标率 | Δ(pp)          |
| ----------- | -------- | -------- | --------------- |
| MEDIUM      | 7.4%     | 18.5%    | **+11.1** |
| SHORT       | 28.6%    | 7.1%     | -21.4           |
| ULTRA_SHORT | 33.3%    | 57.1%    | **+23.8** |

> 强模型（claude×2 + gemini）在 DSV2 上篇幅达标率显著提升（+18~27pp）。但整体达标率仍然很低，说明大多数模型在篇幅控制上存在系统性困难。ULTRA_SHORT 达标率最高且提升最大，MEDIUM 次之，SHORT 反而恶化。

---

## 四、收益拆解：内容 vs 流程

> **一句话**：强模型内容和流程双涨（Δcontent=+2.7, Δprocess=+14.7）。全模型均值 Δcontent=-0.8 由 ernie/qwen3 拉低，分层看收益结构更清晰。

### 含 gate 版（7 模型均值）

| 维度           | Δ均值         | 正/负 | 说明                                 |
| -------------- | -------------- | ----- | ------------------------------------ |
| **总分** | **+1.4** | 6/1   | ernie 唯一负向                       |
| **内容** | -0.8           | 5/2   | ernie -15.3 和 qwen3 -10.4 拉低均值 |
| **流程** | +6.7           | 4/3   | 分化大（qwen3 +34.1 vs ernie -20.5） |

### 强模型（claude×2 + gemini）配对均值

| 维度 | Δ均值          | 说明                                          |
| ---- | --------------- | --------------------------------------------- |
| 总分 | **+6.3**  | 三个模型均正向                                |
| 内容 | **+2.7**  | gemini +4.3, claude-4.5 +3.6, claude-4.6 +0.3 |
| 流程 | **+14.7** | 三个模型均大幅正向                            |

---

## 五、检查项级变化分析

> 65 组有效配对（7 模型 × 11 共有 task，排除 EB5），按 subcategory_id 统计各检查项的 fail 率变化。
> 仅列出 |Δ| ≥ 5pp 的检查项。注：同一 subcategory 可能包含多个 check item，n 值反映 check item 总数而非样本数。

**content_quality 维度**：

```
  检查项                            DSV1 fail率    DSV2 fail率    变化
  ─────────────────────────────────────────────────────────────────────
  改善 ↓
  character_presence_in_outline     65.0%          23.6%         -41.4pp ✓✓
  character_presence_in_chapters    48.3%          33.3%         -15.0pp ✓✓
  dialogue_character_distinction    84.6%          71.0%         -13.6pp ✓
  genre_fit                         58.5%          46.8%         -11.7pp ✓
  narrative_density                 38.5%          27.4%         -11.0pp ✓
  late_stage_digression             26.2%          21.0%          -5.2pp ✓
  pacing_rationality_advanced       30.8%          25.8%          -5.0pp ✓
  ─────────────────────────────────────────────────────────────────────
  恶化 ↑
  character_design_adherence         9.2%          21.0%         +11.7pp ⚠（详见 §5.3）
  paragraph_repetition               1.5%           8.1%          +6.5pp ⚠
  repeated_endings                   6.2%          10.8%          +4.6pp
  ─────────────────────────────────────────────────────────────────────
  无差异
  character_naming_quality（仅展示） 76.9%          76.9%          0.0pp  ←不计分
```

**business_rule / memory / process 维度**：

```
  检查项                            DSV1 fail率    DSV2 fail率    变化
  ─────────────────────────────────────────────────────────────────────
  改善 ↓
  required_skill_reading            45.0%          10.1%         -34.8pp ✓✓
  log_file_usage                    68.3%          36.6%         -31.7pp ✓✓
  sop_compliance                    33.3%           6.1%         -27.2pp ✓✓
  log_file_creation                 23.3%           9.8%         -13.6pp ✓
  hook_design                       13.9%           6.5%          -7.4pp ✓
  range_constraint                  78.5%          71.0%          -7.5pp ✓
  semantic_redundancy               61.5%          54.8%          -6.7pp ✓
  language_purity                   13.9%           9.7%          -4.2pp
  ─────────────────────────────────────────────────────────────────────
  恶化 ↑
  quantity_constraint                1.6%          18.6%         +17.0pp ✗
  enum_validity                      3.2%          17.7%         +14.6pp ✗
```

### 5.1 角色管理维度的显著改善

角色规划和落地相关的检查项是 DSV2 收益最突出的维度：

| 检查项                                   | 含义                 | DSV1 fail率 | DSV2 fail率 | Δ                         |
| ---------------------------------------- | -------------------- | ----------- | ----------- | -------------------------- |
| **character_presence_in_outline**  | 角色是否在大纲中规划 | 65.0%       | 23.6%       | **-41.4pp 大幅改善** |
| **character_presence_in_chapters** | 角色是否在正文出现   | 48.3%       | 33.3%       | **-15.0pp 改善**     |
| **chapter_length_stability**       | 后期章节不萎缩       | 已单独统计  |             | 无显著差异                 |

**character_presence_in_outline -41.4pp** 是所有检查项中变化最大的。这说明 DSV2 的角色设计指南显著提升了"角色规划→大纲落地"的完整性——DSV1 中 65% 的样本存在"设计了角色但大纲中没有规划"的问题，DSV2 降至 23.6%。

### 5.2 逻辑类检查项的实际变化

rev007+ 将旧的 `logical_contradiction` 拆分为 `structural_logic_defect` + `fixable_logic_inconsistency`。配对口径下：

| 检查项                                | 含义                     | DSV1 fail率 | DSV2 fail率 | Δ                    |
| ------------------------------------- | ------------------------ | ----------- | ----------- | --------------------- |
| **structural_logic_defect**     | 情节逻辑断裂、世界观矛盾 | 49.2%       | 46.2%       | **-3.1pp 改善** |
| **fixable_logic_inconsistency** | 可修复的小逻辑不一致     | 92.3%       | 90.8%       | -1.5pp 天花板效应     |

**结论**：在配对 11 task 口径下，结构性逻辑硬伤实际上轻微改善（-3.1pp），而非恶化。fixable_logic_inconsistency 仍处于 ~91% 的天花板区间，无实质差异。

### 5.3 character_design_adherence 恶化的根因

**+11.7pp 恶化是真实的。** 根因是 DSV2 通过 `CHARACTER_DESIGN_GUIDE.md` 抬高了 Plan（characters.json）质量标杆，但模型在多章节执行中无法贯彻这些更高标准——**Plan→Execute 对齐鸿沟被放大**。

模型间分化明显：claude-4.5 +18.2pp、ernie +35.1pp（恶化最严重），而 claude-4.6 和 kimi 保持 0pp 不变。强模型（claude-4.6）能同时设计好角色并执行到位，中等模型则容易"设计得出但写不出"。

### 5.4 角色命名质量（新增，仅展示不计分）

rev008 新增的 `character_naming_quality` 检查（LLM 评审），设为 **DISPLAY_ONLY**（不参与评分）：

- DSV1 fail 率：76.9%
- DSV2 fail 率：76.9%
- **零差异**：DSV2 的角色设计指南对命名质量没有产生影响

不计分原因：76.9% 的 fail 率说明这是一个"优秀级"标准，大多数模型达不到，但 binary pass/fail 无法反映中等水平的质量改善。

### 5.5 流程合规的改善与新增代价

DSV2 在流程维度的改善非常显著：

- **required_skill_reading**：-34.8pp，DSV2 的分阶段 skill 文件设计让模型更容易找到并阅读指导材料
- **sop_compliance**：-27.2pp，结构化的 SOP 规范显著降低了流程违规
- **log_file_usage/creation**：-31.7pp/-13.6pp，DSV2 的日志规范被更多模型遵循

但 DSV2 结构更复杂也带来了新的合规代价：

- **quantity_constraint**：+17.0pp，更复杂的结构→更多数量约束→更容易违反
- **enum_validity**：+14.6pp，更多枚举字段→更多出错机会

---

## 六、强模型专题分析

> **一句话**：DSV2 对强模型（claude-4.6, claude-4.5, gemini-3-pro）的收益最清晰——33 组配对 0 gate 排除，内容和流程双涨。本节拆解收益到篇幅和检查项维度，定位后续优化方向。

### 6.1 概览

| 模型           | n            | Δ总分         | Δ内容         | Δ流程          | 胜率                | 内容range     |
| -------------- | ------------ | -------------- | -------------- | --------------- | ------------------- | ------------- |
| gemini-3-pro   | 11           | **+6.7** | **+4.3** | +12.2           | 7/11                | -8.0 ~ +23.2  |
| claude-4.5     | 11           | **+6.4** | +3.6           | +12.9           | 8/11                | -16.0 ~ +27.2 |
| claude-4.6     | 11           | **+5.9** | +0.3           | +18.9           | **9/11**      | -7.8 ~ +11.1  |
| **均值** | **33** | **+6.3** | **+2.7** | **+14.7** | **24/33=73%** |               |

三个模型均 0 gate 排除，含 gate 和排 gate 口径完全一致。claude-4.6 胜率最高（9/11），gemini 内容分提升最大（+4.3）。

### 6.2 篇幅分层

| 篇幅                  | 配对数 | Δ内容         | Δ流程          | Δ总分          |
| --------------------- | ------ | -------------- | --------------- | --------------- |
| **MEDIUM**      | 12     | **+1.9** | +5.5            | +3.0            |
| **SHORT**       | 6      | **+5.9** | -4.8            | +2.7            |
| **ULTRA_SHORT** | 15     | **+2.1** | **+29.8** | **+10.4** |

关键发现：

- **三种篇幅的内容分提升方向一致**（+1.9 ~ +5.9），说明 DSV2 对强模型的内容质量提升**不依赖特定篇幅**
- **流程分的篇幅差异巨大**：ULTRA_SHORT +29.8，MEDIUM +5.5，SHORT -4.8。ULTRA_SHORT 的流程大涨主要来自 required_skill_reading 和 sop_compliance 的改善
- SHORT 流程分 -4.8 是因为 log_file_usage 恶化（+33.3pp），但内容分仍然正向

### 6.3 检查项级收益拆解

> 以下为强模型 33 组配对的 fail 率变化。仅列 |Δ|≥5pp 的项。

**内容维度收益**：

```
  检查项                            DSV1 fail率    DSV2 fail率    变化
  ──────────────────────────────────────────────────────────────────
  改善 ↓
  ★ character_presence_in_outline     62.5%          27.3%       -35.2pp
  ★ narrative_density                 21.2%           3.0%       -18.2pp
  ★ genre_fit                         30.3%          18.2%       -12.1pp
    dialogue_character_distinction    69.7%          57.6%       -12.1pp
    outline_execution_fidelity        36.4%          27.3%        -9.1pp
    pacing_rationality_advanced       12.1%           3.0%        -9.1pp
    fixable_logic_inconsistency       93.9%          87.9%        -6.1pp
    emotional_delivery_match          12.1%           6.1%        -6.1pp
```

- **narrative_density（叙事密度）**：-18.2pp，DSV2 的写作技巧指南（Show vs Tell、感官描写）对强模型效果显著
- **fixable_logic_inconsistency（可修复瑕疵）**：-6.1pp，强模型能消化指导并减少瑕疵
- **pacing_rationality_advanced（剧情节奏）**：-9.1pp，强模型在节奏把控上能从规范中获益

**流程维度收益**：

```
  检查项                            DSV1 fail率    DSV2 fail率    变化
  ──────────────────────────────────────────────────────────────────
  改善 ↓
  ★ required_skill_reading            55.3%           3.2%       -52.1pp
  ★ sop_compliance                    45.5%           2.8%       -42.7pp
    log_file_usage                    69.7%          44.4%       -25.3pp
  ★ range_constraint（篇幅）          78.8%          57.6%       -21.2pp
```

- **required_skill_reading -52.1pp**：强模型在 DSV2 中几乎做到了 100% 读取所有 skill 文件（fail 仅 3.2%）
- **sop_compliance -42.7pp**：强模型对结构化 SOP 的遵从度接近完美
- **range_constraint -21.2pp**：强模型在篇幅控制上从 DSV2 获益显著

**恶化项**（DSV2 对强模型的代价）：

```
  检查项                            DSV1 fail率    DSV2 fail率    变化
  ──────────────────────────────────────────────────────────────────
  恶化 ↑
  ⚠ repeated_endings                  18.2%          24.2%        +6.1pp
  ⚠ character_design_adherence         3.0%          12.1%        +9.1pp
    structural_logic_defect           36.4%          42.4%        +6.1pp
    quantity_constraint                3.0%           4.5%        +1.5pp
    enum_validity                      3.0%           3.0%         0.0pp
```

- **repeated_endings +6.1pp**：DSV2 的 SOP 规范可能导致模型在写不动时更频繁地输出结局标记后又硬续。主要集中在 ernie 模型
- **character_design_adherence +9.1pp**：Plan→Execute 鸿沟——DSV2 抬高了角色设计标准但执行中无法贯彻
- **structural_logic_defect +6.1pp**：DSV2 鼓励更复杂的情节结构，强模型尝试了更复杂的布局但增加了逻辑矛盾的风险
- **quantity_constraint / enum_validity**：强模型几乎不受影响（+1.5pp / 0pp）

### 6.4 强模型 DSV2 的剩余短板

> 强模型在 DSV2 上仍然 fail 率 ≥20% 的检查项，指向后续优化方向。

| 检查项                         | DSV2 fail率     | DSV1→DSV2 | 优化方向                                                      |
| ------------------------------ | --------------- | ---------- | ------------------------------------------------------------- |
| fixable_logic_inconsistency    | **90.9%** | -6.1pp     | 天花板效应，几乎所有小说都有小瑕疵                            |
| character_naming_quality       | 60.0%           | (不计分)   | AI 命名倾向，prompt 难改变                                    |
| range_constraint（篇幅）       | **56.8%** | -21.2pp    | 已改善但仍过半不达标，需更强的篇幅控制机制                    |
| dialogue_character_distinction | **50.0%** | -12.1pp    | 角色语言辨识度仍是瓶颈，可强化命名指南中的语言风格差异        |
| structural_logic_defect        | **47.7%** | +6.1pp     | **恶化项**，需关注——DSV2 鼓励复杂结构但增加了逻辑风险 |
| semantic_redundancy            | **40.9%** | 0pp        | 强模型无变化，需要专门的反重复指导                            |
| narrative_tone_match           | 38.6%           | +5.3pp     | 轻微恶化，可在 skill 中增加调性匹配示例                       |
| outline_execution_fidelity     | 36.4%           | -9.1pp     | 改善中但仍较高，大纲→正文的执行鸿沟                          |
| character_presence_in_chapters | 36.4%           | -1.3pp     | 角色出场，强模型无显著变化                                    |
| repeated_endings               | **24.2%** | +6.1pp     | DSV2 的 SOP 完结阶段仍有优化空间                        |

### 6.5 按篇幅的检查项变化

**MEDIUM（12 配对）**——收益最集中的检查项：

| 检查项                        | Δ                | 说明                                  |
| ----------------------------- | ----------------- | ------------------------------------- |
| character_presence_in_outline | **-58.3pp** | 91.7%→33.3%，中篇改善最大            |
| narrative_density             | **-33.3pp** | 33.3%→0%，中篇叙事密度问题被完全解决 |
| range_constraint              | **-33.3pp** | 91.7%→58.3%，中篇篇幅控制大幅改善    |
| late_stage_digression         | **-25.0pp** | 后期跑偏问题显著减少                  |
| repeated_endings              | +8.3pp            | 中篇有轻微恶化                         |
| character_design_adherence    | +16.7pp           | ⚠ 中篇的 Plan→Execute 鸿沟最大      |

**ULTRA_SHORT（15 配对）**——改善最均匀：

| 检查项                         | Δ                | 说明                           |
| ------------------------------ | ----------------- | ------------------------------ |
| character_presence_in_outline  | **-33.3pp** | 短篇也有大幅改善               |
| dialogue_character_distinction | **-26.7pp** | 角色语言辨识度在短篇上改善最大 |
| range_constraint               | **-26.7pp** | 短篇篇幅控制改善               |
| genre_fit                      | **-20.0pp** | 题材契合度改善                 |
| late_stage_digression          | +13.3pp           | ⚠ 短篇后期跑偏有恶化          |

**SHORT（6 配对）**——信号混杂：

SHORT 仅 6 组配对，部分检查项出现大幅波动（如 character_presence_in_chapters +46.7pp、log_file_usage +33.3pp），但样本量太小，不宜过度解读。内容分 +5.9 表明整体仍然正向。

### 6.6 后续优化建议（基于强模型数据）

| 优先级       | 优化方向                                 | 依据                                                                 | 预期收益                                        |
| ------------ | ---------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------- |
| **P1** | **repeated_endings 优化**          | 强模型 +6.1pp，仍有轻微恶化                                                 | 优化 SOP 完结阶段设计可进一步改善               |
| **P0** | **range_constraint 增强**          | 仍有 56.8% fail，但已证明可改善（-21.2pp），篇幅控制机制有效但不够强 | 强模型可能再提 10-15pp                          |
| **P1** | **semantic_redundancy 专项指导**   | 40.9% fail，DSV1→DSV2 零变化，现有 skill 文件没有覆盖               | 新增反重复 skill 可能带来改善                   |
| **P1** | **structural_logic_defect 防护**   | 强模型独有恶化 +6.1pp，DSV2 鼓励复杂结构但增加逻辑风险               | 在 OUTLINE_DESIGN_GUIDE 中增加逻辑自检步骤      |
| **P2** | **dialogue_character_distinction** | 50% fail，改善中（-12.1pp）但仍是瓶颈                                | 在角色设计指南中增加语言风格差异化要求          |
| **P2** | **narrative_tone_match 调性示例**  | 轻微恶化 +5.3pp                                                      | 在 WRITING_TECHNIQUE_GUIDE 中增加调性匹配正反例 |

---

## 七、模型分层分析

> 分层标准：DSV1 总分 ≥75 为强，≥50 为中，<50 为弱。
> 以下所有数据均基于 11 个共有 task 的配对。

### 7.1 强模型（claude-4.6=82.8, gemini=78.0, claude-4.5=75.1）

**配对 Δtotal +5.9 ~ +6.7，内容和流程均正向。**

| 模型         | Δ内容         | Δ流程          | Δ总分         | n  |
| ------------ | -------------- | --------------- | -------------- | -- |
| gemini-3-pro | **+4.3** | **+12.2** | **+6.7** | 11 |
| claude-4.5   | **+3.6** | **+12.9** | **+6.4** | 11 |
| claude-4.6   | +0.3           | **+18.9** | **+5.9** | 11 |

强模型 0 gate 排除，两种口径完全一致。总分提升来自内容和流程的双重贡献（Δcontent=+2.7，Δprocess=+14.7）。

### 7.2 中等模型（doubao=72.0, kimi=64.9, qwen3=65.0, ernie=49.5）

| 模型   | Δ总分         | Δ内容(含gate) | Δ内容(排gate)       | 模式                                                   |
| ------ | -------------- | -------------- | -------------------- | ------------------------------------------------------ |
| kimi   | +1.7           | **+6.5** | +6.5 (n=6)           | "内容受益者"：MEDIUM 上 +12.7                          |
| doubao | **+3.4** | **+5.4** | +5.4 (n=11)          | 内容和流程双涨（0 gate 排除）                          |
| qwen3  | **+2.9** | -10.4          | -12.6 (n=4)          | "流程受益者"：内容下降，流程 +34.1                     |
| ernie  | -16.9          | -15.3          | **-8.9** (n=7) | 大幅负向；正常完成的 task 上也显著更差                 |

中等模型分化严重，这本身就是模型能力差异的体现——doubao/kimi 能从更丰富的 context 中提取有用信息转化为更好的内容，而 qwen3/ernie 面对更复杂的约束反而更容易出错。**"读了方法论不等于会用"**——qwen3 skill 读取率 94% 但内容分排 gate 后 -12.6，ernie 即便正常完成（排 gate）内容仍 -8.9。

### 7.3 弱模型（EB5-midtrain=46.5）

6 组配对中 5 组至少一方 gate fail（83%），已自动排除出汇总。根因是模型能力不足——不会用 write_file 工具。

---

## 八、结论

### Context Engineering 有效吗？

**取决于模型能力。Context engineering 放大而非弥补能力差距——强模型全面受益，弱模型反而被拖累。**

```
  层级            11-task 配对数据
  ──────────────────────────────────────────────────────
  强模型(3)       Δcontent=+2.7, Δprocess=+14.7, 胜率 100%
  中等偏上(2)     doubao +5.4, kimi +6.5（内容正向，流程分化）
  中等偏下(2)     qwen3 -10.4, ernie -15.3（内容均负向）
  全模型均值(7)   Δtotal=+1.4, Δcontent=-0.8, Δprocess=+6.7
                  胜率 62%（40/65），但被 ernie 大幅拉偏
  ULTRA_SHORT     Δtotal=+3.8, 收益最集中的篇幅
  MEDIUM          Δcontent=-1.9（5/7 正向，ernie -23.9 拉低）
  篇幅达标率      强模型 +18~27pp，整体仍低（DSV1 20.9% → DSV2 28.6%）
```

### DSV2 的收益来源

| 收益来源                    | 贡献       | 证据                                                                         |
| --------------------------- | ---------- | ---------------------------------------------------------------------------- |
| **角色规划完整性**    | ★★★★★ | character_presence_in_outline**-41.4pp**，最大单项改善                 |
| **分阶段 Skill 文件** | ★★★★★ | required_skill_reading -34.8pp，模型读取率从 55% 升至 90%                    |
| **结构化 SOP 规范**   | ★★★★★ | sop_compliance -27.2pp，流程违规大幅下降                                     |
| **日志管理规范**      | ★★★★☆ | log_file_usage -31.7pp，log_file_creation -13.6pp                            |
| **ULTRA_SHORT 质量**  | ★★★☆☆ | Δtotal=+3.8，最短篇幅下规范指导对多数模型有效                               |
| **角色设计指南**      | ★★★★☆ | dialogue_distinction -13.6pp，genre_fit -11.7pp；但 design_adherence +11.7pp |
| **角色正文出场**      | ★★★☆☆ | character_presence_in_chapters -15.0pp                                       |

### DSV2 的代价

| 代价                               | 严重度 | 备注                               |
| ---------------------------------- | ------ | ---------------------------------- |
| quantity_constraint +17.0pp        | 中     | 结构更复杂→更多数量约束→更易违反 |
| enum_validity +14.6pp              | 中     | 更多枚举字段→更多出错机会         |
| character_design_adherence +11.7pp | 中     | Plan→Execute 对齐鸿沟被放大       |

### rev008 新发现

| 发现                              | 说明                                                              |
| --------------------------------- | ----------------------------------------------------------------- |
| **角色规划完整性 -41.4pp**  | DSV2 的角色设计指南对"角色→大纲"环节有巨大改善                   |
| **角色命名质量 76.9% fail** | DSV1=DSV2 零差异，AI 命名倾向无法通过 prompt 改变（仅展示不计分） |
| **篇幅达标率整体低**        | DSV1 20.9%，DSV2 28.6%，强模型显著改善                            |

### Context Engineering 的适用边界

**本场景的数据揭示了 context engineering 的一个根本性局限：它能规范流程，但无法教 LLM 写好故事。**

小说写作是一项一创（原创）场景——最终交付物的质量取决于模型的创作能力（叙事密度、题材驾驭、角色塑造），而不是流程是否规范。DSV2 能设计出更细致的 SOP（配方选择→大纲设计→分章写作），能强制模型读 skill 文件、写日志、按格式输出，但这些只是让模型"按规矩做事"，无法让它"做出好东西"。

数据印证了这一点：

```
  DSV2 收益分布
  ─────────────────────────────────────
  流程维度   Δprocess = +6.7   ← SOP、skill读取、日志管理大幅改善
  内容维度   Δcontent = -0.8   ← 叙事密度、题材契合、角色辨识度几乎不变
```

context engineering 真正能发挥大作用的场景特征是：**能形成清晰细致的 SOP，且 SOP 越细致，最终交付的内容质量就越高**。典型的例子是结构化的信息处理任务（数据提取、报告生成、客服流程），在这类场景中，流程规范度与交付质量强相关——按步骤做就能做好。

而小说写作恰恰不满足这个条件：SOP 只能确保模型交付出"格式合规、流程完整"的产物，但"好故事、好角色、好节奏"依赖的是模型自身的创作能力，无法通过 prompt 中更精细的步骤指导来获得。这解释了为什么 DSV2 在流程分上大幅领先（+6.7），而内容分几乎持平（-0.8）——**context engineering 的收益天花板，由"SOP细致度能否转化为交付质量"这一条件决定**。

---

<details>
<summary>A. 数据来源与方法</summary>

- **数据提取**：`analysis/extract_rev006_data.py --revision 008`
- **原始数据**：`analysis/rev008_all_data.json`（214 条记录，8 模型）
- **分析脚本**：`analysis/analyze_dsv1_vs_dsv2.py --revision 008`（11 shared tasks 版本）
- **分析输出**：`analysis/dsv1_v2_analysis_output.json`（含 paired_summary / paired_no_gate / length_paired / range_constraint）
- **11 个共有 task**：
  - MEDIUM: NW_CLEAR_MEDIUM_ANGSTY_001, NW_CLEAR_MEDIUM_SUSPENSE_001, NW_CLEAR_MEDIUM_SWEET_001, NW_IP_MEDIUM_NEUTRAL_001
  - SHORT: NW_CLEAR_SHORT_ANGSTY_001, NW_CLEAR_SHORT_SWEET_001
  - ULTRA_SHORT: NW_ULTRA_SHORT_ANGSTY_001 ~ 005
- **配对标准**：sample_id 完全匹配，双方 total_score 非 null
- **配对数**：claude×2/gemini/doubao 各 11 对，ernie 9 对，qwen3 6 对，kimi 6 对，EB5 6 对（排除）
- **评分公式**：total = content×0.7 + process×0.3；content 基准60分公式
- **分层标准**：DSV1 总分 ≥75 为强（3），≥50 为中（4），<50 为弱（1）
- **IP_MEDIUM_NEUTRAL_001 归入 MEDIUM** 长度分组
- **数据清洗**：排除 `execution_status=error` 且工作区无章节文件（`chapter_*.md`）的样本（3 个被排除：claude-4.6 dsv2 HEROINE_001、ernie dsv1 SUSPENSE_001、ernie dsv1 US_ANGSTY_004）；排除无 check_result 的样本
- **rev008 变更**：(1) sop_stage_coverage → chapter_output_existence (2) 新增 character_naming_quality（仅展示不计分） (3) 删除 workspace_file_compliance

</details>

<details>
<summary>B. EB5 排除原因</summary>

EB5-midtrain 的 6 组配对（DSV2 缺 5 个 ultra_short）中 5 组至少一方 gate fail，gate fail 率 83%，超过 50% 阈值。根因是模型能力不足——不会用 write_file 工具，把所有内容以纯文本输出在对话消息里。

</details>

<details>
<summary>C. Gate 触发汇总</summary>

**DSV1**: gate_triggered 约 10%
**DSV2**: gate_triggered 约 12%

| 模型         | DSV1 | DSV2 | 主要故障模式                                                |
| ------------ | ---- | ---- | ----------------------------------------------------------- |
| EB5-midtrain | 6    | 6    | 纯文本输出不使用工具                                        |
| ernie-5.0    | 2    | 2    | 看到 ###STOP### 后自行停止；SOP 遗漏（另有 2 个 DSV1 error 样本已排除） |
| qwen3-max    | 1    | 2    | SOP 部分阶段遗漏                                            |
| doubao-2.0   | 0    | 0    | rev008 修复了 2 个假门控（仅缺 outline.json，章节实际完整） |
| claude-4.6   | 0    | 0    | HEROINE_001 已排除（execution_status=error，无章节文件）    |

> 注：qwen3 US_ANGSTY_001~005（execution_status=error，0 tool calls）已从数据中排除，不计入上表。

</details>

<details>
<summary>D. rev007 → rev008 数值变化说明</summary>

rev008 的变更导致部分数值与 rev007 报告有差异：

1. **chapter_output_existence 替代 sop_stage_coverage**：修复了 doubao 的 2 个假门控（NW_CLEAR_SHORT_ANGSTY_001、NW_ULTRA_SHORT_ANGSTY_003），这些样本写了完整章节但缺 outline.json。修复后 doubao gate fail 数从 2→0。
2. **character_naming_quality 新增（仅展示不计分）**：设为 DISPLAY_ONLY，不参与评分。76.9% fail 率 binary pass/fail 无法反映中等水平改善。
3. **workspace_file_compliance 删除**：该项在 business_rule_compliance 维度，影响流程分。由于 DSV2 fail 率更高（+7.6pp），删除后 DSV2 相对优势略降。

| 指标               | rev007 | rev008 | 变化原因                                                |
| ------------------ | ------ | ------ | ------------------------------------------------------- |
| Δtotal 配对均值   | +4.2   | +1.4   | checker 检查项迭代 + error 样本过滤修正（214 条）        |
| Δcontent 配对均值 | +2.8   | -0.8   | 内容维度检查项调整 + ernie 零章节样本排除后均值翻负      |
| Δprocess 配对均值 | +7.4   | +6.7   | 流程分小幅回落                                          |
| 胜率               | 67%    | 62%    | 65 组配对（原 67 组，排除 3 个零章节 error 样本）        |
| 内容正向模型       | 6/7    | 5/7    | ernie 翻转为负向                                        |

</details>
