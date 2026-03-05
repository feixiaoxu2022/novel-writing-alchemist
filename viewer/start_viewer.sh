#!/bin/bash
# 启动测试结果查看器
#
# 用法:
#   bash start_viewer.sh [port] [--config scenarios.remote.json]
#
# 配置文件选择优先级:
#   1. --config 参数指定
#   2. 同目录下 scenarios.local.json（本地覆盖，不提交到 git）
#   3. 同目录下 scenarios.json（默认）

cd "$(dirname "$0")"

PORT=${1:-8889}
CONFIG_ARG=""

# 解析 --config 参数
for arg in "$@"; do
    if [[ "$arg" == --config=* ]]; then
        CONFIG_ARG="--config ${arg#--config=}"
    elif [[ "$arg" == "--config" ]]; then
        # 下一个参数是值，交给 Python 解析
        CONFIG_ARG=""
    fi
done

# 如果没有显式指定 --config，且没有 scenarios.local.json，
# 则检测是否是远程环境（/home/work 存在），自动使用 scenarios.remote.json
if [[ -z "$CONFIG_ARG" && ! -f "scenarios.local.json" ]]; then
    if [[ -d "/home/work" && -f "scenarios.remote.json" ]]; then
        CONFIG_ARG="--config scenarios.remote.json"
        echo "检测到远程环境，使用 scenarios.remote.json"
    fi
fi

PYTHON=""
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "❌ 错误: 未找到Python"
    echo "请安装Python 3"
    exit 1
fi

exec $PYTHON viewer_server.py $PORT $CONFIG_ARG
