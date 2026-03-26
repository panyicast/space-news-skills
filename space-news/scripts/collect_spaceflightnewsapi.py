#!/usr/bin/env python3
"""Collect recent space news candidates from Spaceflight News API and map them into space-news JSON format."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://api.spaceflightnewsapi.net/v4/articles/"


def iso_days_ago(days: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat().replace("+00:00", "Z")


def fetch_articles(days: int, limit: int) -> list[dict]:
    params = {
        "published_at_gte": iso_days_ago(days),
        "limit": limit,
        "ordering": "-published_at",
    }
    url = f"{API_BASE}?{urlencode(params)}"
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "OpenClaw-space-news/1.0"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("results", []) if isinstance(payload, dict) else []


def infer_category(title: str, summary: str, url: str) -> str:
    text = f"{title} {summary} {url}".lower()
    if any(keyword in text for keyword in ("startup", "funding", "contract", "commercial", "venture", "series a", "seed")):
        return "startup"
    if any(keyword in text for keyword in ("conference", "workshop", "forum", "symposium", "call for papers", "cfp")):
        return "conference"
    if any(keyword in text for keyword in ("github", "open-source", "open source", "repository")):
        return "open_source"
    if any(keyword in text for keyword in ("remote sensing", "earth observation", "sar", "geospatial")):
        return "eo_ai"
    if any(keyword in text for keyword in ("ai", "artificial intelligence", "autonomy", "machine learning", "onboard", "mission operations")):
        return "ai_product"
    if any(keyword in text for keyword in ("esa", "nasa", "jaxa", "isro", "cnsa", "agency", "program", "mission")):
        return "agency_program"
    return "mission"


def infer_domain_tag(title: str, summary: str, url: str) -> str:
    text = f"{title} {summary} {url}".lower()
    if any(keyword in text for keyword in ("defense", "military", "space force", "national security", "missile warning", "ssa", "stm")):
        return "defense"
    if any(keyword in text for keyword in ("startup", "funding", "contract", "commercial", "venture", "launch company")):
        return "commercial"
    if any(keyword in text for keyword in ("weather", "disaster", "agriculture", "navigation", "communication", "public service", "climate")):
        return "civil"
    if any(keyword in text for keyword in ("esa", "nasa", "jaxa", "isro", "cnsa", "agency", "government", "national")):
        return "agency_national"
    return "research_academic"


def infer_item_type(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    if any(keyword in text for keyword in ("launch", "landing", "dock", "returned", "milestone", "demonstration")):
        return "milestone"
    if any(keyword in text for keyword in ("announced", "unveiled", "introduced", "release")):
        return "release"
    if any(keyword in text for keyword in ("funding", "raised", "contract", "investment")):
        return "funding"
    return "update"


def normalize_article(article: dict) -> dict | None:
    title = str(article.get("title", "")).strip()
    url = str(article.get("url", "")).strip()
    summary = str(article.get("summary", "")).strip()
    published_at = str(article.get("published_at", "")).strip()
    news_site = str(article.get("news_site", "")).strip()

    if not title or not url or not published_at:
        return None

    date_value = published_at[:10]
    category = infer_category(title, summary, url)
    return {
        "title": title,
        "category": category,
        "domain_tag": infer_domain_tag(title, summary, url),
        "date": date_value,
        "entities": news_site,
        "summary": summary,
        "impact": "",
        "url": url,
        "source_type": "media",
        "item_type": infer_item_type(title, summary),
        "cross_confirmed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect recent news from Spaceflight News API")
    parser.add_argument("--days", type=int, default=7, help="Lookback window in days")
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of news items")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    args = parser.parse_args()

    raw_articles = fetch_articles(days=max(1, args.days), limit=max(1, args.limit))
    normalized = [item for item in (normalize_article(article) for article in raw_articles) if item is not None]
    Path(args.output).write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
