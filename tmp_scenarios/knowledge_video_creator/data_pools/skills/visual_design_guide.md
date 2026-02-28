# 技术教程视频视觉设计指南

## 一、视觉设计的核心原则

技术视频的视觉设计不是"美化"，是"认知辅助"。每一个视觉元素都必须服务于一个目的：**帮助观众更快、更准确地理解技术概念**。

### 1.1 三个层次

```
Level 1: 信息可读 — 文字清晰、图表不拥挤、代码能看清
Level 2: 结构可感 — 层级关系、流程方向、对比差异一目了然
Level 3: 认知助推 — 视觉隐喻帮助理解抽象概念，无需额外解释
```

### 1.2 技术视频 vs 普通演示

| 维度 | 普通PPT | 技术教程视频 |
|------|---------|-------------|
| 信息密度 | 一页≤6行 | 一页1-3个核心点 |
| 停留时间 | 观众自行翻页 | 每页5-15秒（视频节奏） |
| 动态性 | 静态为主 | 渐进显示、高亮动画 |
| 代码展示 | 截图贴入 | 逐行高亮、运行演示 |

## 二、PPT内容语言规范（最高优先级）

### 核心原则：观众看PPT，不是读代码

PPT幻灯片是面向技术人员的**视觉辅助**，不是代码文档的截图。所有内容必须以中文为主体，让观众扫一眼就能抓住要点。

### 2.0.1 中文化规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 中文优先 | 所有要点、标题、描述用中文 | "格式合规"，不是 `format_compliance` |
| 术语首次标注 | 英文术语首次出现标注一次：中文（English），后续只用中文 | "门控层（Gate Layer）" → 后续直接说"门控层" |
| 禁止裸英文 | PPT正文不得出现未翻译的英文变量名/函数名 | ❌ `basic_deduction` → ✅ "基础项扣分" |
| 公式中文化 | 公式/表达式的变量必须用中文标注含义 | 见下方示例 |

### 2.0.2 内容表达对比

**对比1：公式展示**

❌ 差的方式（像代码文档）：
```
Latency_Score = weighted_avg(p50, p99, timeout_rate)
Overall = Latency_Score * 0.6 + Reliability * 0.4
```

✅ 好的方式（像教学PPT）：
```
📊 API性能评分公式

响应时长分 =
  P50延迟 × 40% + P99延迟 × 40% + 超时率 × 20%

总分 = 响应时长分 × 60% + 可用性分 × 40%
```

**对比2：概念列表**

❌ 差的方式（英文术语堆砌）：
```
① presentation_layer → handles UI
② business_logic_layer → core processing
③ data_access_layer → database ops
④ infrastructure_layer → deployment
```

✅ 好的方式（中文+简短解释）：
```
系统四层架构

① 表现层 — 处理用户界面和交互
② 业务逻辑层 — 核心处理规则和流程
③ 数据访问层 — 数据库读写和缓存管理
④ 基础设施层 — 部署、监控和运维
```

**对比3：配置/代码展示**

❌ 差的方式（直接贴YAML）：
```yaml
health_check:
  condition: "service.status == 'running'"
auto_scaling:
  condition: "cpu_usage > 80 and request_count > threshold"
```

✅ 好的方式（可视化+中文标注）：
```
自动运维策略：按条件触发

🎯 健康检查 → 服务状态异常时自动重启
🎯 自动扩容 → CPU超80%且请求量超阈值时扩容
🎯 自动降级 → 下游服务超时时启用降级方案

原理：根据运行时指标自动决定执行哪些运维操作
```

### 2.0.3 代码/配置展示限制

- 整个PPT中**最多2页**使用代码布局（code layout）
- 每页代码不超过10行，且每行必须有中文注释
- 禁止在PPT上展示目录结构树——改用结构示意图或口播描述
- 如果技术概念可以用"图示+中文标注"替代代码，必须优先使用图示

## 三、PPT页面设计规范

### 3.1 页面类型

| 页面类型 | 用途 | 布局特征 |
|---------|------|---------|
| title_slide | 集标题/章节标题 | 大标题居中，副标题/集数在下方 |
| concept_intro | 引入新概念 | 左侧概念名+图标，右侧一句话定义 |
| comparison | 对比两种方案/概念 | 左右分栏，语义色对比（绿=推荐/橙=问题） |
| process_flow | 展示流程/步骤 | 横向流程图，箭头连接，当前步高亮 |
| code_display | 展示代码片段（**整个PPT最多2页**） | 深色背景，语法高亮，每行中文注释 |
| architecture | 展示系统架构 | 模块框图，连线表示关系 |
| key_takeaway | 本节要点总结 | 编号列表，图标标注重要等级 |
| question | 互动提问 | 大字号问题文本，思考时间标注 |

### 3.2 配色方案

**整体风格：高级极简，暖色调 + 低饱和语义色。** 详细代码见第八章 8.1 节。

```yaml
# 背景
bg_warm:    "#F5F0E8"    # 暖米色 — 内容页主背景（禁止冷灰色）
bg_cream:   "#FAF8F5"    # 奶油色 — 嵌套容器底色
bg_dark:    "#2D2D2D"    # 深灰（非纯黑）— 代码页

# 语义色（全部低饱和）
orange:     "#D4956A"    # 柔和橙 — 概念A / 警告
green:      "#6BAF8D"    # 柔和绿 — 概念B / 正确 / 推荐
rose:       "#C47C7C"    # 柔和玫红 — 概念C / 重要 / 错误
blue:       "#6B8DB5"    # 柔和蓝 — 信息 / 流程

# 文字
text_black: "#1A1A1A"    # 主文字（近黑非纯黑）
text_dark:  "#4A4A4A"    # 次要文字
text_gray:  "#8A8A8A"    # 辅助说明
```

**规则**：
- 同一页面除黑/白/灰外，最多使用3种语义色
- 代码页面使用 `bg_dark`（`#2D2D2D`）深色背景
- 对比页面使用语义色容器（如橙=问题 / 绿=推荐），不用高饱和红绿
- 禁止高饱和荧光色（如 `#2563EB`、`#EF4444`、`#F59E0B`）

### 3.3 字体与排版

```
标题: 24-32pt 粗体
正文: 16-20pt 常规
代码: 14-18pt 等宽字体
注释: 12-14pt 灰色
```

- 行间距：1.5倍
- 每页文字不超过50个汉字（不含代码）
- 留白 ≥ 页面面积30%

## 四、图表设计规范

### 4.1 流程图

**适用场景**：步骤、工作流、决策逻辑

**设计要求**：
- 从左到右或从上到下排列
- 每个节点用圆角矩形，宽度一致
- 箭头线条粗细统一（2px）
- 当前讨论的节点高亮（蓝色边框+浅蓝背景），其余灰色
- 分支用菱形判断节点

**描述格式**：
```
流程图：持续集成/持续部署流程
[代码提交] → [自动构建] → [单元测试] → [部署上线]
    ↑                                         │
    └─────────────────────────────────────────┘
高亮节点：自动构建
标注：每次提交自动触发流水线，测试失败则回到代码修改
```

### 4.2 架构图

**适用场景**：系统组件、模块关系

**设计要求**：
- 分层展示（上层调用下层）
- 每层用不同背景色区分
- 组件用矩形+名称+一句话说明
- 连线标注交互方式（API调用、数据流、事件触发）

**描述格式**：
```
架构图：微服务电商系统
┌─────────────────────────┐
│  Gateway Layer           │ 浅蓝
│  [API Gateway] [Auth]    │
├─────────────────────────┤
│  Service Layer           │ 浅绿
│  [Order] [Payment] [Inv] │
├─────────────────────────┤
│  Data Layer              │ 浅灰
│  [MySQL] [Redis] [MQ]    │
└─────────────────────────┘
连线：API Gateway --路由--> Order Service
      Order Service --异步--> Payment Service
      Payment Service --缓存--> Redis
```

### 4.3 对比表

**适用场景**：两种方案优劣、版本差异、概念区分

**设计要求**：
- 2-3列，不超过6行
- 表头加粗+背景色
- 推荐项用绿色勾 ✓，不推荐用红色叉 ✗
- 关键差异行加高亮背景

### 4.4 时间线

**适用场景**：演进历史、版本迭代、学习路径

**设计要求**：
- 水平时间轴
- 节点标注时间+事件名
- 当前阶段用大圆点+详细说明
- 未来阶段用虚线

## 五、代码展示设计

### 5.1 代码片段

**重要**：整个PPT中最多只能有2页使用代码布局。优先使用"中文图示"替代代码。

**要求**：
- 语言标注（Python/YAML/JSON/Bash）
- 行号显示
- 关键行用黄色背景高亮（`highlight_lines`字段指定）
- 注释用灰色
- 每次展示不超过20行，超过的分成多个片段

**描述格式**：
```yaml
code_snippet:
  language: python
  title: "API限流器实现"
  content: |
    def rate_limiter(requests, window_sec=60, max_count=100):
        now = time.time()
        recent = [r for r in requests if now - r.timestamp < window_sec]
        if len(recent) >= max_count:
            return Response(status=429, body="请求过于频繁")
        
        requests.append(Request(timestamp=now))
        return process_request()
  highlight_lines: [3, 4, 5]
  annotation: "注意滑动窗口的设计：只统计最近N秒内的请求数，过期请求自动失效"
```

### 5.2 代码对比

**适用场景**：改进前后、正确/错误写法

**要求**：
- 左右分栏或上下对比
- 左/上 = Before（红色标题）
- 右/下 = After（绿色标题）
- 变更行高亮

## 六、动画与过渡效果

### 6.1 推荐的动画类型

| 动画类型 | 用途 | 描述方式 |
|---------|------|---------|
| fade_in | 渐进显示要点 | "要点1先出现，停顿2秒，要点2渐入" |
| highlight | 强调当前讨论的部分 | "高亮第3行代码，其余变灰" |
| zoom_in | 放大细节 | "放大架构图中的Checker模块" |
| build_up | 逐步构建完整图形 | "先画流程框，再画连线，再加标注" |
| morph | 概念变形/演进 | "方案A的架构图渐变为方案B" |

### 6.2 禁止的动画

- 旋转、弹跳、飞入等花哨效果
- 每页超过2种动画效果
- 动画时长超过3秒
- 无意义的装饰性动画

## 七、视觉素材清单规范

每集脚本必须附带完整的视觉素材清单，每个素材项包含：

```yaml
visual_asset:
  asset_id: "ep1_slide_03"
  type: "ppt_slide" | "flow_chart" | "architecture_diagram" | "comparison_table" | "code_snippet" | "timeline"
  title: "素材标题"
  description: "详细的视觉描述（足够让设计师或AI生成工具直接制作）"
  layout: "页面类型（参见2.1）"
  color_scheme: "light" | "dark"
  estimated_duration: "在视频中展示的秒数"
  animation: "动画效果描述（可选）"
```

## 八、Matplotlib/PIL 幻灯片绘制规范（核心章节）

当你使用 `execute_code` 通过 matplotlib/PIL 绘制幻灯片 PNG 时，**必须遵循本章节的设计规范**。

### 8.0 设计理念：高级极简

目标风格：**专业技术文档插图**——干净、温暖、层级清晰。

核心原则：
1. **暖色调**：米色/奶油色背景，不用冷灰色
2. **低饱和色**：所有颜色都柔和，不用高饱和鲜艳色
3. **嵌套层级**：用容器嵌套表达包含关系，而不是用装饰元素堆砌
4. **大量留白**：宁可空也不要挤——留白是高级感的来源
5. **极少色彩**：每页最多3种主题色，每种颜色对应一个固定语义
6. **字号落差大**：标题极大、正文中等、标注小——形成清晰视觉层级

**禁止的做法**：
- 不要在角落放半透明装饰圆（显得花哨）
- 不要用渐变强调条（过度设计）
- 不要把所有颜色都用上——克制是关键
- 不要用高饱和色做大面积填充

### 8.1 基础设置模板

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
import numpy as np
import os

# ===== 字体 =====
FONT_CANDIDATES = [
    '/System/Library/Fonts/PingFang.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
]
FONT_PATH = None
for _fp in FONT_CANDIDATES:
    if os.path.exists(_fp):
        FONT_PATH = _fp
        break

def fp(size, weight='normal'):
    props = fm.FontProperties(fname=FONT_PATH, size=size)
    if weight == 'bold':
        props.set_weight('bold')
    return props

# ===== 画布 =====
WIDTH, HEIGHT = 19.2, 10.8
DPI = 100

# ===== 配色系统：暖色调 + 低饱和 =====
C = {
    # 背景
    'bg_warm':   '#F5F0E8',   # 暖米色 — 内容页主背景
    'bg_cream':  '#FAF8F5',   # 更浅的奶油色 — 嵌套容器底色
    'bg_dark':   '#2D2D2D',   # 深灰（非纯黑）— 封面/代码页
    'bg_dark2':  '#3A3A3A',   # 略浅深灰 — 代码区域

    # 容器/卡片
    'card_white':  '#FFFFFF',
    'card_lavender': '#E8E4F0',  # 淡紫 — 第二层嵌套容器（低饱和）
    'card_blue':   '#E3EDF7',    # 淡蓝 — 辅助容器

    # 语义色（全部低饱和）
    'orange':      '#D4956A',   # 柔和橙 — 概念A/警告
    'orange_light':'#FDF2E9',   # 橙色浅底
    'green':       '#6BAF8D',   # 柔和绿 — 概念B/正确
    'green_light': '#E8F5EE',   # 绿色浅底
    'rose':        '#C47C7C',   # 柔和玫红 — 概念C/重要
    'rose_light':  '#FAE8E8',   # 玫红浅底
    'blue':        '#6B8DB5',   # 柔和蓝 — 信息/流程
    'blue_light':  '#E3EDF7',   # 蓝色浅底

    # 文字
    'text_black':  '#1A1A1A',   # 主文字 — 近黑（非纯黑）
    'text_dark':   '#4A4A4A',   # 次要文字
    'text_gray':   '#8A8A8A',   # 辅助说明
    'text_white':  '#FAFAFA',

    # 边框
    'border':      '#D5D0C8',   # 暖灰边框
    'border_light':'#E8E4DC',   # 更浅的边框
}
```

### 8.2 背景与容器

```python
def fill_bg(ax, fig, color=C['bg_warm']):
    """纯色暖背景 — 简洁即高级"""
    fig.patch.set_facecolor(color)
    ax.set_facecolor(color)

def draw_card(ax, x, y, w, h, fc=C['card_white'], ec=C['border'], lw=1.0, radius=0.3):
    """圆角卡片 — 不带阴影，靠边框和底色区分层级"""
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={radius}",
        facecolor=fc, edgecolor=ec, lw=lw, zorder=2
    )
    ax.add_patch(card)
    return card
```

**层级表达方式**（用嵌套容器而非阴影）：
```
最外层：bg_warm (#F5F0E8) 米色背景
  第一层容器：card_white (#FFFFFF) 白色 + 暖灰边框
    第二层容器：card_lavender (#E8E4F0) 淡紫底 + 浅边框
      第三层容器：card_white (#FFFFFF) 白色 + 语义色边框
```

### 8.3 标题设计

标题不需要竖色条或装饰线——**靠字号大小和粗细建立层级**。

```python
def draw_title(ax, title, x=1.2, y=9.8, size=34):
    """页面标题 — 大号粗体，左对齐"""
    ax.text(x, y, title, fontproperties=fp(size, 'bold'),
            ha='left', va='center', color=C['text_black'], zorder=5)

def draw_subtitle(ax, text, x=1.2, y=9.0, size=16):
    """副标题/说明 — 灰色小字"""
    ax.text(x, y, text, fontproperties=fp(size),
            ha='left', va='center', color=C['text_gray'], zorder=5)
```

### 8.4 标签胶囊（Tag Pill）

用于在容器内标注小类别，替代编号圆标——更轻量、更优雅。

```python
def draw_tag(ax, x, y, text, fc=C['orange_light'], ec=C['orange'], tc=C['orange']):
    """小标签胶囊 — 用于分类标注"""
    tw = len(text) * 0.22 + 0.6  # 自适应宽度
    tag = FancyBboxPatch((x, y - 0.2), tw, 0.4,
        boxstyle="round,pad=0.1", facecolor=fc, edgecolor=ec, lw=0.8, zorder=5)
    ax.add_patch(tag)
    ax.text(x + tw/2, y, text, fontproperties=fp(11, 'bold'),
            ha='center', va='center', color=tc, zorder=6)
```

### 8.5 箭头与连接线

```python
def draw_arrow(ax, x1, y1, x2, y2, color=C['text_gray'], lw=1.5):
    """简洁箭头 — 细灰线"""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='->', color=color, lw=lw, mutation_scale=15),
        zorder=4)

def draw_line(ax, x1, y1, x2, y2, color=C['border'], lw=1.0, style='-'):
    """连接线"""
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, linestyle=style, zorder=3)
```

### 8.6 图例（Legend）

当页面使用多种颜色区分概念时，在右下角放小图例说明颜色含义。

```python
def draw_legend(ax, items, x=14.5, y_start=2.5):
    """右下角小图例
    items = [('概念A', C['orange']), ('概念B', C['green']), ...]
    """
    for i, (label, color) in enumerate(items):
        y = y_start - i * 0.6
        circle = plt.Circle((x, y), 0.15, facecolor='none', edgecolor=color, lw=1.5, zorder=5)
        ax.add_patch(circle)
        ax.text(x + 0.4, y, label, fontproperties=fp(12),
                ha='left', va='center', color=C['text_dark'], zorder=5)
```

### 8.7 五种标准布局模板

#### 模板 A：封面页
```python
def layout_cover(ax, fig, title, subtitle=''):
    fill_bg(ax, fig, C['bg_warm'])
    # 居中大标题
    ax.text(9.6, 6.2, title, fontproperties=fp(48, 'bold'),
            ha='center', va='center', color=C['text_black'], zorder=5)
    if subtitle:
        ax.text(9.6, 4.8, subtitle, fontproperties=fp(20),
                ha='center', va='center', color=C['text_gray'], zorder=5)
```

#### 模板 B：嵌套架构图页
用于展示系统结构、包含关系、组件层级。**这是最核心的布局**。
```python
def layout_nested(ax, fig, title):
    """嵌套容器布局 — 用 draw_card 逐层嵌套表达包含关系"""
    fill_bg(ax, fig, C['bg_warm'])
    draw_title(ax, title)
    # 示意：外层容器
    draw_card(ax, 1.0, 0.8, 17.2, 8.0, fc=C['bg_cream'], ec=C['border'])
    # 内层容器
    draw_card(ax, 1.5, 1.2, 10.0, 7.2, fc=C['card_lavender'], ec=C['border_light'])
    # 最内层
    draw_card(ax, 2.0, 4.0, 5.0, 3.5, fc=C['card_white'], ec=C['orange'], lw=1.2)
    # ... 按需添加更多嵌套层
```

#### 模板 C：双栏对比页
```python
def layout_comparison(ax, fig, title, left_title, right_title):
    fill_bg(ax, fig, C['bg_warm'])
    draw_title(ax, title)
    # 左栏
    draw_card(ax, 1.0, 1.0, 8.0, 7.5, fc=C['card_white'], ec=C['border'])
    ax.text(5.0, 7.8, left_title, fontproperties=fp(20, 'bold'),
            ha='center', va='center', color=C['text_black'], zorder=5)
    # 右栏
    draw_card(ax, 10.2, 1.0, 8.0, 7.5, fc=C['card_white'], ec=C['border'])
    ax.text(14.2, 7.8, right_title, fontproperties=fp(20, 'bold'),
            ha='center', va='center', color=C['text_black'], zorder=5)
    # 内容用 ax.text 按需填充，标签用 draw_tag
```

#### 模板 D：要点列表页
```python
def layout_list(ax, fig, title, items):
    """纵向要点列表 — 每个卡片包含标题+说明+案例三层内容
    items = [{'title': '...', 'desc': '...', 'example': '例：...', 'color': 'blue'}, ...]
    """
    fill_bg(ax, fig, C['bg_warm'])
    draw_title(ax, title)
    n = len(items)
    item_h = min(1.8, 7.0 / n - 0.3)  # 适当增大卡片高度以容纳案例行
    for i, item in enumerate(items):
        y = 8.2 - i * (item_h + 0.3)
        color = item.get('color', 'blue')
        # 卡片
        draw_card(ax, 1.5, y - item_h, 16.2, item_h,
                  fc=C['card_white'], ec=C['border_light'])
        # 左侧色条
        bar = FancyBboxPatch((1.5, y - item_h), 0.15, item_h,
            boxstyle="round,pad=0.02", facecolor=C[color], edgecolor='none', zorder=4)
        ax.add_patch(bar)
        # 标题行
        ax.text(2.3, y - item_h * 0.25, item['title'],
                fontproperties=fp(18, 'bold'), ha='left', va='center',
                color=C['text_black'], zorder=5)
        # 说明行
        if item.get('desc'):
            ax.text(2.3, y - item_h * 0.52, item['desc'],
                    fontproperties=fp(13), ha='left', va='center',
                    color=C['text_dark'], zorder=5)
        # 案例行（灰色小字，必须有）
        if item.get('example'):
            ax.text(2.3, y - item_h * 0.78, item['example'],
                    fontproperties=fp(11), ha='left', va='center',
                    color=C['text_gray'], zorder=5)
```

**要点卡片内容三层结构**（必须遵循）：
```
┌──────────────────────────────────────────┐
│▎ 概念标题（18pt 粗体黑色）               │
│  一句话说明这个概念的含义（13pt 深灰）    │
│  例：来自源材料的具体案例（11pt 浅灰）    │
└──────────────────────────────────────────┘
```
每个卡片**必须**包含案例行。如果一个概念没有具体案例，说明拆解得不够——要么补案例，要么合并到其他概念中。
```

#### 模板 E：流程图页
```python
def layout_flow(ax, fig, title, steps):
    """横向流程 — 用卡片+箭头"""
    fill_bg(ax, fig, C['bg_warm'])
    draw_title(ax, title)
    n = len(steps)
    margin = 1.5
    usable = WIDTH - 2 * margin
    sw = min(2.5, (usable - (n-1) * 1.0) / n)
    gap = (usable - n * sw) / max(n-1, 1)
    yc = 4.5
    for i, step in enumerate(steps):
        x = margin + i * (sw + gap)
        color = step.get('color', 'blue')
        draw_card(ax, x, yc - 1.2, sw, 2.4, fc=C['card_white'], ec=C[color], lw=1.2)
        ax.text(x + sw/2, yc + 0.3, step['name'], fontproperties=fp(15, 'bold'),
                ha='center', va='center', color=C['text_black'], zorder=5)
        if step.get('desc'):
            ax.text(x + sw/2, yc - 0.4, step['desc'], fontproperties=fp(11),
                    ha='center', va='center', color=C['text_gray'], zorder=5)
        if i < n - 1:
            ax_end = x + sw + gap * 0.2
            draw_arrow(ax, ax_end, yc, ax_end + gap * 0.6, yc)
```

### 8.8 视觉规则

| 编号 | 规则 | 要求 |
|------|------|-----|
| V1 | 暖色调背景 | 使用 `#F5F0E8`（米色）或 `#FAF8F5`（奶油色），禁止冷灰色 `#F8FAFC` |
| V2 | 低饱和色 | 所有主题色使用柔和色调（如 `#D4956A` 而非 `#F59E0B`），禁止高饱和荧光色 |
| V3 | 嵌套表层级 | 用容器嵌套而非阴影/装饰来表达信息层级 |
| V4 | 极简装饰 | 不要放半透明装饰圆、渐变强调条等花哨元素——留白就是最好的装饰 |
| V5 | 字号落差大 | 标题 34-48pt → 小标题 18-22pt → 正文 13-16pt → 标注 11-12pt |
| V6 | 每页≤3色 | 除黑/白/灰外，每页最多使用3种语义色 |
| V7 | 留白充足 | 元素之间、元素与边缘之间保持宽裕间距（≥1.0单位） |
| V8 | 色彩绑定语义 | 同一颜色在整套幻灯片中始终代表同一个概念 |
| V9 | 标签用胶囊 | 分类标注使用 `draw_tag()` 胶囊，不用实心圆标 |
| V10 | 不重复嵌入 | 不要先生成图片再截图嵌入；直接在画布上绘制 |

### 8.9 常见错误与修正

**错误1：高饱和色大面积填充**
```python
# ❌ 左栏整个填充鲜红底色
draw_card(ax, 1, 2, 8, 6, fc='#FEE2E2', ec='#EF4444')

# ✅ 白底卡片 + 语义色细边框 + 内部标签标注
draw_card(ax, 1, 2, 8, 6, fc=C['card_white'], ec=C['rose'], lw=1.2)
draw_tag(ax, 1.5, 7.2, '问题', fc=C['rose_light'], ec=C['rose'], tc=C['rose'])
```

**错误2：装饰过度**
```python
# ❌ 渐变背景 + 装饰圆 + 渐变强调条 + 渐变分隔线
draw_gradient_bg(ax, fig, '#EEF2FF', '#F8FAFC')
draw_decorative_circles(ax, theme='light')
draw_accent_bar(ax, COLORS['primary'])

# ✅ 纯色暖背景，干净
fill_bg(ax, fig, C['bg_warm'])
```

**错误3：裸文字堆砌**
```python
# ❌ 直接在空白画布上堆文字
ax.text(2, 8, '第一点', fontproperties=fp(16))
ax.text(2, 6, '第二点', fontproperties=fp(16))

# ✅ 用卡片组织，色条标识
draw_card(ax, 1.5, 7, 16, 1.2, fc=C['card_white'], ec=C['border_light'])
bar = FancyBboxPatch((1.5, 7), 0.15, 1.2,
    boxstyle="round,pad=0.02", facecolor=C['blue'], edgecolor='none', zorder=4)
ax.add_patch(bar)
ax.text(2.2, 7.6, '第一点', fontproperties=fp(16, 'bold'), ...)
```

**错误4：先生成图片再嵌入幻灯片**
```python
# ❌ 二次渲染
img = Image.open('images/diagram.png')
ax.imshow(img, ...)

# ✅ 直接在画布上用 draw_card + draw_arrow + draw_tag 绘制
```
