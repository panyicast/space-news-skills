#!/usr/bin/env python3
"""
GitHub CLI-based repository summary for environments where authenticated `gh`
works better than anonymous GitHub API access.
"""

import json
import subprocess
import sys
from typing import Any


def run_gh(args: list[str]) -> Any:
    result = subprocess.run(
        ["gh", *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    stdout = result.stdout.strip()
    if not stdout:
        return None
    return json.loads(stdout)


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python github_cli_summary.py <owner> <repo>", file=sys.stderr)
        sys.exit(1)

    owner, repo = sys.argv[1], sys.argv[2]
    full_repo = f"{owner}/{repo}"

    repo_info = run_gh(
        [
            "repo",
            "view",
            full_repo,
            "--json",
            "name,description,stargazerCount,forkCount,primaryLanguage,licenseInfo,createdAt,updatedAt,pushedAt,url,defaultBranchRef",
        ]
    )

    try:
        releases = run_gh(["release", "list", "--repo", full_repo, "--limit", "5", "--json", "name,tagName,publishedAt,isLatest"])
    except Exception:
        releases = []

    try:
        issues = run_gh(["issue", "list", "--repo", full_repo, "--limit", "10", "--state", "all", "--json", "number,title,state,createdAt,updatedAt,url,comments"])
    except Exception:
        issues = []

    try:
        prs = run_gh(["pr", "list", "--repo", full_repo, "--limit", "10", "--state", "all", "--json", "number,title,state,createdAt,updatedAt,url"])
    except Exception:
        prs = []

    try:
        commits = run_gh(["api", f"repos/{full_repo}/commits?per_page=10"])
    except Exception:
        commits = []

    summary = {
        "name": repo_info.get("name"),
        "description": repo_info.get("description"),
        "url": repo_info.get("url"),
        "stars": repo_info.get("stargazerCount"),
        "forks": repo_info.get("forkCount"),
        "language": (repo_info.get("primaryLanguage") or {}).get("name"),
        "license": (repo_info.get("licenseInfo") or {}).get("name"),
        "created_at": repo_info.get("createdAt"),
        "updated_at": repo_info.get("updatedAt"),
        "pushed_at": repo_info.get("pushedAt"),
        "default_branch": (repo_info.get("defaultBranchRef") or {}).get("name"),
        "latest_releases": releases,
        "top_issues": issues,
        "recent_prs": prs,
        "recent_commits": [
            {
                "sha": item.get("sha"),
                "message": ((item.get("commit") or {}).get("message") or "").split("\n", 1)[0],
                "date": ((item.get("commit") or {}).get("author") or {}).get("date"),
                "url": item.get("html_url"),
            }
            for item in commits
        ],
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
