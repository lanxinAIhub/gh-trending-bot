#!/bin/bash
# GitHub Trending AI 速报 - 每日运行脚本
# 配合 cron: 0 9 * * * /home/lanxin/edict/gh-trending-bot/run_daily.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Token 从 ~/.github_token 文件读取（不写入脚本！）
export GITHUB_TOKEN=$(cat ~/.github_token 2>/dev/null || echo "")

echo "=== GitHub Trending 速报 $(date) ==="
python3 scripts/fetch_trending.py

echo ""
echo "=== 生成 MarkDown 报告 ==="
python3 scripts/generate_report.py

echo ""
echo "=== 推送到 GitHub ==="
cd "$SCRIPT_DIR"
git add data/ reports/
git commit -m "📊 更新趋势报告 $(date '+%Y-%m-%d %H:%M')" || echo "无新内容"
git push origin main || echo "⚠️ push失败，请检查token"
