# Checklist 优化总结

## 优化目标

将所有模板通用的检查项提取到 `common_check_list`，减少重复，提高可维护性。

## 优化前后对比

### 优化前
- 每个模板独立维护 6-8 个检查项
- 大量重复的检查项（命名格式、JSON Schema、HITL交互等）
- 修改通用检查需要更新 10 个模板

### 优化后
- **16 个通用检查项** → `common_check_list`
- **1-4 个模板特定检查项** → 各模板的 `check_list`
- 修改通用检查只需更新一处

## Common Check List（16项）

### 1. Format Compliance（格式规范遵循）- 5项
1. `common_01` - 章节命名格式：`chapter_NN.md`
2. `common_02` - creative_intent.json Schema验证
3. `common_03` - characters.json Schema验证
4. `common_04` - outline.json Schema验证
5. `common_16` - 基础文件存在性：creative_intent.json, characters.json, outline.json, chapters/

### 2. Business Rule Compliance（业务规则遵循）- 4项
6. `common_05` - X轴模式ID格式：`^[A-G]\d{1,2}$`
7. `common_06` - Y轴标签枚举：12种之内
8. `common_07` - Y轴标签数量：2-3个
9. `common_08` - forbidden_elements存在性：至少1个

### 3. Interaction Completeness（交互完整性）- 2项
10. `common_09` - 配方选择阶段HITL调用
11. `common_10` - 写作准备阶段HITL调用

### 4. Content Quality - Basic（内容质量-基础层）- 5项
12. `common_11` - 主题一致性
13. `common_12` - 主要角色一致性
14. `common_13` - 人物设定一致性
15. `common_14` - 无逻辑硬伤
16. `common_15` - 语言纯净性

## 模板特定检查项

### Short/Medium 模板（有tone）- 3项
1. `reaction_strength` - 反应强度约束（↗/↘/✷）
2. `word_count` - 字数约束（根据word_count类型）
3. `emotional_delivery` - 情感交付匹配

### Long 模板（有tone）- 4项
1. **`writing_log存在`** - writing_log.md必须存在（长篇特有）
2. `reaction_strength` - 反应强度约束
3. `word_count` - 字数约束
4. `emotional_delivery` - 情感交付匹配

### Neutral 模板（无tone）- 1项
1. `word_count` - 字数约束

### Long Neutral 模板 - 2项
1. **`writing_log存在`** - writing_log.md必须存在
2. `word_count` - 字数约束

## 样本检查项数量分布

| 检查项数 | 模板数 | 类型说明 |
|---------|--------|---------|
| **17项** | 1 | Neutral（无tone，无long） |
| **18项** | 2 | Long Neutral（无tone，有long） |
| **19项** | 6 | 有tone（无long） |
| **20项** | 1 | Long + Tone（都有） |

### 具体分布

#### 17项：Neutral Medium
- NW_IP_MEDIUM_NEUTRAL (1个)

#### 18项：Long Neutral
- NW_IP_LONG_NEUTRAL (1个)
- NW_IP_ULTRA_LONG_NEUTRAL (1个)

#### 19项：Short/Medium with Tone
- NW_ULTRA_SHORT_ANGSTY (5个)
- NW_CLEAR_SHORT_SWEET (2个)
- NW_CLEAR_SHORT_ANGSTY (5个)
- NW_CLEAR_MEDIUM_SWEET (2个)
- NW_CLEAR_MEDIUM_ANGSTY (5个)
- NW_CLEAR_MEDIUM_SUSPENSE (1个)

#### 20项：Long with Tone
- NW_CLEAR_LONG_ANGSTY (1个)

**总样本数：24个**

## 关键设计决策

### 1. writing_log.md 为何是模板特定？
- **原因**：只有 >8000字 的长篇创作才需要writing_log.md来维护前后一致性
- **实现**：long/ultra_long 模板保留 `check_01_writing_log存在`，其他模板删除
- **优点**：避免短篇样本因缺少无用文件而失败

### 2. 为何 base 4 files 在 common_16？
- **原因**：所有模板都必需这4个文件（creative_intent.json, characters.json, outline.json, chapters/）
- **实现**：新增 `common_16_基础文件存在性` 到 common_check_list
- **优点**：一次定义，全部模板共享

### 3. 为何 dimension_id=format_compliance？
- **澄清**：`format_compliance` 指"输出结构规范遵循"，不仅是"格式"
- **逻辑**：文件存在性属于"结构完整性"（subcategory_id=structural_integrity）
- **层级**：format_compliance > structural_integrity > file_existence

## 实现步骤

### Step 1: 添加 common_check_list
在 `unified_scenario_design.yaml` 中添加：
```yaml
common_check_list:
  description: 所有模板通用的检查项（16项），会自动合并到每个模板的check_list中
  checks:
    - check_id: common_01_章节命名格式
      ...
    - check_id: common_16_基础文件存在性
      ...
```

### Step 2: 修改 sample_generator
在 `scripts/sample_generator/main.py` 中：
1. 加载 `common_checks`
2. 修改 `_convert_checklist()` 先添加common checks，再添加template checks

### Step 3: 清理模板重复项
运行 `clean_checklists.py`：
- 删除 配方选择交互、写作准备确认、主题一致性、语言纯净性
- 重新编号剩余检查项

### Step 4: 优化文件检查
运行 `optimize_file_checks.py`：
- 7个模板：删除 check_01（base 4 files 已在 common_16）
- 3个long模板：修改 check_01 只检查 writing_log.md

### Step 5: 重新生成样本
运行 `python3 scripts/sample_generator/main.py`：
- 自动合并 16 common + 1-4 template checks
- 生成 24 个样本
- 验证所有样本 checklist 结构正确

## 验证结果

✓ 所有样本 checklist 结构正确
✓ Common checks 正确合并（16项）
✓ Template checks 正确附加（1-4项）
✓ Long 模板正确包含 writing_log.md 检查
✓ Neutral 模板正确排除 reaction_strength 和 emotional_delivery
✓ 样本总数：24个

## 优化效果

### 可维护性提升
- **修改成本降低**：通用检查只需修改一处
- **一致性保证**：所有样本共享相同的通用检查逻辑
- **清晰度提升**：模板 check_list 只包含真正特定的检查项

### 质量提升
- **覆盖更全**：新增了 主要角色一致性、人物设定一致性、逻辑硬伤 3个重要检查
- **逻辑更清晰**：通用 vs 特定检查项明确分离
- **验证更精确**：writing_log.md 只在需要的场景验证

## 文件清单

### 配置文件
- `unified_scenario_design.yaml` - 添加 common_check_list，优化所有模板

### 实现代码
- `scripts/sample_generator/main.py` - 添加 common checks 合并逻辑

### 工具脚本
- `clean_checklists.py` - 批量清理模板重复项
- `optimize_file_checks.py` - 优化文件存在性检查

### 生成文件
- `samples/eval.jsonl` - 24个评测样本
- `samples/eval_readable.json` - 可读版本
- `samples/viewer.html` - HTML查看器
