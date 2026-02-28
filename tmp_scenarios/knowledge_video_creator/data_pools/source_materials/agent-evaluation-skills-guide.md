# Agent Evaluation Skills 完整指南

> 仓库地址: https://github.com/feixiaoxu2022/agent-evaluation-skills

这是一套 LLM Agent 评测的标准化流程，共 7 个步骤。

---

## 一、全局总览：谁产出什么，给谁用

```
步骤1 场景设计
    │
    ├──→ unified_scenario_design.yaml
    │       ├── entities        ──→ 步骤5（定义数据结构）
    │       ├── business_rules  ──→ 步骤2（转化为System Prompt）
    │       ├── check_items     ──→ 步骤4（实现检查逻辑）
    │       └── tools_required  ──→ 步骤3（实现MCP工具）
    │
    ▼
步骤2 业务规则编写
    │
    ├──→ BusinessRules.md       ──→ 步骤5（作为Agent的System Prompt）
    │
    ▼
步骤3 工具实现
    │
    ├──→ tools/*.py             ──→ 步骤6（Agent调用的工具）
    │
    ▼
步骤4 检查器实现
    │
    ├──→ checkers/*.py          ──→ 步骤6（验证Agent执行结果）
    │
    ▼
步骤5 样本编写
    │
    ├──→ data_pools/*.jsonl     （中间产物，根据entities填充数据）
    ├──→ samples/eval.jsonl     ──→ 步骤6（评测输入）
    │
    ▼
步骤6 评测执行
    │
    ├──→ execution/*.json       （Agent执行结果）
    ├──→ evaluation/summary.json（评测汇总）
    │
    ▼
步骤7 失败分析
    │
    └──→ analysis/*.json        （根因分析报告）
```

---

## 二、依赖关系图

```
                    ┌─────────────────────────────────────────┐
                    │         步骤1: 场景设计                   │
                    │   输出: unified_scenario_design.yaml     │
                    └─────────────────────────────────────────┘
                                        │
            ┌───────────────┬───────────┴───────────┬───────────────┐
            ▼               ▼                       ▼               ▼
    ┌──────────────┐ ┌──────────────┐      ┌──────────────┐ ┌──────────────┐
    │ business_    │ │ tools_       │      │ check_items  │ │ entities     │
    │ rules        │ │ required     │      │              │ │              │
    └──────────────┘ └──────────────┘      └──────────────┘ └──────────────┘
            │               │                       │               │
            ▼               ▼                       ▼               ▼
    ┌──────────────┐ ┌──────────────┐      ┌──────────────┐ ┌──────────────┐
    │ 步骤2:       │ │ 步骤3:       │      │ 步骤4:       │ │ 步骤5:       │
    │ 业务规则编写  │ │ 工具实现     │      │ 检查器实现    │ │ 样本编写     │
    │              │ │              │      │              │ │              │
    │ 输出:        │ │ 输出:        │      │ 输出:        │ │ 输出:        │
    │ Business     │ │ tools/*.py   │      │ checkers/    │ │ data_pools/  │
    │ Rules.md     │ │              │      │ *.py         │ │ samples/     │
    └──────────────┘ └──────────────┘      └──────────────┘ └──────────────┘
            │               │                       │               │
            └───────────────┴───────────┬───────────┴───────────────┘
                                        ▼
                    ┌─────────────────────────────────────────┐
                    │         步骤6: 评测执行                   │
                    │                                         │
                    │   输入: samples + tools + checker       │
                    │   输出: execution/*.json                │
                    │         evaluation/summary.json         │
                    └─────────────────────────────────────────┘
                                        │
                                        ▼
                    ┌─────────────────────────────────────────┐
                    │         步骤7: 失败分析                   │
                    │                                         │
                    │   输入: 失败的 execution/*.json          │
                    │   输出: analysis/*.json                 │
                    └─────────────────────────────────────────┘
```

---

## 三、每一步详解

### 步骤 1：场景设计

**做什么**：定义整个评测场景的蓝图

**输入**：业务需求（你想测什么）

**输出**：`unified_scenario_design.yaml`，包含 4 个核心部分：

| 输出内容 | 说明 | 给谁用 |
|----------|------|--------|
| `entities` | 数据结构定义（有哪些实体、每个实体有哪些字段） | → 步骤5 |
| `business_rules` | 业务规则定义（Agent要遵守什么规则） | → 步骤2 |
| `check_items` | 检查项定义（用什么方式验证、验证什么） | → 步骤4, 5 |
| `tools_required` | 工具定义（需要哪些API） | → 步骤3 |

**示例**：

```yaml
# unified_scenario_design.yaml

# 1. 实体定义 - 告诉步骤5"数据长什么样"
entities:
  - entity_name: "meeting_room"
    attributes:
      - name: "room_id"
        type: "string"
      - name: "capacity"
        type: "integer"
        constraints: "10-100"  # 约束条件，用于生成数据
      - name: "equipment"
        type: "array"
        possible_values: ["投影仪", "白板", "视频会议系统"]

# 2. 业务规则 - 告诉步骤2"要写什么规则"
business_rules:
  - rule_id: "BR001"
    name: "预订时长限制"
    constraint: "单次预订不超过8小时"
  - rule_id: "BR002"
    name: "设备确认规则"
    constraint: "有设备需求时，必须先查询设备再预订"

# 3. 检查项 - 告诉步骤4"要实现什么检查"，告诉步骤5"样本里要配什么检查"
check_items:
  - check_id: "CHK001"
    check_type: "entity_attribute_equals"  # 检查类型
    params:
      path: "create_booking.details.duration"
      operator: "<="
      expected: 8
  - check_id: "CHK002"
    check_type: "prerequisite_check_performed"  # 另一种检查类型
    params:
      prerequisite_tool: "get_room_equipment"
      target_tool: "create_booking"

# 4. 工具定义 - 告诉步骤3"要实现什么工具"
tools_required:
  - tool_name: "list_meeting_rooms"
    parameters: [date, min_capacity]
  - tool_name: "get_room_equipment"
    parameters: [room_id]
  - tool_name: "create_booking"
    parameters: [room_id, date, start_time, end_time, attendees]
```

#### 步骤1 详解：从输入到输出的推导过程

**输入详解**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              输入                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 业务需求描述（你想让 Agent 做什么）                                    │
│     ┌─────────────────────────────────────────────────────────────────┐ │
│     │ 例如：                                                          │ │
│     │ "我们需要一个会议室预订助手，用户可以查询可用会议室、              │ │
│     │  查看设备配置、预订会议室。预订时需要考虑容量匹配、                │ │
│     │  时间冲突、设备需求等。"                                         │ │
│     └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  2. 评测目标（你想测试 Agent 的哪些能力）                                  │
│     ┌─────────────────────────────────────────────────────────────────┐ │
│     │ 9 项能力中选择：                                                 │ │
│     │ □ 多模态理解      □ 复杂上下文理解    ☑ 工具使用                  │ │
│     │ ☑ 任务规划        ☑ Prompt遵循       ☑ 多轮对话管理              │ │
│     │ □ 反思与调整      □ 多源信息融合      □ 领域知识规划              │ │
│     └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  3. 难度设计方法（可选，用什么方式制造难度）                                │
│     ┌─────────────────────────────────────────────────────────────────┐ │
│     │ □ 复杂业务规则    □ 领域知识门槛      □ 人类共识任务              │ │
│     │ □ 多轮需求变更    □ 信息分层（多步推理）                          │ │
│     └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**推导过程**：

整个过程是从业务需求中逐步抽取和推导：

```
业务需求描述
     │
     ├──→ 识别实体 ──────────────→ entities
     │
     ├──→ 识别业务规则 ──────────→ business_rules
     │         │
     │         └──→ 推导检查项 ──→ check_items
     │
     └──→ 识别需要的操作 ────────→ tools_required
```

**第一步：从业务需求中识别「实体」**

思考问题：这个业务场景涉及哪些"东西"？每个"东西"有什么属性？

```
业务需求：
"用户可以查询可用会议室、查看设备配置、预订会议室。
 预订时需要考虑容量匹配、时间冲突、设备需求等。"

分析过程：
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  提到了"会议室" ──→ 这是一个实体                                         │
│      │                                                                  │
│      ├── "可用会议室" ──→ 有可用状态                                     │
│      ├── "容量匹配" ──→ 有容量属性                                       │
│      ├── "设备配置" ──→ 有设备列表                                       │
│      └── "时间冲突" ──→ 有已预订时间段                                   │
│                                                                         │
│  提到了"预订" ──→ 这也是一个实体                                         │
│      │                                                                  │
│      ├── 预订哪个会议室 ──→ room_id                                      │
│      ├── 预订什么时间 ──→ date, start_time, end_time                    │
│      └── 多少人参加 ──→ attendees                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

输出：
entities:
  - entity_name: "meeting_room"
    attributes:
      - {name: "room_id", type: "string"}
      - {name: "capacity", type: "integer", constraints: "10-100"}
      - {name: "equipment", type: "array", possible_values: ["投影仪", "白板", ...]}

  - entity_name: "booking"
    attributes:
      - {name: "room_id", type: "string"}
      - {name: "date", type: "date"}
      - {name: "start_time", type: "time"}
      - {name: "end_time", type: "time"}
      - {name: "attendees", type: "integer"}
```

**第二步：从业务需求中识别「业务规则」**

思考问题：Agent 需要遵守哪些规则？什么情况下应该怎么做？

```
业务需求：
"预订时需要考虑容量匹配、时间冲突、设备需求等。"

分析过程：
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  "容量匹配" ──→ 规则：会议室容量 >= 参会人数                              │
│                                                                         │
│  "时间冲突" ──→ 规则：不能预订已被占用的时间段                            │
│                                                                         │
│  "设备需求" ──→ 规则：如果用户要设备，必须先确认会议室有这些设备           │
│                                                                         │
│  (补充常识规则)                                                          │
│  预订时长 ──→ 规则：单次预订不超过8小时（公司规定）                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

输出：
business_rules:
  - rule_id: "BR001"
    name: "容量匹配"
    constraint: "选择的会议室容量必须 >= 参会人数"

  - rule_id: "BR002"
    name: "时间冲突检测"
    constraint: "不能预订已被占用的时间段"

  - rule_id: "BR003"
    name: "设备确认"
    constraint: "用户有设备需求时，必须先查询设备配置再预订"

  - rule_id: "BR004"
    name: "预订时长限制"
    constraint: "单次预订不超过8小时"
```

**第三步：从业务规则推导「检查项」**

思考问题：每条规则怎么验证？用什么方式检查？

```
分析过程：
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  BR001 "容量匹配"                                                        │
│      │                                                                  │
│      ├── 怎么验证？──→ 检查最终预订的会议室容量 vs 参会人数               │
│      ├── 数据在哪？──→ final_state 里 create_booking 的返回值            │
│      └── 用什么检查器？──→ entity_attribute_equals                      │
│                                                                         │
│  BR003 "设备确认"                                                        │
│      │                                                                  │
│      ├── 怎么验证？──→ 检查是否先调用了 get_equipment 再调用 create_booking
│      ├── 数据在哪？──→ tool_calls 调用记录                               │
│      └── 用什么检查器？──→ prerequisite_check_performed                 │
│                                                                         │
│  BR004 "预订时长限制"                                                     │
│      │                                                                  │
│      ├── 怎么验证？──→ 检查预订时长 <= 8                                 │
│      ├── 数据在哪？──→ final_state 或 tool_calls 的参数                  │
│      └── 用什么检查器？──→ entity_attribute_equals                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

输出：
check_items:
  - check_id: "CHK001"
    linked_rule: "BR001"
    check_type: "entity_attribute_equals"
    params:
      path: "create_booking.details.room_capacity"
      operator: ">="
      compare_to: "create_booking.details.attendees"

  - check_id: "CHK002"
    linked_rule: "BR003"
    check_type: "prerequisite_check_performed"
    params:
      prerequisite_tool: "get_room_equipment"
      target_tool: "create_booking"

  - check_id: "CHK003"
    linked_rule: "BR004"
    check_type: "entity_attribute_equals"
    params:
      path: "create_booking.details.duration_hours"
      operator: "<="
      expected: 8
```

**第四步：从业务需求中识别「需要的工具」**

思考问题：Agent 需要调用哪些 API 来完成任务？

```
业务需求：
"用户可以查询可用会议室、查看设备配置、预订会议室。"

分析过程：
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  "查询可用会议室" ──→ 需要一个工具：list_meeting_rooms                   │
│      │                                                                  │
│      └── 参数：日期、最小容量                                            │
│                                                                         │
│  "查看设备配置" ──→ 需要一个工具：get_room_equipment                     │
│      │                                                                  │
│      └── 参数：会议室ID                                                  │
│                                                                         │
│  "预订会议室" ──→ 需要一个工具：create_booking                           │
│      │                                                                  │
│      └── 参数：会议室ID、日期、开始时间、结束时间、人数、主题             │
│                                                                         │
│  (补充：检查时间是否可用)                                                 │
│  ──→ 需要一个工具：get_room_availability                                │
│      │                                                                  │
│      └── 参数：会议室ID、日期                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

输出：
tools_required:
  - tool_name: "list_meeting_rooms"
    parameters: [{name: "date", required: true}, {name: "min_capacity", required: false}]
    returns: "会议室列表"

  - tool_name: "get_room_equipment"
    parameters: [{name: "room_id", required: true}]
    returns: "设备列表"

  - tool_name: "get_room_availability"
    parameters: [{name: "room_id", required: true}, {name: "date", required: true}]
    returns: "可用时间段"

  - tool_name: "create_booking"
    parameters: [{name: "room_id"}, {name: "date"}, {name: "start_time"}, ...]
    returns: "预订结果"
```

#### 如何选择 check_type？

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     如何选择 check_type？                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  你想验证什么？                                                          │
│       │                                                                 │
│       ├── 某个值是否符合条件？                                           │
│       │   例：预订时长 <= 8小时                                          │
│       │   ──→ entity_attribute_equals                                  │
│       │                                                                 │
│       ├── 是否调用了某个工具？参数对不对？                                │
│       │   例：create_booking 的 attendees 参数是 15                     │
│       │   ──→ tool_called_with_params                                  │
│       │                                                                 │
│       ├── 工具调用顺序对不对？                                           │
│       │   例：必须先调用 get_equipment 再调用 create_booking            │
│       │   ──→ prerequisite_check_performed                             │
│       │                                                                 │
│       ├── 操作是否成功？                                                 │
│       │   例：预订是否创建成功                                           │
│       │   ──→ create_operation_verified                                │
│       │                                                                 │
│       ├── 回复里有没有关键信息？                                         │
│       │   例：回复中包含"预订成功"                                       │
│       │   ──→ response_contains_keywords                               │
│       │                                                                 │
│       └── 以上都不行，需要语义理解？                                      │
│           例：回复是否礼貌地拒绝了用户                                    │
│           ──→ semantic_check_with_llm （最后手段）                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 核心思考框架

做第一步时，按这个顺序思考：

| 顺序 | 问题 | 产出 |
|------|------|------|
| 1 | 这个业务涉及哪些"东西"？每个"东西"有什么属性？ | entities |
| 2 | Agent 必须遵守哪些规则？什么情况下应该怎么做？ | business_rules |
| 3 | 每条规则怎么验证？能自动检查吗？ | check_items |
| 4 | Agent 需要调用什么 API 来完成任务？ | tools_required |

#### 步骤1 的本质

第一步的本质是**需求分析**：

```
业务需求（自然语言）
       │
       │  分析、抽取、结构化
       ▼
unified_scenario_design.yaml（结构化定义）
       │
       ├── entities        → 数据长什么样
       ├── business_rules  → Agent要遵守什么
       ├── check_items     → 怎么验证Agent做对了
       └── tools_required  → Agent需要什么API
```

这一步做好了，后面的步骤就是"照着做"：
- 步骤2：把 business_rules 写成自然语言
- 步骤3：把 tools_required 实现成代码
- 步骤4：把 check_items 的 check_type 实现成代码
- 步骤5：把 entities 填充成具体数据，组装成样本

---

### 步骤 2：业务规则编写

**做什么**：把步骤1的 `business_rules` 转化为 Agent 能理解的 System Prompt

**输入**：步骤1 的 `business_rules`

**输出**：`BusinessRules.md`

**关键原则**：用业务语言写，不暴露技术细节

```
步骤1 的 business_rules          步骤2 的 BusinessRules.md
┌─────────────────────────┐      ┌─────────────────────────────────────┐
│ - rule_id: "BR001"      │      │ **规则1 (预订时长限制):**            │
│   name: "预订时长限制"   │ ──→  │ - 当：用户请求预订会议室              │
│   constraint: "不超过8h" │      │ - 条件：单次预订不超过8小时           │
│                         │      │ - 回复："单次预订最长8小时..."        │
└─────────────────────────┘      └─────────────────────────────────────┘
```

---

### 步骤 3：工具实现

**做什么**：把步骤1的 `tools_required` 实现为可运行的 MCP 工具

**输入**：步骤1 的 `tools_required`

**输出**：`tools/*.py`（MCP工具代码）

```
步骤1 的 tools_required          步骤3 的 tools/*.py
┌─────────────────────────┐      ┌─────────────────────────────────────┐
│ - tool_name: "create_   │      │ @server.tool()                      │
│   booking"              │ ──→  │ async def create_booking(           │
│   parameters:           │      │     room_id, date, start_time, ...  │
│     - room_id           │      │ ):                                  │
│     - date              │      │     # 实现预订逻辑                    │
│     - start_time        │      │     return {"success": True, ...}   │
└─────────────────────────┘      └─────────────────────────────────────┘
```

---

### 步骤 4：检查器实现

**做什么**：实现步骤1中 `check_items` 定义的各种 `check_type` 的通用检查逻辑

**输入**：步骤1 的 `check_items`（只看 `check_type`，不看具体参数）

**输出**：`checkers/*.py`（检查器代码）

**关键理解**：检查器是**通用代码**，不依赖具体数据

```
步骤1 定义了这些 check_type:
┌─────────────────────────────────────────┐
│ check_items:                            │
│   - check_type: "entity_attribute_equals"│
│   - check_type: "prerequisite_check_performed"
│   - check_type: "tool_called_with_params"│
└─────────────────────────────────────────┘
                    │
                    │ 步骤4 为每种 check_type 实现通用逻辑
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ class Checker:                                                  │
│                                                                 │
│     def entity_attribute_equals(self, params, execution_result):│
│         """通用逻辑：从结果中取值，与期望值比较"""                  │
│         path = params["path"]                                   │
│         operator = params["operator"]                           │
│         expected = params["expected"]                           │
│         actual = get_value(execution_result, path)  # 运行时传入│
│         return compare(actual, operator, expected)              │
│                                                                 │
│     def prerequisite_check_performed(self, params, execution_result):
│         """通用逻辑：检查工具调用顺序"""                           │
│         prereq = params["prerequisite_tool"]                    │
│         target = params["target_tool"]                          │
│         calls = execution_result["tool_calls"]  # 运行时传入     │
│         return index_of(calls, prereq) < index_of(calls, target)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**检查器什么时候用？** → 步骤6评测执行时，拿着检查器代码 + check_items配置 + Agent执行结果，进行验证

---

### 步骤 5：样本编写

**做什么**：生成具体的评测样本

**输入**：
- 步骤1 的 `entities`（数据结构定义）
- 步骤1 的 `check_items`（检查项配置）
- 步骤2 的 `BusinessRules.md`（System Prompt）

**输出**：
- `data_pools/*.jsonl`（中间产物：具体数据）
- `samples/eval.jsonl`（最终样本）

**这一步分 3 个子步骤**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           步骤5：样本编写                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  子步骤 5.1：数据池设计                                                   │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  输入：步骤1 的 entities（数据结构）                                │  │
│  │                                                                   │  │
│  │  entities 说:                     data_pools 填:                  │  │
│  │  ┌─────────────────────────┐      ┌─────────────────────────────┐ │  │
│  │  │ meeting_room:           │      │ rooms.jsonl:                │ │  │
│  │  │   - room_id: string     │ ──→  │ {"room_id":"A101",          │ │  │
│  │  │   - capacity: 10-100    │      │  "capacity":20,             │ │  │
│  │  │   - equipment: [...]    │      │  "equipment":["投影仪"]}     │ │  │
│  │  └─────────────────────────┘      │ {"room_id":"A102",...}      │ │  │
│  │                                   └─────────────────────────────┘ │  │
│  │  输出：data_pools/*.jsonl                                         │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  子步骤 5.2：查询模板设计                                                 │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  设计用户查询的模板：                                               │  │
│  │  - "预订{date}的会议室，{attendees}人，需要{equipment}"             │  │
│  │  - "帮我订一个能容纳{attendees}人的会议室"                          │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  子步骤 5.3：组装完整样本                                                 │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  把以下内容组装成一条完整样本：                                      │  │
│  │                                                                   │  │
│  │  ┌─────────────────┐                                              │  │
│  │  │ data_pools 数据  │──┐                                          │  │
│  │  └─────────────────┘  │                                          │  │
│  │  ┌─────────────────┐  │     ┌─────────────────────────────────┐  │  │
│  │  │ 查询模板         │──┼────▶│ samples/eval.jsonl              │  │  │
│  │  └─────────────────┘  │     │                                 │  │  │
│  │  ┌─────────────────┐  │     │ {                               │  │  │
│  │  │ BusinessRules   │──┤     │   "query": "预订明天...",        │  │  │
│  │  └─────────────────┘  │     │   "system": "你是助手...",       │  │  │
│  │  ┌─────────────────┐  │     │   "environment": [...],         │  │  │
│  │  │ check_items     │──┘     │   "check_list": [...]           │  │  │
│  │  └─────────────────┘        │ }                               │  │  │
│  │                              └─────────────────────────────────┘  │  │
│  │  输出：samples/eval.jsonl                                         │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**完整样本长这样**：

```json
{
  "data_id": "booking_001",
  "query": "预订明天下午2点的会议室，15人，需要投影仪",
  "system": "你是会议室预订助手...（来自BusinessRules.md）",
  "environment": [
    {"path": "data/rooms.json", "content": [...]}  // 来自 data_pools
  ],
  "check_list": [
    {"check_type": "entity_attribute_equals", "params": {...}}  // 来自 check_items
  ]
}
```

---

### 步骤 6：评测执行

**做什么**：运行 Agent，收集结果，用 Checker 验证

**输入**：
- 步骤5 的 `samples/eval.jsonl`
- 步骤3 的 `tools/*.py`
- 步骤4 的 `checkers/*.py`

**输出**：
- `execution/{data_id}.json`（每个样本的执行结果）
- `evaluation/summary.json`（汇总统计）

**执行过程**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           步骤6：评测执行                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  阶段 6.1：Agent 执行                                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  输入样本                        Agent 执行对话                    │  │
│  │  ┌─────────────────┐            ┌─────────────────────────────┐  │  │
│  │  │ query: "预订..." │            │ User: "预订..."              │  │  │
│  │  │ system: "你是..." │  ────▶    │ Agent: 调用 list_rooms()     │  │  │
│  │  │ environment: [...│            │ Agent: 调用 get_equipment()  │  │  │
│  │  └─────────────────┘            │ Agent: 调用 create_booking() │  │  │
│  │                                  └─────────────────────────────┘  │  │
│  │                                               │                   │  │
│  │                                               ▼                   │  │
│  │                                  ┌─────────────────────────────┐  │  │
│  │                                  │ execution/booking_001.json  │  │  │
│  │                                  │                             │  │  │
│  │                                  │ conversation_history: [...] │  │  │
│  │                                  │ tool_calls: [...]           │  │  │
│  │                                  │ final_state: {              │  │  │
│  │                                  │   create_booking: {         │  │  │
│  │                                  │     success: true,          │  │  │
│  │                                  │     room_capacity: 20       │  │  │
│  │                                  │   }                         │  │  │
│  │                                  │ }                           │  │  │
│  │                                  └─────────────────────────────┘  │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  阶段 6.2：Checker 验证                                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  样本中的 check_list          Checker 代码         执行结果        │  │
│  │  (检查什么)                    (怎么检查)          (实际数据)       │  │
│  │  ┌─────────────────┐     ┌─────────────────┐  ┌─────────────────┐ │  │
│  │  │ check_type:     │     │ def entity_     │  │ final_state:    │ │  │
│  │  │   entity_attr...│     │ attribute_equals│  │   create_booking│ │  │
│  │  │ params:         │  +  │ (path, op, exp):│  +│     room_cap:20 │ │  │
│  │  │   path: room_cap│     │   actual = get()│  │                 │ │  │
│  │  │   operator: >=  │     │   return cmp()  │  │                 │ │  │
│  │  │   expected: 15  │     │                 │  │                 │ │  │
│  │  └─────────────────┘     └─────────────────┘  └─────────────────┘ │  │
│  │           │                      │                    │           │  │
│  │           └──────────────────────┼────────────────────┘           │  │
│  │                                  ▼                                │  │
│  │                        ┌─────────────────┐                        │  │
│  │                        │ 20 >= 15 = True │                        │  │
│  │                        │ 结果: PASS ✓    │                        │  │
│  │                        └─────────────────┘                        │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 步骤 7：失败分析

**做什么**：分析失败案例的根本原因

**输入**：步骤6 中失败的 `execution/*.json`

**输出**：`analysis/*.json`（根因分析报告）

**4 类失败归因**：

| 归因类型 | 含义 | 举例 |
|----------|------|------|
| Agent能力问题 | 模型没做对 | 没调用该调用的工具 |
| 样本设计问题 | 测试用例有bug | check_list配置错误 |
| 用户模拟器问题 | 模拟用户行为偏差 | 模拟器没按预期追问 |
| 系统问题 | 工具/框架bug | 工具返回格式错误 |

---

## 四、一个完整例子：从头到尾

假设我们要评测一个"会议室预订助手"：

### 步骤1 输出

```yaml
# unified_scenario_design.yaml

entities:
  - entity_name: "meeting_room"
    attributes:
      - {name: "room_id", type: "string"}
      - {name: "capacity", type: "integer", constraints: "10-100"}

business_rules:
  - rule_id: "BR001"
    constraint: "预订前必须查询设备"

check_items:
  - check_id: "CHK001"
    check_type: "prerequisite_check_performed"
    params:
      prerequisite_tool: "get_room_equipment"
      target_tool: "create_booking"

tools_required:
  - tool_name: "get_room_equipment"
  - tool_name: "create_booking"
```

### 步骤2 输出

```markdown
# BusinessRules.md

**规则1**: 当用户有设备需求时，必须先查询会议室设备配置，确认满足后再预订。
```

### 步骤3 输出

```python
# tools/booking.py

@server.tool()
async def get_room_equipment(room_id: str) -> dict:
    return {"equipment": ["投影仪", "视频会议系统"]}

@server.tool()
async def create_booking(room_id: str, ...) -> dict:
    return {"success": True, "booking_id": "BK001"}
```

### 步骤4 输出

```python
# checkers/checker.py

def prerequisite_check_performed(params, execution_result):
    """检查 prereq 工具是否在 target 工具之前调用"""
    prereq = params["prerequisite_tool"]
    target = params["target_tool"]
    tool_calls = execution_result["tool_calls"]

    prereq_idx = find_index(tool_calls, prereq)
    target_idx = find_index(tool_calls, target)

    return prereq_idx != -1 and prereq_idx < target_idx
```

### 步骤5 输出

```jsonl
# data_pools/rooms.jsonl
{"room_id": "A101", "capacity": 20}

# samples/eval.jsonl
{
  "data_id": "test_001",
  "query": "预订A101会议室，需要视频会议系统",
  "system": "（BusinessRules.md内容）",
  "environment": [{"path": "rooms.json", "content": [{"room_id": "A101"}]}],
  "check_list": [{
    "check_type": "prerequisite_check_performed",
    "params": {"prerequisite_tool": "get_room_equipment", "target_tool": "create_booking"}
  }]
}
```

### 步骤6 过程

```
Agent 执行:
1. User: "预订A101会议室，需要视频会议系统"
2. Agent: 调用 get_room_equipment("A101")  ← 第1次调用
3. Agent: 调用 create_booking("A101", ...)  ← 第2次调用

执行结果:
{
  "tool_calls": [
    {"tool": "get_room_equipment", "index": 0},
    {"tool": "create_booking", "index": 1}
  ]
}

Checker 验证:
- prereq_idx = 0 (get_room_equipment)
- target_idx = 1 (create_booking)
- 0 < 1 → PASS ✓
```

### 如果 Agent 做错了

```
Agent 执行（错误情况）:
1. User: "预订A101会议室，需要视频会议系统"
2. Agent: 直接调用 create_booking("A101", ...)  ← 没有先查设备！

执行结果:
{
  "tool_calls": [
    {"tool": "create_booking", "index": 0}  ← 只有这一个调用
  ]
}

Checker 验证:
- prereq_idx = -1 (get_room_equipment 未调用)
- -1 != -1? False → FAIL ✗
```

### 步骤7 分析

```json
{
  "failure_summary": "Agent未调用get_room_equipment就直接预订",
  "root_cause": {
    "type": "Agent能力问题",
    "dimension": "任务规划",
    "evidence": "tool_calls中缺少get_room_equipment"
  }
}
```

---

## 五、常见问题

### Q1: entities 和 data_pools 什么关系？

```
entities = 数据结构定义（像数据库的表结构）
data_pools = 具体数据（像数据库里的记录）

entities 说：meeting_room 有 room_id 和 capacity 两个字段
data_pools 填：{"room_id": "A101", "capacity": 20}
```

### Q2: check_items 和 Checker 什么关系？

```
check_items = 检查配置（检查什么、用什么方式检查）
Checker = 检查代码（各种检查方式的具体实现）

check_items 说：用 prerequisite_check_performed 方式，检查 get_room_equipment 在 create_booking 之前
Checker 实现：prerequisite_check_performed 这个方法怎么比较调用顺序
```

### Q3: final_state 从哪来？

```
final_state 是 Agent 执行过程中，调用工具后的返回结果

Agent 调用 create_booking() → 工具返回 {"success": true} → 这就是 final_state 的一部分
```

### Q4: 哪些是静态的，哪些是动态的？

| 内容 | 性质 | 何时产生 |
|------|------|----------|
| entities | 静态 | 步骤1 设计时 |
| check_items | 静态 | 步骤1 设计时 |
| Checker 代码 | 静态 | 步骤4 实现时 |
| data_pools | 静态 | 步骤5 编写时 |
| samples | 静态 | 步骤5 编写时 |
| tool_calls | **动态** | 步骤6 Agent 执行时产生 |
| final_state | **动态** | 步骤6 Agent 执行时产生 |
| 检查结果 | **动态** | 步骤6 Checker 执行时产生 |
