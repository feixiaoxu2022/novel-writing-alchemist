#!/usr/bin/env python3
"""
小说创作Agent评测结果查看器 - Python服务器
不需要PHP，使用Python内置的http.server
"""

import os
import json
import glob
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import socket

class ViewerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        # API: 列出所有test_results目录
        if parsed_path.path == '/api/list-results':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # 查找viewer_results目录下的所有测试结果目录
            # viewer_server.py在viewer/子目录中，需要访问上级目录的viewer_results/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            eval_outputs_dir = os.path.join(base_dir, 'viewer_results')
            dirs = []

            if os.path.exists(eval_outputs_dir) and os.path.isdir(eval_outputs_dir):
                for item in os.listdir(eval_outputs_dir):
                    item_path = os.path.join(eval_outputs_dir, item)
                    if os.path.isdir(item_path):
                        # 检查目录中是否有有效的JSON结果文件
                        json_files = glob.glob(os.path.join(item_path, '*.json'))
                        has_valid_result = False
                        for json_file in json_files:
                            if os.path.basename(json_file) != 'execution_report.json':
                                has_valid_result = True
                                break

                        if has_valid_result:
                            # 保存相对路径：viewer_results/xxx
                            dirs.append(f'viewer_results/{item}')

            # 按修改时间倒序排序
            dirs.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)

            self.wfile.write(json.dumps(dirs, ensure_ascii=False).encode('utf-8'))
            return

        # API: 获取具体结果数据
        elif parsed_path.path == '/api/get-result':
            params = parse_qs(parsed_path.query)
            dir_name = params.get('dir', [''])[0]

            if not dir_name:
                self.send_error(400, 'Missing dir parameter')
                return

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            result_dir = os.path.join(base_dir, dir_name)

            if not os.path.isdir(result_dir):
                self.send_error(404, f'Directory not found: {dir_name}')
                return

            # 查找第一个JSON结果文件（非execution_report.json）
            json_files = glob.glob(os.path.join(result_dir, '*.json'))
            result_file = None

            for file in json_files:
                if os.path.basename(file) != 'execution_report.json':
                    result_file = file
                    break

            if not result_file or not os.path.exists(result_file):
                self.send_error(404, 'Result file not found')
                return

            # 读取主结果文件
            with open(result_file, 'r', encoding='utf-8') as f:
                result_data = json.load(f)

            # 读取交付物（workspace下的文件）
            deliverables = {}
            sample_id = result_data.get('data_id')

            if sample_id:
                workspace_dir = os.path.join(result_dir, f'{sample_id}_env', 'workspace')
                if os.path.isdir(workspace_dir):
                    deliverables = self.read_workspace_files(workspace_dir)

            # 返回完整数据
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response_data = {
                'result': result_data,
                'deliverables': deliverables,
                'directory': dir_name
            }

            self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))
            return

        # 其他请求使用默认处理（静态文件）
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def read_workspace_files(self, workspace_dir):
        """递归读取workspace目录下的所有文件"""
        files = {}

        for root, dirs, filenames in os.walk(workspace_dir):
            for filename in filenames:
                # 跳过隐藏文件和servers.json
                if filename.startswith('.') or filename == 'servers.json':
                    continue

                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, workspace_dir)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 限制文件大小，避免返回过大的数据
                    if len(content) > 100000:
                        content = content[:100000] + "\n\n... [内容过长，已截断]"

                    files[relative_path] = content
                except Exception as e:
                    files[relative_path] = f"[无法读取文件: {str(e)}]"

        return files

    def log_message(self, format, *args):
        """自定义日志格式"""
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))


def get_local_ip():
    """获取本机内网IP地址"""
    try:
        # 创建一个UDP socket连接外部地址（不实际发送数据）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def main():
    port = 8888
    # 绑定到0.0.0.0，监听所有网络接口（允许内网访问）
    server_address = ('0.0.0.0', port)

    local_ip = get_local_ip()

    print("🚀 启动小说创作Agent评测结果查看器...")
    print("")
    print(f"本机访问: http://localhost:{port}/viewer.html")
    print(f"内网访问: http://{local_ip}:{port}/viewer.html")
    print("")
    print("按 Ctrl+C 停止服务器")
    print("")

    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    httpd = HTTPServer(server_address, ViewerHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        httpd.shutdown()


if __name__ == '__main__':
    main()
