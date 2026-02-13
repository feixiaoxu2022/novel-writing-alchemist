# 评估体系升级方案

> **起因**: deliverable_quality_audit_v1.md 发现五类严重质量问题（章节克隆、提前终止、长度崩塌、叙事退化、逻辑缺陷），其中前三类完全可程序化检测但当前checker未覆盖
> **目标**: 让评估分数真实反映交付物质量，而不是"流程合规性"

---

## 一、当前体系的核心问题

### 1.1 检测盲区

当前42个检查项的覆盖范围与真实质量问题的映射：

| 质量审查发现的问题 | 影响样本数 | 当前是否有检查项覆盖 | 能否程序化 |
|-------------------|----------|-------------------|----------|
| 章节克隆（36章内容完全一样） | 5+ | **无** | 100%程序化 |
| 提前终止（写了0-3章就结束） | 26 | 部分覆盖¹ | 100%程序化 |
| 章节长度崩塌（后期缩至<10%） | 18 | **无** | 100%程序化 |
| 段落级重复（同章/跨章逐字复制） | 多个 | **无** | 90%程序化 |
| 叙事质量退化（变为摘要/报告体） | 多个 | 部分覆盖² | 需LLM judge |
| 对话同质化（所有角色说话一样） | 多个 | **无** | 需LLM judge |
| 大纲偏离（不执行自己设计的大纲） | 多个 | **无** | 需LLM judge |
| 智斗逻辑崩坏（密码谜题不成立） | 个别 | **无** | 需LLM judge |

¹ `chapters目录存在性`(#19)只检查"有没有章节文件"，不检查数量是否合理
² `完整叙事文本`(#34)和`后期章节跑偏`(#37)理论上覆盖，但实际judge prompt可能无法捕捉"237字的摘要体"这种极端退化

**结论**: 审查发现的前三大问题（占总问题样本的60%+）完全没有被当前checker覆盖。

### 1.2 评分权重失衡

当前评分是4个维度等权平均：

```
total = mean(format_compliance, business_rule_compliance, memory_management, content_quality)
```

问题：
- `format_compliance`(4项) 和 `memory_management`(2项) 加起来只有6个检查"格式和日志"的项，却占总分的50%
- `business_rule_compliance`(23项) 中有9项是"是否读取了某个知识库文件"，这些是流程动作而非质量指标
- 一个模型可以做到：读了所有知识库、创建了所有文件、格式全对、写了日志，但实际内容是36章克隆 —— 它仍然可能拿到 **75+分**（format=100, business=100, memory=100, content_quality=0 → 平均75）

这意味着一个产出"灾难级"交付物的样本可以得到"Good"评级。

### 1.3 content_quality的basic层门槛过高但区分度不足

- **过高**: basic层任何一项fail就0-60分，导致轻微瑕疵（如一处语言纯净性问题）和灾难级失败（36章克隆）得到一样的分数
- **区分度不足**: 没有advanced层活跃检查项，所有basic全过的样本都是65分（"合格"），无法区分"凑合能看"和"真正优秀"

---

## 二、升级方案

### 2.1 新增程序化检查项（rev_005）

以下检查项全部可程序化实现，不依赖LLM，检测成本为零：

#### P1: 章节克隆检测（content_repetition_cloning）

```
检测逻辑:
1. 对每个chapter文件，去掉第一行（标题行），计算剩余内容的hash
2. 统计相同hash的连续章节数
3. 也检测"前N字节相同"的近似克隆（标题行不同但正文一样）

判定阈值:
- 完全克隆(hash一致) >= 2章 → fail
- 近似克隆(前500字节hash一致) >= 3章 → fail

受影响样本（基于审查数据）:
- ernie DSV2 SWEET_001: ch13-48 (36章完全克隆)
- ernie DSV1 SWEET_001: ch13-48 (36章完全克隆)
- EB5 DSV2 ADVENTURE_001: ch25-45 (21章近似克隆)
- EB5 DSV1 ANGSTY_002: ch25-44 (20章交替克隆)
```

#### P2: 交替重复检测（content_repetition_alternating）

```
检测逻辑:
1. 提取奇数章和偶数章的文件大小序列
2. 检测是否存在A-B-A-B交替模式（连续>=3轮）

判定阈值:
- 交替重复轮数 >= 3 → fail

受影响样本:
- EB5 DSV1 ANGSTY_002: 1403/1508 bytes 交替
```

#### P3: 章节完成度检测（chapter_completion_ratio）

```
检测逻辑:
1. 从outline.json中提取规划的章节数（或从大纲的chapters/key_chapters列表长度推断）
2. 实际写出的章节数 / 规划章节数

判定阈值:
- 实际/规划 < 30% → fail（极端不完整）
- 实际章节数 = 0 → fail（什么都没写）
- 对于无法从大纲提取规划数的情况：实际章节数 <= 1 且 样本类型包含 MEDIUM → fail

受影响样本: 26个提前终止样本
```

#### P4: 章节长度稳定性检测（chapter_length_stability）

```
检测逻辑:
1. 计算前1/3章节的平均字数（first_avg）
2. 计算后1/4章节的平均字数（last_avg）
3. ratio = last_avg / first_avg

判定阈值:
- ratio < 0.25 → fail（严重崩塌）
- 后1/4中任何单章 < 200字 → fail（极端退化）

受影响样本: 18个长度崩塌样本
注意: 需排除只有1-3章的样本（这些由P3覆盖）
```

#### P5: 段落级重复检测（paragraph_repetition）

```
检测逻辑:
1. 将每章按段落拆分（以空行分隔）
2. 对每个 >= 50字的段落，计算hash
3. 检测同一章内和跨章的重复段落

判定阈值:
- 同章内完全相同的段落 >= 2处 → fail
- 跨章完全相同的段落（排除章节标题模板） >= 5处 → fail

受影响样本:
- glm DSV2 HEROINE_001: ch05内同段落复制、ch08四个模板场景
- qwen3 DSV2 ADVENTURE_001: ch06内同观点三次重复
```

### 2.2 新增LLM judge检查项（advanced层）

以下检查项需要LLM语义理解，建议放入content_quality的**advanced层**，用于区分"合格"与"优秀"：

#### L1: 对话辨识度（dialogue_character_distinction）

```
judge目标: 不同角色的对话是否有语言风格差异
judge方法: 抽取3个主要角色各5段对话，让LLM判断是否能仅通过对话内容区分说话者
评判标准:
- 优秀: 不看角色标注也能识别说话者
- 合格: 有一定区分但不够鲜明
- 不合格: 去掉角色名后无法区分

关联审查发现:
- qwen3 ANGSTY_001: 所有角色共享"神秘暗示体"
- glm HEROINE_001: 外公和周明说一模一样的话
```

#### L2: 大纲执行忠实度（outline_execution_fidelity）

```
judge目标: 实际写出的章节是否忠实执行了自己设计的outline.json
judge方法: 抽取outline中3个关键转折点/场景的描述，在对应章节中验证是否出现
评判标准:
- 优秀: 关键转折点全部体现，细节与大纲一致
- 合格: 主线一致但细节有偏离
- 不合格: 关键转折点缺失或与大纲矛盾

关联审查发现:
- qwen3 ANGSTY_001: 大纲设计"彻底悲剧"实际写成"悬念续集"
- qwen3 BRAINY_ACTION_001: 大纲9章只写7章，核心设定矛盾
```

#### L3: 叙事密度（narrative_density）

```
judge目标: 章节是否包含足够的场景描写、感官细节、心理活动，而非纯对话/事件罗列
judge方法: 随机抽取3章，统计对话行占比、环境描写密度、心理活动密度
评判标准:
- 优秀: 对话:叙述比例合理，有丰富的感官细节
- 合格: 以叙述为主但描写较粗
- 不合格: 退化为纯对话骨架或事件列表

关联审查发现:
- kimi SUSPENSE_001 后期章节退化为"人物摘要列表"
- glm HEROINE_001 ch05退化为纯对话骨架
- qwen3 ADVENTURE_001 ch06退化为议论文
```

### 2.3 评分权重重构

#### 方案: 分层评分 + 一票否决

```
第一层：完成度门槛（Gate）
  检查项: P3(章节完成度) + P1(章节克隆) + P2(交替重复)
  逻辑: 任何一项fail → 直接判定为"不合格"，总分上限30分
  理由: 0章交付或36章克隆不是"质量差"，是"根本没有有效交付"

第二层：基础质量（Baseline）
  检查项: 当前basic层所有项 + P4(长度稳定性) + P5(段落重复)
  逻辑: 通过门槛后，basic层全过 → 60分起步；每fail一项扣分
  权重: 这一层决定60-70分的区间

第三层：内容质量进阶（Advanced）
  检查项: L1(对话辨识度) + L2(大纲执行) + L3(叙事密度) + 现有的情感交付
  逻辑: basic全过后，advanced决定70-100分的区间
  权重: 按通过率线性映射到70-100分
```

具体评分公式：

```python
def calculate_score(gate_results, basic_results, advanced_results,
                    format_results, business_results, memory_results):
    
    # 第一层：完成度门槛
    if any gate check failed:
        content_score = min(30, count_passed_basic / total_basic * 30)
    else:
        # 第二层：基础质量
        basic_pass_rate = count_passed_basic / total_basic
        if basic_pass_rate < 1.0:
            content_score = 30 + basic_pass_rate * 40  # 30-70分
        else:
            # 第三层：进阶质量
            advanced_pass_rate = count_passed_advanced / total_advanced
            content_score = 70 + advanced_pass_rate * 30  # 70-100分
    
    # 流程维度（降权）
    process_score = mean(format_score, business_score, memory_score)
    
    # 最终分数: 内容占70%, 流程占30%
    total = content_score * 0.7 + process_score * 0.3
    
    return total
```

关键变化：
1. **内容质量占70%，流程合规占30%**（当前是各占25%即等权）
2. **引入一票否决门槛**：克隆/0章交付直接上限30分
3. **三层递进评分**：门槛→基础→进阶，区分度从"不合格/合格"扩展为"不合格/及格/良好/优秀"

### 2.4 变化前后对比（以典型样本为例）

| 样本 | 当前得分(估) | 升级后得分(估) | 变化原因 |
|------|------------|-------------|---------|
| ernie DSV2 SWEET (36章克隆) | ~75 (format+business+memory全过) | **≤30** | 门槛层P1 fail，一票否决 |
| EB5 DSV2 BRAINY_ACTION (0章) | ~70 (流程做了，文件创建了) | **≤30** | 门槛层P3 fail，一票否决 |
| kimi DSV1 SUSPENSE (60章→237字) | ~65 (content basic有些fail) | **~40** | P4长度崩塌fail，basic层多项fail |
| qwen3 DSV2 HEROINE (1章) | ~65 | **≤30** | 门槛层P3 fail |
| claude-4.5 DSV2 BRAINY_ACTION (正常) | ~75 | **~80** | advanced层情感交付+叙事密度加分 |
| claude-4.6 DSV2 BRAINY_ACTION (正常) | ~75 | **~85** | advanced层全面加分 |

---

## 三、实施路径

### 阶段一：程序化检查项实现（1-2天）

1. 在 `checker_execute.py` 中实现 P1-P5 的检测逻辑
2. 在 `common_check_list.yaml` 中注册新检查项
3. 生成 `rev_005` checklist
4. 对所有已完成样本的env目录运行增量recheck（`--only-checks`）
5. 验证：确认审查报告中列出的所有问题样本都被正确检测到

### 阶段二：评分权重重构（0.5天）

1. 修改 `checker_score.py`，实现分层评分+一票否决逻辑
2. 对所有已有check_result做重算，对比新旧分数
3. 验证：确认"36章克隆得75分"的情况不再出现

### 阶段三：LLM judge新增（2-3天）

1. 编写 L1/L2/L3 的 judge criteria YAML（参考现有criteria的格式）
2. 在 `checker_execute.py` 中注册为 `semantic_check` + `llm_semantic_analysis`
3. 标记为 `quality_tier: advanced`
4. 对claude/gemini的优质样本做试运行，校准judge prompt的评判标准
5. 全量运行

### 阶段四：回归验证（1天）

1. 对全部~160个样本重跑完整checker
2. 生成新旧分数对比报告
3. 人工抽查10个样本，验证新分数与人工判断的一致性

---

## 四、风险和注意事项

### 4.1 不能做的事
- **不能直接修改已有检查项的语义**：已有的check_result是基于现有定义生成的，改变定义会导致历史结果不可比
- **不能删除已有检查项**：向后兼容，只能新增
- **不能让新检查项的阈值过于激进**：应该先宽后紧，基于数据校准

### 4.2 需要决策的点
1. **门槛层的一票否决上限是30分还是0分？** 建议30分——因为即使0章交付，流程部分（读了知识库、做了规划）仍有价值
2. **advanced层检查项是否影响当前已有的check_result？** 建议不影响——advanced层只在新一轮评估中生效
3. **是否需要rev_005的checklist，还是在rev_004基础上追加？** 建议新建rev_005——保持版本清晰
4. **content_quality的70%权重是否会让流程维度被忽视？** 可以考虑设置流程维度的最低门槛（如<80%时有额外扣分）
