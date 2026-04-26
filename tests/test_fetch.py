#!/usr/bin/env python3
"""GitHub Trending Bot - 单元测试"""
import sys
import os
import json

# 确保脚本可以导入 project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_generate_summary():
    """测试摘要生成函数"""
    from scripts.fetch_trending import generate_summary

    mock_repo = {
        "full_name": "test/repo",
        "description": "A test repository",
        "stargazers_count": 1234,
        "language": "Python",
        "html_url": "https://github.com/test/repo",
    }

    summary = generate_summary(mock_repo)
    assert "test/repo" in summary
    assert "1234" in summary
    assert "Python" in summary
    print("✅ test_generate_summary passed")


def test_fetch_trending_returns_list():
    """测试 fetch_trending 返回 list"""
    from scripts.fetch_trending import fetch_trending

    result = fetch_trending(lang="python")
    assert isinstance(result, list)
    print(f"✅ test_fetch_trending_returns_list passed (got {len(result)} items)")


def test_report_file_structure():
    """测试报告文件结构"""
    report_path = os.path.join(os.path.dirname(__file__), "../data/latest_report.json")
    if os.path.exists(report_path):
        with open(report_path) as f:
            data = json.load(f)
        assert "generated_at" in data
        assert "repos" in data
        assert isinstance(data["repos"], list)
        print(f"✅ test_report_file_structure passed (got {len(data['repos'])} repos)")
    else:
        print("⚠️  report file not found, skipping")


def test_md_report_generation():
    """测试 Markdown 报告生成"""
    from scripts.generate_report import generate_md_report

    out_path = generate_md_report()
    if out_path and os.path.exists(out_path):
        with open(out_path) as f:
            content = f.read()
        assert "GitHub Trending" in content
        assert "热门项目" in content
        print("✅ test_md_report_generation passed")
    else:
        print("⚠️  MD report not generated, skipping")


if __name__ == "__main__":
    print("🧪 运行单元测试...\n")
    test_generate_summary()
    test_fetch_trending_returns_list()
    test_report_file_structure()
    test_md_report_generation()
    print("\n✅ 所有测试完成")
