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

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_CODE_PLAN_KEY", "")
if not MINIMAX_API_KEY:
    print("⚠️  未设置 MiniMax API Key，跳过AI摘要")

MINIMAX_BASE_URL = "https://api.minimaxi.com"
DEFAULT_MODEL = "MiniMax-Text-01"
CHAT_COMPLETION_URL = f"{MINIMAX_BASE_URL}/v1/chat/completions"

def call_minimax_chat(model: str, messages: List[Dict], max_tokens: int = 200,
                       temperature: float = 0.7) -> Optional[str]:
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MINIMAX_API_KEY}"}
    try:
        resp = requests.post(CHAT_COMPLETION_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()
        if resp.status_code == 200:
            return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        else:
            err = data.get("error", {})
            print(f"   ❌ API错误: {err.get('message', data)}")
            return None
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None

def generate_repo_summary(repo_name: str, description: str, stars: int, 
                         language: str, url: str) -> str:
    """生成单个repo的AI中文摘要"""
    if not MINIMAX_API_KEY:
        return f"**{repo_name}** ⭐{stars} | {language} | {description}"
    
    prompt = f"""请为以下GitHub项目生成一句精炼的中文介绍（30-60字）：
项目名：{repo_name}
描述：{description}
星标数：{stars}
语言：{language}
URL：{url}

要求：客观、专业、突出项目特色，直接返回中文介绍，不要前缀。"""
    
    messages = [{"role": "user", "content": prompt}]
    summary = call_minimax_chat(DEFAULT_MODEL, messages, max_tokens=100)
    
    if summary:
        return f"- **{repo_name}** ⭐{stars} | {language} | {summary}"
    return f"- **{repo_name}** ⭐{stars} | {language} | {description}"

def generate_daily_summary(repo_summaries: List[str]) -> str:
    """生成今日趋势综合摘要"""
    if not MINIMAX_API_KEY or not repo_summaries:
        return ""
    
    repos_text = "\n".join(repo_summaries[:10])
    prompt = f"""请分析以下今日GitHub热门项目，生成一段100字左右的中文趋势总结：
{repos_text}

要求：总结今日技术趋势和亮点，直接返回中文，不要前缀。"""
    
    messages = [{"role": "user", "content": prompt}]
    return call_minimax_chat(DEFAULT_MODEL, messages, max_tokens=150) or ""

if __name__ == "__main__":
    # 测试
    test_repo = {"name": "test/repo", "description": "A great project", "stars": 1000, "language": "Python", "url": "https://github.com/test/repo"}
    print(generate_repo_summary(**test_repo))
