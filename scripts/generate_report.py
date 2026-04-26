#!/usr/bin/env python3
"""生成 Markdown 趋势报告"""
import json
import os
from datetime import datetime

def generate_md_report():
    report_path = os.path.join(os.path.dirname(__file__), "../data/latest_report.json")
    if not os.path.exists(report_path):
        print("⚠️ 未找到数据报告，先运行 fetch_trending.py")
        return

    with open(report_path) as f:
        data = json.load(f)

    md = f"""# 📊 GitHub Trending 速报

> 自动生成时间: {data['generated_at']}

## 🔥 热门项目 TOP 20

"""
    for i, repo in enumerate(data["repos"], 1):
        md += f"{i}. {repo}\n"

    md += f"""
---
*由 GitHub Trending Bot 自动生成 | @lanxinAIhub*
"""

    out_path = os.path.join(os.path.dirname(__file__), "../reports/daily.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(md)

    print(f"✅ MarkDown 报告已生成: {out_path}")
    return out_path

if __name__ == "__main__":
    generate_md_report()
