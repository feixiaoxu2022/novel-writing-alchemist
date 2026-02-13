#!/bin/bash
# 使用新的checklist重新评测已有的agent执行结果
#
# 支持两种模式：
#   模式1（旧）：--samples 从样本文件中提取checklist
#   模式2（新）：--revision 从 check_revisions/rev_NNN/ 读取checklist
#
# 推荐使用模式2，无需重新生成完整样本即可迭代评测方案。

set -e

# 默认参数
AGENT_RESULTS_DIR=""
SAMPLES_FILE=""
REVISION=""          # 新增：revision编号（如 001, 002）
DESIGN_DIR=""        # 新增：design目录（如 design_v2），用于定位 check_revisions
OUTPUT_SUFFIX=""     # 输出文件后缀，默认为空（覆盖原check_result.json）
MODEL="gpt-5.2"     # 默认使用gpt-5进行评估
DATA_ID=""           # 可选，仅处理指定样本
RESUME=false         # 新增：resume模式，跳过已有结果的样本
ONLY_CHECKS=""       # 增量模式：只执行指定检查项（逗号分隔序号，如 33,35,36）
ADD_MODE=false       # 增量模式：在已有结果上增跑新检查项

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --agent-results)
            AGENT_RESULTS_DIR="$2"
            shift 2
            ;;
        --samples)
            SAMPLES_FILE="$2"
            shift 2
            ;;
        --revision)
            REVISION="$2"
            shift 2
            ;;
        --design-dir)
            DESIGN_DIR="$2"
            shift 2
            ;;
        --output-suffix)
            OUTPUT_SUFFIX="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --data-id)
            DATA_ID="$2"
            shift 2
            ;;
        --resume)
            RESUME=true
            shift
            ;;
        --only-checks)
            ONLY_CHECKS="$2"
            shift 2
            ;;
        --add)
            ADD_MODE=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$AGENT_RESULTS_DIR" ]; then
    echo "使用方式:"
    echo ""
    echo "  模式1（旧）- 从样本文件提取checklist:"
    echo "  $0 \\"
    echo "    --agent-results <agent执行结果目录> \\"
    echo "    --samples <样本文件(包含新checklist)> \\"
    echo "    [--output-suffix <输出文件后缀，如_v3>] \\"
    echo "    [--model <模型名，默认gpt-5.2>] \\"
    echo "    [--data-id <仅处理指定样本>]"
    echo ""
    echo "  模式2（推荐）- 从 check_definitions/check_revisions 读取:"
    echo "  $0 \\"
    echo "    --agent-results <agent执行结果目录> \\"
    echo "    --revision <revision编号，如 003> \\"
    echo "    [--resume] \\"
    echo "    [--add] \\"
    echo "    [--only-checks <检查项序号，如 33,35,36>] \\"
    echo "    [--model <模型名，默认gpt-5.2>] \\"
    echo "    [--data-id <仅处理指定样本>]"
    echo ""
    echo "示例:"
    echo "  # 模式2：使用 revision 003 重新评测"
    echo "  $0 \\"
    echo "    --agent-results evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101 \\"
    echo "    --revision 003"
    echo ""
    echo "  # 模式2 + resume：跳过已有结果，只处理未完成的样本"
    echo "  $0 \\"
    echo "    --agent-results evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101 \\"
    echo "    --revision 003 \\"
    echo "    --resume"
    echo ""
    echo "  # 增量模式：只重跑第33,35,36项检查（在已有结果上覆盖这些项）"
    echo "  $0 \\"
    echo "    --agent-results evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101 \\"
    echo "    --revision 004 \\"
    echo "    --only-checks 33,35,36"
    echo ""
    echo "  # add模式：在已有结果上增跑新增的检查项（跳过已有项）"
    echo "  $0 \\"
    echo "    --agent-results evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101 \\"
    echo "    --revision 004 \\"
    echo "    --add"
    echo ""
    echo "  # 模式1（旧）：从样本文件提取"
    echo "  $0 \\"
    echo "    --agent-results evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101 \\"
    echo "    --samples design_v1/samples/eval_v3.jsonl \\"
    echo "    --output-suffix _v3"
    echo ""
    echo "  # 测试单个样本"
    echo "  $0 \\"
    echo "    --agent-results evaluation_outputs/eval_v2_20260205_132400_claude-opus-4-5-20251101 \\"
    echo "    --revision 003 \\"
    echo "    --data-id NW_CLEAR_SHORT_SWEET_001"
    exit 1
fi

# 确定工作模式
MODE=""
if [ -n "$REVISION" ]; then
    MODE="revision"
elif [ -n "$SAMPLES_FILE" ]; then
    MODE="samples"
else
    echo "错误: 必须指定 --revision 或 --samples 之一"
    exit 1
fi

# Revision 模式：设置路径
if [ "$MODE" = "revision" ]; then
    # 获取脚本所在目录（scripts/），再向上一层到场景根目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    SCENARIO_ROOT="$SCRIPT_DIR/.."

    # 新结构：check_revisions 在 check_definitions/ 目录下
    REVISION_DIR="$SCENARIO_ROOT/check_definitions/check_revisions/rev_${REVISION}"
    CHECKLIST_FILE="$REVISION_DIR/checklist.jsonl"
    CRITERIA_DIR="$REVISION_DIR/judge_criteria"

    if [ ! -d "$REVISION_DIR" ]; then
        echo "错误: revision 目录不存在: $REVISION_DIR"
        exit 1
    fi
    if [ ! -f "$CHECKLIST_FILE" ]; then
        echo "错误: checklist 文件不存在: $CHECKLIST_FILE"
        exit 1
    fi

    # 自动设置 output_suffix（如果用户没有手动指定）
    if [ -z "$OUTPUT_SUFFIX" ]; then
        OUTPUT_SUFFIX="_rev${REVISION}"
    fi

    echo "模式: revision (从 check_definitions/check_revisions 读取)"
    echo "Revision 目录: $REVISION_DIR"
fi

# 根据模型名自动选择API端点和密钥（参考run_test.sh）
if [[ "$MODEL" == ernie-* ]]; then
    # ERNIE模型使用千帆API
    API_KEY="bce-v3/ALTAK-mCOi62yEOQCJIvZVDI521/10000568a22b656d14d37bb80abb5da439026f1a"
    API_BASE="https://qianfan.baidubce.com/v2"

    # 模型名映射：简写 -> 完整名称
    case "$MODEL" in
        "ernie-5.0")
            MODEL="ernie-5.0-thinking-preview"
            echo "✓ 已将模型名映射为: $MODEL"
            ;;
    esac

    echo "✓ 检测到ERNIE模型，使用千帆API端点: $API_BASE"
else
    # 其他模型使用内部API
    API_KEY="sk-3AYbtGCuXtiVmCDd8nfJoKwNibOagcDswEJiJLwJnOjwPVVF"
    API_BASE="http://yy.dbh.baidu-int.com/v1"
    echo "✓ 使用内部API端点: $API_BASE"
fi

# 检查路径
if [ ! -d "$AGENT_RESULTS_DIR" ]; then
    echo "错误: agent执行结果目录不存在: $AGENT_RESULTS_DIR"
    exit 1
fi

if [ "$MODE" = "samples" ] && [ ! -f "$SAMPLES_FILE" ]; then
    echo "错误: 样本文件不存在: $SAMPLES_FILE"
    exit 1
fi

# 统计
SUCCESS_COUNT=0
FAILED_COUNT=0
SKIPPED_COUNT=0

echo "=========================================="
echo "Recheck 开始"
echo "=========================================="
echo "Agent执行结果目录: $AGENT_RESULTS_DIR"
if [ "$MODE" = "revision" ]; then
    echo "Revision: $REVISION"
    echo "Checklist: $CHECKLIST_FILE"
    echo "Judge Criteria: $CRITERIA_DIR"
else
    echo "样本文件: $SAMPLES_FILE"
fi
echo "输出后缀: ${OUTPUT_SUFFIX:-无（覆盖原文件）}"
echo "模型: $MODEL"
echo "API端点: $API_BASE"
echo "Resume模式: $RESUME"
echo "Add模式: $ADD_MODE"
echo "指定检查项: ${ONLY_CHECKS:-全部}"
echo ""

# 获取脚本所在目录（可能在前面已经设置过）
SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"

# 遍历agent执行结果
for result_json in "$AGENT_RESULTS_DIR"/*.json; do
    # 跳过非agent结果文件
    basename=$(basename "$result_json" .json)
    if [[ "$basename" == summary_* ]] || [[ "$basename" == temp_* ]] || [[ "$basename" == execution_report ]]; then
        continue
    fi

    # 如果指定了data_id，只处理该样本
    if [ -n "$DATA_ID" ] && [ "$basename" != "$DATA_ID" ]; then
        continue
    fi

    env_dir="$AGENT_RESULTS_DIR/${basename}_env"

    # 转换result_json为绝对路径（避免cd后路径失效）
    result_json_abs="$(cd "$(dirname "$result_json")" && pwd)/$(basename "$result_json")"

    # 检查env目录是否存在
    if [ ! -d "$env_dir" ]; then
        echo "⚠️  $basename: env目录不存在，跳过"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    # 转换env_dir为绝对路径（在确认目录存在后）
    env_dir_abs="$(cd "$env_dir" && pwd)"

    # 检查checker.py是否存在
    if [ ! -f "$env_dir/checker.py" ]; then
        echo "⚠️  $basename: checker.py不存在，跳过"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    # 确定输出文件名（提前计算，用于resume检查）
    if [ -n "$OUTPUT_SUFFIX" ]; then
        output_file="check_result${OUTPUT_SUFFIX}.json"
    else
        output_file="check_result.json"
    fi

    # Resume模式：检查输出文件是否已存在（--add和--only-checks模式下不跳过）
    if [ "$RESUME" = true ] && [ -f "$env_dir/$output_file" ] && [ "$ADD_MODE" = false ] && [ -z "$ONLY_CHECKS" ]; then
        echo "⏭️  $basename: 已存在 $output_file，跳过"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    echo "------------------------------------------"
    echo "处理样本: $basename"

    # 构造bench.json
    temp_bench="$env_dir_abs/temp_bench_recheck.json"

    if [ "$MODE" = "revision" ]; then
        # Revision 模式：从 checklist.jsonl 提取，并部署 judge_criteria
        python3 "$SCRIPT_DIR/extract_bench_from_revision.py" \
            --checklist "$CHECKLIST_FILE" \
            --data-id "$basename" \
            --output "$temp_bench" \
            --deploy-criteria-dir "$CRITERIA_DIR" \
            --env-dir "$env_dir_abs"
    else
        # Samples 模式（旧）：从样本文件提取
        python3 "$SCRIPT_DIR/extract_bench_from_sample.py" \
            --samples "$SAMPLES_FILE" \
            --data-id "$basename" \
            --output "$temp_bench" \
            --deploy-env-dir "$env_dir_abs"
    fi

    if [ $? -ne 0 ]; then
        echo "❌ $basename: 构造bench.json失败"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        continue
    fi

    # 使用支持v3扩展类型的最新版checker（切换到checker目录执行，解决import依赖）
    CHECKER_DIR="$SCRIPT_DIR/../env"
    cd "$CHECKER_DIR"

    # 构建checker.py调用命令
    CHECKER_CMD=(
        python3 checker.py
        --bench "$temp_bench"
        --result "$result_json_abs"
        --model "$MODEL"
        --base-url "$API_BASE"
        --api-key "$API_KEY"
        --output "$env_dir_abs/$output_file"
        --work-dir "$env_dir_abs"
    )

    # 增量模式：传递已有结果和指定检查项
    existing_result_file="$env_dir_abs/$output_file"
    if [ "$ADD_MODE" = true ] && [ -f "$existing_result_file" ]; then
        CHECKER_CMD+=(--existing-result "$existing_result_file")
        echo "  [增量] 基于已有结果: $output_file"
    fi
    if [ -n "$ONLY_CHECKS" ]; then
        CHECKER_CMD+=(--only-checks "$ONLY_CHECKS")
        # --only-checks 隐含需要已有结果（如果存在的话）
        if [ "$ADD_MODE" = false ] && [ -f "$existing_result_file" ]; then
            CHECKER_CMD+=(--existing-result "$existing_result_file")
        fi
        echo "  [指定] 只执行检查项: $ONLY_CHECKS"
    fi

    "${CHECKER_CMD[@]}"

    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "✅ $basename: recheck完成 -> $output_file"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "❌ $basename: recheck失败"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi

    # 清理临时文件并返回原目录
    rm -f "$temp_bench"
    cd - > /dev/null
done

echo ""
echo "=========================================="
echo "Recheck 完成"
echo "=========================================="
echo "成功: $SUCCESS_COUNT"
echo "失败: $FAILED_COUNT"
echo "跳过: $SKIPPED_COUNT"
echo ""

if [ $FAILED_COUNT -gt 0 ]; then
    exit 1
fi
