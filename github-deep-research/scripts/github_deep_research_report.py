#!/usr/bin/env python3
"""
Generate a markdown report for a GitHub repository using gh-first data collection.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone


def run_python_summary(owner: str, repo: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            __file__.replace('github_deep_research_report.py', 'github_cli_summary.py'),
            owner,
            repo,
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
    return json.loads(result.stdout)


def first_line(text: str | None) -> str:
    if not text:
        return ""
    return text.strip().splitlines()[0]


def render_report(data: dict, owner: str, repo: str) -> str:
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    top_issues = data.get('top_issues', [])[:5]
    prs = data.get('recent_prs', [])[:5]
    commits = data.get('recent_commits', [])[:5]
    releases = data.get('latest_releases', [])[:5]

    issue_lines = "\n".join(
        f"- #{item['number']} {item['title']}（{item['state']}）: {item['url']}"
        for item in top_issues
    ) or "- 未获取到高价值 issue 列表"

    pr_lines = "\n".join(
        f"- #{item['number']} {item['title']}（{item['state']}）: {item['url']}"
        for item in prs
    ) or "- 未获取到近期 PR 列表"

    commit_lines = "\n".join(
        f"- `{item['sha'][:7]}` {first_line(item['message'])}（{item['date']}）"
        for item in commits
    ) or "- 未获取到近期 commit 列表"

    release_lines = "\n".join(
        f"- {item.get('tagName') or item.get('name') or '未命名版本'}（{item.get('publishedAt') or '时间未知'}）"
        for item in releases
    ) or "- 未检测到近期 release"

    summary = f"该仓库当前 stars 为 {data.get('stars', '未知')}，forks 为 {data.get('forks', '未知')}，主语言为 {data.get('language') or '未知'}。从近期 PR、Issue 与 commit 节奏看，仓库仍处于活跃演进状态，适合继续跟踪其功能扩展、修复节奏与维护质量。"

    return f"# GitHub 深度研究报告：{owner}/{repo}\n\n" \
           f"生成时间：{now}\n\n" \
           f"## Executive Summary\n\n{summary}\n\n" \
           f"## Repository Snapshot\n\n" \
           f"- 仓库：`{owner}/{repo}`\n" \
           f"- 链接：{data.get('url', '')}\n" \
           f"- 描述：{data.get('description') or '无'}\n" \
           f"- Stars：{data.get('stars', '未知')}\n" \
           f"- Forks：{data.get('forks', '未知')}\n" \
           f"- 主语言：{data.get('language') or '未知'}\n" \
           f"- 许可证：{data.get('license') or '未知'}\n" \
           f"- 创建时间：{data.get('created_at') or '未知'}\n" \
           f"- 最近更新时间：{data.get('updated_at') or '未知'}\n" \
           f"- 最近推送：{data.get('pushed_at') or '未知'}\n" \
           f"- 默认分支：{data.get('default_branch') or '未知'}\n\n" \
           f"## Recent Releases\n\n{release_lines}\n\n" \
           f"## Top Issues\n\n{issue_lines}\n\n" \
           f"## Recent Pull Requests\n\n{pr_lines}\n\n" \
           f"## Recent Commits\n\n{commit_lines}\n\n" \
           f"## Initial Assessment\n\n" \
           f"- 该报告当前基于 `gh` CLI 获取的 GitHub 原生数据生成。\n" \
           f"- 如需更完整结论，后续应补充：官方文档、项目主页、论文页、release notes、媒体报道。\n" \
           f"- 本报告适合作为 `space-news` 在开源项目方向上的前置分析材料，而不是单独替代最终情报简报。\n"


def main() -> None:
    if len(sys.argv) < 3:
        print('Usage: python github_deep_research_report.py <owner> <repo> [output.md]', file=sys.stderr)
        sys.exit(1)

    owner, repo = sys.argv[1], sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else f'research_{repo}_{datetime.now().strftime("%Y%m%d")}.md'

    data = run_python_summary(owner, repo)
    report = render_report(data, owner, repo)

    with open(output_path, 'w', encoding='utf-8') as handle:
        handle.write(report)

    print(output_path)


if __name__ == '__main__':
    main()
