#!/usr/bin/env python3
"""
MiniMax AI Summary Generator for GitHub Trending Bot
Generates Chinese AI summaries for repositories using MiniMax API.
"""
import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any

# ── API Key Resolution ────────────────────────────────────────────────────────
# Priority: MINIMAX_API_KEY > MINIMAX_CODE_PLAN_KEY
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_CODE_PLAN_KEY", "")
if not MINIMAX_API_KEY:
    print("⚠️  未设置 MiniMax API Key，请设置 MINIMAX_API_KEY 或 MINIMAX_CODE_PLAN_KEY 环境变量")

MINIMAX_BASE_URL = "https://api.minimaxi.com"
DEFAULT_MODEL = "MiniMax-Text-01"

# ── API Endpoints ─────────────────────────────────────────────────────────────
CHAT_COMPLETION_URL = f"{MINIMAX_BASE_URL}/v1/chat/completions"
TEXT_COMPLETION_URL = f"{MINIMAX_BASE_URL}/v1/text/chatcompletion"


def call_minimax_chat(model: str, messages: List[Dict], max_tokens: int = 200,
                       temperature: float = 0.7) -> Optional[str]:
    """Call MiniMax chat completion API (newer models like MiniMax-Text-01)."""
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
        else:
            err = data.get("error", {})
            print(f"   ❌ API错误 [{err.get('type', '?')}]: {err.get('message', data)}")
            return None
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None


def call_minimax_text(model: str, messages: List[Dict], max_tokens: int = 200) -> Optional[str]:
    """Call MiniMax text completion API (older models like abab5.5-chat)."""
    # Convert messages to a single prompt string
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
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
        else:
            err = data.get("base_resp", {})
            print(f"   ❌ API错误: {err.get('status_msg', data)}")
            return None
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None


def generate_repo_summary(repo: Dict[str, Any], model: str = DEFAULT_MODEL,
                          use_text_api: bool = False) -> str:
    """Generate a concise Chinese AI summary for a single repository."""
    name = repo.get("full_name", "未知项目")
    desc = repo.get("description") or "无描述"
    stars = repo.get("stargazers_count", 0)
    lang = repo.get("language") or "未知"
    url = repo.get("html_url", "")
    topics = repo.get("topics", []) or []
    topics_str = "、".join(topics[:5]) if topics else "无"
    
    prompt = f"""你是一个专业的开源项目分析师。请为以下GitHub项目生成一段简洁的中文摘要（80字以内）：

项目名称：{name}
编程语言：{lang}
星标数：{stars:,}
项目描述：{desc}
技术标签：{topics_str}

请直接输出中文摘要，无需解释。"""

    messages = [{"role": "user", "content": prompt}]
    
    if use_text_api:
        result = call_minimax_text(model, messages)
    else:
        result = call_minimax_chat(model, messages, max_tokens=150, temperature=0.7)
    
    if result:
        return result.strip()
    else:
        # Fallback to simple description
        return f"{desc[:60]}..." if len(desc) > 60 else desc


def generate_daily_summary(repos: List[Dict[str, Any]], model: str = DEFAULT_MODEL,
                           use_text_api: bool = False) -> str:
    """Generate a comprehensive daily summary of all trending repos."""
    repo_list = "\n".join([
        f"{i+1}. {r.get('full_name', '')} - ⭐{r.get('stargazers_count', 0):,} "
        f"[{r.get('language', '?')}] - {r.get('description', '') or '无描述'}"
        for i, r in enumerate(repos)
    ])
    
    prompt = f"""你是一个专业的开源趋势分析师。请分析以下今日GitHub热门项目，生成一段综合的中文趋势解读（150字以内）：

{repo_list}

请直接输出趋势分析，无需解释。"""

    messages = [{"role": "user", "content": prompt}]
    
    if use_text_api:
        return call_minimax_text(model, messages, max_tokens=250) or "今日GitHub热门项目涵盖多语言开源项目，反映了开发者社区的最新兴趣方向。"
    else:
        return call_minimax_chat(model, messages, max_tokens=250, temperature=0.7) or "今日GitHub热门项目涵盖多语言开源项目，反映了开发者社区的最新兴趣方向。"


def test_api() -> bool:
    """Test MiniMax API connectivity."""
    if not MINIMAX_API_KEY:
        print("❌ 未设置 API Key")
        return False
    
    print(f"🔑 使用 API Key: {MINIMAX_API_KEY[:12]}...")
    
    # Try MiniMax-Text-01 first (newer models)
    test_messages = [{"role": "user", "content": "请回复'API连接正常'，只需回复这四个字"}]
    result = call_minimax_chat(DEFAULT_MODEL, test_messages, max_tokens=50)
    
    if result:
        print(f"✅ MiniMax API连接正常 (model={DEFAULT_MODEL})")
        return True
    
    # Fallback to abab5.5-chat with text API
    print("⚠️ MiniMax-Text-01 不可用，尝试 abab5.5-chat...")
    result = call_minimax_text("abab5.5-chat", test_messages, max_tokens=50)
    if result:
        print(f"✅ MiniMax API连接正常 (model=abab5.5-chat, text API)")
        return True
    
    print("❌ MiniMax API调用失败，请检查 API Key 和余额")
    return False


def summarize_repos(repos: List[Dict], skip_ai: bool = False) -> List[Dict]:
    """Add AI summaries to a list of repos. Returns list of dicts with summary field."""
    if skip_ai or not repos:
        return repos
    
    print(f"\n🤖 正在生成 AI 摘要 ({len(repos)} 个项目)...")
    
    # Generate daily summary first
    print("📝 生成今日趋势综合摘要...")
    daily_summary = generate_daily_summary(repos)
    print(f"   摘要: {daily_summary[:60]}...")
    
    results = []
    for i, repo in enumerate(repos, 1):
        print(f"   [{i}/{len(repos)}] {repo.get('full_name', '?')}...", end=" ", flush=True)
        
        summary = generate_repo_summary(repo)
        repo_with_summary = {**repo, "ai_summary": summary}
        results.append(repo_with_summary)
        
        print(f"✅ {summary[:40]}...")
        time.sleep(0.3)  # Rate limiting
    
    return results, daily_summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MiniMax AI Summary Generator")
    parser.add_argument("--test", action="store_true", help="Test API connectivity")
    parser.add_argument("--skip-ai", action="store_true", help="Skip AI generation (use simple summaries)")
    args = parser.parse_args()
    
    if args.test:
        test_api()
    else:
        # Load repos from data file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(os.path.dirname(script_dir), "data", "latest_report.json")
        
        if not os.path.exists(data_path):
            print(f"⚠️ 未找到数据文件: {data_path}")
            print("请先运行 fetch_trending.py")
            sys.exit(1)
        
        with open(data_path) as f:
            data = json.load(f)
        
        # Convert string summaries back to full repo data
        # In real usage, fetch_trending.py stores the full repo objects
        print("ℹ️ 直接运行 ai_summary.py 需要先修改 fetch_trending.py 以存储完整repo数据")
        print("请使用 run_daily.sh 运行完整流程")
