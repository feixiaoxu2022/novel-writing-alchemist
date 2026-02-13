#!/bin/bash
# =============================================================================
# 远程服务器一键部署脚本
# 用法: bash deploy.sh
# 在远程服务器 10.25.70.163 上运行，完成环境搭建
# =============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ========== 配置区 ==========
WORK_DIR="$HOME/novel_eval"
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"
GITHUB_REPO_NOVEL="https://${GITHUB_TOKEN}@github.com/feixiaoxu2022/novel-writing-alchemist.git"
GITHUB_REPO_BENCHMARK="https://${GITHUB_TOKEN}@github.com/feixiaoxu2022/mcp-benchmark.git"
# 代理配置（百度内网拉 GitHub / PyPI 需要）
PROXY="http://agent.baidu.com:8891"
# HTTP 文件服务端口（用于结果回传）
FILE_SERVER_PORT=9090
# ============================

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  远程评测环境一键部署${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "工作目录: $WORK_DIR"
echo ""

# Step 1: 创建工作目录
echo -e "${GREEN}[1/5] 创建工作目录...${NC}"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Step 2: 拉取代码
echo -e "${GREEN}[2/5] 拉取代码仓库...${NC}"

# 设置代理（如果需要）
if curl -s --connect-timeout 5 https://github.com > /dev/null 2>&1; then
    echo "  GitHub 直连可用"
else
    echo "  GitHub 直连不可用，启用代理..."
    export https_proxy="$PROXY"
    export http_proxy="$PROXY"
fi

if [ -d "novel-writing-alchemist" ]; then
    echo "  novel-writing-alchemist 已存在，更新 remote 并 pull..."
    cd novel-writing-alchemist
    git remote set-url origin "$GITHUB_REPO_NOVEL" 2>/dev/null || git remote add origin "$GITHUB_REPO_NOVEL"
    git pull origin main
    cd ..
else
    echo "  克隆 novel-writing-alchemist..."
    git clone "$GITHUB_REPO_NOVEL"
fi

if [ -d "mcp-benchmark" ]; then
    echo "  mcp-benchmark 已存在，更新 remote 并 pull..."
    cd mcp-benchmark
    git remote set-url origin "$GITHUB_REPO_BENCHMARK" 2>/dev/null || git remote add origin "$GITHUB_REPO_BENCHMARK"
    git pull origin main
    cd ..
else
    echo "  克隆 mcp-benchmark..."
    git clone "$GITHUB_REPO_BENCHMARK"
fi

# mcp-benchmark 仓库根目录即是 release 内容(framework/ 在根目录下)
# 创建兼容软链接: mcp-benchmark/release -> mcp-benchmark
if [ ! -e "mcp-benchmark/release" ]; then
    ln -s "$(pwd)/mcp-benchmark" "mcp-benchmark/release"
    echo "  ✓ 创建兼容软链接: mcp-benchmark/release -> mcp-benchmark"
fi

# Step 3: 创建 Python 虚拟环境并安装依赖
echo -e "${GREEN}[3/5] 配置 Python 环境...${NC}"

cd "$WORK_DIR"

if [ -d ".venv" ]; then
    echo "  虚拟环境已存在，激活..."
else
    echo "  创建虚拟环境..."
    python3 -m venv .venv
fi

VENV_PIP="$WORK_DIR/.venv/bin/pip3"
VENV_PYTHON="$WORK_DIR/.venv/bin/python3"
echo "  Python: $VENV_PYTHON"
echo "  版本: $($VENV_PYTHON --version)"

# 升级 pip（使用代理访问 PyPI）
echo "  升级 pip..."
(export https_proxy="$PROXY"; $VENV_PIP install --upgrade pip -q)

# 安装依赖（使用代理访问 PyPI）
echo "  安装依赖包..."
(export https_proxy="$PROXY"; $VENV_PIP install -q \
    "fastmcp>=0.1.0" \
    "pydantic>=2.0" \
    "requests" \
    "litellm" \
    "jsonschema>=4.0.0" \
    "PyYAML")

# 激活虚拟环境供后续验证使用
source .venv/bin/activate

echo "  验证关键包..."
python3 -c "import fastmcp; print(f'  ✓ fastmcp {fastmcp.__version__}')"
python3 -c "import litellm; v = getattr(litellm, '__version__', 'installed'); print(f'  ✓ litellm {v}')"
python3 -c "import requests; print(f'  ✓ requests {requests.__version__}')"
python3 -c "import jsonschema; print(f'  ✓ jsonschema {jsonschema.__version__}')"

# Step 4: 修补路径配置
echo -e "${GREEN}[4/5] 修补路径配置...${NC}"

NOVEL_DIR="$WORK_DIR/novel-writing-alchemist"
FRAMEWORK_DIR="$WORK_DIR/mcp-benchmark/release/framework"
PYTHON_PATH="$WORK_DIR/.venv/bin/python3"

# 修补 servers.json 中的 Python 路径
SERVERS_JSON="$NOVEL_DIR/env/servers.json"
if [ -f "$SERVERS_JSON" ]; then
    echo "  修补 servers.json 中的 Python 路径..."
    # 用 python 做 JSON 安全修改
    python3 -c "
import json
with open('$SERVERS_JSON', 'r') as f:
    data = json.load(f)
for name, cfg in data.get('mcpServers', {}).items():
    cfg['command'] = '$PYTHON_PATH'
with open('$SERVERS_JSON', 'w') as f:
    json.dump(data, f, indent=2)
print('  ✓ servers.json 已修补: command -> $PYTHON_PATH')
"
fi

# 验证框架可导入
echo "  验证框架可导入..."
PYTHONPATH="$FRAMEWORK_DIR:$PYTHONPATH" python3 -c "
from benchkit.executor import main
print('  ✓ benchkit.executor 可导入')
" 2>/dev/null || echo -e "${YELLOW}  ⚠ benchkit.executor 导入失败，请检查 mcp-benchmark 仓库${NC}"

# Step 5: 网络连通性测试
echo -e "${GREEN}[5/5] 网络连通性测试...${NC}"

# 取消代理测试内网
unset https_proxy http_proxy

python3 -c "
import requests
try:
    r = requests.get('http://yy.dbh.baidu-int.com/v1/models', timeout=10,
                     headers={'Authorization': 'Bearer sk-3AYbtGCuXtiVmCDd8nfJoKwNibOagcDswEJiJLwJnOjwPVVF'})
    if r.status_code < 500:
        print('  ✓ LLM API (yy.dbh.baidu-int.com) 可达')
    else:
        print(f'  ⚠ LLM API 返回 {r.status_code}')
except Exception as e:
    print(f'  ✗ LLM API 不可达: {e}')
"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "目录结构:"
echo "  $WORK_DIR/"
echo "  ├── novel-writing-alchemist/   # 评测场景"
echo "  ├── mcp-benchmark/             # 评测框架"
echo "  └── .venv/                     # Python 虚拟环境"
echo ""
echo "下一步:"
echo "  1. 运行评测:  bash $NOVEL_DIR/remote_deploy/run_eval.sh <模型名> <样本文件>"
echo "  2. 示例:      bash $NOVEL_DIR/remote_deploy/run_eval.sh gemini-3-pro-preview design_v2/samples/eval_dsv2.jsonl"
echo ""
