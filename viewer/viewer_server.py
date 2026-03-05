#!/usr/bin/env python3
"""
四场景评测结果统一查看器 v3.1
支持 NWA / NTS / SD / KVC 四个场景的评测结果浏览、多模型对比、标注
"""

import os
import json
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import socket
from datetime import datetime
from pathlib import Path


class ScenarioConfig:
    """场景配置"""
    def __init__(self, config_dict):
        self.id = config_dict['id']
        self.name = config_dict['name']
        self.root = Path(config_dict['root'])
        self.samples_dirs = [self.root / d for d in config_dict['samples_dirs']]
        self.eval_outputs_dir = self.root / config_dict['eval_outputs_dir']
        self.check_result_pattern = config_dict['check_result_pattern']
        self.description = config_dict.get('description', '')


def load_scenarios(config_file=None):
    """加载场景配置

    优先级：
    1. 命令行 --config 指定的文件
    2. 同目录下的 scenarios.local.json（本地开发覆盖）
    3. 同目录下的 scenarios.json（默认）
    """
    viewer_dir = Path(__file__).parent
    if config_file:
        config_path = Path(config_file)
        if not config_path.is_absolute():
            config_path = viewer_dir / config_path
    elif (viewer_dir / 'scenarios.local.json').exists():
        config_path = viewer_dir / 'scenarios.local.json'
    else:
        config_path = viewer_dir / 'scenarios.json'

    print(f"加载配置: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return {s['id']: ScenarioConfig(s) for s in config['scenarios']}


# 全局场景配置（main() 中初始化，此处占位）
SCENARIOS = {}


class UnifiedViewerHandler(SimpleHTTPRequestHandler):
    """统一三场景 Viewer API Handler"""

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)

        # === 场景列表 ===
        if path == '/api/v3/scenarios':
            return self.handle_get_scenarios()

        # === 批次列表 ===
        # /api/v3/{scenario}/batches
        m = re.match(r'^/api/v3/(\w+)/batches$', path)
        if m:
            return self.handle_get_batches(m.group(1))

        # === 批次样本列表 ===
        # /api/v3/{scenario}/batch/{batch_name}/samples
        m = re.match(r'^/api/v3/(\w+)/batch/(.+)/samples$', path)
        if m:
            return self.handle_get_batch_samples(m.group(1), m.group(2))

        # === 样本详情 ===
        # /api/v3/{scenario}/sample/{data_id}
        m = re.match(r'^/api/v3/(\w+)/sample/([^/]+)$', path)
        if m:
            batch_name = params.get('batch_name', [''])[0]
            return self.handle_get_sample_detail(m.group(1), batch_name, m.group(2))

        # === 文件内容 ===
        # /api/v3/{scenario}/sample/{data_id}/file
        m = re.match(r'^/api/v3/(\w+)/sample/([^/]+)/file$', path)
        if m:
            batch_name = params.get('batch_name', [''])[0]
            model = params.get('model', [''])[0]
            file_path = params.get('file_path', [''])[0]
            return self.handle_get_file(m.group(1), batch_name, m.group(2), model, file_path)

        # === 图片内容（二进制）===
        # /api/v3/{scenario}/sample/{data_id}/image
        m = re.match(r'^/api/v3/(\w+)/sample/([^/]+)/image$', path)
        if m:
            batch_name = params.get('batch_name', [''])[0]
            model = params.get('model', [''])[0]
            file_path = params.get('file_path', [''])[0]
            return self.handle_get_image(m.group(1), batch_name, m.group(2), model, file_path)

        # === 分析报告 ===
        # /api/v3/{scenario}/reports
        m = re.match(r'^/api/v3/(\w+)/reports$', path)
        if m:
            return self.handle_get_reports(m.group(1))

        # /api/v3/{scenario}/report/{filename}
        m = re.match(r'^/api/v3/(\w+)/report/(.+)$', path)
        if m:
            return self.handle_get_report_content(m.group(1), m.group(2))

        # 静态文件
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        data = json.loads(body)

        # === 标注保存 ===
        m = re.match(r'^/api/v3/(\w+)/annotation/(sample|file)$', path)
        if m:
            scenario_id, ann_type = m.group(1), m.group(2)
            if ann_type == 'sample':
                return self.handle_save_sample_annotation(scenario_id, data)
            else:
                return self.handle_save_file_annotation(scenario_id, data)

        return self.send_json_response({'error': 'Unknown endpoint'}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # ==================== 场景 ====================

    def handle_get_scenarios(self):
        """返回可用场景列表"""
        scenarios = []
        for sid, sc in SCENARIOS.items():
            scenarios.append({
                'id': sc.id,
                'name': sc.name,
                'description': sc.description,
                'available': sc.root.exists()
            })
        return self.send_json_response({'scenarios': scenarios})

    # ==================== 批次管理 ====================

    def _get_scenario(self, scenario_id):
        sc = SCENARIOS.get(scenario_id)
        if not sc:
            return None
        return sc

    def handle_get_batches(self, scenario_id):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        if not sc.eval_outputs_dir.exists():
            return self.send_json_response({'batches': []})

        batch_map = {}
        for eval_dir in sc.eval_outputs_dir.iterdir():
            if not eval_dir.is_dir():
                continue

            match = re.match(r'(?:eval_)?(.+?)_(\d{8}_\d{6})_(.+)', eval_dir.name)
            if not match:
                continue

            batch_name, timestamp, model = match.groups()
            if batch_name.startswith('test') or batch_name == 'eval':
                continue

            if batch_name not in batch_map:
                batch_map[batch_name] = {
                    'batch_name': batch_name,
                    'eval_dirs': [],
                    'models': set()
                }
            batch_map[batch_name]['eval_dirs'].append(eval_dir.name)
            batch_map[batch_name]['models'].add(model)

        batches = []
        for batch_name, batch_info in batch_map.items():
            samples_file = self._find_samples_file(sc, batch_name)
            sample_count = 0
            if samples_file and samples_file.exists():
                with open(samples_file, 'r', encoding='utf-8') as f:
                    sample_count = sum(1 for line in f if line.strip())

            batches.append({
                'batch_name': batch_name,
                'sample_count': sample_count,
                'model_count': len(batch_info['models']),
                'models': sorted(list(batch_info['models']))
            })

        batches.sort(key=lambda x: x['batch_name'], reverse=True)
        return self.send_json_response({'batches': batches})

    def handle_get_batch_samples(self, scenario_id, batch_name):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        samples_file = self._find_samples_file(sc, batch_name)
        if not samples_file or not samples_file.exists():
            return self.send_json_response({'error': f'Samples file not found for batch: {batch_name}'}, 404)

        sample_infos = []
        with open(samples_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                sample = json.loads(line)
                data_id = sample.get('data_id')
                query = sample.get('query', '')
                query_summary = query[:100] + '...' if len(query) > 100 else query
                sample_infos.append({'data_id': data_id, 'query_summary': query_summary})

        eval_dirs = self._find_batch_eval_dirs(sc, batch_name)

        samples = []
        for sample_info in sample_infos:
            data_id = sample_info['data_id']
            models = []
            for eval_dir_name in eval_dirs:
                eval_dir = sc.eval_outputs_dir / eval_dir_name
                result_file = eval_dir / f'{data_id}.json'
                if result_file.exists():
                    try:
                        with open(result_file, 'r', encoding='utf-8') as f:
                            result_data = json.load(f)
                        models.append({
                            'model': result_data.get('model', 'unknown'),
                            'status': result_data.get('execution_status', 'unknown'),
                            'execution_time': result_data.get('execution_time', 0),
                            'has_annotation': 'manual_annotation' in result_data
                        })
                    except Exception:
                        pass

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

    def handle_get_sample_detail(self, scenario_id, batch_name, data_id):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        samples_file = self._find_samples_file(sc, batch_name)
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

        eval_dirs = self._find_batch_eval_dirs(sc, batch_name)

        models = []
        for eval_dir_name in eval_dirs:
            eval_dir = sc.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'
            if not result_file.exists():
                continue

            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
            except Exception:
                continue

            # 读取workspace文件
            workspace_dir = eval_dir / f'{data_id}_env' / 'workspace'
            workspace_files = {}
            if workspace_dir.exists():
                workspace_files = self._read_workspace_files(workspace_dir)

            # 读取 check_result
            check_result = None
            check_result_revision = None
            env_dir = eval_dir / f'{data_id}_env'
            if env_dir.exists():
                check_result, check_result_revision = self._load_check_result(env_dir, sc.check_result_pattern)

            models.append({
                'model': result_data.get('model', 'unknown'),
                'execution_status': result_data.get('execution_status', 'unknown'),
                'execution_time': result_data.get('execution_time', 0),
                'response': result_data.get('response', ''),
                'conversation_history': result_data.get('conversation_history', []),
                'tool_call_list': result_data.get('tool_call_list', []),
                'final_state': result_data.get('final_state', {}),
                'workspace_files': workspace_files,
                'sample_annotation': result_data.get('manual_annotation', {}),
                'file_annotations': result_data.get('file_annotations', {}),
                'check_result': check_result,
                'check_result_revision': check_result_revision
            })

        return self.send_json_response({
            'data_id': data_id,
            'original_task': original_task,
            'models': models
        })

    def handle_get_file(self, scenario_id, batch_name, data_id, model, file_path):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        eval_dirs = self._find_batch_eval_dirs(sc, batch_name)
        target_eval_dir = None

        for eval_dir_name in eval_dirs:
            eval_dir = sc.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'
            if result_file.exists():
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result_data = json.load(f)
                    if result_data.get('model') == model:
                        target_eval_dir = eval_dir
                        break
                except Exception:
                    pass

        if not target_eval_dir:
            return self.send_json_response({'error': 'Model result not found'}, 404)

        workspace_dir = target_eval_dir / f'{data_id}_env' / 'workspace'
        file_full_path = workspace_dir / file_path

        if not file_full_path.exists():
            return self.send_json_response({'error': 'File not found'}, 404)

        try:
            with open(file_full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return self.send_json_response({'error': f'Failed to read file: {str(e)}'}, 500)

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

    def handle_get_image(self, scenario_id, batch_name, data_id, model, file_path):
        """返回图片/视频二进制内容，支持 HTTP Range（视频拖进度条需要）"""
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        eval_dirs = self._find_batch_eval_dirs(sc, batch_name)
        target_eval_dir = None

        for eval_dir_name in eval_dirs:
            eval_dir = sc.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'
            if result_file.exists():
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result_data = json.load(f)
                    if result_data.get('model') == model:
                        target_eval_dir = eval_dir
                        break
                except Exception:
                    pass

        if not target_eval_dir:
            return self.send_json_response({'error': 'Model result not found'}, 404)

        workspace_dir = target_eval_dir / f'{data_id}_env' / 'workspace'
        file_full_path = workspace_dir / file_path

        if not file_full_path.exists():
            return self.send_json_response({'error': 'File not found'}, 404)

        suffix = file_full_path.suffix.lower()
        content_type_map = {
            '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.gif': 'image/gif', '.webp': 'image/webp',
            '.mp4': 'video/mp4', '.webm': 'video/webm',
        }
        content_type = content_type_map.get(suffix, 'application/octet-stream')
        file_size = file_full_path.stat().st_size

        # 解析 Range 请求头（浏览器 <video> 需要）
        range_header = self.headers.get('Range')
        try:
            if range_header and range_header.startswith('bytes='):
                start_str, _, end_str = range_header[6:].partition('-')
                start = int(start_str) if start_str else 0
                end = int(end_str) if end_str else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1
                with open(file_full_path, 'rb') as f:
                    f.seek(start)
                    data = f.read(length)
                self.send_response(206)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            else:
                with open(file_full_path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(file_size))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            return self.send_json_response({'error': f'Failed to read file: {str(e)}'}, 500)

    # ==================== 分析报告 ====================

    def handle_get_reports(self, scenario_id):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        analysis_dir = sc.root / 'analysis'
        reports = []
        if analysis_dir.exists():
            for f in sorted(analysis_dir.iterdir()):
                if f.suffix in ('.md', '.json') and f.is_file():
                    reports.append({
                        'filename': f.name,
                        'size': f.stat().st_size,
                        'modified': f.stat().st_mtime
                    })
        return self.send_json_response({'reports': reports})

    def handle_get_report_content(self, scenario_id, filename):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        report_path = sc.root / 'analysis' / filename
        if not report_path.exists():
            return self.send_json_response({'error': f'Report not found: {filename}'}, 404)

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.send_json_response({'filename': filename, 'content': content})
        except Exception as e:
            return self.send_json_response({'error': str(e)}, 500)

    # ==================== 标注 ====================

    def handle_save_sample_annotation(self, scenario_id, data):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        batch_name = data.get('batch_name')
        data_id = data.get('data_id')
        model = data.get('model')
        annotation = data.get('annotation', {})

        if not all([batch_name, data_id, model]):
            return self.send_json_response({'error': 'Missing required parameters'}, 400)

        result_file_path = self._find_model_result_file(sc, batch_name, data_id, model)
        if not result_file_path:
            return self.send_json_response({'error': 'Result file not found'}, 404)

        with open(result_file_path, 'r', encoding='utf-8') as f:
            result_data = json.load(f)

        annotation['annotated_at'] = datetime.now().isoformat()
        result_data['manual_annotation'] = annotation

        with open(result_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        return self.send_json_response({'success': True, 'message': '样本标注已保存'})

    def handle_save_file_annotation(self, scenario_id, data):
        sc = self._get_scenario(scenario_id)
        if not sc:
            return self.send_json_response({'error': f'Unknown scenario: {scenario_id}'}, 404)

        batch_name = data.get('batch_name')
        data_id = data.get('data_id')
        model = data.get('model')
        file_path = data.get('file_path')
        annotation = data.get('annotation', {})

        if not all([batch_name, data_id, model, file_path]):
            return self.send_json_response({'error': 'Missing required parameters'}, 400)

        result_file_path = self._find_model_result_file(sc, batch_name, data_id, model)
        if not result_file_path:
            return self.send_json_response({'error': 'Result file not found'}, 404)

        with open(result_file_path, 'r', encoding='utf-8') as f:
            result_data = json.load(f)

        if 'file_annotations' not in result_data:
            result_data['file_annotations'] = {}

        annotation['annotated_at'] = datetime.now().isoformat()
        result_data['file_annotations'][file_path] = annotation

        with open(result_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        return self.send_json_response({'success': True, 'message': '文件标注已保存'})

    # ==================== 辅助方法 ====================

    def _find_samples_file(self, sc, batch_name):
        """从场景的 samples 目录中查找样本文件"""
        for samples_dir in sc.samples_dirs:
            for pattern in [f'eval_{batch_name}.jsonl', f'{batch_name}.jsonl']:
                samples_file = samples_dir / pattern
                if samples_file.exists():
                    return samples_file
        return None

    def _find_batch_eval_dirs(self, sc, batch_name):
        """查找批次的所有评测结果目录，同一模型只保留时间戳最新的目录"""
        if not sc.eval_outputs_dir.exists():
            return []

        # model -> (timestamp, dir_name)
        latest = {}
        for eval_dir in sc.eval_outputs_dir.iterdir():
            if not eval_dir.is_dir():
                continue
            name = eval_dir.name
            if not (name.startswith(f'eval_{batch_name}_') or
                    (name.startswith(f'{batch_name}_') and not name.startswith('eval_'))):
                continue
            m = re.match(r'(?:eval_)?(.+?)_(\d{8}_\d{6})_(.+)', name)
            if not m:
                continue
            _, timestamp, model = m.groups()
            if model not in latest or timestamp > latest[model][0]:
                latest[model] = (timestamp, name)

        return sorted(v[1] for v in latest.values())

    def _find_model_result_file(self, sc, batch_name, data_id, model):
        """找到特定模型的结果文件路径"""
        eval_dirs = self._find_batch_eval_dirs(sc, batch_name)
        for eval_dir_name in eval_dirs:
            eval_dir = sc.eval_outputs_dir / eval_dir_name
            result_file = eval_dir / f'{data_id}.json'
            if result_file.exists():
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result_data = json.load(f)
                    if result_data.get('model') == model:
                        return result_file
                except Exception:
                    pass
        return None

    def _load_check_result(self, env_dir, pattern):
        """根据场景的 check_result 模式加载评测结果"""
        check_result = None
        revision = None

        if '*' in pattern:
            # 带通配符的模式（如 check_result_rev*.json）— 取版本号最大的
            check_files = sorted(
                env_dir.glob(pattern),
                key=lambda p: p.stem,
                reverse=True
            )
            if check_files:
                latest = check_files[0]
                rev_match = re.search(r'rev(\d+)', latest.stem)
                revision = rev_match.group(0) if rev_match else None
                try:
                    with open(latest, 'r', encoding='utf-8') as f:
                        check_result = json.load(f)
                except Exception as e:
                    print(f"Failed to load {latest.name}: {e}")
        else:
            # 固定文件名（如 check_result.json）
            check_file = env_dir / pattern
            if check_file.exists():
                try:
                    with open(check_file, 'r', encoding='utf-8') as f:
                        check_result = json.load(f)
                    # 尝试从内容中读取版本
                    revision = check_result.get('check_version')
                except Exception as e:
                    print(f"Failed to load {check_file.name}: {e}")

        return check_result, revision

    # 跳过二进制文件的扩展名（图片和视频单独处理）
    BINARY_EXTENSIONS = {'.mp3', '.wav', '.pptx', '.xlsx', '.docx', '.pdf',
                         '.zip', '.tar', '.gz'}
    # 图片扩展名：slides_png/ 下用 __image__: 标记返回，其余跳过
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    # 视频扩展名：output.mp4 和 segments/*.mp4 用 __video__: 标记返回，其余跳过
    VIDEO_EXTENSIONS = {'.mp4', '.webm'}

    def _read_workspace_files(self, workspace_dir):
        """递归读取workspace文件"""
        files = {}
        for root, dirs, filenames in os.walk(workspace_dir):
            for filename in filenames:
                if filename.startswith('.') or filename == 'servers.json':
                    continue
                suffix = os.path.splitext(filename)[1].lower()
                if suffix in self.BINARY_EXTENSIONS:
                    continue
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, workspace_dir)
                rel_normalized = relative_path.replace(os.sep, '/')
                # 图片：slides_png/ 下保留，其他跳过
                if suffix in self.IMAGE_EXTENSIONS:
                    if rel_normalized.startswith('videos/slides_png/'):
                        files[relative_path] = f'__image__:{relative_path}'
                    continue
                # 视频：output.mp4 和 segments/*.mp4 保留，其他跳过
                if suffix in self.VIDEO_EXTENSIONS:
                    if rel_normalized == 'videos/output.mp4' or \
                       rel_normalized.startswith('videos/segments/'):
                        files[relative_path] = f'__video__:{relative_path}'
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    files[relative_path] = content
                except Exception as e:
                    files[relative_path] = f"[无法读取: {str(e)}]"

        # 排序: 结构化文件优先，章节/剧本按编号排序
        def sort_key(path):
            p = path.lower()
            # NWA / NTS / SD 场景
            if 'creative_intent' in p:
                return (1, 0, path)
            elif p == 'novel_analysis.json':
                return (1, 1, path)
            elif p == 'drama_plan.json':
                return (1, 2, path)
            elif p == 'topic_brief.json':
                return (1, 3, path)
            elif 'characters' in p and p.endswith('.json'):
                return (2, 0, path)
            elif 'outline' in p and p.endswith('.json'):
                return (3, 0, path)
            elif 'chapter' in p or 'episode' in p:
                m = re.search(r'(\d+)', path)
                num = int(m.group(1)) if m else 999
                return (4, num, path)
            elif 'writing_log' in p:
                return (99, 0, path)
            # KVC 场景
            elif p == 'knowledge_analysis.json':
                return (1, 0, path)
            elif p == 'video_script.json':
                return (1, 1, path)
            elif p == 'ppt_design.json':
                return (1, 2, path)
            elif p.startswith('source_materials' + os.sep) or p.startswith('source_materials/'):
                return (2, 0, path)
            elif p.startswith('videos' + os.sep) or p.startswith('videos/'):
                m = re.search(r'(\d+)', path)
                num = int(m.group(1)) if m else 999
                return (5, num, path)
            # script 通用（NTS/SD/KVC 均可能有）
            elif 'script' in p:
                m = re.search(r'(\d+)', path)
                num = int(m.group(1)) if m else 999
                return (4, num, path)
            else:
                return (50, 0, path)

        sorted_paths = sorted(files.keys(), key=sort_key)
        return {p: files[p] for p in sorted_paths}

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def log_message(self, format, *args):
        sys.stdout.write("[%s] %s - %s\n" % (
            datetime.now().strftime('%H:%M:%S'),
            self.address_string(),
            format % args
        ))


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    import argparse
    parser = argparse.ArgumentParser(description='四场景评测结果统一查看器')
    parser.add_argument('port', nargs='?', type=int, default=8889, help='监听端口（默认 8889）')
    parser.add_argument('--config', default=None, help='指定场景配置文件（默认自动检测 scenarios.local.json 或 scenarios.json）')
    args = parser.parse_args()

    global SCENARIOS
    SCENARIOS = load_scenarios(args.config)

    port = args.port
    local_ip = get_local_ip()

    print("=" * 50)
    print("  四场景评测结果统一查看器 v3.1")
    print("=" * 50)
    print()
    print(f"本机访问: http://localhost:{port}/viewer.html")
    print(f"内网访问: http://{local_ip}:{port}/viewer.html")
    print()
    print("已加载场景:")
    for sid, sc in SCENARIOS.items():
        available = "OK" if sc.root.exists() else "NOT FOUND"
        print(f"  [{available}] {sc.name} -> {sc.root}")
    print()
    print("按 Ctrl+C 停止服务器")
    print()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    httpd = HTTPServer(('0.0.0.0', port), UnifiedViewerHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.shutdown()


if __name__ == '__main__':
    main()
