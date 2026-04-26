#!/bin/bash
# GitHub Trending AI 速报 - 每日运行脚本 (含AI摘要)
# 配合 cron: 0 9 * * * /home/lanxin/edict/gh-trending-bot/run_daily.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Token 从 ~/.github_token 文件读取
export GITHUB_TOKEN=$(cat ~/.github_token 2>/dev/null || echo "")

echo "=== GitHub Trending 速报 $(date) ==="

# Test MiniMax API key availability
if [ -n "$MINIMAX_API_KEY" ] || [ -n "$MINIMAX_CODE_PLAN_KEY" ]; then
    export MINIMAX_API_KEY="${MINIMAX_API_KEY:-$MINIMAX_CODE_PLAN_KEY}"
    echo "🤖 AI摘要功能: 已启用 (MINIMAX_API_KEY已设置)"
else
    echo "⚠️ AI摘要功能: 未启用（请设置 MINIMAX_API_KEY 环境变量）"
    echo "   export MINIMAX_API_KEY=your_key_here"
fi

echo ""
echo "=== 抓取 GitHub 热门项目 + AI摘要 ==="
python3 scripts/fetch_trending.py

echo ""
echo "=== 生成 MarkDown 报告 ==="
python3 scripts/generate_report.py

echo ""
echo "=== 推送到 GitHub ==="
cd "$SCRIPT_DIR"
git add data/ reports/
git commit -m "📊 更新趋势报告 $(date '+%Y-%m-%d %H:%M')" || echo "无新内容"
git push origin feature/ai-summary 2>/dev/null || git push origin main 2>/dev/null || echo "⚠️ push失败，请检查token"

echo ""
echo "=== 完成 ==="
