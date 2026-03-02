#!/bin/bash
# 清理因 _summarize 带 tools 导致空摘要的受影响样本 (Novel Writing场景)
# 生成时间: 2026-03-02
# 用途: 在远程服务器上删除受影响样本的 env 目录和轨迹 JSON，然后重跑
# 使用: bash scripts/cleanup_handoff_affected_samples.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "[DRY RUN] 仅打印将要执行的命令，不实际删除"
fi

do_rm() {
    if $DRY_RUN; then
        echo "  [DRY] rm -rf $1"
    else
        echo "  rm -rf $1"
        rm -rf "$1"
    fi
}

# ============================================================
# Novel Writing (14个受影响样本)
# ============================================================
NW_DIR="evaluation_outputs/eval_dsv2_20260211_103353_ernie-5.0-thinking-preview"
NW_SAMPLES=(
    NW_CLEAR_MEDIUM_ANGSTY_001
    NW_CLEAR_MEDIUM_BRAINY_ACTION_001
    NW_CLEAR_MEDIUM_HEROINE_001
    NW_CLEAR_MEDIUM_SUSPENSE_001
    NW_CLEAR_MEDIUM_SWEET_001
    NW_CLEAR_SHORT_ANGSTY_001
    NW_CLEAR_SHORT_SWEET_001
    NW_IP_MEDIUM_NEUTRAL_001
    NW_ULTRA_SHORT_ANGSTY_001
    NW_ULTRA_SHORT_ANGSTY_002
    NW_ULTRA_SHORT_ANGSTY_003
    NW_ULTRA_SHORT_ANGSTY_004
    NW_ULTRA_SHORT_ANGSTY_005
    NW_VAGUE_MEDIUM_SWEET_DRAMA_001
)

echo "=== NovelWriting: ${#NW_SAMPLES[@]} 个受影响样本 ==="
for s in "${NW_SAMPLES[@]}"; do
    do_rm "${NW_DIR}/${s}.json"
    do_rm "${NW_DIR}/${s}_env"
done

echo ""
echo "删除完成。请重新运行评测。"
