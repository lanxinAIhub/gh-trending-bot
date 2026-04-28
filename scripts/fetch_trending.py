#!/usr/bin/env python3
"""GitHub Trending Fetcher + AI Summary"""
import os
import sys

# Add script dir to path for ai_summary import
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import requests
import json
from datetime import datetime
from ai_summary import generate_repo_summary, generate_daily_summary

TOKEN_FILE = os.path.expanduser("~/.github_token")
HEADERS = {}

if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE) as f:
        token = f.read().strip()
    if token:
        HEADERS["Authorization"] = f"token {token}"

def fetch_trending(lang="python", days=30):
    url = "https://api.github.com/search/repositories"
    date_from = (datetime.now().replace(day=1) if datetime.now().month == 1 
                 else datetime.now().replace(month=datetime.now().month-1)).strftime("%Y-%m-%d")
    params = {"q": f"language:{lang} pushed:>{date_from}", "sort": "stars", "order": "desc", "per_page": 5}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("items", [])

def fetch_top_repos():
    repos = []
    for lang in ["python", "javascript", "rust", "go", "typescript"]:
        try:
            items = fetch_trending(lang)
            repos.extend(items)
        except Exception as e:
            print(f"⚠️ {lang} fetch failed: {e}")
    repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
    return repos[:15]

def main():
    print("📡 正在抓取GitHub热门项目...")
    repos = fetch_top_repos()
    print(f"✅ 获取到 {len(repos)} 个项目")
    
    report = {"generated_at": datetime.now().isoformat(), "repos": [], "ai_summary": ""}
    repo_summaries = []
    
    for repo in repos:
        summary = generate_repo_summary(
            repo_name=repo.get("full_name", ""),
            description=repo.get("description") or "无描述",
            stars=repo.get("stargazers_count", 0),
            language=repo.get("language", "未知"),
            url=repo.get("html_url", "")
        )
        report["repos"].append(summary)
        repo_summaries.append(summary)
        print(summary)
    
    # AI综合摘要
    if repo_summaries:
        daily = generate_daily_summary(repo_summaries)
        if daily:
            report["ai_summary"] = daily
            print(f"\n🤖 今日趋势：{daily}")
    
    # 保存报告
    data_dir = os.path.join(os.path.dirname(script_dir), "data")
    os.makedirs(data_dir, exist_ok=True)
    report_path = os.path.join(data_dir, "latest_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 报告已保存: {report_path}")
    return report

if __name__ == "__main__":
    main()
