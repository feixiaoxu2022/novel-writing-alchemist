# BenchKit User Simulator集成方案

## 1. 核心目标

升级BenchKit框架，支持LLM智能用户模拟器，实现：
- 让agent在需要用户确认时能继续执行（目的1）
- 精确验证agent的HITL交互行为（目的2：通过tool_call记录）

## 2. 支持的两种Agent交互模式

### 模式1：Tool-based HITL（结构化交互）
```python
# Agent调用
request_human_review(
    stage="配方选择",
    type="question",
    question="我生成了3个配方，请选择一个",
    options=["方案A", "方案B", "方案C"]
)

# Simulator智能评估3个配方，返回选择
# 返回: "选择方案B"
```

### 模式2：Response-based HITL（自然对话）
```python
# Agent在response中询问
"我为您生成了以下3个配方方案：
Plan A: 复仇的罪(X) × 赛博朋克+规则怪谈(Y) → ↗ 爽文
Plan B: 追逐(X) × 赛博朋克+刑侦悬疑(Y) → ↘ 虐心
Plan C: 谜(X) × 无限流+规则怪谈(Y) → ✷ 烧脑
请问您选择哪个方案？"

# Simulator智能评估，返回选择
# 返回: "选择方案A"
```

## 3. 架构设计

### 3.1 组件职责

```
┌─────────────────────────────────────────────────────┐
│ Executor (orchestrator层)                           │
│ - 初始化LLMUserSimulator                            │
│ - 提供user_input_callback给agent                   │
│ - 管理simulator的生命周期                           │
└─────────────────┬───────────────────────────────────┘
                  │ callback
                  ↓
┌─────────────────────────────────────────────────────┐
│ MCPAgent.solve()                                    │
│ - 接收user_input_callback参数（可选）              │
│ - 在两个位置检测需要用户输入：                      │
│   1. Tool调用时（检测HITL tool）                    │
│   2. 无tool调用时（检测response内容）               │
│ - 调用callback获取simulator响应                     │
│ - 注入user message继续执行                          │
└─────────────────┬───────────────────────────────────┘
                  │ tool calls
                  ↓
┌─────────────────────────────────────────────────────┐
│ MCP Service (novel_writing_service.py)              │
│ - request_human_review工具（不修改）                │
│ - 从.hitl_context.json读取答案                      │
│ - 保持原有逻辑不变                                  │
└─────────────────────────────────────────────────────┘
```

### 3.2 执行流程

**Tool-based模式流程**：
```
1. Agent调用request_human_review(stage="配方选择")
2. agent.py检测到HITL tool调用
3. 回调executor的user_input_callback
4. Executor调用simulator.step(agent_message)
5. Simulator智能评估3个配方，返回选择（如"选择方案B"）
6. Executor将选择写入.hitl_context.json
7. agent.py继续调用MCP service的request_human_review
8. MCP service读取.hitl_context.json返回答案
9. agent.py将tool_result添加到conversation
10. 继续下一轮
```

**Response-based模式流程**：
```
1. Agent在response中询问配方选择（无tool调用）
2. agent.py检测response内容包含配方选择模式
3. 回调executor的user_input_callback
4. Executor调用simulator.step(agent_response)
5. Simulator智能评估3个配方，返回选择
6. agent.py将simulator返回作为user message添加到messages
7. 继续下一轮（不break）
```

## 4. 代码实现方案

### 4.1 agent.py修改

#### 4.1.1 solve()方法签名修改

```python
def solve(
    self,
    query: str,
    system_prompt: Optional[str] = None,
    user_input_callback: Optional[Callable] = None  # 新增参数
) -> Dict[str, Any]:
```

#### 4.1.2 检测逻辑（新增方法）

```python
def _needs_user_input_via_tool(self, tool_call: Dict) -> tuple[bool, str]:
    """
    检测工具调用是否需要用户输入

    Returns:
        (needs_input, stage): 是否需要输入 + HITL阶段名称
    """
    tool_name = tool_call.get("function", {}).get("name", "")

    # 检测request_human_review工具
    if "request_human_review" in tool_name:
        # 解析参数获取stage
        arguments_str = tool_call.get("function", {}).get("arguments", "{}")
        try:
            arguments = json.loads(arguments_str)
            stage = arguments.get("stage", "")
            interaction_type = arguments.get("type", "")

            # 只对question类型的交互调用simulator
            # confirmation类型不需要（MCP service会自动返回accept）
            if interaction_type == "question":
                return True, stage
        except:
            pass

    return False, ""

def _needs_user_input_via_response(self, message: Dict) -> tuple[bool, str]:
    """
    检测response内容是否在等待用户输入

    Returns:
        (needs_input, content): 是否需要输入 + 完整response内容
    """
    content = message.get("content", "")
    if not content:
        return False, ""

    # 检测配方选择模式（支持多种表达）
    selection_keywords = ["请选择", "请问您选择", "选择哪个", "选择方案"]
    recipe_keywords = ["Plan A", "Plan B", "方案A", "方案B", "配方"]

    has_selection = any(kw in content for kw in selection_keywords)
    has_recipe = any(kw in content for kw in recipe_keywords)

    if has_selection and has_recipe:
        return True, content

    return False, ""
```

#### 4.1.3 Tool调用处理修改（在line 776-826之间插入）

```python
for tool_call in tool_calls:
    tool_id = tool_call.get("id", "")
    function = tool_call.get("function", {})
    tool_name = function.get("name", "")
    arguments_str = function.get("arguments", "{}")

    try:
        arguments = json.loads(arguments_str)
    except json.JSONDecodeError:
        arguments = {}

    # ========== 新增：检测是否需要用户输入（Tool模式） ==========
    needs_input, stage = self._needs_user_input_via_tool(tool_call)
    if needs_input and user_input_callback:
        logger.info(f"检测到HITL交互 (Tool模式): stage={stage}")

        # 回调executor获取simulator响应
        simulator_response = user_input_callback(
            trajectory=trajectory,
            tool_call=tool_call,
            stage=stage,
            mode="tool"
        )

        logger.info(f"Simulator响应: {simulator_response}")
        # simulator_response会被callback写入.hitl_context.json
        # 继续正常调用MCP service，它会读取这个答案
    # ============================================================

    logger.info(f"调用工具: {tool_name}({arguments})")

    # 通过MCP客户端调用工具（保持不变）
    tool_result = self.mcp_client.call_tool(tool_name, arguments)

    # ... 后续处理保持不变 ...
```

#### 4.1.4 无工具调用判断修改（在line 763-768修改）

```python
# 检查是否有工具调用
tool_calls = message.get("tool_calls")
if not tool_calls:
    # ========== 新增：检测response是否在等待用户输入 ==========
    needs_input, response_content = self._needs_user_input_via_response(message)

    if needs_input and user_input_callback:
        logger.info(f"检测到HITL交互 (Response模式)")

        # 回调executor获取simulator响应
        simulator_response = user_input_callback(
            trajectory=trajectory,
            response_content=response_content,
            mode="response"
        )

        logger.info(f"Simulator响应: {simulator_response}")

        # 将simulator响应作为user message添加到messages
        user_msg = {"role": "user", "content": simulator_response}
        messages.append(user_msg)
        trajectory.append(user_msg)

        # 不break，继续下一轮
        continue
    # ============================================================

    # 没有工具调用且不需要用户输入，任务完成
    final_response = message.get("content", "")
    logger.info(f"任务完成，最终回复: {final_response[:100]}...")
    break
```

### 4.2 executor.py修改

#### 4.2.1 新增simulator支持的execute函数

```python
def execute_sample_with_simulator(
    sample: Dict,
    mcp_client: MCPClient,
    agent: MCPAgent,
    results_dir: Path,
    env_dir: Optional[Path] = None,
    use_simulator: bool = False
) -> Dict:
    """
    执行单个样本（支持user simulator）

    Args:
        sample: 样本配置
        mcp_client: MCP客户端
        agent: Agent实例
        results_dir: 结果目录
        env_dir: 环境目录（MCP service所在目录）
        use_simulator: 是否使用user simulator
    """
    data_id = sample.get("data_id")
    query = sample.get("query", "")
    system_prompt = sample.get("system", "")

    # 初始化user simulator（如果需要）
    simulator = None
    user_input_callback = None

    if use_simulator:
        # 检查sample配置是否启用simulator
        simulator_config = sample.get("user_simulator_config")
        if simulator_config and simulator_config.get("enabled"):
            from benchkit.user_simulator import LLMUserSimulator

            simulator = LLMUserSimulator(
                model=simulator_config.get("model"),
                provider=simulator_config.get("provider")
            )

            # 初始化simulator
            spec_dict = {
                "prompt": simulator_config.get("prompt", ""),
                "style": simulator_config.get("style", "reactive"),
                "stop_condition": simulator_config.get("stop_condition", "STOP"),
                "max_rounds": simulator_config.get("max_rounds", 8)
            }

            simulator.reset(system_prompt, query, spec_dict)
            logger.info(f"User Simulator已初始化: {simulator_config.get('model')}")

            # 定义callback函数
            def user_input_callback(
                trajectory: List[Dict] = None,
                tool_call: Dict = None,
                response_content: str = None,
                stage: str = None,
                mode: str = None
            ) -> str:
                """
                User input callback for agent

                Args:
                    trajectory: 当前对话轨迹
                    tool_call: 工具调用信息（Tool模式）
                    response_content: Response内容（Response模式）
                    stage: HITL阶段名称（Tool模式）
                    mode: 交互模式（"tool" or "response"）
                """
                if mode == "tool":
                    # Tool模式：从tool_call中提取agent message
                    # 找到最后一条assistant message（包含工具调用的那条）
                    agent_message = None
                    for msg in reversed(trajectory):
                        if msg.get("role") == "assistant":
                            agent_message = msg.get("content", "")
                            break

                    if not agent_message:
                        agent_message = f"Agent调用了{tool_call.get('function', {}).get('name')}工具"

                elif mode == "response":
                    # Response模式：直接使用response_content
                    agent_message = response_content

                else:
                    return "继续"

                # 调用simulator获取响应
                simulator_response = simulator.step(agent_message)

                # Tool模式需要将答案写入.hitl_context.json
                if mode == "tool" and env_dir and stage:
                    hitl_context_file = env_dir / "workspace" / ".hitl_context.json"

                    # 读取现有context
                    hitl_context = {}
                    if hitl_context_file.exists():
                        with open(hitl_context_file, 'r', encoding='utf-8') as f:
                            hitl_context = json.load(f)

                    # 更新hitl_responses
                    if "hitl_responses" not in hitl_context:
                        hitl_context["hitl_responses"] = {}

                    hitl_context["hitl_responses"][stage] = {
                        "answer": simulator_response
                    }

                    # 写回文件
                    with open(hitl_context_file, 'w', encoding='utf-8') as f:
                        json.dump(hitl_context, f, ensure_ascii=False, indent=2)

                    logger.info(f"已更新.hitl_context.json: {stage} -> {simulator_response}")

                return simulator_response

    # 执行任务
    result = agent.solve(
        query=query,
        system_prompt=system_prompt,
        user_input_callback=user_input_callback  # 传入callback
    )

    # 保存结果（保持原有逻辑）
    result_data = {
        "data_id": data_id,
        "response": result.get("response", ""),
        "conversation_history": result.get("conversation_history", []),
        "tool_call_list": result.get("tool_call_list", []),
        "execution_status": result.get("execution_status", "success"),
        "workspace_path": str(env_dir / "workspace") if env_dir else ""
    }

    if result.get("error"):
        result_data["error"] = result["error"]

    return result_data
```

### 4.3 样本配置修改

#### 修改unified_scenario_design.yaml

将`hitl_responses`改为`user_simulator_config`：

```yaml
# 旧配置（硬编码答案）
user_need_templates:
  - need_template_id: NW_RECIPE_ONLY_NO_INSPIRATION
    hitl_responses:
      配方选择:
        question: 我生成了3个配方方案，请选择一个
        answer: 选择方案A  # 硬编码

# 新配置（智能simulator）
user_need_templates:
  - need_template_id: NW_RECIPE_ONLY_NO_INSPIRATION
    user_simulator_config:
      enabled: true
      model: "claude-3-5-sonnet-20241022"
      provider: "anthropic"
      style: "reactive"
      max_rounds: 8
      prompt: |
        你是一个正在寻求小说创作帮助的真实用户。你最初的需求是：

        {user_original_need}

        现在Agent为你生成了3个配方方案（Plan A、Plan B、Plan C），请评估并选择最匹配你需求的方案。

        评估维度：
        1. 情感倾向匹配 (35%)：配方的reaction_strength是否符合你的情感偏好
        2. 题材相关性 (25%)：Y轴标签是否包含你提到的题材元素
        3. 冲突匹配 (20%)：X轴模式是否与你的故事核心冲突相关
        4. 避雷红线遵守 (20%)：配方的forbidden_elements是否包含你拒绝的元素

        请用简洁自然的语言回复，如："选择方案B" 或 "用Plan A"
```

## 5. 兼容性考虑

### 5.1 向后兼容

- `user_input_callback`参数为可选，默认为None
- 当callback为None时，行为与原来完全相同
- 旧样本（使用hitl_responses）继续工作（MCP service从.hitl_context.json读取）
- 新样本（使用user_simulator_config）启用智能simulator

### 5.2 渐进式迁移

可以按场景逐步迁移：
1. 先在novel_writing场景验证
2. 逐步扩展到其他需要智能HITL的场景（如bikeshare配角投票）

## 6. 验证方案

### 6.1 Tool模式验证

1. Agent调用request_human_review(stage="配方选择")
2. 验证callback被触发
3. 验证simulator返回合理选择（基于4维度评估）
4. 验证.hitl_context.json被正确更新
5. 验证MCP service读取到正确答案
6. 验证tool_call_list中记录了request_human_review调用

### 6.2 Response模式验证

1. Agent在response中询问配方选择
2. 验证检测逻辑识别出询问模式
3. 验证simulator返回合理选择
4. 验证user message被正确添加
5. 验证对话继续进行（不break）

## 7. 优势总结

### 7.1 满足两个核心目的

✅ **目的1：让agent完成任务**
- 检测到HITL交互时，simulator提供响应
- Agent获得用户回复后继续执行
- 无需人工介入

✅ **目的2：精确验证HITL交互**
- Tool模式：checker可精确验证tool_call_list
  - 验证调用了request_human_review
  - 验证stage参数正确
  - 验证type参数正确
- Response模式：通过response内容验证
  - 虽然不如tool精确，但至少能验证agent询问了

### 7.2 架构优势

- **最小侵入**：只修改agent.py和executor.py，MCP service不变
- **清晰职责**：orchestrator管理simulator，agent负责检测和回调
- **灵活扩展**：callback机制可支持更多交互模式
- **向后兼容**：不影响现有场景和样本

## 8. 实现计划

1. ✅ 设计方案（本文档）
2. ⏳ 修改agent.py添加callback支持
3. ⏳ 修改executor.py实现simulator集成
4. ⏳ 修改unified_scenario_design.yaml样本配置
5. ⏳ 在novel_writing场景测试验证
6. ⏳ 编写测试用例和文档
