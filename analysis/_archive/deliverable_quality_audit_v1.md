# 交付物质量审查报告 v1

> **审查日期**: 2026-02-13
> **审查范围**: 全部16个评估目录(DSV1×7 + DSV2×9)中status=success的样本交付章节
> **审查方法**: 程序化批量扫描 + 人工深度阅读(6个样本精读，10+个样本抽查)

---

## 一、发现的质量问题分类

本轮审查发现五类主要质量问题，按严重程度排序：

1. **章节克隆** (Chapter Cloning) — 灾难级
2. **提前终止** (Early Termination) — 严重
3. **章节长度崩塌** (Length Collapse) — 严重
4. **叙事质量退化** (Narrative Degradation) — 中度
5. **内容逻辑缺陷** (Logic Defects) — 中度

---

## 二、章节克隆 (Chapter Cloning)

### 2.1 定义
模型在生成后期陷入循环，输出内容几乎完全相同的"章节"，仅标题行的章节编号不同。

### 2.2 确认案例

#### 案例1: ernie DSV2 SWEET — 36章完全克隆

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv2_20260211_103353_ernie-5.0-thinking-preview` |
| **样本ID** | `NW_CLEAR_MEDIUM_SWEET_001` |
| **env路径** | `NW_CLEAR_MEDIUM_SWEET_001_env/workspace/chapters/` |
| **总章节数** | 48 |
| **克隆范围** | chapter_13.md — chapter_48.md (36章) |
| **克隆特征** | 所有36章文件大小精确一致: **2207 bytes** |
| **验证方式** | 直接比较文本内容，除第一行标题("chapter_13.mp3" vs "chapter_48.mp3")外完全相同 |
| **克隆内容样本** | "苏野站在平衡木上，这次她没再故意歪肩膀。林昭的平板上，肌肉负荷曲线终于从红色变成了黄色——安全值内……" |

**注意**: 这与之前发现的 ernie DSV1 SWEET_001 (ch13-48 identical) 是完全相同的克隆模式，说明 ernie 在此题材上有系统性的克隆倾向。

#### 案例2: EB5 DSV2 ADVENTURE — 21章近似克隆

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat` |
| **样本ID** | `NW_CLEAR_MEDIUM_ADVENTURE_001` |
| **env路径** | `NW_CLEAR_MEDIUM_ADVENTURE_001_env/workspace/chapters/` |
| **总章节数** | 45 |
| **克隆范围** | chapter_25.md — chapter_45.md (21章) |
| **克隆特征** | 所有21章文件大小几乎一致(1247-1249 bytes)；去掉第一行后前500字节MD5完全相同 |
| **验证方式** | 用 hashlib 对去标题行后的前500字节计算MD5，21章全部一致(hash: a6ec673f) |
| **克隆内容样本** | "清晨的阳光洒在横断山脉的深处，三人沿着来时的路缓缓前行……'我们真的不带走任何东西吗？'沈书白突然停下脚步……" |

#### 案例3: EB5 DSV1 ANGSTY_002 — 交替重复克隆

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat` |
| **样本ID** | `NW_ULTRA_SHORT_ANGSTY_002` |
| **env路径** | `NW_ULTRA_SHORT_ANGSTY_002_env/workspace/chapters/` |
| **总章节数** | 44 |
| **克隆范围** | chapter_25.md — chapter_44.md (20章) |
| **克隆特征** | 交替出现两种大小: **1403 bytes** 和 **1508 bytes**，A-B-A-B-A-B 模式 |
| **验证方式** | 逐文件检查 `wc -c`，奇数章=1403, 偶数章=1508 |

### 2.3 历史已知的克隆案例（前次会话发现）

| 评估目录 | 样本ID | 克隆范围 | 说明 |
|----------|--------|---------|------|
| `eval_dsv1_20260205_140957_ernie-5.0-thinking-preview` | `NW_CLEAR_MEDIUM_SWEET_001` | ch13-48 (36章) | ernie DSV1也是SWEET题材 |
| `eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat` | `NW_CLEAR_MEDIUM_ANGSTY_001` | ch13-48 (36章) | EB5 DSV1, 已知 |

---

## 三、提前终止 (Early Termination)

### 3.1 定义
样本 `execution_status=success`，但交付章节数 ≤ 3。模型在需求对话/大纲设计阶段耗费过多turn后，写了极少章节就输出 `####STOP####` 终止对话。

### 3.2 完整案例清单（26个样本）

| 模型 | 版本 | 评估目录 | 样本ID | 章节数 | turns | tool_calls |
|------|------|----------|--------|--------|-------|------------|
| claude-opus-4-5-20251101 | DSV1 | eval_dsv1_20260205_132400_claude-opus-4-5-20251101 | NW_ULTRA_SHORT_ANGSTY_001 | 3 | 37 | 24 |
| ernie-5.0-thinking-preview | DSV1 | eval_dsv1_20260205_140957_ernie-5.0-thinking-preview | NW_ULTRA_SHORT_ANGSTY_003 | 3 | 37 | 17 |
| ernie-5.0-thinking-preview | DSV2 | eval_dsv2_20260211_103353_ernie-5.0-thinking-preview | NW_CLEAR_MEDIUM_ADVENTURE_001 | 3 | 71 | 16 |
| ernie-5.0-thinking-preview | DSV2 | eval_dsv2_20260211_103353_ernie-5.0-thinking-preview | NW_IP_MEDIUM_NEUTRAL_001 | 0 | 117 | 55 |
| gemini-3-pro-preview | DSV1 | eval_dsv1_20260205_141134_gemini-3-pro-preview | NW_CLEAR_MEDIUM_ANGSTY_001 | 3 | 65 | 33 |
| gemini-3-pro-preview | DSV1 | eval_dsv1_20260205_141134_gemini-3-pro-preview | NW_CLEAR_MEDIUM_SWEET_001 | 2 | 40 | 23 |
| gemini-3-pro-preview | DSV1 | eval_dsv1_20260205_141134_gemini-3-pro-preview | NW_CLEAR_SHORT_SWEET_001 | 1 | 36 | 20 |
| gemini-3-pro-preview | DSV2 | eval_dsv2_20260212_114551_gemini-3-pro-preview | NW_CLEAR_MEDIUM_SUSPENSE_001 | 3 | 64 | 33 |
| gemini-3-pro-preview | DSV2 | eval_dsv2_20260212_114551_gemini-3-pro-preview | NW_CLEAR_SHORT_SWEET_001 | 1 | 54 | 33 |
| glm-4.7 | DSV1 | eval_dsv1_20260212_201213_glm-4.7 | NW_CLEAR_MEDIUM_ANGSTY_001 | 0 | 30 | 14 |
| glm-4.7 | DSV1 | eval_dsv1_20260212_201213_glm-4.7 | NW_ULTRA_SHORT_ANGSTY_004 | 0 | 12 | 2 |
| glm-4.7 | DSV2 | eval_dsv2_20260212_201303_glm-4.7 | NW_CLEAR_SHORT_SWEET_001 | 0 | 39 | 20 |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_CLEAR_MEDIUM_ADVENTURE_001 | 3 | 38 | 20 |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_CLEAR_MEDIUM_SUSPENSE_001 | 3 | 49 | 26 |
| kimi-k2.5 | DSV2 | eval_dsv2_20260211_131949_kimi-k2.5 | NW_CLEAR_MEDIUM_ANGSTY_001 | 3 | 58 | 31 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV1 | eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat | NW_CLEAR_MEDIUM_ANGSTY_001 | 0 | 9 | 1 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV1 | eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat | NW_CLEAR_MEDIUM_SUSPENSE_001 | 0 | 69 | 30 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV1 | eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat | NW_IP_MEDIUM_NEUTRAL_001 | 1 | 39 | 16 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV2 | eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat | NW_CLEAR_MEDIUM_ANGSTY_001 | 0 | 71 | 30 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV2 | eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat | NW_CLEAR_MEDIUM_BRAINY_ACTION_001 | 0 | 45 | 16 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV2 | eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat | NW_CLEAR_MEDIUM_HEROINE_001 | 0 | 57 | 24 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV2 | eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat | NW_CLEAR_MEDIUM_SWEET_001 | 0 | 15 | 4 |
| openai_EB5-0209-A35B-midtrain-128k-chat | DSV2 | eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat | NW_VAGUE_MEDIUM_SWEET_DRAMA_001 | 0 | 13 | 4 |
| qwen3-max-2026-01-23 | DSV1 | eval_dsv1_20260213_143137_qwen3-max-2026-01-23 | NW_CLEAR_MEDIUM_SUSPENSE_001 | 1 | 35 | 16 |
| qwen3-max-2026-01-23 | DSV2 | eval_dsv2_20260213_143908_qwen3-max-2026-01-23 | NW_CLEAR_MEDIUM_ANGSTY_001 | 1 | 65 | 30 |
| qwen3-max-2026-01-23 | DSV2 | eval_dsv2_20260213_143908_qwen3-max-2026-01-23 | NW_CLEAR_MEDIUM_HEROINE_001 | 1 | 51 | 24 |

### 3.3 按模型汇总

| 模型 | 总success样本 | 0-3章样本 | 占比 | 典型表现 |
|------|-------------|----------|------|---------|
| EB5-midtrain | 23 | 8 | 34.8% | 最严重，DSV2有5/9是0章 |
| gemini | 24 | 5 | 20.8% | SWEET题材最易触发 |
| glm-4.7 | 7 | 3 | 42.9% | 样本总量少，但占比最高 |
| qwen3-max | 24 | 3 | 12.5% | 写了1章就####STOP#### |
| kimi | 48 | 3 | 6.3% | 仅DSV2出现 |
| ernie | 17 | 3 | 17.6% | IP题材最易触发 |
| claude-4.5 | 23 | 1 | 4.3% | 仅ULTRA_SHORT出现 |
| claude-4.6 | 9 | 0 | 0% | 无此问题 |

### 3.4 终止模式验证

通过阅读对话历史确认，典型的提前终止模式是：

1. 模型写完 chapter_01.md 后
2. 可能写了 writing_log.md (写作日志)
3. 直接输出 `####STOP####` 终止对话

已在以下样本的对话历史末尾验证了此模式:
- `eval_dsv1_20260213_143137_qwen3-max-2026-01-23 / NW_CLEAR_MEDIUM_SUSPENSE_001`: 写完ch01后直接STOP
- `eval_dsv2_20260213_143908_qwen3-max-2026-01-23 / NW_CLEAR_MEDIUM_HEROINE_001`: 写完ch01+writing_log后STOP
- `eval_dsv2_20260213_143908_qwen3-max-2026-01-23 / NW_CLEAR_MEDIUM_ANGSTY_001`: 写完ch01+writing_log后STOP（最后一条assistant消息是checklist自检，然后对话结束）
- `eval_dsv1_20260205_141134_gemini-3-pro-preview / NW_CLEAR_MEDIUM_ANGSTY_001`: 写完ch03+writing_log后STOP

---

## 四、章节长度崩塌 (Length Collapse)

### 4.1 定义
交付的后期章节字数相比前期章节出现 >65% 的缩短（last5_avg / first5_avg < 35%）。

### 4.2 确认案例（18个样本）

| 模型 | 版本 | 评估目录 | 样本ID | 总章数 | 前5章均(bytes) | 后5章均(bytes) | 衰减比 |
|------|------|----------|--------|--------|---------------|---------------|--------|
| kimi-k2.5 | DSV1 | eval_dsv1_20260211_202557_kimi-k2.5 | NW_CLEAR_MEDIUM_SUSPENSE_001 | 60 | 11,994 | 953 | **7.9%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_VAGUE_MEDIUM_SWEET_DRAMA_001 | 26 | 8,248 | 671 | **8.1%** |
| EB5-midtrain | DSV1 | eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat | NW_ULTRA_SHORT_ANGSTY_002 | 44 | 13,723 | 1,466 | **10.7%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260211_131949_kimi-k2.5 | NW_CLEAR_MEDIUM_SWEET_001 | 42 | 11,474 | 1,455 | **12.7%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_CLEAR_MEDIUM_HEROINE_001 | 38 | 9,664 | 1,639 | **17.0%** |
| kimi-k2.5 | DSV1 | eval_dsv1_20260211_202557_kimi-k2.5 | NW_CLEAR_MEDIUM_SWEET_001 | 20 | 15,837 | 3,345 | **21.1%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_IP_MEDIUM_NEUTRAL_001 | 16 | 14,129 | 3,080 | **21.8%** |
| kimi-k2.5 | DSV1 | eval_dsv1_20260211_202557_kimi-k2.5 | NW_IP_MEDIUM_NEUTRAL_001 | 14 | 17,022 | 3,927 | **23.1%** |
| ernie-5.0 | DSV2 | eval_dsv2_20260211_103353_ernie-5.0-thinking-preview | NW_CLEAR_MEDIUM_SWEET_001 | 48 | 8,707 | 2,207 | **25.3%** |
| kimi-k2.5 | DSV1 | eval_dsv1_20260211_202557_kimi-k2.5 | NW_CLEAR_MEDIUM_ANGSTY_001 | 15 | 20,912 | 5,341 | **25.5%** |
| claude-4.6 | DSV2 | eval_dsv2_20260211_204123_claude-opus-4-6 | NW_CLEAR_MEDIUM_SWEET_001 | 35 | 13,420 | 3,472 | **25.9%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260211_131949_kimi-k2.5 | NW_CLEAR_SHORT_SWEET_001 | 13 | 14,436 | 3,993 | **27.7%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260211_131949_kimi-k2.5 | NW_CLEAR_MEDIUM_SUSPENSE_001 | 20 | 15,600 | 4,365 | **28.0%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260211_131949_kimi-k2.5 | NW_CLEAR_MEDIUM_BRAINY_ACTION_001 | 15 | 18,129 | 5,424 | **29.9%** |
| claude-4.5 | DSV1 | eval_dsv1_20260205_132400_claude-opus-4-5-20251101 | NW_CLEAR_MEDIUM_SWEET_001 | 60 | 10,051 | 3,158 | **31.4%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260211_131949_kimi-k2.5 | NW_CLEAR_MEDIUM_ADVENTURE_001 | 35 | 10,527 | 3,368 | **32.0%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_CLEAR_MEDIUM_ANGSTY_001 | 12 | 11,825 | 3,834 | **32.4%** |
| kimi-k2.5 | DSV2 | eval_dsv2_20260210_171439_kimi-k2.5 | NW_CLEAR_MEDIUM_SWEET_001 | 28 | 6,629 | 2,202 | **33.2%** |

### 4.3 长度崩塌极端案例

**kimi DSV1 SUSPENSE_001 (60章, 衰减至7.9%)**

这是最极端的崩塌案例。具体表现:
- **评估目录**: `eval_dsv1_20260211_202557_kimi-k2.5`
- **样本ID**: `NW_CLEAR_MEDIUM_SUSPENSE_001`
- **chapter_01.md**: 3,935字 — 有民国场景描写、对话、氛围("梧桐叶落了一地，在路灯下泛着尸斑似的黄")
- **chapter_55.md**: 237字 — 纯角色列表+口号("他们的牺牲，不会白费")
- **chapter_58.md**: 243字 — 纯摘要体("她作为守夜人的经历，她如何被干扰频率解救，她如何重新获得自由")

**后15章(ch46-60)全部在237-587字之间，不再是小说叙事，而是事件/人物摘要列表。**

### 4.4 按模型汇总

| 模型 | 严重崩塌样本数 | 说明 |
|------|-------------|------|
| kimi-k2.5 | **13** | 跨DSV1和DSV2普遍存在，是最突出的长度崩塌模型 |
| EB5-midtrain | 1 | 与交替克隆重叠 |
| ernie-5.0 | 1 | 与完全克隆重叠(ch13-48全是2207 bytes) |
| claude-4.6 | 1 | 仅SWEET_001出现 |
| claude-4.5 | 1 | 仅SWEET_001且60章仍有3158 avg |

---

## 五、叙事质量退化 (Narrative Degradation)

### 5.1 深度阅读评估结果

以下样本经过逐章阅读，从叙事质量、对话质量、人物一致性、重复问题、大纲偏离等维度进行了评估。

#### 5.1.1 qwen3-max DSV1 ANGSTY_001 — 评级: 不及格

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv1_20260213_143137_qwen3-max-2026-01-23` |
| **样本ID** | `NW_CLEAR_MEDIUM_ANGSTY_001` |
| **阅读章节** | ch01, ch03, ch05, ch08, ch10 |
| **总章数/字数** | 10章, 各章816-1958字 |

**发现的问题**:

1. **剧情逻辑崩塌**: 反转套反转，每章推翻前章真相
   - ch05: 特警逮捕陈局
   - ch08: "被抓的只是我的替身"推翻ch05
   - ch08: 沈清漪"其实是我的实验"推翻前面所有人物动机

2. **严重偏离自己的大纲**:
   - outline设计: "没有机械降神，只有残酷的现实"和"彻底悲剧结局"
   - 实际执行: 大量机械降神(特警救场、替身诡计、实验揭秘)，结尾变成悬念续集

3. **对话同质化**: 所有角色（局长/法医/证人/刑警）共享同一套"神秘暗示体"话术

4. **重复句式**: "天旋地转""那么凄美那么决绝"在不同章节原文复制

5. **后期退化**: ch10仅816字，大量空洞抒情

#### 5.1.2 qwen3-max DSV2 BRAINY_ACTION_001 — 评级: 不及格

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv2_20260213_143908_qwen3-max-2026-01-23` |
| **样本ID** | `NW_CLEAR_MEDIUM_BRAINY_ACTION_001` |
| **阅读章节** | ch01, ch04, ch07 (全7章精读) |
| **总章数** | 7章 (大纲设计9章, **缺少ch08"最后的对决"和ch09"新的开始"**) |

**发现的问题**:

1. **故事结构残缺**: 大纲9章只写了7章，缺少高潮和结局

2. **智斗名不副实**:
   - ch04密码: 直接猜"13"就对了
   - ch04第二道门: "13+7=20, 20-13=7, 会不会是7？"——逻辑不成立但答案正确
   - ch06密码: "太复杂了，直接砸吧"→门自己开了

3. **核心设定矛盾**:
   - ch05: 主角是沈墨(天才科学家)的克隆体
   - ch07: 主角是陈明远(天才侦探)的克隆体
   - 两个身份互相矛盾，未解决

4. **反派出场5次模式完全相同**: 微笑→说话→打响指→消失

5. **结尾句式复制**:
   - ch04: "两人冲出医院大门，外面是一片荒芜的街道。远处，一家24小时便利店的招牌在夜色中闪烁着微弱的光。"
   - ch06: "三人冲出商场，外面是一片荒芜的街道。远处，一所学校的轮廓在夜色中若隐若现。"

#### 5.1.3 qwen3-max DSV2 ADVENTURE_001 — 评级: 及格偏下

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv2_20260213_143908_qwen3-max-2026-01-23` |
| **样本ID** | `NW_CLEAR_MEDIUM_ADVENTURE_001` |
| **阅读章节** | ch01, ch03, ch06 |
| **总章数/字数** | 6章, ch01最长(约5500字) |

**发现的问题**:

1. **ch06严重注水**: 同一观点("建立数字化档案系统""让村寨人参与保护")在同一章内**逐字重复3次**

2. **ch06叙事性丧失**: 全章17个`###`子标题，内容变成议论文/工作报告体，不再是小说

3. **角色崩塌**: 退伍特种兵陈峰在ch06说话风格变成文化局干部（"完全同意，只有这样，文化遗产才能真正得到传承"）

4. **正面**: ch01-03质量不错，有具体的感官描写（"空气中弥漫着纸张和墨水的陈旧气味"）

#### 5.1.4 glm-4.7 DSV2 HEROINE_001 — 评级: 不及格

| 字段 | 值 |
|------|-----|
| **评估目录** | `eval_dsv2_20260212_201303_glm-4.7` |
| **样本ID** | `NW_CLEAR_MEDIUM_HEROINE_001` |
| **阅读章节** | ch01, ch03, ch05, ch08, ch10 |
| **总章数** | 10章, ch05仅1470字 |

**发现的问题**:

1. **系统性重复（最严重）**:
   - "明天，会是新的一天" — 单章(ch08)内出现3次，全文至少6次
   - "夕阳很美，把天空染成橘红色，像一幅油画" — 至少5次
   - "她有真本事，她会站起来的" — 至少5次

2. **模板化场景批量生成**: ch08有4个客户接待场景，结构完全相同:
   - `客户描述→"帮我看看"→林清鉴定→结论→客户反应`

3. **同章段落复制**: ch05内距44行的两处完全相同的段落:
   - "她坐在工作台前，想起离婚那天的情景。顾泽明把纸箱塞给她……"

4. **跨角色台词克隆**: ch10中外公和周明对林清"看走眼"一事的回应**一字不差**:
   - "看走眼不可怕，可怕的是不敢承认。你承认了，赔偿了，这就够了。"

5. **正面**: ch01和ch03有合格的网文水准，特别是ch03老太太鉴定段落有真实感

---

## 六、章节数分布全景

### 6.1 按模型和版本统计

| 模型 | 版本 | N | 0-3章 | 4-6章 | 7-10章 | 11+章 | 平均 | 最小 | 最大 |
|------|------|---|-------|-------|--------|-------|------|------|------|
| claude-4.5 | DSV1 | 14 | 1 | 5 | 2 | 6 | 15.9 | 3 | 60 |
| claude-4.5 | DSV2 | 9 | 0 | 0 | 2 | 7 | 20.4 | 9 | 32 |
| claude-4.6 | DSV2 | 9 | 0 | 0 | 1 | 8 | 24.6 | 10 | 40 |
| ernie-5.0 | DSV1 | 9 | 1 | 1 | 5 | 2 | 11.8 | 3 | 40 |
| ernie-5.0 | DSV2 | 8 | 2 | 1 | 0 | 5 | 14.4 | 0 | 48 |
| gemini | DSV1 | 14 | 3 | 6 | 4 | 1 | 5.9 | 1 | 14 |
| gemini | DSV2 | 10 | 2 | 3 | 4 | 1 | 6.6 | 1 | 11 |
| glm-4.7 | DSV1 | 4 | 2 | 0 | 0 | 2 | 9.5 | 0 | 21 |
| glm-4.7 | DSV2 | 3 | 1 | 0 | 1 | 1 | 14.3 | 0 | 36 |
| kimi-k2.5 | DSV1 | 14 | 0 | 4 | 3 | 7 | 14.1 | 4 | 60 |
| kimi-k2.5 | DSV2 | 20 | 3 | 0 | 1 | 16 | 19.1 | 3 | 42 |
| EB5-midtrain | DSV1 | 14 | 3 | 0 | 4 | 7 | 12.4 | 0 | 44 |
| EB5-midtrain | DSV2 | 9 | 5 | 0 | 2 | 2 | 4.8 | 0 | 15 |
| qwen3-max | DSV1 | 14 | 1 | 2 | 11 | 0 | 7.6 | 1 | 10 |
| qwen3-max | DSV2 | 10 | 2 | 4 | 4 | 0 | 5.7 | 1 | 9 |

### 6.2 关键观察

1. **Claude-4.5/4.6 是唯一始终维持高章节产出的模型**: DSV2平均20-25章，无极端低值
2. **qwen3-max 从不超过10章**: DSV1最大10章，DSV2最大9章，是产出上限最低的模型
3. **kimi-k2.5 两极分化最严重**: 同时有60章和3章的样本，但高章节数伴随严重的长度崩塌
4. **EB5 DSV2 完成度极低**: 9个样本中5个是0-3章，平均仅4.8章
5. **gemini 产出稳定但偏低**: 平均5.9-6.6章，标准差较小

---

## 七、模型质量梯队总结

| 梯队 | 模型 | 核心特征 | 代表性问题样本 |
|------|------|---------|--------------|
| **A** | Claude-4.5, Claude-4.6 | 后期不退化，感官细节丰富，对话有辨识度 | claude-4.5 DSV1 SWEET_001 有轻微长度崩塌(31.4%) |
| **B** | Gemini | 开头有文学性，但产出量低且后期递减 | DSV1 ANGSTY_001/SWEET_001提前终止(1-3章) |
| **C** | Kimi | 早期章节可读，但后期严重崩塌至摘要体 | DSV1 SUSPENSE_001: 60章但后15章仅237-587字 |
| **D** | Qwen3-max | 概念有创意但执行力不足，智斗逻辑崩坏 | DSV2 BRAINY_ACTION_001: 设定矛盾+故事残缺 |
| **D** | GLM-4.7 | 系统性重复和模板化，完成度低 | DSV2 HEROINE_001: 模板客户×4+段落复制 |
| **E** | Ernie-5.0, EB5-midtrain | 章节克隆，0章完成度，工程级失败 | ernie DSV2 SWEET_001: 36章克隆；EB5 DSV2 5/9样本0章 |

---

## 八、对后续checker开发的启示

本轮审查确认了以下问题可以通过**程序化检测**:

| 检测项 | 检测方法 | 已在content_quality_basic.yaml v1.8定义 |
|--------|---------|---------------------------------------|
| 章节克隆 | 去标题行后比较文件hash或前N字节 | 是 (内容重复注水) |
| 交替克隆 | 检测奇偶章节大小的A-B交替模式 | 是 (内容重复注水) |
| 长度崩塌 | last5_avg / first5_avg < 阈值 | 是 (章节长度稳定性) |
| 段落级重复 | 滑动窗口比较同章/跨章的长文本段 | 是 (内容重复注水) |
| 提前终止 | 章节数 < 预期值的30% | 需要新增检查项 |
| 口号式结尾循环 | 统计特定句式在全文中的出现频次 | 可扩展 |

以下问题**需要LLM judge**:
- 对话同质化 / 角色语言辨识度
- 大纲偏离程度
- 智斗逻辑的合理性
- 叙事质量（流水账 vs 细腻描写）

---

## 附录：评估目录路径对照表

| 简称 | 完整目录名 |
|------|-----------|
| claude45-DSV1 | `eval_dsv1_20260205_132400_claude-opus-4-5-20251101` |
| ernie-DSV1 | `eval_dsv1_20260205_140957_ernie-5.0-thinking-preview` |
| gemini-DSV1 | `eval_dsv1_20260205_141134_gemini-3-pro-preview` |
| EB5-DSV1 | `eval_dsv1_20260211_193709_openai_EB5-0209-A35B-midtrain-128k-chat` |
| kimi-DSV1 | `eval_dsv1_20260211_202557_kimi-k2.5` |
| glm-DSV1 | `eval_dsv1_20260212_201213_glm-4.7` |
| qwen3-DSV1 | `eval_dsv1_20260213_143137_qwen3-max-2026-01-23` |
| kimi-DSV2-171439 | `eval_dsv2_20260210_171439_kimi-k2.5` |
| ernie-DSV2 | `eval_dsv2_20260211_103353_ernie-5.0-thinking-preview` |
| claude45-DSV2 | `eval_dsv2_20260211_122519_claude-opus-4-5-20251101` |
| kimi-DSV2-131949 | `eval_dsv2_20260211_131949_kimi-k2.5` |
| EB5-DSV2 | `eval_dsv2_20260211_202805_openai_EB5-0209-A35B-midtrain-128k-chat` |
| claude46-DSV2 | `eval_dsv2_20260211_204123_claude-opus-4-6` |
| gemini-DSV2 | `eval_dsv2_20260212_114551_gemini-3-pro-preview` |
| glm-DSV2 | `eval_dsv2_20260212_201303_glm-4.7` |
| qwen3-DSV2 | `eval_dsv2_20260213_143908_qwen3-max-2026-01-23` |
