# 📊 GitHub Trending AI 速报

> 🤖 自动抓取 GitHub 热门项目，用 AI 生成中文摘要

## 功能

- ✅ 自动抓取 GitHub 多语言热门项目（Python/JavaScript/Rust/Go/TypeScript）
- ✅ **AI 智能摘要**（MiniMax 大模型）—— 每个项目生成中文解读
- ✅ **今日趋势综合解读** —— AI 分析当日整体趋势
- ✅ 按星标排序，输出 TOP 15
- ✅ 每日自动运行（cron: 每天 09:00）
- ✅ 生成 MarkDown 报告并推送到 GitHub

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/lanxinAIhub/gh-trending-bot.git
cd gh-trending-bot

# 2. 配置 GitHub Token
cp ~/.github_token ~/.github_token  # 或手动创建 ~/.github_token 文件

# 3. 配置 MiniMax API Key（用于AI摘要）
export MINIMAX_API_KEY=your_minimax_api_key_here
# 或使用 coding plan key:
export MINIMAX_CODE_PLAN_KEY=your_coding_plan_key_here

# 4. 运行抓取（自动生成AI摘要）
SKIP_AI_SUMMARY=1 python3 scripts/fetch_trending.py  # 跳过AI摘要

# 5. 生成报告
python3 scripts/generate_report.py

# 6. 完整流程
./run_daily.sh
```

## AI 摘要功能

### API Key 配置

AI 摘要功能需要 MiniMax API Key。两种配置方式：

**方式一：标准 API Key（推荐）**
```bash
export MINIMAX_API_KEY=your_api_key
```

**方式二：Coding Plan Key**
```bash
export MINIMAX_CODE_PLAN_KEY=sk-cp-your-key
```

> ⚠️ Coding Plan Key 仅支持 MiniMax-Text-01 等特定模型。如遇 "token plan not support model" 错误，请使用标准 API Key。

### 跳过 AI 摘要

如需仅抓取数据不生成 AI 摘要：
```bash
export SKIP_AI_SUMMARY=1
python3 scripts/fetch_trending.py
```

### API 测试

```bash
python3 scripts/ai_summary.py --test
```

## 自动化部署

```bash
# 设置每日自动运行
echo "0 9 * * * /path/to/gh-trending-bot/run_daily.sh" | crontab -

# 确认 cron 生效
crontab -l
```

## 项目结构

```
gh-trending-bot/
├── scripts/
│   ├── fetch_trending.py   # 抓取 GitHub Trending + AI摘要
│   ├── generate_report.py  # 生成 MarkDown 报告
│   └── ai_summary.py       # AI摘要模块（独立工具）
├── data/
│   └── latest_report.json  # 最新数据（含完整repo信息）
├── reports/
│   └── daily.md            # 每日报告
├── run_daily.sh            # 每日运行脚本
└── README.md
```

## 数据格式

`data/latest_report.json` 结构：
```json
{
  "generated_at": "2026-04-26T09:00:00",
  "ai_enabled": true,
  "daily_summary": "今日趋势解读...",
  "repos": [
    {
      "full_name": "owner/repo",
      "stargazers_count": 12345,
      "language": "Python",
      "ai_summary": "AI生成的中文摘要...",
      ...
    }
  ]
}
```

## 变现路径

1. **GitHub Sponsors** - 开发者赞助
2. **Star 打赏** - 靠质量吸引 Star
3. **Pro 版本** - 提供 AI 深度分析（付费）
4. **Bounties** - 帮开发者推广项目收费

---

*🦞 由 OpenClaw AI Agent 自动创建和维护 | AI摘要由 MiniMax 大模型驱动*
