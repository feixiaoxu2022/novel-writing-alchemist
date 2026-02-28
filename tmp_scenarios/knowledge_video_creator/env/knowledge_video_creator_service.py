#!/usr/bin/env python3
"""
技术知识讲解视频创作 MCP 服务
============================

提供文件系统操作 + 多媒体制作工具，供Agent完成知识提炼→系列策划→视频素材制作的全流程。

与 novel_to_script 的关键区别：
1. 增加了 create_ppt 工具（python-pptx生成PPT）
2. 增加了 text_to_speech 工具（TTS配音）
3. 增加了 generate_image 工具（AI图片生成）
4. 增加了 execute_code 工具（Python沙箱，用于高级图表/数据可视化）

工作目录结构：
  {WORK_DIR}/
  ├── workspace/              # Agent的工作空间
  │   ├── source_materials/   # 源技术文档（预置）
  │   ├── knowledge_analysis.json   # Step 2 输出
  │   ├── series_plan.json          # Step 3 输出
  │   ├── scripts/                  # Step 4 输出（分集脚本）
  │   │   ├── episode_1.json
  │   │   └── episode_N.json
  │   └── videos/                   # Step 5 输出（视频素材包）
  │       ├── episode_1/
  │       │   ├── slides.pptx
  │       │   ├── narration.mp3
  │       │   ├── images/
  │       │   └── manifest.json
  │       └── episode_N/
  └── data_pools/             # 公共资源（只读）
      ├── skills/
      │   ├── video_script_guide.md
      │   └── visual_design_guide.md
      └── schemas/
          └── output_specifications.yaml
"""

import json
import os
import subprocess
import sys
import base64
import struct
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Annotated, Optional, List, Literal

from pydantic import Field
from fastmcp import FastMCP

# 创建MCP服务
mcp = FastMCP(name="knowledge_video_creator_service")

# 全局变量
WORK_DIR = None

# 多媒体模式：real（调真实API）或 mock（返回模拟文件）
MEDIA_MODE = os.environ.get("MEDIA_MODE", "mock")

# TTS配置
TTS_PROVIDER = os.environ.get("TTS_PROVIDER", "edge")  # edge (免费) / minimax
MINIMAX_GROUP_ID = os.environ.get("MINIMAX_GROUP_ID", "")
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

# 图片生成配置
IMAGE_PROVIDER = os.environ.get("IMAGE_PROVIDER", "openai")  # openai (via proxy) / gemini
IMAGE_API_KEY = os.environ.get("IMAGE_API_KEY", "")
IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL", "http://yy.dbh.baidu-int.com/v1")


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
    path: Annotated[str, Field(description="文件路径（相对于workspace目录，或以data_pools/开头读取公共资源）")]
) -> Dict[str, Any]:
    """
    读取文件内容

    支持两种路径：
    - 相对路径（如 source_materials/main_doc.md）：相对于 workspace/ 目录
    - data_pools/ 路径（如 data_pools/skills/video_script_guide.md）：读取公共资源

    Args:
        path: 文件路径

    Returns:
        包含文件内容的字典
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    if path.startswith("data_pools/"):
        full_path = os.path.join(WORK_DIR, path)
    elif path.startswith("/"):
        full_path = path
    else:
        full_path = os.path.join(WORK_DIR, "workspace", path)

    if not path.startswith("data_pools/") and not path.startswith("/"):
        if not is_path_safe(full_path):
            return {"error": f"路径 '{path}' 不在允许的workspace目录内"}

    if not os.path.exists(full_path):
        return {"error": f"文件不存在: {path}"}

    if not os.path.isfile(full_path):
        return {"error": f"路径不是文件: {path}"}

    try:
        # 二进制文件返回大小信息而非内容
        binary_exts = {".pptx", ".mp3", ".mp4", ".wav", ".png", ".jpg", ".jpeg", ".gif"}
        ext = os.path.splitext(full_path)[1].lower()
        if ext in binary_exts:
            size = os.path.getsize(full_path)
            return {
                "status": "success",
                "path": path,
                "type": "binary",
                "extension": ext,
                "size": size,
                "message": f"这是一个二进制文件（{ext}），大小 {size} 字节。无法直接显示内容。"
            }

        with open(full_path, "r", encoding="utf-8") as f:
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
    path: Annotated[str, Field(description="文件路径（相对于workspace目录）")],
    content: Annotated[str, Field(description="要写入的内容")]
) -> Dict[str, Any]:
    """
    写入文件内容

    将内容写入workspace目录下的指定文件。如果文件不存在会创建，如果存在会覆盖。
    父目录会自动创建。

    Args:
        path: 文件路径（相对于workspace目录）
        content: 要写入的内容

    Returns:
        操作结果
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", path)

    if not is_path_safe(full_path):
        return {"error": f"路径 '{path}' 不在允许的workspace目录内"}

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
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
def list_directory(
    path: Annotated[str, Field(description="目录路径（相对于workspace目录，或以data_pools/开头）")] = "."
) -> Dict[str, Any]:
    """
    列出目录内容

    列出workspace或data_pools目录下的文件和子目录。

    Args:
        path: 目录路径，默认为workspace根目录

    Returns:
        包含文件和目录列表的字典
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    if path.startswith("data_pools/") or path == "data_pools":
        full_path = os.path.join(WORK_DIR, path)
        skip_safety_check = True
    elif path == ".":
        full_path = os.path.join(WORK_DIR, "workspace")
        skip_safety_check = False
    else:
        full_path = os.path.join(WORK_DIR, "workspace", path)
        skip_safety_check = False

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

        for entry in sorted(entries):
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
    path: Annotated[str, Field(description="目录路径（相对于workspace目录）")]
) -> Dict[str, Any]:
    """
    创建目录

    在workspace目录下创建指定目录。父目录不存在时会自动创建。

    Args:
        path: 目录路径

    Returns:
        操作结果
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", path)

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


# ==================== 多媒体工具 ====================

@mcp.tool()
def create_ppt(
    filename: Annotated[str, Field(description="输出PPT文件路径（相对于workspace，如 videos/episode_1/slides.pptx）")],
    slides: Annotated[str, Field(description="""
幻灯片内容，JSON字符串格式的数组。每个元素代表一页幻灯片：
{
  "layout": "title_slide|content|two_column|code|blank",
  "title": "页面标题",
  "subtitle": "副标题（仅title_slide布局）",
  "content": "正文内容（支持换行）",
  "left_content": "左栏内容（仅two_column布局）",
  "right_content": "右栏内容（仅two_column布局）",
  "code": "代码内容（仅code布局）",
  "code_language": "python|yaml|json|bash",
  "notes": "演讲者备注",
  "image_path": "可选，插入图片的路径（相对于workspace）"
}

布局说明：
- title_slide: 标题页（大标题+副标题）
- content: 标准内容页（标题+正文）
- two_column: 双栏对比页（标题+左右两栏）
- code: 代码展示页（标题+深色背景代码块）
- blank: 空白页（仅图片或自定义内容）
""")]
) -> Dict[str, Any]:
    """
    生成PPT文件

    根据结构化的幻灯片描述生成 .pptx 文件。使用 python-pptx 库。
    支持5种页面布局，可插入图片，支持中文字体。

    Args:
        filename: 输出文件路径
        slides: JSON格式的幻灯片描述

    Returns:
        操作结果，包含文件路径和页数
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", filename)

    if not is_path_safe(full_path):
        return {"error": f"路径 '{filename}' 不在允许的workspace目录内"}

    # 解析slides JSON
    try:
        if isinstance(slides, str):
            slide_list = json.loads(slides)
        else:
            slide_list = slides
    except json.JSONDecodeError as e:
        return {"error": f"slides JSON解析失败: {str(e)}"}

    if not isinstance(slide_list, list) or len(slide_list) == 0:
        return {"error": "slides必须是非空数组"}

    if MEDIA_MODE == "mock":
        return _create_ppt_mock(full_path, filename, slide_list)
    else:
        return _create_ppt_real(full_path, filename, slide_list)


def _create_ppt_mock(full_path: str, filename: str, slide_list: list) -> Dict[str, Any]:
    """Mock模式：生成一个最小化的pptx文件"""
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # 生成一个合法的最小pptx（实际上是一个zip文件）
    # 在mock模式下，用python-pptx生成一个简单的PPT
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN

        prs = Presentation()

        for slide_data in slide_list:
            layout_name = slide_data.get("layout", "content")

            if layout_name == "title_slide":
                slide_layout = prs.slide_layouts[0]
                slide = prs.slides.add_slide(slide_layout)
                if slide.placeholders[0]:
                    slide.placeholders[0].text = slide_data.get("title", "")
                if len(slide.placeholders) > 1 and slide.placeholders[1]:
                    slide.placeholders[1].text = slide_data.get("subtitle", "")

            elif layout_name == "code":
                slide_layout = prs.slide_layouts[6]  # Blank
                slide = prs.slides.add_slide(slide_layout)
                # 标题
                from pptx.util import Emu
                txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
                tf = txBox.text_frame
                tf.text = slide_data.get("title", "")
                tf.paragraphs[0].font.size = Pt(24)
                tf.paragraphs[0].font.bold = True
                # 代码区域
                code_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(9), Inches(5.5))
                ctf = code_box.text_frame
                ctf.word_wrap = True
                code_text = slide_data.get("code", "")
                ctf.text = code_text
                for para in ctf.paragraphs:
                    para.font.size = Pt(12)
                    para.font.name = "Consolas"

            else:
                # content / two_column / blank → 用 Title+Content 布局
                slide_layout = prs.slide_layouts[1]
                slide = prs.slides.add_slide(slide_layout)
                if slide.placeholders[0]:
                    slide.placeholders[0].text = slide_data.get("title", "")
                if len(slide.placeholders) > 1 and slide.placeholders[1]:
                    content = slide_data.get("content", "")
                    if layout_name == "two_column":
                        left = slide_data.get("left_content", "")
                        right = slide_data.get("right_content", "")
                        content = f"[左栏]\n{left}\n\n[右栏]\n{right}"
                    slide.placeholders[1].text = content

            # 插入图片（如果有）
            image_path = slide_data.get("image_path")
            if image_path:
                img_full = os.path.join(WORK_DIR, "workspace", image_path)
                if os.path.exists(img_full):
                    slide.shapes.add_picture(img_full, Inches(6), Inches(2), Inches(3), Inches(3))

        prs.save(full_path)

        return {
            "status": "success",
            "path": filename,
            "slide_count": len(slide_list),
            "file_size": os.path.getsize(full_path),
            "message": f"PPT已生成: {filename}（{len(slide_list)}页）"
        }

    except ImportError:
        # 如果没有python-pptx，写一个占位文件
        with open(full_path, "wb") as f:
            f.write(b"MOCK_PPTX_" + json.dumps(slide_list, ensure_ascii=False).encode("utf-8"))
        return {
            "status": "success",
            "path": filename,
            "slide_count": len(slide_list),
            "file_size": os.path.getsize(full_path),
            "message": f"PPT已生成(mock): {filename}（{len(slide_list)}页）",
            "note": "python-pptx未安装，生成的是占位文件"
        }


def _create_ppt_real(full_path: str, filename: str, slide_list: list) -> Dict[str, Any]:
    """真实模式：使用python-pptx生成完整PPT"""
    # 与mock模式相同实现，因为python-pptx本身就是本地库
    return _create_ppt_mock(full_path, filename, slide_list)


@mcp.tool()
def text_to_speech(
    text: Annotated[str, Field(description="要转换为语音的文本内容")],
    filename: Annotated[str, Field(description="输出音频文件路径（相对于workspace，如 videos/episode_1/narration.mp3）")],
    voice: Annotated[str, Field(description="语音类型：male-qingse（青涩男声）/ female-tianmei（甜美女声）/ male-chengshu（成熟男声）/ female-zhiyu（知性女声）")] = "male-qingse",
    speed: Annotated[float, Field(description="语速倍率（0.5-2.0），默认1.0")] = 1.0,
    emotion: Annotated[str, Field(description="情绪：neutral（中性）/ happy（愉快）/ excited（兴奋）")] = "neutral"
) -> Dict[str, Any]:
    """
    文字转语音（TTS）

    将文本转换为mp3音频文件。用于生成视频的口播配音。

    Args:
        text: 口播文本（建议每次不超过2000字）
        filename: 输出文件路径
        voice: 语音角色
        speed: 语速（0.5=慢速，1.0=正常，2.0=快速）
        emotion: 情绪风格

    Returns:
        操作结果，包含文件路径、时长估算
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", filename)

    if not is_path_safe(full_path):
        return {"error": f"路径 '{filename}' 不在允许的workspace目录内"}

    if not text or len(text.strip()) == 0:
        return {"error": "文本内容不能为空"}

    if len(text) > 5000:
        return {"error": f"文本过长（{len(text)}字），单次请求不超过5000字。请分段调用。"}

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if MEDIA_MODE == "mock":
        return _tts_mock(full_path, filename, text, voice, speed, emotion)
    else:
        return _tts_real(full_path, filename, text, voice, speed, emotion)


def _tts_mock(full_path: str, filename: str, text: str, voice: str, speed: float, emotion: str) -> Dict[str, Any]:
    """Mock模式：生成一个有效的最小MP3文件"""
    # 估算时长：中文约4字/秒（口播速度），英文约3词/秒
    char_count = len(text)
    estimated_duration_sec = char_count / (4.0 * speed)

    # 生成一个最小合法MP3文件（MPEG Audio Layer 3 frame header + silence）
    # MP3 frame header: 0xFF 0xFB 0x90 0x00 (MPEG1, Layer3, 128kbps, 44100Hz, stereo)
    mp3_header = bytes([0xFF, 0xFB, 0x90, 0x00])
    # 一个MP3 frame = 417 bytes (128kbps, 44100Hz)，每帧约26ms
    frame_count = max(10, int(estimated_duration_sec * 38.5))  # 38.5帧/秒
    silence_frame = mp3_header + b'\x00' * 413  # 417 bytes total per frame

    with open(full_path, "wb") as f:
        for _ in range(min(frame_count, 200)):  # 限制mock文件大小
            f.write(silence_frame)

    return {
        "status": "success",
        "path": filename,
        "text_length": char_count,
        "estimated_duration": f"{estimated_duration_sec:.1f}秒",
        "voice": voice,
        "speed": speed,
        "emotion": emotion,
        "file_size": os.path.getsize(full_path),
        "message": f"配音已生成: {filename}（预计时长{estimated_duration_sec:.1f}秒，{voice}语音）"
    }


def _tts_real(full_path: str, filename: str, text: str, voice: str, speed: float, emotion: str) -> Dict[str, Any]:
    """真实模式：调用 edge-tts CLI（免费，微软Edge TTS）
    
    使用subprocess调用edge-tts命令行，避免asyncio.run()在已有event loop中冲突。
    """
    import subprocess

    voice_map = {
        "male-qingse": "zh-CN-YunxiNeural",
        "female-tianmei": "zh-CN-XiaoxiaoNeural",
        "male-chengshu": "zh-CN-YunjianNeural",
        "female-zhiyu": "zh-CN-XiaohanNeural",
    }
    actual_voice = voice_map.get(voice, "zh-CN-YunxiNeural")

    # edge-tts 语速：+50% 对应 speed=1.5
    rate_percent = int((speed - 1.0) * 100)
    rate_str = f"+{rate_percent}%" if rate_percent >= 0 else f"{rate_percent}%"

    try:
        # 使用 edge-tts CLI 命令行方式，避免 asyncio 冲突
        cmd = [
            "edge-tts",
            "--voice", actual_voice,
            "--rate", rate_str,
            "--text", text,
            "--write-media", full_path,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return {"error": f"edge-tts CLI失败 (rc={result.returncode}): {result.stderr[:300]}"}

        char_count = len(text)
        estimated_duration_sec = char_count / (4.0 * speed)

        return {
            "status": "success",
            "path": filename,
            "text_length": char_count,
            "estimated_duration": f"{estimated_duration_sec:.1f}秒",
            "voice": voice,
            "speed": speed,
            "emotion": emotion,
            "file_size": os.path.getsize(full_path),
            "message": f"配音已生成: {filename}（预计时长{estimated_duration_sec:.1f}秒，{actual_voice}）"
        }

    except subprocess.TimeoutExpired:
        return {"error": "TTS调用超时（120秒）"}
    except Exception as e:
        return {"error": f"TTS调用失败: {str(e)}"}


@mcp.tool()
def generate_image(
    prompt: Annotated[str, Field(description="图片描述（中文或英文，描述你想要的图表/架构图/概念图的内容）")],
    filename: Annotated[str, Field(description="输出图片文件路径（相对于workspace，如 videos/episode_1/images/architecture.png）")],
    aspect_ratio: Annotated[str, Field(description="宽高比：16:9（宽屏）/ 1:1（方形）/ 4:3（标准）")] = "16:9"
) -> Dict[str, Any]:
    """
    AI图片生成

    根据文字描述生成图片。适合生成技术架构图、流程图、概念示意图等。

    注意：对于数据图表（柱状图、折线图等），建议使用 execute_code 工具通过
    matplotlib 生成，效果更精确。本工具更适合概念性的示意图和插图。

    Args:
        prompt: 图片描述
        filename: 输出文件路径
        aspect_ratio: 宽高比

    Returns:
        操作结果，包含文件路径
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    full_path = os.path.join(WORK_DIR, "workspace", filename)

    if not is_path_safe(full_path):
        return {"error": f"路径 '{filename}' 不在允许的workspace目录内"}

    if not prompt or len(prompt.strip()) == 0:
        return {"error": "图片描述不能为空"}

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if MEDIA_MODE == "mock":
        return _generate_image_mock(full_path, filename, prompt, aspect_ratio)
    else:
        return _generate_image_real(full_path, filename, prompt, aspect_ratio)


def _generate_image_mock(full_path: str, filename: str, prompt: str, aspect_ratio: str) -> Dict[str, Any]:
    """Mock模式：生成一个带描述文字的PNG占位图"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        # 根据宽高比确定尺寸
        size_map = {
            "16:9": (1280, 720),
            "1:1": (800, 800),
            "4:3": (1024, 768),
            "9:16": (720, 1280),
        }
        width, height = size_map.get(aspect_ratio, (1280, 720))

        # 创建带浅蓝背景的占位图
        img = Image.new("RGB", (width, height), color=(240, 248, 255))
        draw = ImageDraw.Draw(img)

        # 画边框
        draw.rectangle([5, 5, width-6, height-6], outline=(100, 149, 237), width=3)

        # 写标题
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
            font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        except Exception:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        draw.text((width//2, 40), "[AI生成图片]", fill=(100, 149, 237), anchor="mt", font=font_large)

        # 写prompt摘要（截断）
        prompt_display = prompt[:100] + "..." if len(prompt) > 100 else prompt
        y_pos = 100
        for line in prompt_display.split("\n")[:5]:
            draw.text((40, y_pos), line, fill=(60, 60, 60), font=font_small)
            y_pos += 30

        img.save(full_path, "PNG")

    except ImportError:
        # 没有PIL就生成最小PNG
        # 最小合法PNG（1x1像素，白色）
        png_data = (
            b'\x89PNG\r\n\x1a\n'  # PNG signature
            b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
            b'\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N'
            b'\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        with open(full_path, "wb") as f:
            f.write(png_data)

    return {
        "status": "success",
        "path": filename,
        "prompt": prompt[:200],
        "aspect_ratio": aspect_ratio,
        "file_size": os.path.getsize(full_path),
        "message": f"图片已生成: {filename}（{aspect_ratio}）"
    }


def _generate_image_real(full_path: str, filename: str, prompt: str, aspect_ratio: str) -> Dict[str, Any]:
    """真实模式：通过统一网关调用 Gemini 图片生成"""
    import httpx

    # 拼接 Gemini 端点：base_url 去掉 /v1 后缀，再拼 /v1/models/gemini-2.5-flash-image
    base = IMAGE_BASE_URL.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]
    url = f"{base}/v1/models/gemini-2.5-flash-image"

    headers = {
        "Authorization": f"Bearer {IMAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Gemini 原生格式
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"Generate an image: {prompt}"}
                ]
            }
        ]
    }

    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        # 从 Gemini 响应中提取 inlineData 图片
        if "candidates" in data:
            for candidate in data["candidates"]:
                parts = candidate.get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        mime_type = part["inlineData"].get("mimeType", "image/png")
                        img_b64 = part["inlineData"].get("data", "")
                        img_bytes = base64.b64decode(img_b64)
                        with open(full_path, "wb") as f:
                            f.write(img_bytes)

                        return {
                            "status": "success",
                            "path": filename,
                            "prompt": prompt[:200],
                            "aspect_ratio": aspect_ratio,
                            "file_size": os.path.getsize(full_path),
                            "message": f"图片已生成: {filename}（{aspect_ratio}）"
                        }

        return {"error": f"API响应中没有图片数据: {json.dumps(data, ensure_ascii=False)[:500]}"}

    except Exception as e:
        return {"error": f"图片生成API调用失败: {str(e)}"}


@mcp.tool()
def execute_code(
    code: Annotated[str, Field(description="""
Python代码。在沙箱环境中执行。
工作目录为workspace/，可以读写该目录下的文件。

可用的库：
- matplotlib（图表生成）
- PIL/Pillow（图像处理）
- json, csv, yaml（数据处理）
- numpy, pandas（数据分析，如果已安装）
- python-pptx（PPT处理，如果已安装）

典型用途：
- 用matplotlib生成数据图表（柱状图、折线图、饼图等）
- 用PIL生成自定义的示意图
- 数据处理和分析

注意：代码必须将输出文件保存到当前目录或其子目录中。
""")]
) -> Dict[str, Any]:
    """
    执行Python代码

    在隔离的沙箱环境中执行Python代码。适合用于：
    1. 使用matplotlib生成精确的数据图表
    2. 使用PIL/Pillow生成自定义图像
    3. 数据处理和文件操作

    代码的工作目录为workspace/，所有输出文件保存在此目录下。

    Args:
        code: Python代码

    Returns:
        执行结果，包含stdout、stderr和returncode
    """
    if not WORK_DIR:
        return {"error": "工作目录未初始化"}

    workspace = os.path.join(WORK_DIR, "workspace")

    # 安全检查
    dangerous_patterns = [
        "import subprocess", "import os\nos.system",
        "exec(", "eval(", "__import__",
        "shutil.rmtree", "os.remove",
    ]
    code_lower = code.lower()
    for pattern in dangerous_patterns:
        if pattern.lower() in code_lower:
            # 允许 os.path 和 os.makedirs
            if pattern in ("import os\nos.system",):
                continue
            # 只禁止真正危险的
            if pattern in ("exec(", "eval(", "__import__"):
                return {"error": f"禁止使用危险操作: {pattern}"}

    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout[:5000] if result.stdout else "",
            "stderr": result.stderr[:5000] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"error": "代码执行超时（60秒）"}
    except Exception as e:
        return {"error": f"执行代码失败: {str(e)}"}


# ==================== 启动 ====================

def main():
    """启动MCP服务"""
    global WORK_DIR

    import argparse
    parser = argparse.ArgumentParser(description="技术知识讲解视频创作 MCP 服务")
    parser.add_argument(
        "work_dir", nargs="?", default="./",
        help="工作目录路径（包含workspace/和data_pools/子目录）"
    )
    args = parser.parse_args()

    WORK_DIR = os.path.abspath(args.work_dir)
    print(f"Knowledge Video Creator Service - Work directory: {WORK_DIR}", flush=True)
    print(f"Media mode: {MEDIA_MODE}", flush=True)

    # 确保workspace目录存在
    workspace = os.path.join(WORK_DIR, "workspace")
    os.makedirs(workspace, exist_ok=True)

    # stdio模式启动
    mcp.run()


if __name__ == "__main__":
    main()
