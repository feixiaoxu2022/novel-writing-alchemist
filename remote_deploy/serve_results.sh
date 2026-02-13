#!/bin/bash
# =============================================================================
# 远程 HTTP 文件服务
# 用法: bash serve_results.sh [端口]
# 服务整个 novel-writing-alchemist 目录，支持浏览/下载/日志查看/打包
# =============================================================================

PORT="${1:-9090}"
WORK_DIR="$HOME/novel_eval"
NOVEL_DIR="$WORK_DIR/novel-writing-alchemist"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ ! -d "$NOVEL_DIR" ]; then
    echo "错误: 项目目录不存在: $NOVEL_DIR"
    exit 1
fi

# 获取服务器 IP
SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "$(hostname)")

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  远程 HTTP 文件服务${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "服务根目录: $NOVEL_DIR"
echo "服务地址:   http://${SERVER_IP}:${PORT}/"
echo ""

# 列出评测目录
RESULTS_DIR="$NOVEL_DIR/evaluation_outputs"
if [ -d "$RESULTS_DIR" ]; then
    echo -e "${YELLOW}评测结果:${NC}"
    ls -d "$RESULTS_DIR"/*/ 2>/dev/null | while read dir; do
        dirname=$(basename "$dir")
        json_count=$(ls "$dir"/*.json 2>/dev/null | grep -v execution_report | wc -l)
        echo "  $dirname/ ($json_count 个样本)"
    done
    echo ""
fi

# 列出日志文件
LOGS_DIR="$NOVEL_DIR/logs"
if [ -d "$LOGS_DIR" ]; then
    echo -e "${YELLOW}日志文件:${NC}"
    ls -lh "$LOGS_DIR"/*.log 2>/dev/null | awk '{print "  " $NF " (" $5 ")"}'
    echo ""
fi

echo -e "${YELLOW}常用 API:${NC}"
echo "  列出评测结果:   curl http://${SERVER_IP}:${PORT}/api/list"
echo "  查看日志:       curl http://${SERVER_IP}:${PORT}/api/logs/<文件名>"
echo "  查看日志尾部:   curl http://${SERVER_IP}:${PORT}/api/logs/<文件名>?lines=50"
echo "  读取任意文件:   curl http://${SERVER_IP}:${PORT}/api/file/<相对路径>"
echo "  打包下载结果:   curl -o r.tar.gz http://${SERVER_IP}:${PORT}/api/tar/<评测目录名>"
echo "  浏览目录:       http://${SERVER_IP}:${PORT}/ (浏览器打开)"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
echo ""

cd "$NOVEL_DIR"

source "$WORK_DIR/.venv/bin/activate"

python3 -c "
import http.server
import socketserver
import os
import tarfile
import json
import urllib.parse

PORT = $PORT
ROOT = '$NOVEL_DIR'

class EnhancedHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        raw_path = self.path.split('?')[0].strip('/')
        query = ''
        if '?' in self.path:
            query = self.path.split('?', 1)[1]
        params = urllib.parse.parse_qs(query)

        # /api/list -- 列出评测目录
        if raw_path == 'api/list':
            eval_dir = os.path.join(ROOT, 'evaluation_outputs')
            result = []
            if os.path.isdir(eval_dir):
                for name in sorted(os.listdir(eval_dir)):
                    full = os.path.join(eval_dir, name)
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
            self._json_response(result)
            return

        # /api/logs/<filename> -- 读取日志文件
        if raw_path.startswith('api/logs/'):
            filename = raw_path[len('api/logs/'):]
            log_path = os.path.join(ROOT, 'logs', filename)
            if not os.path.isfile(log_path):
                self.send_error(404, f'Log not found: {filename}')
                return
            lines_param = params.get('lines', ['100'])[0]
            search = params.get('search', [None])[0]
            with open(log_path, 'r', errors='replace') as f:
                all_lines = f.readlines()
            if search:
                all_lines = [l for l in all_lines if search in l]
            if lines_param == 'all':
                shown = all_lines
            else:
                n = int(lines_param)
                shown = all_lines[-n:]
            self._json_response({
                'filename': filename,
                'total_lines': len(all_lines),
                'shown_lines': len(shown),
                'content': ''.join(shown)
            })
            return

        # /api/logs -- 列出所有日志文件
        if raw_path == 'api/logs':
            logs_dir = os.path.join(ROOT, 'logs')
            files = []
            if os.path.isdir(logs_dir):
                for f in sorted(os.listdir(logs_dir)):
                    fp = os.path.join(logs_dir, f)
                    if os.path.isfile(fp):
                        files.append({
                            'name': f,
                            'size': os.path.getsize(fp),
                            'modified': os.path.getmtime(fp),
                        })
            self._json_response(files)
            return

        # /api/file/<path> -- 读取任意文件（文本）
        if raw_path.startswith('api/file/'):
            rel = raw_path[len('api/file/'):]
            filepath = os.path.normpath(os.path.join(ROOT, rel))
            if not filepath.startswith(ROOT):
                self.send_error(403, 'Access denied')
                return
            if not os.path.isfile(filepath):
                self.send_error(404, f'File not found: {rel}')
                return
            try:
                with open(filepath, 'r', errors='replace') as f:
                    content = f.read()
                self._json_response({
                    'path': rel,
                    'size': os.path.getsize(filepath),
                    'content': content
                })
            except Exception as e:
                self.send_error(500, str(e))
            return

        # /api/tar/<dirname> -- 打包下载评测结果目录
        if raw_path.startswith('api/tar/'):
            dirname = raw_path[len('api/tar/'):]
            target = os.path.join(ROOT, 'evaluation_outputs', dirname)
            if not os.path.isdir(target):
                self.send_error(404, f'Directory not found: {dirname}')
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/gzip')
            self.send_header('Content-Disposition', f'attachment; filename=\"{dirname}.tar.gz\"')
            self.end_headers()
            with tarfile.open(fileobj=self.wfile, mode='w:gz') as tar:
                tar.add(target, arcname=dirname)
            return

        # /api/ls/<path> -- 列出目录内容
        if raw_path.startswith('api/ls'):
            rel = raw_path[len('api/ls'):].strip('/')
            target = os.path.normpath(os.path.join(ROOT, rel)) if rel else ROOT
            if not target.startswith(ROOT):
                self.send_error(403, 'Access denied')
                return
            if not os.path.isdir(target):
                self.send_error(404, f'Not a directory: {rel}')
                return
            entries = []
            for name in sorted(os.listdir(target)):
                fp = os.path.join(target, name)
                entries.append({
                    'name': name,
                    'type': 'dir' if os.path.isdir(fp) else 'file',
                    'size': os.path.getsize(fp) if os.path.isfile(fp) else 0,
                })
            self._json_response({'path': rel or '.', 'entries': entries})
            return

        # 默认: 静态文件浏览
        return super().do_GET()

    def _json_response(self, data):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

with socketserver.TCPServer(('', PORT), EnhancedHandler) as httpd:
    print(f'HTTP 服务已启动: 0.0.0.0:{PORT}')
    print(f'服务根目录: {ROOT}')
    httpd.serve_forever()
"
