# output_completeness 检查项问题分析

分析时间: 2026-02-06

## 🔍 问题现象

用户发现：**所有模型在 `output_completeness` 这个检查项上都是100%通过率**

统计报告显示：
```
| business_rule_compliance | output_completeness | 交付文件类型的完整性 |
| Claude Opus 4.5          | 100.0% (8/8)        |
| Ernie 5.0                | 100.0% (7/7)        |
| Gemini 3 Pro             | 100.0% (6/6)        |
```

## 🐛 根本原因

### 1. 检查项定义过于宽松

从 `unified_scenario_design.yaml` 中的定义：

```yaml
- check_id: 最终交付物存在性
  check_name: 最终交付物完整性
  dimension_id: business_rule_compliance
  subcategory_id: output_completeness
  check_type: entity_attribute_equals
  params:
    entity_type: file
    target_id: workspace/chapters/
    attribute_key: exists         # 只检查目录是否存在
    expected_value: true
  weight: 1.0
  is_critical: true
```

**问题**：这个检查项只验证 `workspace/chapters/` 目录是否存在，完全不关心：
- ❌ 目录里是否有文件
- ❌ 文件数量是否合理
- ❌ 文件命名是否符合规范 (chapter_NN.md)
- ❌ 文件内容是否非空
- ❌ 是否有其他必需文件 (creative_intent.json, characters.json, outline.json)

### 2. 名称误导性

**检查名称**："最终交付物完整性"
**实际检查**：只检查 chapters/ 目录存在

名称暗示会验证交付物的完整性，但实际上只是最基础的目录存在性检查，存在严重的**名实不符**问题。

## 📊 实际数据验证

### Claude Opus 4.5 的8个样本分析

```
output_completeness.score 分布:
  score= 50.0:  5个样本  (有其他critical检查失败)
  score=100.0:  3个样本  (所有critical检查通过)
```

**所有8个样本的检查项22都是"合格"**，因为都创建了 chapters/ 目录。

### score=50的样本失败原因

5个 score=50 的样本分析：

| 样本ID | 检查项22 | 检查项25 (字数约束) | 失败原因 |
|--------|---------|-------------------|---------|
| NW_CLEAR_SHORT_SWEET_001 | ✓ 合格 | ✗ 不合格 | 字数34639，超出范围[27000, 33000] |
| NW_CLEAR_SHORT_SWEET_002 | ✓ 合格 | ✗ 不合格 | 字数34956，超出范围[27000, 33000] |
| NW_ULTRA_SHORT_ANGSTY_002 | ✓ 合格 | ✗ 不合格 | 字数12706，超出范围[5850, 11000] |
| NW_ULTRA_SHORT_ANGSTY_004 | ✓ 合格 | ✗ 不合格 | 字数11912，超出范围[5850, 11000] |
| NW_CLEAR_SHORT_ANGSTY_001 | ✓ 合格 | ✗ 不合格 | 字数9724，不足范围[27000, 33000] |

**关键发现**：
- 检查项22（output_completeness）100%通过
- 检查项25（range_constraint）失败率很高
- 这说明 Agent 都创建了目录，但输出质量/数量有问题

## 🔄 两个 output_completeness 的混淆

系统中存在**两个不同含义的 output_completeness**：

### (1) 汇总字段 - output_completeness (顶层字段)

位置：`check_result_v3.json` 顶层

```json
{
  "output_completeness": {
    "score": 50.0,
    "pass_rate": 0.5,
    "total": 2,           // 所有critical检查项的数量
    "passed": 1,          // 通过的critical检查项数量
    "failed": 1,
    "critical_items": [...]
  }
}
```

**作用**：汇总所有 `is_critical: true` 检查项的结果，判断样本是否"执行成功"

### (2) 检查项 - output_completeness (subcategory_id)

位置：`check_list` 中的一个具体检查项（检查项22）

```yaml
subcategory_id: output_completeness
check_name: 最终交付物完整性
```

**作用**：检查 chapters/ 目录是否存在

### 统计脚本的处理

```python
# 过滤执行失败的样本
output_completeness = result.get('output_completeness', {})
if output_completeness.get('score', 0) == 0:
    continue  # 跳过execution_failed的样本
```

**问题**：这个逻辑认为只要 `output_completeness.score > 0` 就算执行成功。但实际上：
- score=50 表示有critical检查失败（如字数不符）
- 这些样本**不应该被计入统计**，但现在被计入了

## ⚠️ 当前问题影响

### 1. 检查项过于宽松

**检查项22"最终交付物完整性"** 几乎不可能失败，只要 Agent 执行了 `create_directory("chapters")`，就通过了。

**结果**：所有模型100%通过，**无法区分模型能力差异**。

### 2. 统计逻辑不准确

现在的过滤条件 `output_completeness.score > 0` 会包含那些有 critical 失败的样本（如字数不符），导致统计结果不准确。

**应该的逻辑**：
- `output_completeness.score == 100` 或 `pass_rate == 1.0` 才算真正的"执行成功"
- `output_completeness.score < 100` 应该归类为"执行失败"（有critical检查未通过）

### 3. 名称混淆

两个不同含义的 `output_completeness` 造成理解困难：
- 开发者容易混淆汇总字段和具体检查项
- 用户看到报告时会误以为"交付完整性"检查很全面

## 💡 修复建议

### 建议1：增强检查项22的验证逻辑

将 `output_completeness` 检查项改为复合检查：

```yaml
- check_id: 最终交付物存在性
  check_name: 最终交付物完整性
  dimension_id: business_rule_compliance
  subcategory_id: output_completeness
  check_type: composite_check  # 改为复合检查
  params:
    checks:
      - name: chapters目录存在
        entity_type: directory
        target_id: workspace/chapters/
        attribute_key: exists
        expected_value: true

      - name: 章节文件数量合理
        entity_type: directory
        target_id: workspace/chapters/
        attribute_key: file_count
        expected_value:
          min: 1  # 至少1个章节文件

      - name: 章节命名符合规范
        entity_type: directory
        target_id: workspace/chapters/
        attribute_key: file_name_pattern
        expected_value: "^chapter_\\d{2}\\.md$"

      - name: 必需JSON文件存在
        files_exist:
          - workspace/creative_intent.json
          - workspace/characters.json
          - workspace/outline.json
  weight: 1.0
  is_critical: true
```

### 建议2：修正统计脚本的过滤逻辑

```python
# 修改前
if output_completeness.get('score', 0) == 0:
    continue

# 修改后
if output_completeness.get('pass_rate', 0) < 1.0:
    # 只统计所有critical检查都通过的样本
    continue
```

### 建议3：重命名避免混淆

**选项A**：重命名检查项
- 将 subcategory_id 从 `output_completeness` 改为 `chapters_directory_exists`
- 检查名称改为"chapters目录存在性"

**选项B**：重命名汇总字段
- 将顶层汇总字段从 `output_completeness` 改为 `execution_summary` 或 `critical_checks_summary`

### 建议4：分级检查

将"交付完整性"拆分为多个层次：

1. **基础层 (必需)**：目录结构存在
   - chapters/ 存在
   - JSON文件存在

2. **规范层 (critical)**：格式符合规范
   - 文件命名正确
   - JSON格式有效
   - 至少有N个章节文件

3. **质量层 (non-critical)**：内容质量
   - 文件内容非空
   - 字数符合要求
   - 语义质量检查

## 📌 优先级建议

**P0 - 立即修复**：
1. 修正统计脚本的过滤逻辑 (`pass_rate == 1.0` 而非 `score > 0`)
2. 在分析报告中添加说明，明确当前 output_completeness 只检查目录存在

**P1 - 下个版本**：
1. 增强 output_completeness 检查项，加入文件数量、命名规范验证
2. 重命名避免混淆

**P2 - 长期优化**：
1. 重构为分级检查体系
2. 设计更细粒度的交付质量评估

## 🎯 预期效果

修复后：
- **检查项22** 能够真正验证交付物完整性，通过率会下降到合理水平（预计60-80%）
- **统计准确性** 提升，只统计真正"执行成功"的样本
- **能力区分度** 提高，能更好地区分不同模型的交付质量

---

**分析人**: Claude Sonnet 4.5
**分析时间**: 2026-02-06
**优先级**: P0（影响统计准确性）
