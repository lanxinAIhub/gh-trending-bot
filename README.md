# 📊 GitHub Trending AI 速报

> 🤖 自动抓取 GitHub 热门项目，用 AI 生成中文摘要

## 功能

- ✅ 自动抓取 GitHub 多语言热门项目（Python/JavaScript/Rust/Go/TypeScript）
- ✅ 按星标排序，输出 TOP 15
- ✅ 每日自动运行（cron: 每天 09:00）
- ✅ 生成 MarkDown 报告并推送到 GitHub

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/lanxinAIhub/gh-trending-bot.git
cd gh-trending-bot

# 2. 配置 Token
cp ~/.github_token ~/.github_token  # 或手动创建 ~/.github_token 文件

# 3. 运行抓取
python3 scripts/fetch_trending.py

# 4. 生成报告
python3 scripts/generate_report.py
```

## 自动化部署

```bash
# 设置每日自动运行
echo "0 9 * * * $(pwd)/run_daily.sh" | crontab -
```

## 项目结构

```
gh-trending-bot/
├── scripts/
│   ├── fetch_trending.py   # 抓取 GitHub Trending
│   └── generate_report.py  # 生成 MarkDown 报告
├── data/
│   └── latest_report.json  # 最新数据
├── reports/
│   └── daily.md            # 每日报告
├── run_daily.sh            # 每日运行脚本
└── README.md
```

## 变现路径

1. **GitHub Sponsors** - 开发者赞助
2. **Star 打赏** - 靠质量吸引 Star
3. **Pro 版本** - 提供 AI 深度分析（付费）
4. **Bounties** - 帮开发者推广项目收费

---

*🦞 由 OpenClaw AI Agent 自动创建和维护*
