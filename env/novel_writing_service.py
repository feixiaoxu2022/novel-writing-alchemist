#!/usr/bin/env python3
"""
短剧创作MCP服务
================

提供完整的文件系统操作和HITL交互工具。
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Annotated, Optional, List, Literal
from pydantic import Field
from fastmcp import FastMCP

# 创建MCP服务
mcp = FastMCP(name="shortdrama_service")

# 全局变量
WORK_DIR = None
HITL_CONTEXT = {}


def load_hitl_context():
    """从workspace/.hitl_context.json加载HITL上下文"""
    global HITL_CONTEXT

    if not WORK_DIR:
        return

    context_file = os.path.join(WORK_DIR, "workspace", ".hitl_context.json")

    if os.path.exists(context_file):
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                HITL_CONTEXT = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load HITL context: {e}")
            HITL_CONTEXT = {}
    else:
        HITL_CONTEXT = {}


def is_path_safe(path: str) -> bool:
    """检查路径是否在workspace目录内"""
    try:
        resolved = Path(path).resolve()
        workspace = Path(WORK_DIR).resolve() / "workspace"
        return resolved.is_relative_to(workspace)
    except Exception:
        return False


# ==================== 文件系统工具 ====================

@mcp.tool()
def read_file(
    path: Annotated[str, Field(description="文件路径")]
) -> Dict[str, Any]:
    """
    读取文件内容

    Args:
        path: 文件路径

    Returns:
        包含文件内容的字典
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    # 支持绝对路径和相对路径
    if path.startswith("data_pools/"):
        # data_pools路径相对于工作目录
        full_path = os.path.join(WORK_DIR, path)
    elif path.startswith("/"):
        full_path = path
    else:
        # 其他路径相对于workspace
        full_path = os.path.join(WORK_DIR, "workspace", path)

    # 安全检查（只对workspace内的路径做检查）
    if path.startswith("workspace/") or (not path.startswith("data_pools/") and not path.startswith("/")):
        if not is_path_safe(full_path):
            return {"error": f"路径 '{path}' 不在允许的workspace目录内"}

    if not os.path.exists(full_path):
        return {"error": f"文件不存在: {path}"}

    if not os.path.isfile(full_path):
        return {"error": f"路径不是文件: {path}"}

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "status": "success",
            "path": path,
            "content": content,
            "size": len(content)
        }
    except Exception as e:
        return {"error": f"读取文件失败: {str(e)}"}


@mcp.tool()
def write_file(
    path: Annotated[str, Field(description="文件路径")],
    content: Annotated[str, Field(description="要写入的内容")]
) -> Dict[str, Any]:
    """
    写入文件内容

    将内容写入指定文件。如果文件不存在会创建，如果存在会覆盖。

    Args:
        path: 文件路径
        content: 要写入的内容

    Returns:
        操作结果
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", path)

    # 安全检查
    if not is_path_safe(full_path):
        return {"error": f"路径 '{path}' 不在允许的workspace目录内"}

    try:
        # 确保父目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "status": "success",
            "path": path,
            "size": len(content),
            "message": f"文件已写入: {path}"
        }
    except Exception as e:
        return {"error": f"写入文件失败: {str(e)}"}


@mcp.tool()
def write_files(
    files: Annotated[List[Dict[str, str]], Field(description="文件列表，每个元素包含path和content字段")]
) -> Dict[str, Any]:
    """
    批量写入多个文件

    一次性写入多个文件，提高效率。

    Args:
        files: 文件列表，格式：[{"path": "...", "content": "..."}, ...]

    Returns:
        批量操作结果

    Example:
        files = [
            {"path": "topic_brief.json", "content": "{...}"},
            {"path": "characters/role1.json", "content": "{...}"}
        ]
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    if not files or not isinstance(files, list):
        return {"error": "files参数必须是非空列表"}

    success_files = []
    failed_files = []

    for file_item in files:
        if not isinstance(file_item, dict):
            failed_files.append({
                "path": "unknown",
                "error": "文件项必须是字典"
            })
            continue

        path = file_item.get("path")
        content = file_item.get("content")

        if not path:
            failed_files.append({
                "path": "unknown",
                "error": "缺少path字段"
            })
            continue

        if content is None:
            failed_files.append({
                "path": path,
                "error": "缺少content字段"
            })
            continue

        # 转换为字符串
        if not isinstance(content, str):
            content = str(content)

        full_path = os.path.join(WORK_DIR, "workspace", path)

        # 安全检查
        if not is_path_safe(full_path):
            failed_files.append({
                "path": path,
                "error": f"路径不在允许的workspace目录内"
            })
            continue

        try:
            # 确保父目录存在
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            success_files.append({
                "path": path,
                "size": len(content)
            })
        except Exception as e:
            failed_files.append({
                "path": path,
                "error": str(e)
            })

    total = len(files)
    success_count = len(success_files)
    failed_count = len(failed_files)

    return {
        "status": "success" if failed_count == 0 else "partial" if success_count > 0 else "error",
        "total": total,
        "success_count": success_count,
        "failed_count": failed_count,
        "success_files": success_files,
        "failed_files": failed_files,
        "message": f"批量写入完成：成功 {success_count}/{total} 个文件"
    }


@mcp.tool()
def list_directory(
    path: Annotated[str, Field(description="目录路径")] = "."
) -> Dict[str, Any]:
    """
    列出目录内容

    Args:
        path: 目录路径，默认为当前目录

    Returns:
        包含文件和目录列表的字典
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    # 支持data_pools路径
    if path.startswith("data_pools/") or path == "data_pools":
        # data_pools路径相对于工作目录
        full_path = os.path.join(WORK_DIR, path)
        # data_pools不需要安全检查
        skip_safety_check = True
    elif path == ".":
        full_path = os.path.join(WORK_DIR, "workspace")
        skip_safety_check = False
    else:
        full_path = os.path.join(WORK_DIR, "workspace", path)
        skip_safety_check = False

    # 安全检查（data_pools除外）
    if not skip_safety_check and not is_path_safe(full_path):
        return {"error": f"路径 '{path}' 不在允许的workspace目录内"}

    if not os.path.exists(full_path):
        return {"error": f"目录不存在: {path}"}

    if not os.path.isdir(full_path):
        return {"error": f"路径不是目录: {path}"}

    try:
        entries = os.listdir(full_path)

        files = []
        directories = []

        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            if os.path.isfile(entry_path):
                files.append({
                    "name": entry,
                    "type": "file",
                    "size": os.path.getsize(entry_path)
                })
            elif os.path.isdir(entry_path):
                directories.append({
                    "name": entry,
                    "type": "directory"
                })

        return {
            "status": "success",
            "path": path,
            "files": files,
            "directories": directories,
            "total": len(files) + len(directories)
        }
    except Exception as e:
        return {"error": f"列出目录失败: {str(e)}"}


@mcp.tool()
def create_directory(
    path: Annotated[str, Field(description="目录路径")]
) -> Dict[str, Any]:
    """
    创建目录

    创建指定的目录。如果父目录不存在会自动创建。

    Args:
        path: 目录路径

    Returns:
        操作结果
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", path)

    # 安全检查
    if not is_path_safe(full_path):
        return {"error": f"路径 '{path}' 不在允许的workspace目录内"}

    try:
        os.makedirs(full_path, exist_ok=True)

        return {
            "status": "success",
            "path": path,
            "message": f"目录已创建: {path}"
        }
    except Exception as e:
        return {"error": f"创建目录失败: {str(e)}"}


@mcp.tool()
def bash(
    command: Annotated[str, Field(description="要执行的shell命令")]
) -> Dict[str, Any]:
    """
    执行shell命令

    在workspace目录下执行shell命令。出于安全考虑，命令只能在workspace目录内执行。

    Args:
        command: shell命令

    Returns:
        命令执行结果
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    workspace = os.path.join(WORK_DIR, "workspace")

    # 安全检查：禁止某些危险命令
    dangerous_commands = ['rm -rf /', 'mkfs', 'dd', 'format', ':(){:|:&};:']
    for dangerous in dangerous_commands:
        if dangerous in command:
            return {"error": f"禁止执行危险命令: {command}"}

    # 禁止cd到workspace外
    if command.strip().startswith('cd '):
        target = command.strip()[3:].strip()
        if target.startswith('/') or target.startswith('..'):
            return {"error": "禁止cd到workspace目录外"}

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": command
        }
    except subprocess.TimeoutExpired:
        return {"error": "命令执行超时（30秒）"}
    except Exception as e:
        return {"error": f"执行命令失败: {str(e)}"}


# ==================== HITL工具 ====================

@mcp.tool()
def request_human_review(
    stage: Annotated[Literal["灵感激发", "配方选择", "写作准备确认", "开篇审阅", "结局类型确认"], Field(description="当前阶段名称，仅支持：灵感激发（询问模式）、配方选择（询问模式）、写作准备确认（确认模式）、开篇审阅（确认模式）、结局类型确认（询问模式）")],
    type: Annotated[Literal["confirmation", "question"], Field(description="交互类型：confirmation（确认）或 question（询问）")],
    summary: Annotated[Optional[str], Field(description="确认模式下的总结信息，或询问模式下的当前进度描述")] = None,
    question: Annotated[Optional[str], Field(description="询问模式下的具体问题")] = None,
    options: Annotated[Optional[List[str]], Field(description="询问模式下的可选答案列表")] = None
) -> Dict[str, Any]:
    """
    请求用户确认或收集信息

    所有调用都会通过用户模拟器进行真实交互。

    两种模式：
    1. confirmation模式：关键阶段完成后请求用户确认
       - 用户可以确认继续、提出修改意见或要求重新生成

    2. question模式：关键信息缺失时询问用户
       - 从用户获取具体的回答和选择

    Args:
        stage: 当前阶段名称
        type: 交互类型（confirmation或question）
        summary: [confirmation模式] 总结信息
        question: [question模式] 具体问题
        options: [question模式] 可选答案列表

    Returns:
        Dict包含：
        - status: "success"
        - action: 用户响应类型（"accept"或"answer"）
        - answer: 用户的回答
        - message: 提示信息
    """

    # 重新加载上下文（支持动态更新）
    load_hitl_context()

    # 统一从hitl_responses读取答案
    hitl_responses = HITL_CONTEXT.get("hitl_responses", {})

    if type == "confirmation":
        # 确认模式：从hitl_responses读取用户确认或意见
        if stage not in hitl_responses or not hitl_responses[stage].get("answer"):
            # 没有配置答案时，默认确认继续
            return {
                "status": "success",
                "action": "accept",
                "answer": "确认，继续",
            }

        answer = hitl_responses[stage].get("answer")
        return {
            "status": "success",
            "action": "accept",
            "answer": answer,
            "message": f"用户已确认阶段'{stage}'"
        }

    elif type == "question":
        # 询问模式：从hitl_responses读取预设答案
        if stage not in hitl_responses or not hitl_responses[stage].get("answer"):
            # 没有配置答案时，模拟真实用户的回复（不暴露技术细节）
            return {
                "status": "success",
                "action": "answer",
                "answer": "我刚才说的内容里应该有相关信息，请仔细看看。如果确实没有，你自己判断就行。",
            }

        answer = hitl_responses[stage].get("answer")
        return {
            "status": "success",
            "action": "answer",
            "answer": answer,
        }

    else:
        return {
            "error": f"不支持的交互类型: {type}",
            "detail": "type参数必须是 'confirmation' 或 'question'"
        }


def main():
    """启动服务"""
    global WORK_DIR

    import argparse
    parser = argparse.ArgumentParser(description="短剧创作MCP服务")
    parser.add_argument("work_dir", nargs="?", default="./",
                       help="工作目录路径（包含workspace/和data_pools/子目录）")
    args = parser.parse_args()

    WORK_DIR = os.path.abspath(args.work_dir)
    print(f"Short Drama Service - Work directory: {WORK_DIR}", flush=True)

    # 确保workspace目录存在
    workspace = os.path.join(WORK_DIR, "workspace")
    os.makedirs(workspace, exist_ok=True)

    # 初始加载HITL上下文
    load_hitl_context()

    # stdio模式启动
    mcp.run()


if __name__ == "__main__":
    main()
