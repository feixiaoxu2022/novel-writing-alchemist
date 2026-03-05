#!/usr/bin/env python3
"""
EB5 模型轻量负载均衡代理

功能：
- 对每个 EB5 模型的多个实例做轮询 + 故障转移
- 请求超时或失败自动切换到下一个实例
- 健康检查：连续失败 N 次的实例标记为不健康，定期恢复探测
- 三个模型各监听一个本地端口

用法：
    python3 eb5_lb_proxy.py                    # 启动全部三个代理
    python3 eb5_lb_proxy.py --model eb5-full   # 只启动 eb5-full 代理
    python3 eb5_lb_proxy.py --model eb5-lite --model eb5-flagship  # 启动指定的

端口映射：
    eb5-full:     localhost:9001 -> 16 个后端实例
    eb5-flagship: localhost:9002 -> 8 个后端实例
    eb5-lite:     localhost:9003 -> 8 个后端实例
"""

import argparse
import http.server
import json
import logging
import socket
import socketserver
import threading
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

# ============================================================
# 后端实例配置
# ============================================================

EB5_BACKENDS = {
    "eb5-full": {
        "port": 9001,
        "instances": [
            "10.95.246.228:1211", "10.95.246.228:1222",
            "10.95.246.219:1211", "10.95.246.219:1222",
            "10.95.246.17:1211",  "10.95.246.17:1222",
            "10.95.242.35:1211",  "10.95.242.35:1222",
            "10.95.240.142:1211", "10.95.240.142:1222",
            "10.95.235.226:1211", "10.95.235.226:1222",
            "10.95.236.25:1211",  "10.95.236.25:1222",
            "10.95.236.23:1211",  "10.95.236.23:1222",
        ],
    },
    "eb5-flagship": {
        "port": 9002,
        "instances": [
            "10.95.240.153:8433", "10.95.240.153:8784",
            "10.95.240.145:8433", "10.95.240.145:8784",
            "10.95.240.148:8433", "10.95.240.148:8784",
            "10.95.246.166:8433", "10.95.246.166:8784",
        ],
    },
    "eb5-lite": {
        "port": 9003,
        "instances": [
            "10.95.240.42:3211", "10.95.240.42:3222",
            "10.95.240.42:3223", "10.95.240.42:3224",
            "10.95.240.42:3225", "10.95.240.42:3226",
            "10.95.240.42:3227", "10.95.240.42:3228",
        ],
    },
}

# ============================================================
# 后端实例状态管理
# ============================================================

@dataclass
class BackendInstance:
    address: str
    healthy: bool = True
    consecutive_failures: int = 0
    last_failure_time: float = 0.0
    total_requests: int = 0
    total_failures: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    # 连续失败多少次标记为不健康
    FAILURE_THRESHOLD: int = 3
    # 不健康实例多久后重新探测（秒）
    RECOVERY_INTERVAL: float = 120.0

    def mark_success(self):
        with self.lock:
            self.consecutive_failures = 0
            self.healthy = True
            self.total_requests += 1

    def mark_failure(self):
        with self.lock:
            self.consecutive_failures += 1
            self.total_failures += 1
            self.total_requests += 1
            self.last_failure_time = time.time()
            if self.consecutive_failures >= self.FAILURE_THRESHOLD:
                self.healthy = False

    def is_available(self) -> bool:
        with self.lock:
            if self.healthy:
                return True
            # 不健康但超过恢复间隔，允许探测
            if time.time() - self.last_failure_time > self.RECOVERY_INTERVAL:
                return True
            return False


class LoadBalancer:
    """轮询 + 故障转移负载均衡器"""

    def __init__(self, model_name: str, instances: List[str], request_timeout: int = 300):
        self.model_name = model_name
        self.backends = [BackendInstance(address=addr) for addr in instances]
        self.current_index = 0
        self.index_lock = threading.Lock()
        self.request_timeout = request_timeout
        self.logger = logging.getLogger(model_name)

    def _next_index(self) -> int:
        with self.index_lock:
            idx = self.current_index
            self.current_index = (self.current_index + 1) % len(self.backends)
            return idx

    def get_available_backends(self) -> List[BackendInstance]:
        """按轮询顺序返回可用实例列表"""
        available = []
        start = self._next_index()
        for i in range(len(self.backends)):
            backend = self.backends[(start + i) % len(self.backends)]
            if backend.is_available():
                available.append(backend)
        return available

    def forward_request(self, path: str, method: str, headers: dict, body: Optional[bytes]) -> tuple:
        """
        转发请求到后端，失败自动切换。
        返回 (status_code, response_headers, response_body)
        """
        available = self.get_available_backends()
        if not available:
            # 所有实例都不可用，强制尝试所有
            self.logger.warning("所有实例不可用，强制轮询全部实例")
            available = self.backends

        last_error = None
        for backend in available:
            url = f"http://{backend.address}{path}"
            self.logger.info(f"-> {backend.address} ({method} {path})")

            try:
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers=headers,
                    method=method,
                )
                with urllib.request.urlopen(req, timeout=self.request_timeout) as resp:
                    resp_body = resp.read()
                    resp_headers = dict(resp.headers)
                    status = resp.status

                backend.mark_success()
                self.logger.info(f"<- {backend.address} OK ({status}, {len(resp_body)} bytes)")
                return status, resp_headers, resp_body

            except urllib.error.HTTPError as e:
                # HTTP 错误（4xx/5xx）- 读取错误 body 返回给客户端
                # 4xx 通常是客户端问题（如模型返回 400），不算后端故障
                error_body = e.read() if e.fp else b""
                if 400 <= e.code < 500:
                    self.logger.warning(f"<- {backend.address} HTTP {e.code} (客户端错误，不切换)")
                    backend.mark_success()  # 4xx 不算后端故障
                    return e.code, dict(e.headers), error_body
                else:
                    self.logger.warning(f"<- {backend.address} HTTP {e.code} (服务端错误，切换下一个)")
                    backend.mark_failure()
                    last_error = e

            except (urllib.error.URLError, socket.timeout, OSError) as e:
                self.logger.warning(f"<- {backend.address} 连接失败/超时: {e}")
                backend.mark_failure()
                last_error = e

            except Exception as e:
                self.logger.warning(f"<- {backend.address} 未知错误: {e}")
                backend.mark_failure()
                last_error = e

        # 所有实例都失败
        error_msg = json.dumps({
            "error": {
                "message": f"所有 {self.model_name} 后端实例均不可用: {last_error}",
                "type": "proxy_error",
            }
        }).encode("utf-8")
        return 502, {"Content-Type": "application/json"}, error_msg

    def status(self) -> dict:
        """返回所有实例状态"""
        return {
            "model": self.model_name,
            "backends": [
                {
                    "address": b.address,
                    "healthy": b.healthy,
                    "consecutive_failures": b.consecutive_failures,
                    "total_requests": b.total_requests,
                    "total_failures": b.total_failures,
                }
                for b in self.backends
            ],
        }


# ============================================================
# HTTP 代理服务器
# ============================================================

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    """代理请求处理器"""

    # 由外部设置
    lb: LoadBalancer = None

    def do_POST(self):
        self._proxy()

    def do_GET(self):
        # GET /status 返回后端状态
        if self.path == "/status":
            body = json.dumps(self.lb.status(), indent=2, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._proxy()

    def _proxy(self):
        # 读取请求体
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # 构建转发 headers（去掉 hop-by-hop）
        skip_headers = {"host", "connection", "transfer-encoding", "keep-alive"}
        headers = {}
        for key, value in self.headers.items():
            if key.lower() not in skip_headers:
                headers[key] = value

        # 转发
        status, resp_headers, resp_body = self.lb.forward_request(
            path=self.path,
            method=self.command,
            headers=headers,
            body=body,
        )

        # 返回响应
        self.send_response(status)
        for key, value in resp_headers.items():
            if key.lower() not in ("transfer-encoding", "connection", "keep-alive"):
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(resp_body)))
        self.end_headers()
        self.wfile.write(resp_body)

    def log_message(self, format, *args):
        # 静默默认日志，用 logging 模块代替
        pass


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_proxy(model_name: str, config: dict, request_timeout: int):
    """启动一个模型的代理服务器"""
    port = config["port"]
    instances = config["instances"]
    logger = logging.getLogger(model_name)

    lb = LoadBalancer(model_name, instances, request_timeout=request_timeout)

    # 创建 handler class（每个模型独立）
    handler_class = type(
        f"ProxyHandler_{model_name}",
        (ProxyHandler,),
        {"lb": lb},
    )

    server = ThreadedHTTPServer(("0.0.0.0", port), handler_class)
    logger.info(f"代理启动: 0.0.0.0:{port} -> {len(instances)} 个后端实例")
    logger.info(f"  后端: {', '.join(instances)}")
    logger.info(f"  状态页: http://localhost:{port}/status")
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="EB5 轻量负载均衡代理")
    parser.add_argument(
        "--model", action="append", dest="models",
        choices=list(EB5_BACKENDS.keys()),
        help="指定要启动的模型代理（可多次指定），不指定则启动全部",
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="单次请求超时秒数（默认 300）",
    )
    args = parser.parse_args()

    models = args.models or list(EB5_BACKENDS.keys())

    print("=" * 50)
    print("  EB5 负载均衡代理")
    print("=" * 50)
    for m in models:
        cfg = EB5_BACKENDS[m]
        print(f"  {m}: localhost:{cfg['port']} -> {len(cfg['instances'])} 实例")
    print(f"  请求超时: {args.timeout}s")
    print("=" * 50)

    threads = []
    for model_name in models:
        config = EB5_BACKENDS[model_name]
        t = threading.Thread(
            target=start_proxy,
            args=(model_name, config, args.timeout),
            daemon=True,
        )
        t.start()
        threads.append(t)

    # 主线程等待
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n代理已停止")


if __name__ == "__main__":
    main()
