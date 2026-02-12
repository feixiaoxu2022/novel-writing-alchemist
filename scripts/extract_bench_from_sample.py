#!/usr/bin/env python3
"""
从样本文件中提取指定data_id的bench数据
支持将environment中的文件部署到指定目录（用于recheck场景）
"""
import json
import sys
import os
import base64
import argparse


def deploy_environment_files(environment, deploy_dir):
    """将environment中的文件部署到指定目录

    environment格式: [{path, type, content}, ...]
    type为"text"时content是文本，type为"binary"时content是base64编码
    支持带子目录的路径（如 judge_criteria/content_quality_basic.yaml）
    """
    if not environment:
        return 0

    deployed_count = 0
    for entry in environment:
        rel_path = entry.get('path', '')
        content = entry.get('content', '')
        file_type = entry.get('type', 'text')

        if not rel_path:
            continue

        file_path = os.path.join(deploy_dir, rel_path)
        # 确保父目录存在
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        if file_type == 'binary':
            # base64编码的二进制文件
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(content))
        else:
            # 文本文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        deployed_count += 1

    return deployed_count


def extract_bench(samples_file, data_id, output_file, deploy_env_dir=None):
    """从样本文件中提取指定data_id的bench数据

    Args:
        samples_file: 样本文件路径
        data_id: 要提取的data_id
        output_file: 输出bench.json路径
        deploy_env_dir: 可选，将environment文件部署到此目录
    """
    try:
        # 读取样本文件（使用errors='replace'处理无效字符）
        with open(samples_file, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                if line.strip():
                    sample = json.loads(line)
                    if sample.get('data_id') == data_id:
                        environment = sample.get('environment', {})

                        # 构造bench.json
                        bench = {
                            'data_id': sample['data_id'],
                            'check_list': sample['check_list'],
                            'environment': environment,
                            'query': sample.get('query', ''),
                            'system': sample.get('system', '')
                        }

                        # 使用ensure_ascii=True避免Unicode编码问题
                        with open(output_file, 'w', encoding='utf-8') as out:
                            json.dump(bench, out, ensure_ascii=True, indent=2)

                        print(f'✓ 成功提取 {data_id} 的bench数据', file=sys.stderr)

                        # 部署environment文件到_env目录
                        if deploy_env_dir and environment:
                            deployed = deploy_environment_files(
                                environment, deploy_env_dir
                            )
                            print(
                                f'✓ 已部署 {deployed} 个environment文件到 {deploy_env_dir}',
                                file=sys.stderr
                            )

                        return 0

        print(f'错误: 未找到data_id={data_id}的样本', file=sys.stderr)
        return 1

    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description='从样本文件中提取bench数据')
    parser.add_argument('--samples', required=True, help='样本文件路径')
    parser.add_argument('--data-id', required=True, help='要提取的data_id')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--deploy-env-dir', default=None,
                        help='将environment文件部署到此目录（用于recheck时补充_env中缺失的文件）')

    args = parser.parse_args()

    return extract_bench(args.samples, args.data_id, args.output,
                         deploy_env_dir=args.deploy_env_dir)


if __name__ == '__main__':
    sys.exit(main())
