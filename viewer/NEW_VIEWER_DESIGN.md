# Novel Writing Alchemist Viewer v2.0 设计文档

## 一、核心功能需求

### 1.1 多模型对比展示
- 加载某一批样本（如v2版本的14个样本）的多个模型的评测结果
- 横向对比展示同一样本在不同模型上的表现
- 展示内容包括：原始任务信息、agent执行轨迹、workspace生成文件

### 1.2 双层标注系统
- **样本级标注**：对整个样本的评测结果进行标注（如：整体质量、是否典型案例等）
- **文件级标注**：对workspace中的特定文件进行标注（如：章节质量、角色设定合理性等）
- 标注结果持久化：保存到独立字段，写回JSON文件

### 1.3 友好展示界面
- 样本列表：快速浏览所有样本的执行状态
- 详情视图：多模型横向对比
- 文件树：workspace文件结构导航
- 标注面板：便捷的标注操作界面

---

## 二、数据结构设计

### 2.1 批次配置 (Batch Config)
```json
{
  "batch_name": "eval_v2",
  "samples_file": "design_v1/samples/eval_v2.jsonl",
  "evaluation_dirs": [
    "eval_v2_20260205_132400_claude-opus-4-5-20251101",
    "eval_v2_20260205_140957_ernie-5.0-thinking-preview",
    "eval_v2_20260205_141134_gemini-3-pro-preview"
  ]
}
```

### 2.2 样本列表数据 (Sample List)
```json
{
  "batch_name": "eval_v2",
  "samples": [
    {
      "data_id": "NW_ULTRA_SHORT_ANGSTY_001",
      "query_summary": "创作一个超短篇忧伤小说...",
      "models": [
        {
          "model": "claude-opus-4-5-20251101",
          "status": "success",
          "execution_time": 1391.5,
          "has_annotation": false
        },
        {
          "model": "ernie-5.0-thinking-preview",
          "status": "success",
          "execution_time": 1523.2,
          "has_annotation": true
        }
      ]
    }
  ]
}
```

### 2.3 样本详情数据 (Sample Detail)
```json
{
  "data_id": "NW_ULTRA_SHORT_ANGSTY_001",
  "original_task": {
    "query": "...",
    "system": "...",
    "check_list": [...],
    "user_simulator_prompt": "...",
    "environment": {...}
  },
  "models": [
    {
      "model": "claude-opus-4-5-20251101",
      "execution_status": "success",
      "execution_time": 1391.5,
      "response": "...",
      "conversation_history": [...],
      "tool_call_list": [...],
      "final_state": {...},
      "workspace_files": {
        "creative_intent.json": "...",
        "characters.json": "...",
        "outline.json": "...",
        "chapters/chapter_01.md": "...",
        "chapters/chapter_02.md": "...",
        "chapters/chapter_03.md": "..."
      },
      "sample_annotation": {
        "overall_quality": "",
        "is_typical_case": false,
        "notes": ""
      },
      "file_annotations": {
        "chapters/chapter_01.md": {
          "quality_rating": "",
          "notes": ""
        }
      }
    }
  ]
}
```

### 2.4 标注数据结构 (Annotation Schema)

#### 样本级标注字段（添加到评测结果JSON的顶层）
```json
{
  "manual_annotation": {
    "annotated_at": "2026-02-05T15:30:00",
    "overall_quality": "good|fair|poor",
    "is_typical_case": true,
    "category_tags": ["tool_use_error", "creative_quality_issue"],
    "notes": "Agent在第3轮对话中..."
  }
}
```

#### 文件级标注字段（添加到每个文件的元数据）
```json
{
  "file_annotations": {
    "chapters/chapter_01.md": {
      "annotated_at": "2026-02-05T15:30:00",
      "quality_rating": "good|fair|poor",
      "issues": ["character_inconsistency", "pacing_problem"],
      "notes": "角色性格在第二段发生不合理转变..."
    }
  }
}
```

---

## 三、API接口设计

### 3.1 批次管理

#### GET /api/v2/batches
获取所有可用批次列表
```json
Response: {
  "batches": [
    {
      "batch_name": "eval_v2",
      "sample_count": 14,
      "model_count": 3,
      "models": ["claude-opus-4-5", "ernie-5.0-thinking", "gemini-3-pro"]
    }
  ]
}
```

#### GET /api/v2/batch/:batch_name/samples
获取批次的样本列表（含各模型执行状态）
```json
Response: {
  "batch_name": "eval_v2",
  "samples": [...]  // 见2.2样本列表数据
}
```

### 3.2 样本详情

#### GET /api/v2/sample/:data_id
获取样本的详细信息（含所有模型的执行结果）
```json
Query Params:
  - batch_name: 批次名称（必需）

Response: {
  "data_id": "...",
  "original_task": {...},
  "models": [...]  // 见2.3样本详情数据
}
```

#### GET /api/v2/sample/:data_id/file
获取特定模型的特定workspace文件内容
```json
Query Params:
  - batch_name: 批次名称（必需）
  - model: 模型名称（必需）
  - file_path: workspace中的文件路径（必需）

Response: {
  "file_path": "chapters/chapter_01.md",
  "content": "...",
  "annotation": {...}  // 如果有标注
}
```

### 3.3 标注操作

#### POST /api/v2/annotation/sample
保存样本级标注
```json
Request Body: {
  "batch_name": "eval_v2",
  "data_id": "NW_ULTRA_SHORT_ANGSTY_001",
  "model": "claude-opus-4-5-20251101",
  "annotation": {
    "overall_quality": "good",
    "is_typical_case": true,
    "category_tags": ["tool_use_error"],
    "notes": "..."
  }
}

Response: {
  "success": true,
  "message": "标注已保存"
}
```

#### POST /api/v2/annotation/file
保存文件级标注
```json
Request Body: {
  "batch_name": "eval_v2",
  "data_id": "NW_ULTRA_SHORT_ANGSTY_001",
  "model": "claude-opus-4-5-20251101",
  "file_path": "chapters/chapter_01.md",
  "annotation": {
    "quality_rating": "fair",
    "issues": ["character_inconsistency"],
    "notes": "..."
  }
}

Response: {
  "success": true,
  "message": "文件标注已保存"
}
```

---

## 四、前端界面设计

### 4.1 布局结构
```
+---------------------------------------+
| Header: Batch Selector + Statistics  |
+-------+-------------------------------+
| Left  |        Main Content           |
| Panel |                               |
|       | +---------------------------+ |
| Sample| | Model Tabs                | |
| List  | | [Claude] [Ernie] [Gemini] | |
|       | +---------------------------+ |
|       | | Trajectory View           | |
|       | |                           | |
|       | +---------------------------+ |
|       | | Workspace Files           | |
|       | | - creative_intent.json    | |
|       | | - chapters/chapter_01.md  | |
|       | +---------------------------+ |
|       | | Annotation Panel          | |
|       | | Sample-level + File-level | |
+-------+-------------------------------+
```

### 4.2 交互流程
1. 用户选择批次（如"eval_v2"）
2. 左侧显示样本列表，带状态标记
3. 点击样本，右侧显示多模型对比视图
4. 切换模型Tab查看不同模型的执行结果
5. 点击workspace文件查看内容
6. 在标注面板中添加/编辑标注
7. 保存标注，实时更新到JSON文件

---

## 五、实现计划

### Phase 1: 后端API实现
- [ ] 重构viewer_server.py，实现新的API接口
- [ ] 实现批次扫描和样本加载逻辑
- [ ] 实现标注的读取和保存逻辑

### Phase 2: 前端界面实现
- [ ] 重新设计viewer.html，实现多模型对比布局
- [ ] 实现样本列表和详情视图
- [ ] 实现文件查看器
- [ ] 实现标注面板

### Phase 3: 测试和优化
- [ ] 使用v2批次数据进行完整测试
- [ ] 优化性能（大文件加载、批量标注）
- [ ] 完善交互体验

---

## 六、技术栈
- 后端：Python Flask + JSON文件存储
- 前端：HTML + CSS + JavaScript（原生，无框架依赖）
- 数据格式：JSONL（样本）+ JSON（评测结果）
