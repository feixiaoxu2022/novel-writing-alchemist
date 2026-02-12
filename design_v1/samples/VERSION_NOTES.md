# 样本版本说明

## 文件结构

```
samples/
├── eval.jsonl              # 默认版本（等同于eval_v1.jsonl）
├── eval_readable.json      # 默认版本的可读格式
├── eval_v1.jsonl           # V1版本（弱指令："参考"）
├── eval_v1_readable.json   # V1可读格式
├── eval_v2.jsonl           # V2版本（强指令："必须阅读"）
├── eval_v2_readable.json   # V2可读格式
└── viewer.html             # HTML查看器
```

## 版本差异

### V1版本（eval_v1.jsonl）

**System Prompt**: `BusinessRules.md`

**指令特征**：使用弱指令词"参考"

- "如创作短篇，**参考** `data_pools/skills/SHORT_STORY_GUIDE.md`"
- "**参考** `data_pools/skills/CHARACTER_NAMING_GUIDE.md`"
- "JSON格式验证：**参考** `data_pools/schemas/*.schema.json`"

**预期问题**：模型在token成本压力下可能跳过阅读这些补充文档

### V2版本（eval_v2.jsonl）⭐️ 推荐

**System Prompt**: `BusinessRules_v2.md`

**指令特征**：使用强指令词"必须先阅读"/"必须依次阅读"，并明确触发时机

- "**如果目标字数在6500-10000字范围，必须先阅读** `data_pools/skills/SHORT_STORY_GUIDE.md`"
- "**在生成characters.json之前，必须依次阅读以下两个文件**：`CHARACTER_NAMING_GUIDE.md`和`NAME_DATABASE.xlsx`"
- "**在输出每个JSON文件前，必须先读取对应schema验证格式**"
- 在阶段2和阶段3添加了强制前置检查点

**新增约束**：

- **字数达标要求**：如果用户明确给定具体篇幅要求，必须确保实际创作内容达到该字数要求后才能输出STOP标记
  - 不得在未达到用户要求字数时提前结束创作
  - 如果接近字数上限但情节未完，优先保证情节完整性

**改进目标**：强制模型阅读补充文档，提升输出质量和格式规范性，确保完成用户指定的字数要求

## 统计对比

| 指标 | V1 | V2 |
|------|----|----|
| 文件大小 | 800KB | 823KB |
| 样本数量 | 14 | 14 |
| "参考"出现次数 | 5次 | 2次 |
| "必须先阅读"出现次数 | 0次 | 1次 |
| "必须依次阅读"出现次数 | 0次 | 1次 |
| 字数达标约束 | 无 | 有 |

## 使用建议

- **对比基准评测**：使用 `eval_v1.jsonl`（或默认的`eval.jsonl`）
- **改进版评测**：使用 `eval_v2.jsonl` 测试强指令效果
- **对比实验**：同时运行v1和v2，对比模型在不同指令强度下的表现差异
- **成本控制**：两个版本字数相同（约82.5万字），成本一致

## 评测命令示例

```bash
# V1版本（默认，对比基准）
bash run_test.sh gemini-3-pro-preview samples/eval_v1.jsonl

# V2版本（强指令改进版）
bash run_test.sh gemini-3-pro-preview samples/eval_v2.jsonl

# 默认版本（等同于V1）
bash run_test.sh gemini-3-pro-preview samples/eval.jsonl
```

---

生成时间: 2026-02-04
生成器版本: design_v1
