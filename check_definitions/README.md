# Check Definitions - 检查项定义（与场景输入解耦）

本目录包含小说创作场景的所有检查项定义，**与场景输入版本（design_v1/design_v2）解耦**。

## 目录结构

```
check_definitions/
├── README.md                       # 本文件
├── common_check_list.yaml          # 通用检查项（所有模板共用）
├── template_checks/                # 各模板特有的检查项
│   ├── NW_VAGUE_MEDIUM_SWEET_DRAMA.yaml
│   ├── NW_CLEAR_SHORT_SWEET.yaml
│   └── ...
├── judge_criteria/                 # LLM评判标准
│   ├── content_quality_basic.yaml  # 内容质量基础评判标准
│   └── emotional_delivery.yaml     # 情感交付评判标准
└── check_revisions/                # 检查方案版本管理
    ├── REVISION_LOG.yaml           # 版本日志
    ├── rev_001/                    # 版本001
    ├── rev_002/                    # 版本002
    └── rev_003/                    # 版本003（当前活跃）
```

## 解耦设计说明

### 为什么解耦？

之前的设计中，checklist定义嵌入在`design_v1/unified_scenario_design.yaml`和`design_v2/unified_scenario_design.yaml`中。
这导致每次修改检查项都需要同步两个版本，增加了维护负担和出错风险。

**场景输入版本（v1/v2）** 管理的内容：
- query（用户输入）
- system prompt
- hitl_responses（用户模拟器预设回复）
- user_simulator_prompt

**检查项版本（check_definitions）** 管理的内容：
- 通用检查项（common_check_list.yaml）
- 模板特有检查项（template_checks/*.yaml）
- LLM评判标准（judge_criteria/*.yaml）

两者是**正交的维度**，应该独立演进。

### 如何使用？

1. **修改检查项**：直接编辑本目录下的文件
2. **创建新revision**：
   ```bash
   cd design_v2
   python scripts/sample_generator/main.py --export-check-revision ../check_definitions/check_revisions/rev_NNN
   ```
3. **生成样本时**：sample_generator会自动从`../check_definitions/`读取检查项定义

## 版本历史

| 版本 | 日期 | 检查项数 | 主要变更 |
|------|------|----------|----------|
| rev_001 | 2026-02-10 | 39 | 初始版本 |
| rev_002 | 2026-02-10 | 38 | 移除emotional_tendency_consistency |
| rev_003 | 2026-02-11 | 41 | 新增repeated_endings、late_stage_digression、读取CONSISTENCY_MANAGEMENT_GUIDE.md |

详细变更记录见 `check_revisions/REVISION_LOG.yaml`
