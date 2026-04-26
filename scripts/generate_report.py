#!/usr/bin/env python3
"""
Generate Markdown trend report from raw JSON data.
Includes AI-generated summaries when available.
"""
import json
import os
from datetime import datetime


def generate_md_report():
    import pathlib
    # __file__ works when run directly; for exec() context, use fallback
    try:
        script_dir = str(pathlib.Path(__file__).parent.resolve())
    except NameError:
        script_dir = str(pathlib.Path("scripts").resolve())
    report_path = os.path.join(script_dir, "../data/latest_report.json")
    
    if not os.path.exists(report_path):
        print("⚠️ 未找到数据报告，请先运行 fetch_trending.py")
        return

    with open(report_path) as f:
        data = json.load(f)

    generated_at = data.get("generated_at", "")
    ai_enabled = data.get("ai_enabled", False)
    daily_summary = data.get("daily_summary", "")
    repos = data.get("repos", [])

    # Build repo list
    repo_lines = []
    for i, repo in enumerate(repos, 1):
        name = repo.get("full_name", "未知")
        stars = repo.get("stargazers_count", 0)
        lang = repo.get("language", "未知")
        url = repo.get("html_url", "#")
        ai_sum = repo.get("ai_summary", "") or repo.get("description", "无描述")
        
        # If AI summary is a simple summary (starts with **), keep as-is
        if ai_sum.startswith("**"):
            repo_lines.append(f"{i}. {ai_sum}")
        else:
            # AI summary is a natural language summary
            repo_lines.append(
                f"{i}. **{name}** ⭐{stars:,} | {lang}\n"
                f"   💡 {ai_sum}\n"
                f"   🔗 {url}"
            )

    repo_md = "\n".join(repo_lines)

    # Header section
    ai_badge = "✅ AI摘要已启用" if ai_enabled else "⚠️ AI摘要未启用（请设置 MINIMAX_API_KEY）"
    
    daily_section = f"""
## 📊 今日趋势解读

{daily_summary}
""" if daily_summary else ""

    md = f"""# 📊 GitHub Trending 速报

> 自动生成时间: {generated_at}  
> {ai_badge}

{daily_section}
## 🔥 热门项目 TOP {len(repos)}

{repo_md}

---
*由 GitHub Trending Bot 自动生成 | @lanxinAIhub*  
*AI摘要由 MiniMax 大模型提供支持*
"""

    out_path = os.path.join(script_dir, "../reports/daily.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ MarkDown 报告已生成: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_md_report()
