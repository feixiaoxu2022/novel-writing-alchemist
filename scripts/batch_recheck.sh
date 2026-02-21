#!/bin/bash
# 批量运行 recheck_with_new_checklist.sh，对所有匹配的 eval 目录执行评测
#
# 支持并行执行多个模型目录（--parallel N），每个目录内部仍然串行处理样本。
# 支持 --resume 模式，跳过已有结果的样本。
# 支持 --pattern 过滤目录。
# 支持 --dry-run 模式，只显示将要执行的命令，不实际执行。
# 支持三种 checklist 来源模式：
#   1. inline（默认）：check_list 内嵌在样本 JSON 中
#   2. revision：从 check_definitions/check_revisions/rev_NNN/ 读取
#   3. samples：从样本 JSONL 文件提取 check_list
#
# 三个场景共享同一份脚本，场景差异通过下方「场景配置区」参数化。
#
# 用法示例:
#   # inline模式（默认）
#   ./scripts/batch_recheck.sh --parallel 3
#
#   # revision 模式
#   ./scripts/batch_recheck.sh --revision 003 --parallel 3
#
#   # 只跑特定模型目录
#   ./scripts/batch_recheck.sh --pattern "*claude*"
#
#   # 只重跑指定检查项（增量覆盖）
#   ./scripts/batch_recheck.sh --only-checks '场景数量合理,内容单元密度' --add
#
#   # dry-run 预览
#   ./scripts/batch_recheck.sh --dry-run

set -e

# ==================== 场景配置区（三个场景唯一不同的部分） ====================
# 修改以下变量适配不同场景，其余代码完全一致
DEFAULT_PATTERN="eval_dsv*"                                      # eval 目录匹配模式
MODEL_NAME_SED='s/eval_dsv[0-9]*_[0-9]*_[0-9]*_//'              # 从目录名提取模型名的 sed 表达式
# =============================================================================

# ==================== 参数 ====================
REVISION=""
PARALLEL=1          # 并行数，默认串行
PATTERN="$DEFAULT_PATTERN"
MODEL="gpt-5.2"    # judge 模型
RESUME=false
DRY_RUN=false
DATA_ID=""          # 可选：仅处理指定样本
OUTPUT_SUFFIX=""    # 可选：覆盖自动生成的后缀
ONLY_CHECKS=""      # 增量模式：只执行指定检查项
ADD_MODE=false      # 增量模式：在已有结果上增跑新检查项
SAMPLES_FILE=""     # samples模式：从样本JSONL提取check_list（优先于inline）

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --revision)
            REVISION="$2"
            shift 2
            ;;
        --parallel)
            PARALLEL="$2"
            shift 2
            ;;
        --pattern)
            PATTERN="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --resume)
            RESUME=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --data-id)
            DATA_ID="$2"
            shift 2
            ;;
        --output-suffix)
            OUTPUT_SUFFIX="$2"
            shift 2
            ;;
        --only-checks)
            ONLY_CHECKS="$2"
            shift 2
            ;;
        --add)
            ADD_MODE=true
            shift
            ;;
        --samples)
            SAMPLES_FILE="$2"
            shift 2
            ;;
        -h|--help)
            echo "用法: $0 [选项]"
            echo ""
            echo "参数:"
            echo "  --revision <NNN>      checklist revision 编号（如 003）。不指定则使用 inline 模式"
            echo ""
            echo "可选参数:"
            echo "  --parallel <N>        并行执行的目录数（默认 1，串行）"
            echo "  --pattern <glob>      eval 目录匹配模式（默认 $DEFAULT_PATTERN）"
            echo "  --model <name>        judge 模型名称（默认 gpt-5.2）"
            echo "  --resume              跳过已有结果的样本"
            echo "  --dry-run             只显示将要执行的命令"
            echo "  --data-id <id>        仅处理指定 data_id 的样本"
            echo "  --output-suffix <s>   覆盖自动后缀（默认 _revNNN）"
            echo "  --only-checks <ids>   只执行指定检查项（逗号分隔，支持语义ID如'场景数量合理,音效BGM覆盖'，也兼容数字序号如'33,35,36'）"
            echo "  --add                 增量模式：在已有结果上增跑新检查项"
            echo "  --samples <file>      从样本JSONL提取check_list（samples模式，优先于inline）"
            echo "  -h, --help            显示帮助"
            echo ""
            echo "示例:"
            echo "  # inline模式（默认，check_list内嵌在样本JSON中）"
            echo "  $0 --parallel 3"
            echo ""
            echo "  # revision 模式，3路并行"
            echo "  $0 --revision 003 --parallel 3"
            echo ""
            echo "  # 只跑 claude 相关目录"
            echo "  $0 --pattern '*claude*'"
            echo ""
            echo "  # resume + 并行"
            echo "  $0 --parallel 3 --resume"
            echo ""
            echo "  # 只重跑指定检查项（语义ID）"
            echo "  $0 --only-checks '场景数量合理,内容单元密度' --add"
            echo ""
            echo "  # 只重跑指定检查项（数字序号，向后兼容）"
            echo "  $0 --only-checks 33,35,36 --add"
            echo ""
            echo "  # 增量模式：在已有结果上增跑新增的检查项"
            echo "  $0 --revision 004 --add"
            echo ""
            echo "  # samples模式：从新JSONL提取check_list，只重跑指定检查项"
            echo "  $0 --samples samples/eval_v3.jsonl --only-checks '检查项名称' --parallel 4"
            exit 0
            ;;
        *)
            echo "未知参数: $1（使用 -h 查看帮助）"
            exit 1
            ;;
    esac
done

# 确定 checklist 来源模式
# 优先级：--samples > --revision > inline（默认）
INLINE_FLAG=""
SAMPLES_FLAG=""
if [ -n "$SAMPLES_FILE" ]; then
    SAMPLES_FLAG="--samples $SAMPLES_FILE"
elif [ -z "$REVISION" ]; then
    INLINE_FLAG="--inline"
fi

# ==================== 路径设置 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCENARIO_ROOT="$SCRIPT_DIR/.."
EVAL_OUTPUTS_DIR="$SCENARIO_ROOT/evaluation_outputs"
RECHECK_SCRIPT="$SCRIPT_DIR/recheck_with_new_checklist.sh"

# 验证
if [ ! -f "$RECHECK_SCRIPT" ]; then
    echo "错误: recheck 脚本不存在: $RECHECK_SCRIPT"
    exit 1
fi

if [ -n "$REVISION" ]; then
    REVISION_DIR="$SCENARIO_ROOT/check_definitions/check_revisions/rev_${REVISION}"
    if [ ! -d "$REVISION_DIR" ]; then
        echo "错误: revision 目录不存在: $REVISION_DIR"
        exit 1
    fi
fi

if [ -n "$SAMPLES_FILE" ] && [ ! -f "$SAMPLES_FILE" ]; then
    echo "错误: 样本文件不存在: $SAMPLES_FILE"
    exit 1
fi

# ==================== 扫描目录 ====================
DIRS=()
while IFS= read -r dir; do
    DIRS+=("$dir")
done < <(find "$EVAL_OUTPUTS_DIR" -maxdepth 1 -type d -name "$PATTERN" | sort)

if [ ${#DIRS[@]} -eq 0 ]; then
    echo "错误: 未找到匹配 '$PATTERN' 的目录在 $EVAL_OUTPUTS_DIR"
    exit 1
fi

# ==================== 显示计划 ====================
echo "=========================================="
echo "  Batch Recheck"
echo "=========================================="
if [ -n "$SAMPLES_FILE" ]; then
    echo "Checklist:   samples模式（从 $SAMPLES_FILE 提取）"
elif [ -n "$REVISION" ]; then
    echo "Checklist:   rev_${REVISION}"
else
    echo "Checklist:   inline模式（内嵌在样本JSON中）"
fi
echo "Judge 模型:  $MODEL"
echo "并行数:      $PARALLEL"
echo "Resume:      $RESUME"
echo "Add模式:     $ADD_MODE"
echo "指定检查项:  ${ONLY_CHECKS:-全部}"
echo "目录模式:    $PATTERN"
echo ""
echo "将处理 ${#DIRS[@]} 个目录:"
for dir in "${DIRS[@]}"; do
    model_name=$(basename "$dir" | sed "$MODEL_NAME_SED")
    echo "  - $(basename "$dir")  [$model_name]"
done
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] 以下命令将被执行:"
    echo ""
    for dir in "${DIRS[@]}"; do
        # 检测 execution/ 子目录（某些场景 agent 结果在子目录下）
        local_dir="$dir"
        if [ -d "$dir/execution" ]; then
            local_dir="$dir/execution"
        fi
        cmd="bash $RECHECK_SCRIPT --agent-results $local_dir --model $MODEL"
        if [ -n "$REVISION" ]; then
            cmd="$cmd --revision $REVISION"
        fi
        if [ -n "$SAMPLES_FLAG" ]; then
            cmd="$cmd $SAMPLES_FLAG"
        fi
        if [ -n "$INLINE_FLAG" ]; then
            cmd="$cmd $INLINE_FLAG"
        fi
        if [ "$RESUME" = true ]; then
            cmd="$cmd --resume"
        fi
        if [ -n "$DATA_ID" ]; then
            cmd="$cmd --data-id $DATA_ID"
        fi
        if [ -n "$OUTPUT_SUFFIX" ]; then
            cmd="$cmd --output-suffix $OUTPUT_SUFFIX"
        fi
        if [ -n "$ONLY_CHECKS" ]; then
            cmd="$cmd --only-checks '$ONLY_CHECKS'"
        fi
        if [ "$ADD_MODE" = true ]; then
            cmd="$cmd --add"
        fi
        echo "  $cmd"
    done
    echo ""
    echo "[DRY RUN] 结束。去掉 --dry-run 实际执行。"
    exit 0
fi

# ==================== 执行 ====================
# 日志目录
if [ -n "$REVISION" ]; then
    LOG_DIR="$SCENARIO_ROOT/logs/batch_recheck_rev${REVISION}_$(date +%Y%m%d_%H%M%S)"
elif [ -n "$SAMPLES_FILE" ]; then
    LOG_DIR="$SCENARIO_ROOT/logs/batch_recheck_samples_$(date +%Y%m%d_%H%M%S)"
else
    LOG_DIR="$SCENARIO_ROOT/logs/batch_recheck_inline_$(date +%Y%m%d_%H%M%S)"
fi
mkdir -p "$LOG_DIR"
echo "日志目录: $LOG_DIR"
echo ""

# 构建每个目录的 recheck 命令并行执行
run_single_dir() {
    local dir="$1"
    local log_file="$2"
    local dir_name
    dir_name=$(basename "$dir")
    local model_name
    model_name=$(echo "$dir_name" | sed "$MODEL_NAME_SED")

    echo "[START] $dir_name ($model_name)" | tee -a "$log_file"
    local start_time
    start_time=$(date +%s)

    # 检测 execution/ 子目录（某些场景 agent 结果在子目录下）
    local agent_results_dir="$dir"
    if [ -d "$dir/execution" ]; then
        agent_results_dir="$dir/execution"
    fi

    # 构建 recheck 命令
    local cmd=(
        bash "$RECHECK_SCRIPT"
        --agent-results "$agent_results_dir"
        --model "$MODEL"
    )
    if [ -n "$REVISION" ]; then
        cmd+=(--revision "$REVISION")
    fi
    if [ -n "$SAMPLES_FILE" ]; then
        cmd+=(--samples "$SAMPLES_FILE")
    fi
    if [ -n "$INLINE_FLAG" ]; then
        cmd+=($INLINE_FLAG)
    fi
    if [ "$RESUME" = true ]; then
        cmd+=(--resume)
    fi
    if [ -n "$DATA_ID" ]; then
        cmd+=(--data-id "$DATA_ID")
    fi
    if [ -n "$OUTPUT_SUFFIX" ]; then
        cmd+=(--output-suffix "$OUTPUT_SUFFIX")
    fi
    if [ -n "$ONLY_CHECKS" ]; then
        cmd+=(--only-checks "$ONLY_CHECKS")
    fi
    if [ "$ADD_MODE" = true ]; then
        cmd+=(--add)
    fi

    # 执行，输出写入日志
    if "${cmd[@]}" >> "$log_file" 2>&1; then
        local end_time
        end_time=$(date +%s)
        local elapsed=$((end_time - start_time))
        echo "[DONE]  $dir_name ($model_name) - ${elapsed}s" | tee -a "$log_file"
        return 0
    else
        local end_time
        end_time=$(date +%s)
        local elapsed=$((end_time - start_time))
        echo "[FAIL]  $dir_name ($model_name) - ${elapsed}s" | tee -a "$log_file"
        return 1
    fi
}

# 导出函数和变量供子进程使用（parallel 模式需要）
export -f run_single_dir
export RECHECK_SCRIPT REVISION MODEL RESUME DATA_ID OUTPUT_SUFFIX ONLY_CHECKS ADD_MODE INLINE_FLAG SAMPLES_FILE MODEL_NAME_SED

TOTAL=${#DIRS[@]}
SUCCESS=0
FAIL=0

if [ "$PARALLEL" -le 1 ]; then
    # ====== 串行模式 ======
    for i in "${!DIRS[@]}"; do
        dir="${DIRS[$i]}"
        dir_name=$(basename "$dir")
        log_file="$LOG_DIR/${dir_name}.log"

        echo "[$((i+1))/$TOTAL] 开始处理: $dir_name"
        if run_single_dir "$dir" "$log_file"; then
            SUCCESS=$((SUCCESS + 1))
        else
            FAIL=$((FAIL + 1))
        fi
        echo ""
    done
else
    # ====== 并行模式 ======
    echo "并行执行中（最多 $PARALLEL 路同时运行）..."
    echo ""

    PIDS=()
    PIDMAP=()
    RUNNING=0

    for dir in "${DIRS[@]}"; do
        dir_name=$(basename "$dir")
        log_file="$LOG_DIR/${dir_name}.log"

        # 等待直到有空闲槽
        while [ $RUNNING -ge "$PARALLEL" ]; do
            wait -n 2>/dev/null || true
            RUNNING=0
            for pid in "${PIDS[@]}"; do
                if kill -0 "$pid" 2>/dev/null; then
                    RUNNING=$((RUNNING + 1))
                fi
            done
        done

        # 启动后台任务
        run_single_dir "$dir" "$log_file" &
        local_pid=$!
        PIDS+=("$local_pid")
        PIDMAP+=("$dir_name")
        RUNNING=$((RUNNING + 1))
        echo "[QUEUED] $dir_name (PID: $local_pid)"
    done

    # 等待所有子进程完成
    echo ""
    echo "等待所有任务完成..."
    for i in "${!PIDS[@]}"; do
        pid="${PIDS[$i]}"
        dir_name="${PIDMAP[$i]}"
        if wait "$pid"; then
            SUCCESS=$((SUCCESS + 1))
        else
            FAIL=$((FAIL + 1))
        fi
    done
fi

# ==================== 汇总报告 ====================
echo ""
echo "=========================================="
echo "  Batch Recheck 汇总"
echo "=========================================="
echo "总计:  $TOTAL 个目录"
echo "成功:  $SUCCESS"
echo "失败:  $FAIL"
echo "日志:  $LOG_DIR"
echo ""

echo "各目录详情:"
for dir in "${DIRS[@]}"; do
    dir_name=$(basename "$dir")
    model_name=$(echo "$dir_name" | sed "$MODEL_NAME_SED")
    log_file="$LOG_DIR/${dir_name}.log"

    if [ -f "$log_file" ]; then
        success_count=$(grep -c "^✅" "$log_file" 2>/dev/null || echo "0")
        fail_count=$(grep -c "^❌" "$log_file" 2>/dev/null || echo "0")
        skip_count=$(grep -c "^⏭️" "$log_file" 2>/dev/null || echo "0")

        if grep -q "^\[FAIL\]" "$log_file" 2>/dev/null; then
            status="FAIL"
        elif grep -q "^\[DONE\]" "$log_file" 2>/dev/null; then
            status="DONE"
        else
            status="????"
        fi

        printf "  %-6s %-30s  check: %s ok / %s fail / %s skip\n" \
            "[$status]" "$model_name" "$success_count" "$fail_count" "$skip_count"
    else
        printf "  %-6s %-30s  (无日志)\n" "[????]" "$model_name"
    fi
done
echo ""

if [ $FAIL -gt 0 ]; then
    echo "⚠️  有 $FAIL 个目录执行失败，请检查日志。"
    exit 1
fi

echo "全部完成。"
