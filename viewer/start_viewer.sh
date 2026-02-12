#!/bin/bash
# 启动测试结果查看器

cd "$(dirname "$0")"

# 检查是否有Python3
if command -v python3 &> /dev/null; then
    python3 viewer_server.py
elif command -v python &> /dev/null; then
    python viewer_server.py
else
    echo "❌ 错误: 未找到Python"
    echo "请安装Python 3"
    exit 1
fi
