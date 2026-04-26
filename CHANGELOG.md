# 📝 CHANGELOG

所有重要的项目变更都会记录在此文件。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [v1.0.0] - 2026-04-26

### 🎉 首发版本

首个完整可用版本，包含核心功能：

- ✅ 多语言 GitHub Trending 抓取（Python/JavaScript/TypeScript/Rust/Go）
- ✅ 按 Star 数量排序，输出 TOP 15
- ✅ AI 生成中文 MarkDown 报告
- ✅ 本地 cron 定时运行脚本
- ✅ GitHub Actions 自动化（`.github/workflows/daily.yml`）
- ✅ Token 安全管理（从 `~/.github_token` 文件读取，不写入代码）
- ✅ README 完整文档
- ✅ CONTRIBUTING 贡献指南

---

## [v1.1.0] - （规划中）

### 🚧 计划功能

- [ ] 支持自定义时间范围（最近7天/30天/全年）
- [ ] 支持指定单一语言抓取（命令行参数）
- [ ] 错误重试机制（requests retry）

---

## [v2.0.0] - （规划中）

### 🚧 计划功能

- [ ] 接入 GPT/Claude API 生成 AI 摘要
- [ ] 增加项目增长趋势分析（较上周 Star 增量）
- [ ] 支持 CSV/JSON 格式导出

---

## [v2.1.0] - （规划中）

### 🚧 计划功能

- [ ] Telegram Bot 推送通知
- [ ] QQ 频道推送
- [ ] 邮件订阅功能

---

## [v3.0.0] - （规划中）

### 🚧 计划功能

- [ ] Web 可视化看板
- [ ] 历史趋势对比图
- [ ] 开发者画像分析

---

## 如何发布新版本

1. 更新本文件顶部版本号和日期
2. 运行 `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
3. 推送标签：`git push origin --tags`
4. GitHub Actions 自动创建 Release（需配置）

```bash
# 示例：发布 v1.1.0
git tag -a v1.1.0 -m "Release v1.1.0: 支持自定义时间范围"
git push origin --tags
```

---

## 版本规范

遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)：

- **MAJOR** (v2.0.0) — 不兼容的 API 变更
- **MINOR** (v1.1.0) — 向后兼容的功能新增
- **PATCH** (v1.0.1) — 向后兼容的问题修复

---

*上次更新：2026-04-26*
