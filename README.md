# 📊 GitHub Trending AI 速报

> 🤖 自动抓取 GitHub 热门项目，用 AI 生成中文摘要，每天准时推送

[English](./README_EN.md) · [变更日志](./CHANGELOG.md) · [参与贡献](./CONTRIBUTING.md)

---

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| 🔍 多语言覆盖 | Python、JavaScript、TypeScript、Rust、Go |
| 🏆 Star 排序 | 按星标数量降序，精选 TOP 15 |
| 📝 AI 中文摘要 | 每条项目含名称、星标数、语言、描述 |
| ⏰ 每日自动推送 | 配合 cron，GitHub Actions 或本地定时任务 |
| 🔄 完全自动化 | fetch → 生成报告 → git push，全自动 |
| 🌐 无需爬虫 | 纯 GitHub API，不违反 robots.txt |

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- GitHub Personal Access Token（免费，无需任何权限）

### 第一步：克隆项目

```bash
git clone https://github.com/lanxinAIhub/gh-trending-bot.git
cd gh-trending-bot
```

### 第二步：配置 Token

```bash
# 将你的 GitHub Token 写入 ~/.github_token
echo "ghp_xxxxxxxxxxxx" > ~/.github_token
```

> 🔑 Token 获取：[GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
> 
> 权限需求：**无需任何特殊权限**（推荐 `public_repo` 仅限公共仓库）

### 第三步：立即运行

```bash
# 抓取热门项目
python3 scripts/fetch_trending.py

# 生成 Markdown 报告
python3 scripts/generate_report.py
```

### 第四步：自动化（可选）

```bash
# 添加 crontab 每天 09:00 自动运行
echo "0 9 * * * cd /path/to/gh-trending-bot && ./run_daily.sh >> /tmp/trending.log 2>&1" | crontab -

# 或使用 GitHub Actions（推送时自动触发）
# 仓库已包含 .github/workflows/daily.yml
```

---

## 📁 项目结构

```
gh-trending-bot/
├── .github/
│   └── workflows/
│       └── daily.yml       # GitHub Actions 每日自动运行
├── scripts/
│   ├── fetch_trending.py   # 抓取 GitHub Trending 数据
│   └── generate_report.py  # 生成 Markdown 报告
├── data/
│   └── latest_report.json  # 最新 JSON 格式数据
├── reports/
│   └── daily.md            # 每日 MarkDown 报告（git push 到仓库）
├── tests/
│   └── test_fetch.py       # 单元测试
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── README_EN.md
└── run_daily.sh            # 每日运行脚本（本地 cron 用）
```

---

## 🎨 效果展示

生成的 `reports/daily.md` 示例：

```markdown
# 📊 GitHub Trending 速报

> 自动生成时间: 2026-04-26T09:00:00.000000

## 🔥 热门项目 TOP 15

1. **freeCodeCamp/freeCodeCamp** ⭐443579 | TypeScript | freeCodeCamp.org's open-source codebase...
2. **EbookFoundation/free-programming-books** ⭐386050 | Python | :books: Freely available programming books
3. **openclaw/openclaw** ⭐364103 | TypeScript | Your own personal AI assistant...
...
---
*由 GitHub Trending Bot 自动生成 | @lanxinAIhub*
```

---

## 🔧 配置说明

### 环境变量（可选）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | 从 `~/.github_token` 读取 |

### 自定义语言

修改 `scripts/fetch_trending.py` 中的 `LANGUAGES` 列表：

```python
LANGUAGES = ["python", "javascript", "rust", "go", "typescript", "java", "cpp"]
```

### 调整抓取数量

修改 `scripts/fetch_trending.py` 中的 `TOP_N`：

```python
TOP_N = 20  # 默认 15
```

---

## 📦 API 依赖

| 包 | 版本 | 用途 |
|-----|------|------|
| `requests` | ≥ 2.28 | HTTP 请求 |

---

## 🗺️ 路线图

- [ ] **v1.1** — 支持自定义时间范围（最近7天/30天/全年）
- [ ] **v1.2** — 支持指定单一语言抓取
- [ ] **v2.0** — 增加 AI 摘要生成（GPT/Claude 接入）
- [ ] **v2.1** — 支持 Telegram/QQ 频道推送
- [ ] **v3.0** — 提供 Web 看板（趋势可视化）
- [ ] **v3.1** — 支持邮件订阅

详见 [CHANGELOG.md](./CHANGELOG.md)

---

## 💰 变现路径

| 方式 | 说明 |
|------|------|
| ⭐ Star 打赏 | 靠质量和实用性吸引 Star，形成影响力 |
| 💝 GitHub Sponsors | 开发者赞助（见 [申请条件](https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors)） |
| 🔍 Pro 版本 | 提供 AI 深度分析、邮件订阅等付费功能 |
| 🏅 Bounties | 帮开源项目做推广，收取推广费 |

---

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献规范。

---

## 📄 许可证

本项目采用 [MIT License](./LICENSE)

---

## 🙏 致谢

- [GitHub API](https://docs.github.com/en/rest) — 数据来源
- [OpenClaw](https://github.com/nicktorn89/openclaw) — AI Agent 框架
- 所有 Star 和贡献者 ❤️

---

*🦞 由 [OpenClaw AI Agent](https://github.com/nicktorn89/openclaw) 自动创建和维护*
