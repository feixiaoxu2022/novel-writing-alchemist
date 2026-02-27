#!/bin/bash
# 批量重算分数（只跑 scorer，不重跑 checker）
# 用途：scorer 逻辑修复后，基于已有 check_details 重新计算 dimension_scores 和 overall_result
# 不调用 LLM，纯本地计算，几秒钟跑完
#
# 用法:
#   ./scripts/batch_rescore.sh                              # 重算所有 eval 目录的最新 rev
#   ./scripts/batch_rescore.sh --revision rev009            # 指定 revision
#   ./scripts/batch_rescore.sh --pattern "eval_dsv2_*_claude*"  # 只跑匹配的目录
#   ./scripts/batch_rescore.sh --dry-run                    # 只打印不写入

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCORER="$PROJECT_ROOT/env/checker_score.py"
EVAL_BASE="$PROJECT_ROOT/evaluation_outputs"

# 默认参数
REVISION=""
PATTERN="eval_dsv*"
DRY_RUN=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --revision) REVISION="$2"; shift 2;;
        --pattern) PATTERN="$2"; shift 2;;
        --dry-run) DRY_RUN=true; shift;;
        *) echo "未知参数: $1"; exit 1;;
    esac
done

# 找最新 revision 的 check_result 文件名
find_check_result() {
    local env_dir="$1"
    if [[ -n "$REVISION" ]]; then
        local f="$env_dir/check_result_${REVISION}.json"
        [[ -f "$f" ]] && echo "$f" || echo ""
    else
        # 找最新的 check_result_revNNN.json
        ls "$env_dir"/check_result_rev*.json 2>/dev/null | sort -V | tail -1
    fi
}

total=0
changed=0
unchanged=0
skipped=0
errors=0

if $DRY_RUN; then
    echo "[DRY RUN] 批量重算分数"
else
    echo "批量重算分数"
fi

for eval_dir in "$EVAL_BASE"/$PATTERN; do
    [[ -d "$eval_dir" ]] || continue
    dir_name=$(basename "$eval_dir")
    dir_changed=0

    for env_dir in "$eval_dir"/*_env; do
        [[ -d "$env_dir" ]] || continue

        cr_path=$(find_check_result "$env_dir")
        [[ -z "$cr_path" ]] && continue

        total=$((total + 1))
        sample_name=$(basename "$env_dir" _env)
        cr_filename=$(basename "$cr_path")

        # 记录旧分数
        old_total=$(python3 -c "import json; d=json.load(open('$cr_path')); print(d.get('overall_result',{}).get('total_score',-1))" 2>/dev/null)

        if $DRY_RUN; then
            # dry-run: 输出到临时文件对比
            tmp_out=$(mktemp)
            python3 "$SCORER" --execution-result "$cr_path" --output "$tmp_out" 2>/dev/null
            new_total=$(python3 -c "import json; d=json.load(open('$tmp_out')); print(d.get('overall_result',{}).get('total_score',-1))" 2>/dev/null)
            rm -f "$tmp_out"
        else
            # 直接覆盖原文件
            python3 "$SCORER" --execution-result "$cr_path" --output "$cr_path" 2>/dev/null
            new_total=$(python3 -c "import json; d=json.load(open('$cr_path')); print(d.get('overall_result',{}).get('total_score',-1))" 2>/dev/null)
        fi

        # 比较分数是否变化
        diff=$(python3 -c "print(abs(float('$new_total') - float('$old_total')) > 0.01)" 2>/dev/null)
        if [[ "$diff" == "True" ]]; then
            changed=$((changed + 1))
            dir_changed=$((dir_changed + 1))
            delta=$(python3 -c "print(f'{float(\"$new_total\") - float(\"$old_total\"):+.2f}')" 2>/dev/null)
            echo "  $sample_name ($cr_filename): $old_total → $new_total ($delta)"
        else
            unchanged=$((unchanged + 1))
        fi
    done

    if [[ $dir_changed -gt 0 ]]; then
        echo "  [$dir_name] $dir_changed 个样本分数变更"
    fi
done

echo ""
echo "总计: $total 个样本, $changed 变更, $unchanged 不变, $skipped 跳过, $errors 错误"
