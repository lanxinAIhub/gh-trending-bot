#!/usr/bin/env python3
"""GitHub Trending Fetcher + AI Summary"""
import requests
import json
import sys
import os
from datetime import datetime

TOKEN_FILE = os.path.expanduser("~/.github_token")
HEADERS = {}

if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE) as f:
        token = f.read().strip()
    if token:
        HEADERS["Authorization"] = f"token {token}"

def fetch_trending(lang="python", days=30):
    url = f"https://api.github.com/search/repositories"
    date_from = (datetime.now().replace(day=1) if datetime.now().month == 1 
                 else datetime.now().replace(month=datetime.now().month-1)).strftime("%Y-%m-%d")
    params = {
        "q": f"language:{lang} pushed:>{date_from}",
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("items", [])

def fetch_top_repos():
    """获取多语言top repos"""
    repos = []
    for lang in ["python", "javascript", "rust", "go", "typescript"]:
        try:
            items = fetch_trending(lang)
            repos.extend(items)
        except Exception as e:
            print(f"⚠️ {lang} fetch failed: {e}")
    repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
    return repos[:15]

def generate_summary(repo):
    """生成repo摘要"""
    name = repo.get("full_name", "")
    desc = repo.get("description", "无描述") or "无描述"
    stars = repo.get("stargazers_count", 0)
    lang = repo.get("language", "未知")
    url = repo.get("html_url", "")
    today_stars = repo.get("stargazers_count", 0)  # 简化版
    return f"- **{name}** ⭐{stars} | {lang} | {desc}"

def main():
    print("📡 正在抓取GitHub热门项目...")
    repos = fetch_top_repos()
    print(f"✅ 获取到 {len(repos)} 个项目")
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "repos": []
    }
    
    for repo in repos:
        summary = generate_summary(repo)
        report["repos"].append(summary)
        print(summary)
    
    # 保存报告
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(script_dir), "data")
    os.makedirs(data_dir, exist_ok=True)
    report_path = os.path.join(data_dir, "latest_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告已保存: {report_path}")
    return report

if __name__ == "__main__":
    main()
