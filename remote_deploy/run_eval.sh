#!/bin/bash
# =============================================================================
# 远程服务器一键评测运行脚本
# 用法: bash run_eval.sh <模型名> <样本文件> [最大轮数] [--resume-dir=目录]
# 示例: bash run_eval.sh gemini-3-pro-preview design_v2/samples/eval_dsv2.jsonl
#       bash run_eval.sh deepseek-v3 design_v2/samples/eval_dsv2.jsonl --resume-dir=evaluation_outputs/eval_dsv2_xxx
# =============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ========== 自动检测工作目录 ==========
WORK_DIR="$HOME/novel_eval"
NOVEL_DIR="$WORK_DIR/novel-writing-alchemist"
FRAMEWORK_DIR="$WORK_DIR/mcp-benchmark/release/framework"
VENV_DIR="$WORK_DIR/.venv"

# 验证部署
if [ ! -d "$NOVEL_DIR" ] || [ ! -d "$FRAMEWORK_DIR" ] || [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}错误: 环境未部署。请先运行 deploy.sh${NC}"
    exit 1
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# ========== 参数解析 ==========
AGENT_MODEL="${1:-deepseek-v3}"
SAMPLES_FILE=""
MAX_TURNS="1000"
MAX_CONCURRENCY="1"
RESUME_DIR=""
RESUME_FLAG=""

# 解析参数
shift || true
for arg in "$@"; do
    if [[ "$arg" == --resume-dir=* ]]; then
        RESUME_DIR="${arg#--resume-dir=}"
        RESUME_FLAG="--resume"
    elif [[ "$arg" == "--resume" ]]; then
        RESUME_FLAG="--resume"
    elif [[ "$arg" == *.jsonl ]] || [[ "$arg" == samples/* ]] || [[ "$arg" == design_* ]]; then
        SAMPLES_FILE="$arg"
    elif [[ "$arg" =~ ^[0-9]+$ ]]; then
        MAX_TURNS="$arg"
    fi
done

# 默认样本文件
SAMPLES_FILE="${SAMPLES_FILE:-design_v2/samples/eval_dsv2.jsonl}"

# ========== API 配置 ==========
# 根据模型选择 API
if [[ "$AGENT_MODEL" == ernie-* ]]; then
    export OPENAI_API_KEY="bce-v3/ALTAK-mCOi62yEOQCJIvZVDI521/10000568a22b656d14d37bb80abb5da439026f1a"
    export OPENAI_BASE_URL="https://qianfan.baidubce.com/v2"
    unset https_proxy
    unset HTTPS_PROXY
    export no_proxy="qianfan.baidubce.com"
    export NO_PROXY="qianfan.baidubce.com"
    case "$AGENT_MODEL" in
        "ernie-5.0") AGENT_MODEL="ernie-5.0-thinking-preview" ;;
    esac
elif [[ "$AGENT_MODEL" == ernie5-midtrain ]]; then
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.226.225:8466/v1"
    AGENT_MODEL="EB5-0209-A35B-midtrain-128k-chat"
elif [[ "$AGENT_MODEL" == eb5-flagship-midtrain ]]; then
    # EB5 旗舰版 Mid-training（8实例，MCP服务器并发受限，设4）
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.240.153:8433/v1"
    MAX_CONCURRENCY=4
    unset https_proxy; unset HTTPS_PROXY
elif [[ "$AGENT_MODEL" == eb5-full-midtrain ]]; then
    # EB5 满血版 Mid-training（16实例，MCP服务器并发受限，设4）
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.246.17:1211/v1"
    MAX_CONCURRENCY=4
    unset https_proxy; unset HTTPS_PROXY
elif [[ "$AGENT_MODEL" == eb5-lite-midtrain ]]; then
    # EB5 高效版 Mid-training（8实例，MCP服务器并发受限，设4）
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.240.42:3226/v1"
    MAX_CONCURRENCY=4
    unset https_proxy; unset HTTPS_PROXY
elif [[ "$AGENT_MODEL" == glm-creative-midtrain ]]; then
    # GLM 创作增强版 Mid-training（MCP服务器并发受限，设4）
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.232.21:8000/v1"
    AGENT_MODEL="cw_glm45air_midt2601_decay_step2762"
    MAX_CONCURRENCY=4
    unset https_proxy; unset HTTPS_PROXY
elif [[ "$AGENT_MODEL" == glm-general-midtrain ]]; then
    # GLM 综合版 Mid-training（MCP服务器并发受限，设4）
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.95.235.233:8000/v1"
    AGENT_MODEL="cw_glm45air_midt2602_decay_step2000"
    MAX_CONCURRENCY=4
    unset https_proxy; unset HTTPS_PROXY
elif [[ "$AGENT_MODEL" == glm-agent-midtrain ]]; then
    # GLM Agent Mid-training（MCP服务器并发受限，设4）
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.52.97.139:8902/v1"
    AGENT_MODEL="/root/paddlejob/workspace/env_run/RLHF/GLM_decay_0124/"
    MAX_CONCURRENCY=4
    unset https_proxy; unset HTTPS_PROXY
elif [[ "$AGENT_MODEL" == infer-ckpt ]]; then
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://10.11.153.127:8091/v1"
    AGENT_MODEL="infer-abfa7a98a29c4df3"
elif [[ "$AGENT_MODEL" == glm-* ]]; then
    export OPENAI_API_KEY="fc0dc81d18124abea8da832af681401b.QsiurjETpUArzi4C"
    export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
    # GLM 需要走代理才能连通，显式设置确保子进程继承
    export https_proxy="http://agent.baidu.com:8891"
    export HTTPS_PROXY="http://agent.baidu.com:8891"
elif [[ "$AGENT_MODEL" == kimi-* ]]; then
    export OPENAI_API_KEY="sk-1SEAgqXCSMB6mplJMKWHvz58GIS00dkS8wUDPxYnvjJNMtSy"
    export OPENAI_BASE_URL="https://api.moonshot.cn/v1"
    # Kimi 同样需要 proxy 连通外网 HTTPS
    export https_proxy="http://agent.baidu.com:8891"
    export HTTPS_PROXY="http://agent.baidu.com:8891"
else
    export OPENAI_API_KEY="sk-9l6YZYau2dgCoziKh6bWNkF0p1ho5mSVHz39jZivtMTmb48i"
    export OPENAI_BASE_URL="http://yy.dbh.baidu-int.com/v1"
fi

# User Simulator 配置
SIMULATOR_MODEL="${USER_SIMULATOR_MODEL:-gemini-3-pro-preview}"
export USER_SIMULATOR_MODEL="$SIMULATOR_MODEL"
export USER_SIMULATOR_MODEL_API_KEY="sk-9l6YZYau2dgCoziKh6bWNkF0p1ho5mSVHz39jZivtMTmb48i"
export USER_SIMULATOR_MODEL_BASE_URL="http://yy.dbh.baidu-int.com/v1"

# Framework 路径
export PYTHONPATH="$FRAMEWORK_DIR:$PYTHONPATH"
export LITELLM_LOG=ERROR

# ========== 修补 servers.json 中的 Python 路径 ==========
cd "$NOVEL_DIR"

SERVERS_JSON="$NOVEL_DIR/env/servers.json"
VENV_PYTHON="$VENV_DIR/bin/python3"
if [ -f "$SERVERS_JSON" ]; then
    CURRENT_CMD=$(python3 -c "import json; d=json.load(open('$SERVERS_JSON')); print(d['mcpServers']['novel_writing_service']['command'])" 2>/dev/null || echo "")
    if [ "$CURRENT_CMD" != "$VENV_PYTHON" ]; then
        echo -e "${YELLOW}修补 servers.json: command -> $VENV_PYTHON${NC}"
        python3 -c "
import json
with open('$SERVERS_JSON') as f:
    d = json.load(f)
d['mcpServers']['novel_writing_service']['command'] = '$VENV_PYTHON'
with open('$SERVERS_JSON', 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')
"
    fi
fi

# ========== 输出目录 ==========
if [ ! -f "$SAMPLES_FILE" ]; then
    echo -e "${RED}错误: 样本文件不存在: $SAMPLES_FILE${NC}"
    echo "可用的样本文件:"
    find . -name "*.jsonl" -path "*/samples/*" 2>/dev/null | sort
    exit 1
fi

SAMPLE_BATCH=$(basename "$SAMPLES_FILE" .jsonl)
OUTPUT_BASE_DIR="evaluation_outputs"

if [ -n "$RESUME_DIR" ]; then
    RESULTS_DIR="$RESUME_DIR"
    LOG_FILE="${RESULTS_DIR}/resume_execution.log"
else
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    MODEL_SUFFIX=$(echo "$AGENT_MODEL" | sed 's/\//_/g')
    OUTPUT_DIR_NAME="${SAMPLE_BATCH}_${TIMESTAMP}_${MODEL_SUFFIX}"
    RESULTS_DIR="${OUTPUT_BASE_DIR}/${OUTPUT_DIR_NAME}"
    LOG_FILE="${RESULTS_DIR}/execution.log"
fi

mkdir -p "$RESULTS_DIR"

# ========== 打印配置 ==========
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  远程评测执行${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  Agent 模型:     $AGENT_MODEL"
echo "  API 端点:       $OPENAI_BASE_URL"
echo "  Simulator 模型: $SIMULATOR_MODEL"
echo "  样本文件:       $SAMPLES_FILE"
echo "  输出目录:       $RESULTS_DIR"
echo "  最大轮数:       $MAX_TURNS"
echo "  并发数:         $MAX_CONCURRENCY"
if [ -n "$RESUME_DIR" ]; then
    echo "  Resume 模式:    是"
fi
echo ""

# ========== 执行评测 ==========
echo -e "${GREEN}开始执行...${NC}"
echo "（建议在 tmux/screen 中运行，防止断连中断）"
echo ""

python3 "$FRAMEWORK_DIR/benchkit/executor.py" \
    --scenario "." \
    --samples "$SAMPLES_FILE" \
    --results-dir "$RESULTS_DIR" \
    --model "$AGENT_MODEL" \
    --base-url "$OPENAI_BASE_URL" \
    --api-key "$OPENAI_API_KEY" \
    --max-turns "$MAX_TURNS" \
    --max-concurrency "$MAX_CONCURRENCY" \
    $RESUME_FLAG \
    --verbose 2>&1 | tee "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✅ 评测完成！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "结果目录: $NOVEL_DIR/$RESULTS_DIR"
    echo ""

    # 统计
    TOTAL=$(ls "$RESULTS_DIR"/*.json 2>/dev/null | grep -v execution_report | wc -l)
    SUCCESS=$(python3 -c "
import json, glob
count = 0
for f in glob.glob('$RESULTS_DIR/*.json'):
    if 'execution_report' in f: continue
    try:
        with open(f) as fh:
            if json.load(fh).get('execution_status') == 'success': count += 1
    except: pass
print(count)
" 2>/dev/null || echo "?")
    echo "  总样本: $TOTAL, 成功: $SUCCESS"
    echo ""
    echo "开启结果下载服务:"
    echo "  bash $NOVEL_DIR/remote_deploy/serve_results.sh"
else
    echo ""
    echo -e "${RED}  ❌ 评测执行失败 (exit code: $EXIT_CODE)${NC}"
    echo "  查看日志: $LOG_FILE"
    exit 1
fi
