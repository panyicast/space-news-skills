#!/usr/bin/env python3
"""Collect recent candidate items for a space intelligence brief via Brave Search."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
DEFAULT_QUERIES = [
    '"space ai" OR "AI for space" OR "artificial intelligence" space',
    '"remote sensing ai" OR "earth observation ai" space',
    'site:github.com (space OR satellite OR orbit OR remote sensing) (AI OR autonomy OR simulation)',
    'site:arxiv.org (space OR satellite OR remote sensing) (AI OR machine learning OR foundation model)',
    'site:esa.int OR site:nasa.gov OR site:jaxa.jp OR site:isro.gov.in (AI OR autonomy OR remote sensing)',
    'space startup AI satellite autonomy remote sensing',
    'space conference AI remote sensing autonomy',
    'military space AI OR defense space autonomy OR SSA AI OR STM AI',
    'commercial space AI startup satellite analytics remote sensing',
    'civil space AI weather disaster monitoring navigation communication',
]


def iso_date_days_ago(days: int) -> str:
    return (dt.date.today() - dt.timedelta(days=days)).isoformat()


def brave_search(api_key: str, query: str, freshness_days: int, count: int) -> list[dict]:
    date_after = iso_date_days_ago(freshness_days)
    url = (
        f"{BRAVE_ENDPOINT}?q={quote_plus(query)}"
        f"&count={count}&country=ALL&search_lang=en&ui_lang=en-US&date_after={date_after}"
    )
    request = Request(url, headers={"Accept": "application/json", "X-Subscription-Token": api_key})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("web", {}).get("results", [])


def infer_category(url: str, title: str, snippet: str) -> str:
    text = f"{title} {snippet} {url}".lower()
    if "github.com" in url:
        return "open_source"
    if "arxiv.org" in url or "paper" in text or "university" in text or "lab" in text:
        return "research"
    if "conference" in text or "workshop" in text or "call for papers" in text or "cfp" in text:
        return "conference"
    if any(keyword in text for keyword in ("startup", "funding", "venture", "seed", "series a")):
        return "startup"
    if any(keyword in text for keyword in ("esa", "nasa", "jaxa", "isro", "cnsa", "agency", "program", "platform")):
        return "agency_program"
    if any(keyword in text for keyword in ("remote sensing", "earth observation", "sar")):
        return "eo_ai"
    if any(keyword in text for keyword in ("autonomy", "onboard ai", "guidance", "navigation", "control", "mission operations")):
        return "ai_product"
    return "mission"


def infer_source_type(url: str) -> str:
    lower = url.lower()
    if any(domain in lower for domain in ("nasa.gov", "esa.int", "jaxa.jp", "isro.gov.in", "cnsa.gov.cn")):
        return "official"
    if "arxiv.org" in lower or "ieee.org" in lower or "nature.com" in lower:
        return "academic"
    if "github.com" in lower or "gitlab" in lower:
        return "opensource"
    if any(domain in lower for domain in ("spacenews.com", "space.com", "reuters.com", "apnews.com")):
        return "media"
    return "media"


def infer_domain_tag(url: str, title: str, snippet: str) -> str:
    text = f"{title} {snippet} {url}".lower()
    if any(keyword in text for keyword in ("defense", "military", "space force", "missile warning", "ssa", "stm", "national security")):
        return "defense"
    if any(keyword in text for keyword in ("startup", "funding", "contract", "commercial", "venture", "series a", "seed")):
        return "commercial"
    if any(keyword in text for keyword in ("weather", "disaster", "agriculture", "navigation", "communication", "public service", "civil")):
        return "civil"
    if any(keyword in text for keyword in ("arxiv", "paper", "university", "lab", "conference", "workshop", "research")):
        return "research_academic"
    if any(keyword in text for keyword in ("nasa", "esa", "jaxa", "isro", "cnsa", "agency", "program")):
        return "agency_national"
    return "research_academic"


def infer_item_type(title: str, snippet: str) -> str:
    text = f"{title} {snippet}".lower()
    if any(keyword in text for keyword in ("paper", "preprint", "study", "benchmark")):
        return "paper"
    if any(keyword in text for keyword in ("conference", "workshop", "forum", "symposium", "cfp")):
        return "conference"
    if any(keyword in text for keyword in ("launch", "landing", "docking", "returned", "milestone", "demonstration")):
        return "milestone"
    if any(keyword in text for keyword in ("release", "announced", "unveiled", "introduced")):
        return "release"
    if any(keyword in text for keyword in ("funding", "raised", "contract", "investment")):
        return "funding"
    if "github.com" in text:
        return "project"
    return "update"


def clean_snippet(value: str) -> str:
    return " ".join((value or "").replace("\n", " ").split()).strip()


def collect(api_key: str, freshness_days: int, count_per_query: int, sleep_seconds: float) -> list[dict]:
    seen_urls: set[str] = set()
    collected: list[dict] = []
    today = dt.date.today().isoformat()

    for query in DEFAULT_QUERIES:
        results = brave_search(api_key, query, freshness_days=freshness_days, count=count_per_query)
        for result in results:
            url = str(result.get("url", "")).strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            title = str(result.get("title", "")).strip()
            snippet = clean_snippet(str(result.get("description", "")))
            collected.append(
                {
                    "title": title,
                    "category": infer_category(url, title, snippet),
                    "domain_tag": infer_domain_tag(url, title, snippet),
                    "date": today,
                    "entities": "",
                    "summary": snippet,
                    "impact": "",
                    "url": url,
                    "source_type": infer_source_type(url),
                    "item_type": infer_item_type(title, snippet),
                    "cross_confirmed": False,
                    "query": query,
                }
            )
        time.sleep(max(sleep_seconds, 0.0))
    return collected


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect candidate space-news items via Brave Search")
    parser.add_argument("--api-key", help="Brave Search API key; can also use BRAVE_API_KEY env")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument("--freshness-days", type=int, default=7, help="Search window in days")
    parser.add_argument("--count-per-query", type=int, default=8, help="Results per query")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Pause between queries")
    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        import os

        api_key = os.environ.get("BRAVE_API_KEY", "")
    if not api_key:
        raise ValueError("Provide --api-key or set BRAVE_API_KEY.")

    items = collect(
        api_key=api_key,
        freshness_days=max(1, args.freshness_days),
        count_per_query=max(1, args.count_per_query),
        sleep_seconds=max(0.0, args.sleep_seconds),
    )
    Path(args.output).write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
