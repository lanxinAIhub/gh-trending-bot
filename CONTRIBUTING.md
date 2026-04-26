# 🤝 参与贡献指南

感谢您对 GitHub Trending AI 速报的兴趣！欢迎提交 Issue 和 Pull Request。

---

## 📋 目录

- [行为准则](#行为准则)
- [如何参与](#如何参与)
- [报告 Bug](#报告-bug)
- [提交功能建议](#提交功能建议)
- [提交代码](#提交代码)
- [代码规范](#代码规范)
- [Git 提交规范](#git-提交规范)

---

## 行为准则

请尊重所有参与者。使用友善、包容的语言。任何形式的骚扰、歧视将不被接受。

---

## 如何参与

### 🐛 报告 Bug

请通过 [GitHub Issues](https://github.com/lanxinAIhub/gh-trending-bot/issues) 报告，提供以下信息：

- 问题简述
- 复现步骤（1. → 2. → 3. ...）
- 预期行为 vs 实际行为
- 环境信息（Python 版本、操作系统）
- 错误日志（如有）

### 💡 提交功能建议

同样通过 [GitHub Issues](https://github.com/lanxinAIhub/gh-trending-bot/issues) 提交，请使用 `enhancement` 标签。

---

## 提交代码

### 开发环境搭建

```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/gh-trending-bot.git
cd gh-trending-bot

# 3. 创建功能分支
git checkout -b feature/your-feature-name
# 或修复分支
git checkout -b fix/your-bug-fix

# 4. 安装依赖（如有）
pip install requests

# 5. 本地测试
python3 scripts/fetch_trending.py
python3 scripts/generate_report.py

# 6. 运行测试
python3 -m pytest tests/ -v
```

### Pull Request 流程

1. **Fork** → **创建分支** → **开发** → **测试** → **Push**
2. 创建 Pull Request 到 `main` 分支
3. 描述清楚改动内容和动机
4. 等待 Review（通常 24-48 小时内）
5. 合并后删除分支

---

## 代码规范

### Python 风格

遵循 [PEP 8](https://pep8.org/)，使用 `black` 格式化代码：

```bash
pip install black
black scripts/*.py
```

### 脚本规范

```python
#!/usr/bin/env python3
"""模块描述（单行）"""

import requests
import json
from datetime import datetime

# 全大写常量
TOKEN_FILE = "~/.github_token"

def fetch_trending(lang="python", days=30):
    """获取指定语言的热门项目

    Args:
        lang: 编程语言
        days: 抓取最近多少天的项目

    Returns:
        list: 仓库列表
    """
    ...
```

### 注释规范

- 公共函数/方法必须有 docstring
- 复杂逻辑添加行内注释
- TODO 使用 `TODO(username):` 格式

---

## Git 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type 类型

| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具变更 |

### 示例

```bash
git commit -m "docs: 更新 README 添加效果展示"
git commit -m "feat: 支持自定义抓取数量 TOP_N"
git commit -m "fix: 修复 days 参数为空时的报错"
```

---

## 🧪 测试

所有新功能请附带测试用例：

```python
# tests/test_fetch.py
import pytest
from scripts.fetch_trending import fetch_trending

def test_fetch_trending_returns_list():
    result = fetch_trending(lang="python")
    assert isinstance(result, list)

def test_fetch_trending_respects_limit():
    result = fetch_trending(lang="python")
    assert len(result) <= 5
```

运行测试：

```bash
python3 -m pytest tests/ -v
```

---

## 📬 联系方式

- GitHub Issues：https://github.com/lanxinAIhub/gh-trending-bot/issues
- 项目维护者：[@lanxinAIhub](https://github.com/lanxinAIhub)

---

*感谢您的参与！每一个贡献都让项目变得更好。*
