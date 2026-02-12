# Novel Writing Alchemist 测试结果查看器

## 简介

本目录包含用于查看和分析Novel Writing Alchemist场景评测结果的Web界面工具。

## 文件说明

- **viewer.html** - 前端界面，提供测试结果的可视化展示
- **viewer_server.py** - Python HTTP服务器，提供REST API接口
- **start_viewer.sh** - 启动脚本

## 功能特性

### 测试结果列表
- 自动扫描 `evaluation_outputs/` 目录下的所有评测结果
- 按修改时间倒序排列
- 显示模型名称、执行状态等关键信息

### 对话轨迹查看
- 完整展示Agent与用户模拟器的多轮对话
- 区分system、user、assistant、tool消息类型
- 高亮显示HITL交互点

### 交付物浏览
- 左侧文件树导航
- 支持点击跳转到指定文件
- 自动高亮当前浏览的文件
- 支持多种文件类型（markdown、yaml、txt等）

### 工具调用日志
- 记录所有MCP工具调用
- 显示工具名称、参数、返回结果
- 便于调试和问题定位

## 使用方法

### 启动服务

```bash
./start_viewer.sh
```

或者直接运行：

```bash
python3 viewer_server.py
```

服务将在 `http://localhost:8001` 启动。

### 访问界面

在浏览器中打开：http://localhost:8001

## 技术实现

- **后端**：Python 3 标准库 `http.server`
- **前端**：原生HTML/CSS/JavaScript，无外部依赖
- **API设计**：RESTful风格
  - `GET /api/list-results` - 获取测试结果列表
  - `GET /api/result?path=xxx` - 获取指定测试结果的详细数据

## 目录结构要求

查看器期望评测结果按以下结构组织：

```
evaluation_outputs/
├── {sample_batch}_{date}_{model}/
│   ├── NW_TEST_SIM_001.json
│   └── ...
└── ...
```

命名格式：`sample批次_日期_模型`

例如：`test_001_20260203_deepseek-v3`

## 注意事项

1. 仅用于本地开发和调试，不适合生产环境
2. 不包含认证机制，请勿暴露到公网
3. Python 3.6+ 即可运行，无需额外依赖
