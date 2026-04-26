#!/usr/bin/env python3
"""
GitHub Trending Fetcher + AI Summary
Fetches trending repos from GitHub and generates AI-powered Chinese summaries.
"""
import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

# ── GitHub Token ───────────────────────────────────────────────────────────────
TOKEN_FILE = os.path.expanduser("~/.github_token")
HEADERS = {}

if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE) as f:
        token = f.read().strip()
    if token:
        HEADERS["Authorization"] = f"token {token}"

# ── MiniMax API Key (from environment) ───────────────────────────────────────
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_CODE_PLAN_KEY", "")
MINIMAX_BASE_URL = "https://api.minimaxi.com"
DEFAULT_MODEL = "MiniMax-Text-01"

CHAT_COMPLETION_URL = f"{MINIMAX_BASE_URL}/v1/chat/completions"
TEXT_COMPLETION_URL = f"{MINIMAX_BASE_URL}/v1/text/chatcompletion"


# ── GitHub API ────────────────────────────────────────────────────────────────
def fetch_trending(lang: str = "python", days: int = 30) -> List[Dict]:
    """Fetch trending repos for a given language."""
    if days >= 20:
        date_from = (datetime.now().replace(day=1) if datetime.now().month == 1
                     else datetime.now().replace(month=datetime.now().month - 1)).strftime("%Y-%m-%d")
    else:
        from datetime import timedelta
        date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{lang} pushed:>{date_from}",
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("items", [])


def fetch_top_repos() -> List[Dict]:
    """Fetch top repos across multiple languages."""
    repos = []
    for lang in ["python", "javascript", "rust", "go", "typescript"]:
        try:
            items = fetch_trending(lang)
            repos.extend(items)
        except Exception as e:
            print(f"⚠️ {lang} fetch failed: {e}")
    repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
    return repos[:15]


# ── MiniMax AI Summary ────────────────────────────────────────────────────────
def _call_minimax_chat(model: str, messages: List[Dict], max_tokens: int = 200,
                       temperature: float = 0.7) -> Optional[str]:
    """Call MiniMax chat completion API."""
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
    }
    try:
        resp = requests.post(CHAT_COMPLETION_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()
        if resp.status_code == 200:
            return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        err = data.get("error", {})
        print(f"   ❌ API错误 [{err.get('type', '?')}]: {err.get('message', 'unknown')}")
        return None
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None


def _call_minimax_text(model: str, prompt: str, max_tokens: int = 200) -> Optional[str]:
    """Call MiniMax text completion API (older models)."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
    }
    try:
        resp = requests.post(TEXT_COMPLETION_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()
        if resp.status_code == 200:
            return data.get("reply", "").strip()
        err = data.get("base_resp", {})
        print(f"   ❌ API错误: {err.get('status_msg', 'unknown')}")
        return None
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None


def _generate_repo_ai_summary(repo: Dict[str, Any]) -> str:
    """Generate AI summary for a single repo using MiniMax API."""
    name = repo.get("full_name", "未知项目")
    desc = repo.get("description") or "无描述"
    stars = repo.get("stargazers_count", 0)
    lang = repo.get("language") or "未知"
    topics = repo.get("topics", []) or []
    topics_str = "、".join(topics[:5]) if topics else "无"

    prompt = f"""你是一个专业的开源项目分析师。请为以下GitHub项目生成一段简洁的中文摘要（60字以内）：

项目：{name}
语言：{lang} | 星标：{stars:,}
描述：{desc}
标签：{topics_str}

直接输出中文摘要："""

    # Try newer chat API first
    result = _call_minimax_chat(DEFAULT_MODEL, [{"role": "user", "content": prompt}],
                                 max_tokens=120, temperature=0.7)
    if result:
        return result.strip()

    # Fallback to older text API
    result = _call_minimax_text("abab5.5-chat", prompt, max_tokens=120)
    if result:
        return result.strip()

    # Ultimate fallback
    return desc[:80] + ("..." if len(desc) > 80 else "")


def _generate_daily_ai_summary(repos: List[Dict]) -> str:
    """Generate a comprehensive daily trend summary."""
    repo_list = "\n".join([
        f"{i+1}. {r.get('full_name', '')} - ⭐{r.get('stargazers_count', 0):,} "
        f"[{r.get('language', '?')}] - {r.get('description', '') or '无描述'}"
        for i, r in enumerate(repos)
    ])

    prompt = f"""你是一个专业的开源趋势分析师。请分析以下今日GitHub热门项目，生成一段综合的中文趋势解读（120字以内）：

{repo_list}

直接输出趋势解读："""

    result = _call_minimax_chat(DEFAULT_MODEL, [{"role": "user", "content": prompt}],
                                 max_tokens=200, temperature=0.7)
    if result:
        return result.strip()

    result = _call_minimax_text("abab5.5-chat", prompt, max_tokens=200)
    if result:
        return result.strip()

    return "今日热门项目涵盖多语言开源项目，反映了开发者社区的最新兴趣方向。"


def _simple_summary(repo: Dict) -> str:
    """Generate a simple non-AI summary."""
    name = repo.get("full_name", "")
    desc = repo.get("description", "无描述") or "无描述"
    stars = repo.get("stargazers_count", 0)
    lang = repo.get("language", "未知")
    return f"**{name}** ⭐{stars:,} | {lang} | {desc}"


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    skip_ai = os.environ.get("SKIP_AI_SUMMARY") == "1"
    has_minimax_key = bool(MINIMAX_API_KEY)

    print("📡 正在抓取GitHub热门项目...")
    repos = fetch_top_repos()
    print(f"✅ 获取到 {len(repos)} 个项目")

    daily_ai_summary = ""
    ai_enabled = False

    if has_minimax_key and not skip_ai:
        print("\n🤖 正在生成 AI 摘要...")
        print(f"   (如需跳过，请设置 SKIP_AI_SUMMARY=1)")

        # Daily summary
        print("📝 生成今日趋势综合摘要...")
        daily_ai_summary = _generate_daily_ai_summary(repos)
        print(f"   ✅ {daily_ai_summary[:60]}...\n")

        # Per-repo summaries
        for i, repo in enumerate(repos, 1):
            name = repo.get("full_name", "?")
            print(f"   [{i}/{len(repos)}] {name}...", end=" ", flush=True)
            ai_sum = _generate_repo_ai_summary(repo)
            repo["ai_summary"] = ai_sum
            print(f"✅ {ai_sum[:40]}...")
            time.sleep(0.25)  # Rate limiting

        ai_enabled = True
    else:
        if not has_minimax_key:
            print("\n⚠️ 未设置 MINIMAX_API_KEY，使用简单摘要")
        for repo in repos:
            repo["ai_summary"] = _simple_summary(repo)

    # Build report
    report = {
        "generated_at": datetime.now().isoformat(),
        "ai_enabled": ai_enabled,
        "daily_summary": daily_ai_summary,
        "repos": repos,
    }

    # Save raw JSON (full repo objects with AI summaries)
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
