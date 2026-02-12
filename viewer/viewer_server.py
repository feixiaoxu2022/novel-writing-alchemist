#!/usr/bin/env python3
"""
小说创作Agent评测结果查看器 v2.0 - 多模型对比 + 标注系统
支持加载多个模型对同一批样本的评测结果，并提供双层标注功能
"""

import os
import json
import glob
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import socket
from datetime import datetime
from pathlib import Path


class ViewerHandlerV2(SimpleHTTPRequestHandler):
    """
    新版Viewer API Handler
    支持批次管理、多模型加载、标注系统
    """

    def __init__(self, *args, **kwargs):
        # 项目根目录
        self.project_root = Path(__file__).parent.parent
        self.samples_dirs = [
            self.project_root / 'design_v1' / 'samples',
            self.project_root / 'design_v2' / 'samples',
        ]
        self.eval_outputs_dir = self.project_root / 'evaluation_outputs'
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # API路由
        if path == '/api/v2/batches':
            return self.handle_get_batches()
        elif path.startswith('/api/v2/batch/') and path.endswith('/samples'):
            # /api/v2/batch/{batch_name}/samples
            batch_name = path.split('/')[4]
            return self.handle_get_batch_samples(batch_name)
        elif path.startswith('/api/v2/sample/'):
            # /api/v2/sample/{data_id} 或 /api/v2/sample/{data_id}/file
            parts = path.split('/')
            if len(parts) >= 5:
                data_id = parts[4]
                if len(parts) == 5:
                    # 获取样本详情
                    params = parse_qs(parsed_path.query)
                    batch_name = params.get('batch_name', [''])[0]
                    return self.handle_get_sample_detail(batch_name, data_id)
                elif len(parts) == 6 and parts[5] == 'file':
                    # 获取文件内容
                    params = parse_qs(parsed_path.query)
                    batch_name = params.get('batch_name', [''])[0]
                    model = params.get('model', [''])[0]
                    file_path = params.get('file_path', [''])[0]
                    return self.handle_get_file(batch_name, data_id, model, file_path)
        elif path.startswith('/api/v2/specs/'):
            # /api/v2/specs/{spec_name}
            spec_name = path.split('/')[4]
            return self.handle_get_spec(spec_name)

        # 静态文件
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body)

        # API路由
        if path == '/api/v2/annotation/sample':
            return self.handle_save_sample_annotation(data)
        elif path == '/api/v2/annotation/file':
            return self.handle_save_file_annotation(data)
        else:
            return self.send_json_response({'error': 'Unknown endpoint'}, 404)

    # ==================== 批次管理 ====================

    def handle_get_batches(self):
        """获取所有可用批次列表"""
        batches = []

        # 扫描evaluation_outputs目录，识别批次
        if not self.eval_outputs_dir.exists():
            return self.send_json_response({'batches': []})

        # 按批次名称分组
        batch_map = {}

        for eval_dir in self.eval_outputs_dir.iterdir():
            if not eval_dir.is_dir():
                continue

            # 解析目录名：eval_{batch_name}_{timestamp}_{model}
            # 或 {batch_name}_{timestamp}_{model}
            match = re.match(r'(?:eval_)?(.+?)_(\d{8}_\d{6})_(.+)', eval_dir.name)
            if not match:
                continue

            batch_name, timestamp, model = match.groups()

            # 过滤掉test开头和纯eval的批次
            if batch_name.startswith('test') or batch_name == 'eval':
                continue

            display_name = batch_name

            # 简化模型名（去掉时间戳后缀）
            model_simple = model

            if display_name not in batch_map:
                batch_map[display_name] = {
                    'batch_name': display_name,
                    'eval_dirs': [],
                    'models': set()
                }

            batch_map[display_name]['eval_dirs'].append(eval_dir.name)
            batch_map[display_name]['models'].add(model_simple)

        # 计算每个批次的样本数量
        for batch_name, batch_info in batch_map.items():
            # 读取samples文件（从多个目录中查找）
            samples_file = self.find_samples_file(batch_name)

            sample_count = 0
            if samples_file and samples_file.exists():
                with open(samples_file, 'r', encoding='utf-8') as f:
                    sample_count = sum(1 for _ in f)

            batches.append({
                'batch_name': batch_name,
                'sample_count': sample_count,
                'model_count': len(batch_info['models']),
                'models': sorted(list(batch_info['models']))
            })

        # 按批次名称排序
        batches.sort(key=lambda x: x['batch_name'], reverse=True)

        return self.send_json_response({'batches': batches})

    def handle_get_batch_samples(self, batch_name):
        """获取批次的样本列表（含各模型执行状态）"""
        # 读取样本文件
        samples_file = self.find_samples_file(batch_name)

        if not samples_file or not samples_file.exists():
            return self.send_json_response({'error': f'Samples file not found for batch: {batch_name}'}, 404)

        # 读取所有样本的data_id和query
        sample_infos = []
        with open(samples_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                sample = json.loads(line)
                data_id = sample.get('data_id')
                query = sample.get('query', '')

                # 生成query摘要（前100字符）
                query_summary = query[:100] + '...' if len(query) > 100 else query

                sample_infos.append({
                    'data_id': data_id,
                    'query_summary': query_summary
                })

        # 查找该批次的所有评测结果目录
        eval_dirs = self.find_batch_eval_dirs(batch_name)

        # 为每个样本加载各模型的执行状态
        samples = []
        for sample_info in sample_infos:
            data_id = sample_info['data_id']
            models = []

            for eval_dir_name in eval_dirs:
                eval_dir = self.eval_outputs_dir / eval_dir_name
                result_file = eval_dir / f'{data_id}.json'

                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result_data = json.load(f)

                    model = result_data.get('model', 'unknown')
                    status = result_data.get('execution_status', 'unknown')
                    exec_time = result_data.get('execution_time', 0)
                    has_annotation = 'manual_annotation' in result_data

                    models.append({
                        'model': model,
                        'status': status,
                        'execution_time': exec_time,
                        'has_annotation': has_annotation
                    })

            samples.append({
                'data_id': data_id,
                'query_summary': sample_info['query_summary'],
                'models': models
            })

        return self.send_json_response({
            'batch_name': batch_name,
            'samples': samples
        })

    # ==================== 样本详情 ====================

    def handle_get_sample_detail(self, batch_name, data_id):
        """获取样本的详细信息（含所有模型的执行结果）"""
        # 读取原始样本信息
        samples_file = self.find_samples_file(batch_name)

        if not samples_file or not samples_file.exists():
            return self.send_json_response({'error': f'Samples file not found: {batch_name}'}, 404)

        original_task = None
        with open(samples_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                sample = json.loads(line)
                if sample.get('data_id') == data_id:
                    original_task = {
                        'query': sample.get('query', ''),
                        'system': sample.get('system', ''),
                        'check_list': sample.get('check_list', []),
                        'user_simulator_prompt': sample.get('user_simulator_prompt', ''),
                        'environment': sample.get('environment', {})
                    }
                    break

        if not original_task:
            return self.send_json_response({'error': f'Sample not found: {data_id}'}, 404)

        # 查找该批次的所有评测结果
        eval_dirs = self.find_batch_eval_dirs(batch_name)

        models = []
        for eval_dir_name in eval_dirs:
            eval_dir = self.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'

            if not result_file.exists():
                continue

            with open(result_file, 'r', encoding='utf-8') as f:
                result_data = json.load(f)

            # 读取workspace文件
            workspace_dir = eval_dir / f'{data_id}_env' / 'workspace'
            workspace_files = {}
            if workspace_dir.exists():
                workspace_files = self.read_workspace_files(workspace_dir)

            # 提取标注信息
            sample_annotation = result_data.get('manual_annotation', {})
            file_annotations = result_data.get('file_annotations', {})

            # 读取check_result_rev003.json评测结果
            check_result = None
            env_dir = eval_dir / f'{data_id}_env'
            check_result_file = env_dir / 'check_result_rev003.json'
            if check_result_file.exists():
                try:
                    with open(check_result_file, 'r', encoding='utf-8') as f:
                        check_result = json.load(f)
                except Exception as e:
                    print(f"Failed to load check_result: {e}")

            models.append({
                'model': result_data.get('model', 'unknown'),
                'execution_status': result_data.get('execution_status', 'unknown'),
                'execution_time': result_data.get('execution_time', 0),
                'response': result_data.get('response', ''),
                'conversation_history': result_data.get('conversation_history', []),
                'tool_call_list': result_data.get('tool_call_list', []),
                'final_state': result_data.get('final_state', {}),
                'workspace_files': workspace_files,
                'sample_annotation': sample_annotation,
                'file_annotations': file_annotations,
                'check_result': check_result
            })

        return self.send_json_response({
            'data_id': data_id,
            'original_task': original_task,
            'models': models
        })

    def handle_get_file(self, batch_name, data_id, model, file_path):
        """获取特定模型的特定workspace文件内容"""
        eval_dirs = self.find_batch_eval_dirs(batch_name)

        # 找到对应模型的评测目录
        target_eval_dir = None
        for eval_dir_name in eval_dirs:
            eval_dir = self.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'

            if result_file.exists():
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                if result_data.get('model') == model:
                    target_eval_dir = eval_dir
                    break

        if not target_eval_dir:
            return self.send_json_response({'error': 'Model result not found'}, 404)

        # 读取文件
        workspace_dir = target_eval_dir / f'{data_id}_env' / 'workspace'
        file_full_path = workspace_dir / file_path

        if not file_full_path.exists():
            return self.send_json_response({'error': 'File not found'}, 404)

        try:
            with open(file_full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return self.send_json_response({'error': f'Failed to read file: {str(e)}'}, 500)

        # 读取文件标注
        result_file = target_eval_dir / f'{data_id}.json'
        with open(result_file, 'r', encoding='utf-8') as f:
            result_data = json.load(f)

        file_annotations = result_data.get('file_annotations', {})
        annotation = file_annotations.get(file_path, {})

        return self.send_json_response({
            'file_path': file_path,
            'content': content,
            'annotation': annotation
        })

    # ==================== 标注操作 ====================

    def handle_save_sample_annotation(self, data):
        """保存样本级标注"""
        batch_name = data.get('batch_name')
        data_id = data.get('data_id')
        model = data.get('model')
        annotation = data.get('annotation', {})

        if not all([batch_name, data_id, model]):
            return self.send_json_response({'error': 'Missing required parameters'}, 400)

        # 找到对应的结果文件
        eval_dirs = self.find_batch_eval_dirs(batch_name)
        result_file_path = None

        for eval_dir_name in eval_dirs:
            eval_dir = self.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'

            if result_file.exists():
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                if result_data.get('model') == model:
                    result_file_path = result_file
                    break

        if not result_file_path:
            return self.send_json_response({'error': 'Result file not found'}, 404)

        # 读取、更新、保存
        with open(result_file_path, 'r', encoding='utf-8') as f:
            result_data = json.load(f)

        # 添加时间戳
        annotation['annotated_at'] = datetime.now().isoformat()
        result_data['manual_annotation'] = annotation

        with open(result_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        return self.send_json_response({
            'success': True,
            'message': '样本标注已保存'
        })

    def handle_save_file_annotation(self, data):
        """保存文件级标注"""
        batch_name = data.get('batch_name')
        data_id = data.get('data_id')
        model = data.get('model')
        file_path = data.get('file_path')
        annotation = data.get('annotation', {})

        if not all([batch_name, data_id, model, file_path]):
            return self.send_json_response({'error': 'Missing required parameters'}, 400)

        # 找到对应的结果文件
        eval_dirs = self.find_batch_eval_dirs(batch_name)
        result_file_path = None

        for eval_dir_name in eval_dirs:
            eval_dir = self.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'

            if result_file.exists():
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                if result_data.get('model') == model:
                    result_file_path = result_file
                    break

        if not result_file_path:
            return self.send_json_response({'error': 'Result file not found'}, 404)

        # 读取、更新、保存
        with open(result_file_path, 'r', encoding='utf-8') as f:
            result_data = json.load(f)

        if 'file_annotations' not in result_data:
            result_data['file_annotations'] = {}

        # 添加时间戳
        annotation['annotated_at'] = datetime.now().isoformat()
        result_data['file_annotations'][file_path] = annotation

        with open(result_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        return self.send_json_response({
            'success': True,
            'message': '文件标注已保存'
        })

    # ==================== 规范文档 ====================

    def handle_get_spec(self, spec_name):
        """获取规范文档内容"""
        # 定义spec文件映射
        spec_files = {
            'capability': self.project_root / 'check_capability_taxonomy.yaml',
            'criteria_basic': self.project_root / 'check_definitions' / 'judge_criteria' / 'content_quality_basic.yaml',
            'criteria_emotional': self.project_root / 'check_definitions' / 'judge_criteria' / 'emotional_delivery.yaml',
        }

        if spec_name not in spec_files:
            return self.send_json_response({'error': f'Unknown spec: {spec_name}'}, 404)

        spec_file = spec_files[spec_name]
        if not spec_file.exists():
            return self.send_json_response({'error': f'Spec file not found: {spec_file}'}, 404)

        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.send_json_response({
                'spec_name': spec_name,
                'content': content
            })
        except Exception as e:
            return self.send_json_response({'error': f'Failed to read spec: {str(e)}'}, 500)

    # ==================== 辅助方法 ====================

    def find_samples_file(self, batch_name):
        """从多个样本目录中查找样本文件"""
        for samples_dir in self.samples_dirs:
            # 尝试 eval_{batch_name}.jsonl
            samples_file = samples_dir / f'eval_{batch_name}.jsonl'
            if samples_file.exists():
                return samples_file
            # 尝试 {batch_name}.jsonl
            samples_file = samples_dir / f'{batch_name}.jsonl'
            if samples_file.exists():
                return samples_file
        return None

    def find_batch_eval_dirs(self, batch_name):
        """查找批次的所有评测结果目录"""
        eval_dirs = []

        if not self.eval_outputs_dir.exists():
            return eval_dirs

        for eval_dir in self.eval_outputs_dir.iterdir():
            if not eval_dir.is_dir():
                continue

            # 匹配 eval_{batch_name}_* 或 {batch_name}_*
            if eval_dir.name.startswith(f'eval_{batch_name}_') or \
               (eval_dir.name.startswith(f'{batch_name}_') and not eval_dir.name.startswith('eval_')):
                eval_dirs.append(eval_dir.name)

        return eval_dirs

    def read_workspace_files(self, workspace_dir):
        """递归读取workspace目录下的所有文件，并按照特定顺序排序"""
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

                    files[relative_path] = content
                except Exception as e:
                    files[relative_path] = f"[无法读取文件: {str(e)}]"

        # 对文件进行排序
        def get_file_order(path):
            """定义文件排序优先级"""
            if path == 'creative_intent.json':
                return (1, 0, path)
            elif path == 'characters.json':
                return (2, 0, path)
            elif path == 'outline.json':
                return (3, 0, path)
            elif path.startswith('chapters/'):
                # 提取章节号进行数字排序
                import re
                match = re.search(r'chapter_(\d+)', path)
                chapter_num = int(match.group(1)) if match else 999
                return (4, chapter_num, path)
            elif path == 'writing_log.md':
                return (99, 0, path)
            else:
                return (50, 0, path)

        # 按优先级排序并构造有序字典
        sorted_paths = sorted(files.keys(), key=get_file_order)
        sorted_files = {path: files[path] for path in sorted_paths}

        return sorted_files

    def send_json_response(self, data, status=200):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def log_message(self, format, *args):
        """自定义日志格式"""
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))


def get_local_ip():
    """获取本机内网IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def main():
    port = 8889
    server_address = ('0.0.0.0', port)

    local_ip = get_local_ip()

    print("启动小说创作Agent评测结果查看器...")
    print("")
    print(f"本机访问: http://localhost:{port}/viewer.html")
    print(f"内网访问: http://{local_ip}:{port}/viewer.html")
    print("")
    print("按 Ctrl+C 停止服务器")
    print("")

    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    httpd = HTTPServer(server_address, ViewerHandlerV2)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        httpd.shutdown()


if __name__ == '__main__':
    main()
