#!/usr/bin/env python3
"""
本地一键拉取远程评测结果
用法:
    python3 fetch_results.py                              # 列出远程所有评测结果
    python3 fetch_results.py --download <目录名>          # 下载指定评测结果
    python3 fetch_results.py --download-all               # 下载所有评测结果
    python3 fetch_results.py --host 10.25.70.163 --port 9090  # 指定远程地址
"""

import argparse
import json
import os
import sys
import tarfile
import io
import urllib.request
import urllib.error

# 默认配置
DEFAULT_HOST = "10.25.70.163"
DEFAULT_PORT = 9090
LOCAL_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "evaluation_outputs"
)


def fetch_json(url):
    """获取 JSON 响应"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"连接失败: {e}")
        print(f"请确认远程服务器上已运行 serve_results.sh")
        sys.exit(1)


def list_remote(base_url):
    """列出远程所有评测结果"""
    data = fetch_json(f"{base_url}/api/list")
    if not data:
        print("远程没有评测结果")
        return

    print(f"\n远程评测结果 ({base_url}):")
    print("-" * 80)
    print(f"{'目录名':<60} {'样本数':>6} {'成功':>6}")
    print("-" * 80)
    for item in data:
        name = item["name"]
        total = item["total_samples"]
        success = item["success"]
        # 检查本地是否已存在
        local_path = os.path.join(LOCAL_OUTPUT_DIR, name)
        local_marker = " [已下载]" if os.path.isdir(local_path) else ""
        print(f"  {name:<58} {total:>6} {success:>6}{local_marker}")

    print("-" * 80)
    print(f"共 {len(data)} 个评测批次")
    print(f"\n下载命令: python3 {os.path.basename(__file__)} --download <目录名>")


def patch_env_dir(target_dir):
    """将结果 JSON 中的远程 env_dir 路径替换为本地路径"""
    import glob
    # 自动检测远程路径前缀（从第一个 JSON 的 env_dir 字段提取）
    local_base = os.path.dirname(os.path.dirname(os.path.abspath(target_dir)))
    patched = 0
    for f in sorted(glob.glob(os.path.join(target_dir, "*.json"))):
        if os.path.basename(f) == "execution_report.json":
            continue
        with open(f, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        env_dir = d.get("env_dir", "")
        if not env_dir or local_base in env_dir:
            continue
        # 从远程路径中提取 evaluation_outputs/... 部分，拼接本地前缀
        # 远程: /home/work/novel_eval/novel-writing-alchemist/evaluation_outputs/xxx/yyy_env
        # 本地: /Users/.../novel_writing_alchemist/evaluation_outputs/xxx/yyy_env
        idx = env_dir.find("evaluation_outputs/")
        if idx >= 0:
            d["env_dir"] = os.path.join(local_base, env_dir[idx:])
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
            patched += 1
    if patched:
        print(f"  ✓ 已修补 {patched} 个文件的 env_dir 路径")


def download_one(base_url, dirname, output_dir):
    """下载一个评测结果目录"""
    url = f"{base_url}/api/tar/{dirname}"
    target_dir = os.path.join(output_dir, dirname)

    if os.path.isdir(target_dir):
        # 检查现有目录中的样本数
        existing = len([f for f in os.listdir(target_dir) if f.endswith(".json") and f != "execution_report.json"])
        print(f"  目录已存在 ({existing} 个样本): {target_dir}")

        # 获取远程信息
        remote_info = fetch_json(f"{base_url}/api/list")
        remote_item = next((x for x in remote_info if x["name"] == dirname), None)
        if remote_item and remote_item["total_samples"] == existing:
            print(f"  样本数一致，跳过下载")
            return False
        else:
            remote_count = remote_item["total_samples"] if remote_item else "?"
            print(f"  远程有 {remote_count} 个样本，本地有 {existing} 个，重新下载...")

    print(f"  下载: {dirname} ...")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
            size_mb = len(data) / 1024 / 1024
            print(f"  已接收 {size_mb:.1f} MB，解压中...")

            # 解压到 output_dir
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
                tar.extractall(path=output_dir)

        # 修补 env_dir 路径（远程路径 → 本地路径）
        patch_env_dir(target_dir)

        print(f"  ✓ 已保存到: {target_dir}")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ✗ 下载失败: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"  ✗ 下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="拉取远程评测结果")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"远程服务器地址 (默认: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"HTTP端口 (默认: {DEFAULT_PORT})")
    parser.add_argument("--download", metavar="DIR", help="下载指定评测目录")
    parser.add_argument("--download-all", action="store_true", help="下载所有评测结果")
    parser.add_argument("--output", default=LOCAL_OUTPUT_DIR, help=f"本地保存目录 (默认: {LOCAL_OUTPUT_DIR})")
    args = parser.parse_args()

    base_url = f"http://{args.host}:{args.port}"

    if args.download:
        os.makedirs(args.output, exist_ok=True)
        print(f"下载目录: {args.download}")
        download_one(base_url, args.download, args.output)

    elif args.download_all:
        os.makedirs(args.output, exist_ok=True)
        data = fetch_json(f"{base_url}/api/list")
        if not data:
            print("远程没有评测结果")
            return

        print(f"共 {len(data)} 个评测批次，开始下载...")
        downloaded = 0
        for item in data:
            print(f"\n[{downloaded + 1}/{len(data)}] {item['name']}")
            if download_one(base_url, item["name"], args.output):
                downloaded += 1
        print(f"\n完成: 新下载 {downloaded} 个，共 {len(data)} 个")

    else:
        list_remote(base_url)


if __name__ == "__main__":
    main()
