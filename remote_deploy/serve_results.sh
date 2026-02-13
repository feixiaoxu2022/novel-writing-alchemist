#!/bin/bash
# =============================================================================
# 远程结果 HTTP 文件服务
# 用法: bash serve_results.sh [端口]
# 在评测完成后运行，开启 HTTP 服务供本地下载结果
# =============================================================================

PORT="${1:-9090}"
WORK_DIR="$HOME/novel_eval"
NOVEL_DIR="$WORK_DIR/novel-writing-alchemist"
RESULTS_DIR="$NOVEL_DIR/evaluation_outputs"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ ! -d "$RESULTS_DIR" ]; then
    echo "错误: 结果目录不存在: $RESULTS_DIR"
    exit 1
fi

# 获取服务器 IP
SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "$(hostname)")

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  评测结果 HTTP 文件服务${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "服务目录: $RESULTS_DIR"
echo "服务地址: http://${SERVER_IP}:${PORT}/"
echo ""

# 列出可下载的评测目录
echo -e "${YELLOW}可下载的评测结果:${NC}"
ls -d "$RESULTS_DIR"/*/ 2>/dev/null | while read dir; do
    dirname=$(basename "$dir")
    json_count=$(ls "$dir"/*.json 2>/dev/null | grep -v execution_report | wc -l)
    echo "  $dirname/ ($json_count 个样本)"
done
echo ""

echo "本地下载命令:"
echo "  python3 fetch_results.py --host ${SERVER_IP} --port ${PORT}"
echo ""
echo "或手动 tar 下载:"
echo "  curl http://${SERVER_IP}:${PORT}/<目录名>.tar.gz -o results.tar.gz"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
echo ""

# 创建临时的增强版 HTTP 服务（支持目录打包下载）
cd "$RESULTS_DIR"

source "$WORK_DIR/.venv/bin/activate"

python3 -c "
import http.server
import socketserver
import os
import tarfile
import io
import json

PORT = $PORT

class EnhancedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip('/')

        # /api/list -- 列出所有评测目录及其状态
        if path == 'api/list':
            result = []
            for name in sorted(os.listdir('.')):
                full = os.path.join('.', name)
                if os.path.isdir(full):
                    json_files = [f for f in os.listdir(full)
                                  if f.endswith('.json') and f != 'execution_report.json']
                    success = 0
                    for jf in json_files:
                        try:
                            with open(os.path.join(full, jf)) as fh:
                                data = json.load(fh)
                                if data.get('execution_status') == 'success':
                                    success += 1
                        except:
                            pass
                    result.append({
                        'name': name,
                        'total_samples': len(json_files),
                        'success': success,
                    })
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
            return

        # /<dirname>.tar.gz -- 打包下载整个目录
        if path.endswith('.tar.gz'):
            dirname = path[:-7]  # remove .tar.gz
            if os.path.isdir(dirname):
                self.send_response(200)
                self.send_header('Content-Type', 'application/gzip')
                self.send_header('Content-Disposition', f'attachment; filename=\"{dirname}.tar.gz\"')
                self.end_headers()
                with tarfile.open(fileobj=self.wfile, mode='w:gz') as tar:
                    tar.add(dirname, arcname=dirname)
                return
            else:
                self.send_error(404, f'Directory not found: {dirname}')
                return

        # 默认行为：文件浏览
        return super().do_GET()

with socketserver.TCPServer(('', PORT), EnhancedHandler) as httpd:
    print(f'HTTP 服务已启动: 0.0.0.0:{PORT}')
    httpd.serve_forever()
"
