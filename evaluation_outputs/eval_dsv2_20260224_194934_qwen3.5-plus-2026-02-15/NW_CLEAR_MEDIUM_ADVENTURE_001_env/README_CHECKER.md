# Checker架构说明

## 架构设计

Checker被拆分为两个独立模块 + 一个wrapper接口：

```
checker.py (wrapper)
├── checker_execute.py    # 第1步：执行检查（贵，含LLM调用，可缓存）
└── checker_score.py      # 第2步：计算分数（便宜，纯计算，可重跑）
```

### 拆分目的

经常需要调整统计逻辑（如维度权重、质量等级判断标准等），拆分后可以：
- **避免重复执行LLM检查**（昂贵且耗时）
- **快速迭代评分逻辑**（直接重跑checker_score.py）
- **保持与benchkit的兼容性**（通过checker.py wrapper）

---

## 使用方式

### 方式1：使用wrapper（benchkit调用）

```bash
python env/checker.py \
  --bench bench.json \
  --result result.json \
  --model claude-3-5-sonnet-20241022 \
  --base-url https://api.anthropic.com \
  --api-key YOUR_API_KEY \
  --output check_result.json \
  --work-dir .
```

**内部流程**：
1. checker.py调用checker_execute.py执行检查
2. checker.py调用checker_score.py计算分数
3. 输出完整的check_result.json

---

### 方式2：独立调用（手动调试或重跑scoring）

#### 第1步：执行检查（生成execution_result.json）

```bash
python env/checker_execute.py \
  --sample-result sample_result.json \
  --checklist unified_scenario_design.yaml \
  --model-name claude-3-5-sonnet-20241022 \
  --api-base https://api.anthropic.com \
  --api-key YOUR_API_KEY \
  --output execution_result.json
```

**输入文件格式**（sample_result.json）：
```json
{
  "sample_id": "NW_NO_INSPIRATION_001",
  "conversation_history": [...],
  "workspace_path": "/path/to/workspace"
}
```

**输出文件格式**（execution_result.json）：
```json
{
  "sample_id": "NW_NO_INSPIRATION_001",
  "check_timestamp": 1234567890,
  "check_details": {
    "检查项1": {
      "result": "pass",
      "reason": "Agent准确识别了无灵感状态",
      "details": "找到证据关键词: 无灵感, 不知道写什么",
      "check_type": "conversation_analysis",
      "dimension_id": "intention_understanding",
      "subcategory_id": "inspiration_state_detection",
      "level": "must_have",
      "description": "Agent准确识别用户的无灵感状态"
    },
    "检查项2": {
      "result": "pass",
      "reason": "质量评分达到要求",
      "details": "开篇有强烈吸引力，Y轴标签特征明显",
      "check_type": "semantic_analysis",
      "dimension_id": "delivery_quality",
      "subcategory_id": "opening_quality",
      "level": "excellent",
      "grading": {
        "hook_strength": 4.2,
        "y_tag_visibility": 3.8
      }
    }
  }
}
```

#### 第2步：计算分数（生成check_result.json）

```bash
python env/checker_score.py \
  --execution-result execution_result.json \
  --capability-taxonomy check_capability_taxonomy.yaml \
  --output check_result.json
```

**输出文件格式**（check_result.json）：
```json
{
  "check_version": "novel_writing_v1.0",
  "sample_id": "NW_NO_INSPIRATION_001",
  "check_timestamp": 1234567890,
  "dimension_scores": {
    "format_compliance": {
      "score": 100.0,
      "pass_rate": 1.0,
      "total": 5,
      "passed": 5,
      "failed": 0,
      "skipped": 0,
      "failed_items": []
    },
    "business_rule_compliance": {
      "score": 95.0,
      "pass_rate": 0.95,
      "total": 20,
      "passed": 19,
      "failed": 1,
      "skipped": 0,
      "failed_items": ["检查项8"]
    },
    "interaction_completeness": {
      "score": 100.0,
      "pass_rate": 1.0,
      "total": 3,
      "passed": 3,
      "failed": 0,
      "skipped": 0,
      "failed_items": []
    },
    "content_quality": {
      "overall_score": 75.5,
      "quality_level": "excellent",
      "basic_layer": {
        "score": 100.0,
        "pass_rate": 1.0,
        "total": 4,
        "passed": 4,
        "failed": 0,
        "skipped": 0,
        "failed_items": []
      },
      "advanced_layer": {
        "score": 77.8,
        "pass_rate": 0.778,
        "total": 9,
        "passed": 7,
        "failed": 2,
        "skipped": 0,
        "failed_items": ["检查项30", "检查项31"]
      }
    }
  },
  "overall_result": {
    "status": "Good",
    "total_score": 92.6,
    "total_checks": 37,
    "passed_checks": 34,
    "failed_checks": 3,
    "pass_rate": 0.919
  },
  "check_details": {...},
  "completion_status": "completed"
}
```

---

## 常见使用场景

### 场景1：调整维度权重

如果需要调整维度权重计算逻辑：

1. **不需要重新执行检查**（execution_result.json已有）
2. **只需修改checker_score.py中的权重逻辑**
3. **重跑第2步**：
   ```bash
   python env/checker_score.py \
     --execution-result execution_result.json \
     --output check_result_v2.json
   ```

### 场景2：调整质量等级判断标准

如果需要调整content_quality的质量等级判断（如basic全过 + advanced≥60%即为优秀）：

1. **不需要重新执行检查**
2. **只需修改checker_score.py中的`calculate_content_quality_score`函数**
3. **重跑第2步**

### 场景3：完整评测流程（benchkit）

直接使用checker.py wrapper，内部自动调用两步：

```bash
python env/checker.py \
  --bench bench.json \
  --result result.json \
  --model claude-3-5-sonnet-20241022 \
  --base-url https://api.anthropic.com \
  --api-key YOUR_API_KEY \
  --output check_result.json
```

---

## 检查类型说明

### 1. conversation_analysis

分析对话历史，验证Agent的意图识别和工作流程遵循。

**子类型**：
- `intention_detection`：意图识别（查找evidence_keywords）
- `workflow_adherence`：工作流程遵循（检查should_not_deploy）

### 2. tool_invocation

检查Agent是否调用了期望的工具，参数是否正确。

### 3. file_content_analysis

分析workspace中的文件内容（配方卡、草稿等）。

**子类型**：
- `recipe_card_completeness`：配方卡完整性
- `recipe_diversity`：配方多样性

### 4. semantic_analysis（需要LLM）

使用LLM进行语义判断和评分。

**子类型**：
- 质量评分（quality_dimensions）：返回grading分数
- 验证规则（validation_rules）：返回matched布尔值

---

## 维度聚合规则

### 4个能力维度

1. **format_compliance**（格式规范遵循）
   - 计算方式：通过率 × 100

2. **business_rule_compliance**（业务规则遵循）
   - 计算方式：通过率 × 100

3. **interaction_completeness**（流程交互完整性）
   - 计算方式：通过率 × 100

4. **content_quality**（内容创作质量）
   - **两层体系**：
     - basic层（基础质量）：4个检查项
     - advanced层（优秀质量）：9个检查项（可选启用）
   - **质量等级计算**：
     - 不合格（0-60分）：basic层有任何失败
     - 合格（60-70分）：basic全过 + advanced通过率<70%
     - 优秀（70分以上）：basic全过 + advanced通过率≥70%

### 总分计算

4个维度等权平均（content_quality使用overall_score）。

---

## 文件清单

```
env/
├── checker.py                    # Wrapper（benchkit调用）
├── checker_execute.py            # 第1步：执行检查
├── checker_score.py              # 第2步：计算分数
└── README_CHECKER.md             # 本文档
```

---

## 版本历史

- **v1.0** (2026-02-02): 初始版本，拆分checker为execute + score两阶段
