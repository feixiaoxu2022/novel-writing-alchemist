#!/bin/bash
# User Simulator集成测试脚本

set -e  # 遇到错误立即退出

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 防止休眠模式检测
if [[ "$NO_SLEEP" == "1" ]] && [[ "$CAFFEINATE_ACTIVE" != "1" ]]; then
    echo -e "${GREEN}🔋 防休眠模式已启用，使用 caffeinate 运行...${NC}"
    export CAFFEINATE_ACTIVE=1
    # 获取脚本的绝对路径
    SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
    exec caffeinate -i bash "$SCRIPT_PATH" "$@"
fi

# 解析命令行参数（智能识别参数类型）
AGENT_MODEL="${1:-deepseek-v3}"  # 默认使用deepseek-v3

# 检查是否有--resume-dir参数
RESUME_DIR=""
RESUME_FLAG=""
for arg in "$@"; do
    if [[ "$arg" == --resume-dir=* ]]; then
        RESUME_DIR="${arg#--resume-dir=}"
        RESUME_FLAG="--resume"
        break
    elif [[ "$arg" == "--resume" ]]; then
        RESUME_FLAG="--resume"
    fi
done

# 过滤掉--resume和--resume-dir后的参数列表
FILTERED_ARGS=()
for arg in "$@"; do
    if [[ "$arg" != "--resume" ]] && [[ "$arg" != --resume-dir=* ]]; then
        FILTERED_ARGS+=("$arg")
    fi
done

# 智能识别第二个参数：数字=MAX_TURNS，文件路径=SAMPLES_FILE
if [[ "${FILTERED_ARGS[1]}" =~ ^[0-9]+$ ]]; then
    # 第二个参数是数字 → MAX_TURNS
    MAX_TURNS="${FILTERED_ARGS[1]}"
    SAMPLES_FILE="${FILTERED_ARGS[2]:-samples/test_001.jsonl}"
    SIMULATOR_MODEL="${FILTERED_ARGS[3]:-${USER_SIMULATOR_MODEL:-gemini-3-pro-preview}}"
elif [[ "${FILTERED_ARGS[1]}" == *.jsonl ]] || [[ "${FILTERED_ARGS[1]}" == samples/* ]] || [[ "${FILTERED_ARGS[1]}" == */* ]]; then
    # 第二个参数是文件路径 → SAMPLES_FILE
    SAMPLES_FILE="${FILTERED_ARGS[1]}"
    MAX_TURNS="${FILTERED_ARGS[2]:-1000}"
    SIMULATOR_MODEL="${FILTERED_ARGS[3]:-${USER_SIMULATOR_MODEL:-gemini-3-pro-preview}}"
else
    # 第二个参数为空或其他 → 使用默认值
    MAX_TURNS="${FILTERED_ARGS[1]:-1000}"
    SAMPLES_FILE="${FILTERED_ARGS[2]:-samples/test_001.jsonl}"
    SIMULATOR_MODEL="${FILTERED_ARGS[3]:-${USER_SIMULATOR_MODEL:-gemini-3-pro-preview}}"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}User Simulator 集成测试${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}用法: bash run_test.sh [Agent模型] [样本文件或最大轮数] [最大轮数] [Simulator模型] [--resume-dir=目录]${NC}"
echo -e "${YELLOW}示例1: bash run_test.sh deepseek-v3 samples/eval.jsonl${NC}"
echo -e "${YELLOW}示例2: bash run_test.sh ernie-5.0 1000 samples/eval.jsonl${NC}"
echo -e "${YELLOW}示例3: bash run_test.sh gemini-3-pro-preview samples/eval.jsonl 1000 deepseek-v3${NC}"
echo -e "${YELLOW}示例4: USER_SIMULATOR_MODEL=deepseek-v3 bash run_test.sh gemini-3-pro-preview samples/eval.jsonl${NC}"
echo -e "${YELLOW}示例5: bash run_test.sh gemini-3-pro-preview samples/eval.jsonl --resume-dir=evaluation_outputs/eval_v2_20260205_141134_gemini-3-pro-preview  # Resume模式${NC}"
echo ""
echo -e "${YELLOW}防休眠模式（推荐长时间运行）：${NC}"
echo -e "${YELLOW}  NO_SLEEP=1 bash run_test.sh gemini-3-pro-preview design_v1/samples/eval.jsonl${NC}"
echo -e "${YELLOW}配合screen后台运行：${NC}"
echo -e "${YELLOW}  screen -S novel_eval${NC}"
echo -e "${YELLOW}  NO_SLEEP=1 bash run_test.sh gemini-3-pro-preview design_v1/samples/eval.jsonl 2>&1 | tee run.log${NC}"
echo -e "${YELLOW}  # 按 Ctrl+A 然后 D 脱离screen${NC}"
echo ""

# 根据模型自动选择API端点和密钥
if [[ "$AGENT_MODEL" == ernie-* ]]; then
    # ERNIE模型使用千帆API
    export OPENAI_API_KEY="bce-v3/ALTAK-mCOi62yEOQCJIvZVDI521/10000568a22b656d14d37bb80abb5da439026f1a"
    export OPENAI_BASE_URL="https://qianfan.baidubce.com/v2"

    # 模型名映射：简写 -> 完整名称
    case "$AGENT_MODEL" in
        "ernie-5.0")
            AGENT_MODEL="ernie-5.0-thinking-preview"
            echo "✓ 已将模型名映射为: $AGENT_MODEL"
            ;;
    esac

    echo "✓ 检测到ERNIE模型，使用千帆API端点: $OPENAI_BASE_URL"
elif [[ "$AGENT_MODEL" == ernie5-midtrain ]]; then
    # ERNIE5 midtrain模型使用内部API
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.226.225:8466/v1"
    AGENT_MODEL="openai/EB5-0209-A35B-midtrain-128k-chat"
    echo "✓ 检测到ernie5-midtrain模型，使用内部API端点: $OPENAI_BASE_URL"
    echo "✓ 已将模型名映射为: $AGENT_MODEL"
else
    # 其他模型使用内部API
    export OPENAI_API_KEY="sk-3AYbtGCuXtiVmCDd8nfJoKwNibOagcDswEJiJLwJnOjwPVVF"
    export OPENAI_BASE_URL="http://yy.dbh.baidu-int.com/v1"
fi

# User Simulator模型配置
export USER_SIMULATOR_MODEL="$SIMULATOR_MODEL"
export USER_SIMULATOR_MODEL_API_KEY="sk-3AYbtGCuXtiVmCDd8nfJoKwNibOagcDswEJiJLwJnOjwPVVF"
export USER_SIMULATOR_MODEL_BASE_URL="http://yy.dbh.baidu-int.com/v1"

# 路径配置
FRAMEWORK_PATH="/Users/feixiaoxu01/Documents/agents/agent_auto_evaluation/universal_scenario_framework/mcp-benchmark/release/framework"
SCENARIO_DIR="."

# 验证样本文件存在
if [ ! -f "$SAMPLES_FILE" ]; then
    echo -e "${RED}错误: 样本文件不存在: $SAMPLES_FILE${NC}"
    exit 1
fi

# 提取样本批次名（从文件名提取，如test_001.jsonl -> test_001）
SAMPLE_BATCH=$(basename "$SAMPLES_FILE" .jsonl)

# 确定输出目录
OUTPUT_BASE_DIR="evaluation_outputs"
if [ -n "$RESUME_DIR" ]; then
    # Resume模式：使用指定的目录
    RESULTS_DIR="$RESUME_DIR"
    LOG_FILE="${RESULTS_DIR}/resume_execution.log"
else
    # 正常模式：生成时间戳目录
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    MODEL_SUFFIX=$(echo "$AGENT_MODEL" | sed 's/\//_/g')
    OUTPUT_DIR_NAME="${SAMPLE_BATCH}_${TIMESTAMP}_${MODEL_SUFFIX}"
    RESULTS_DIR="${OUTPUT_BASE_DIR}/${OUTPUT_DIR_NAME}"
    LOG_FILE="${RESULTS_DIR}/execution.log"
fi

# 确保输出目录存在
mkdir -p "$RESULTS_DIR"

# 设置Python路径，使benchkit模块可被导入
export PYTHONPATH="$FRAMEWORK_PATH:$PYTHONPATH"

# 抑制litellm的冗余日志（Provider List等）
export LITELLM_LOG=ERROR

echo ""
echo -e "${GREEN}测试配置：${NC}"
echo "  - 场景目录: $SCENARIO_DIR"
echo "  - 样本文件: $SAMPLES_FILE"
echo "  - 样本批次: $SAMPLE_BATCH"
echo "  - 输出目录: $RESULTS_DIR"
echo "  - 日志文件: $LOG_FILE"
echo "  - Agent模型: $AGENT_MODEL"
echo "  - API端点: $OPENAI_BASE_URL"
echo "  - Simulator模型: $SIMULATOR_MODEL"
echo "  - 最大轮数: $MAX_TURNS"
if [ -n "$RESUME_DIR" ]; then
    echo "  - Resume模式: 启用（使用已有目录，跳过已完成样本）"
fi
echo ""

# 运行executor
echo -e "${GREEN}开始执行测试...${NC}"
echo ""

python3 "$FRAMEWORK_PATH/benchkit/executor.py" \
  --scenario "$SCENARIO_DIR" \
  --samples "$SAMPLES_FILE" \
  --results-dir "$RESULTS_DIR" \
  --model "$AGENT_MODEL" \
  --base-url "$OPENAI_BASE_URL" \
  --api-key "$OPENAI_API_KEY" \
  --max-turns "$MAX_TURNS" \
  $RESUME_FLAG \
  --verbose 2>&1 | tee "$LOG_FILE"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ 测试执行完成！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "查看结果："
    echo "  - 执行日志: $LOG_FILE"
    echo "  - 结果目录: $RESULTS_DIR"
    echo ""

    # 显示结果摘要
    FIRST_RESULT=$(ls "$RESULTS_DIR"/*.json 2>/dev/null | head -1)
    if [ -f "$FIRST_RESULT" ]; then
        echo -e "${GREEN}样本执行状态（第一个样本）：${NC}"
        python3 -c "
import json
with open('$FIRST_RESULT', 'r', encoding='utf-8') as f:
    result = json.load(f)
    print(f\"  - data_id: {result.get('data_id')}\")
    print(f\"  - model: {result.get('model')}\")
    print(f\"  - execution_status: {result.get('execution_status')}\")
    print(f\"  - execution_time: {result.get('execution_time', 0):.1f}s\")
    print(f\"  - tool_call数量: {len(result.get('tool_call_list', []))}\")
    print(f\"  - 对话轮数: {len([m for m in result.get('conversation_history', []) if m.get('role') == 'user'])}\")
"
        # 统计总样本数
        TOTAL_SAMPLES=$(ls "$RESULTS_DIR"/*.json 2>/dev/null | wc -l)
        echo "  - 总样本数: $TOTAL_SAMPLES"
    fi

    # 检查关键日志
    echo ""
    echo -e "${YELLOW}关键日志检查：${NC}"
    if grep -q "\[HITL检测-Tool模式\]" "$LOG_FILE"; then
        echo "  ✓ 检测到Tool模式HITL交互"
    fi
    if grep -q "\[Callback调用-Tool模式\]" "$LOG_FILE"; then
        echo "  ✓ 检测到Tool模式回调"
    fi
    if grep -q "User Simulator已初始化" "$LOG_FILE"; then
        echo "  ✓ User Simulator初始化成功"
    fi
    if grep -q "Simulator返回响应" "$LOG_FILE"; then
        echo "  ✓ Simulator返回响应"
    fi

else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}❌ 测试执行失败！${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "请查看日志: $LOG_FILE"
    exit 1
fi
