#!/usr/bin/env python3
"""Normalize, rank, classify, and render a Chinese space intelligence brief."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlparse

from space_news_overrides import TITLE_TRANSLATIONS

CATEGORY_LABELS = {
    "mission": "航天任务与任务动态",
    "ai_product": "AI 航天技术与产品",
    "eo_ai": "遥感与对地观测 AI",
    "research": "科研论文与高校成果",
    "conference": "国际会议与学术活动",
    "open_source": "开源项目与工具生态",
    "agency_program": "航天机构项目与新产品",
    "startup": "商业航天与初创公司",
}


DOMAIN_LABELS = {
    "defense": "军事与国防",
    "commercial": "商业航天",
    "civil": "民用与公共服务",
    "research_academic": "科研与学术",
    "agency_national": "国际机构与国家项目",
}

SOURCE_PRIORITY = {
    "official": 40,
    "academic": 34,
    "opensource": 30,
    "media": 24,
    "social": 10,
}

CATEGORY_PRIORITY = {
    "mission": 18,
    "ai_product": 22,
    "eo_ai": 21,
    "research": 18,
    "conference": 14,
    "open_source": 16,
    "agency_program": 17,
    "startup": 14,
}

TYPE_PRIORITY = {
    "milestone": 20,
    "release": 18,
    "paper": 16,
    "project": 15,
    "conference": 12,
    "funding": 11,
    "profile": 10,
    "update": 8,
}

HIGH_SIGNAL_KEYWORDS = (
    "autonomy",
    "autonomous",
    "onboard ai",
    "mission operations",
    "guidance",
    "navigation",
    "control",
    "gnc",
    "remote sensing",
    "earth observation",
    "foundation model",
    "digital twin",
    "simulation",
    "verification",
    "space robotics",
    "docking",
    "rendezvous",
    "ssa",
    "stm",
    "在轨智能",
    "自主导航",
    "遥感",
    "对地观测",
    "数字孪生",
    "仿真验证",
    "空间机器人",
)

DEFAULT_OFFICIAL_DOMAINS = (
    "nasa.gov",
    "jpl.nasa.gov",
    "esa.int",
    "jaxa.jp",
    "isro.gov.in",
    "cnsa.gov.cn",
    "roscosmos.ru",
)

DEFAULT_ACADEMIC_DOMAINS = (
    "arxiv.org",
    "ieee.org",
    "springer.com",
    "sciencedirect.com",
    "nature.com",
)

DEFAULT_MEDIA_DOMAINS = (
    "spacenews.com",
    "space.com",
    "reuters.com",
    "apnews.com",
)


def parse_date(value: str) -> dt.date | None:
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def normalize_source_type(url: str, raw: str) -> str:
    raw = (raw or "").strip().lower()
    if raw in SOURCE_PRIORITY:
        return raw
    host = urlparse(url).netloc.lower()
    if any(domain in host for domain in DEFAULT_OFFICIAL_DOMAINS):
        return "official"
    if any(domain in host for domain in DEFAULT_ACADEMIC_DOMAINS):
        return "academic"
    if "github.com" in host or "gitlab" in host:
        return "opensource"
    if any(domain in host for domain in DEFAULT_MEDIA_DOMAINS):
        return "media"
    if "x.com" in host or "youtube.com" in host or "youtu.be" in host:
        return "social"
    return "media"


def recency_score(event_date: str, today: dt.date) -> int:
    parsed = parse_date(event_date)
    if parsed is None:
        return 0
    delta = (today - parsed).days
    if delta < 0:
        return 0
    if delta <= 2:
        return 15
    if delta <= 7:
        return 10
    if delta <= 14:
        return 6
    if delta <= 30:
        return 3
    return 0


def signal_bonus(text: str) -> int:
    lowered = text.lower()
    hits = sum(1 for keyword in HIGH_SIGNAL_KEYWORDS if keyword in lowered)
    return min(hits * 3, 18)


def score_item(item: dict, today: dt.date) -> int:
    text = f"{item.get('title', '')} {item.get('summary', '')} {item.get('entities', '')}"
    return (
        SOURCE_PRIORITY.get(item.get("source_type", "media"), 0)
        + CATEGORY_PRIORITY.get(item.get("category", "mission"), 0)
        + TYPE_PRIORITY.get(item.get("item_type", "update"), 0)
        + (12 if item.get("cross_confirmed") else 0)
        + recency_score(str(item.get("date", "")), today)
        + signal_bonus(text)
    )


def infer_domain_tag(raw: dict, title: str, summary: str, entities: str, url: str) -> str:
    domain = str(raw.get("domain_tag", "")).strip().lower()
    if domain in DOMAIN_LABELS:
        return domain

    text = f"{title} {summary} {entities} {url}".lower()
    if any(keyword in text for keyword in ("defense", "military", "space force", "missile warning", "ssa", "stm", "national security", "国防", "军事")):
        return "defense"
    if any(keyword in text for keyword in ("startup", "funding", "contract", "commercial", "venture", "series a", "seed", "商业")):
        return "commercial"
    if any(keyword in text for keyword in ("weather", "disaster", "agriculture", "navigation", "communication", "public service", "civil", "气象", "灾害", "导航", "通信", "农业")):
        return "civil"
    if any(keyword in text for keyword in ("arxiv", "paper", "university", "lab", "conference", "workshop", "research", "高校", "实验室", "论文", "会议")):
        return "research_academic"
    if any(keyword in text for keyword in ("nasa", "esa", "jaxa", "isro", "cnsa", "agency", "国家项目", "航天局")):
        return "agency_national"
    return "research_academic"


def is_pure_english_title(title: str) -> bool:
    if not title:
        return False
    return all(ord(char) < 128 for char in title)


def format_title(title: str) -> str:
    translated = TITLE_TRANSLATIONS.get(title)
    if translated and is_pure_english_title(title):
        return f"{title}（{translated}）"
    return title


def normalize_item(raw: dict) -> dict | None:
    title = str(raw.get("title", "")).strip()
    url = str(raw.get("url", raw.get("source_url", ""))).strip()
    date_value = str(raw.get("date", raw.get("event_date", ""))).strip()
    if not title or not url or parse_date(date_value) is None:
        return None

    category = str(raw.get("category", "mission")).strip().lower()
    if category not in CATEGORY_LABELS:
        category = "mission"

    entities = str(raw.get("entities", "")).strip()
    summary = str(raw.get("summary", "")).strip()

    return {
        "title": format_title(title),
        "category": category,
        "domain_tag": infer_domain_tag(raw, title, summary, entities, url),
        "date": parse_date(date_value).isoformat(),
        "entities": entities,
        "summary": summary,
        "impact": str(raw.get("impact", "")).strip(),
        "url": url,
        "source_type": normalize_source_type(url, str(raw.get("source_type", ""))),
        "item_type": str(raw.get("item_type", "update")).strip().lower() or "update",
        "cross_confirmed": bool(raw.get("cross_confirmed", False)),
    }


def render_brief(items: list[dict], start_date: str, end_date: str, title: str) -> str:
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"时间范围：{start_date} 至 {end_date}")
    lines.append("")
    lines.append("## 本期摘要")
    lines.append("")
    lines.append("本期简报重点跟踪航天领域近期的重要动态，并优先关注人工智能在航天任务、遥感处理、任务运营、工程仿真与开源生态中的进展。以下条目按情报价值综合排序，兼顾来源权威性、技术含量、产业影响与时间新近程度。")
    lines.append("")
    lines.append("## 重点事件")
    lines.append("")

    for index, item in enumerate(items, start=1):
        lines.append(f"### {index}. {item['title']}")
        lines.append(f"- 分类：{CATEGORY_LABELS[item['category']]}")
        lines.append(f"- 领域标签：{DOMAIN_LABELS.get(item['domain_tag'], '科研与学术')}")
        lines.append(f"- 时间：{item['date']}")
        lines.append(f"- 涉及主体：{item['entities'] or '未明确披露'}")
        lines.append(f"- 内容摘要：{item['summary'] or '目前公开信息有限。'}")
        lines.append(f"- 关注点 / 影响：{item['impact'] or '该事件可能对航天技术路线、产业竞争或科研方向产生持续影响。'}")
        lines.append(f"- 来源链接：{item['url']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Chinese space intelligence brief from normalized JSON items")
    parser.add_argument("--input", required=True, help="Path to input JSON array")
    parser.add_argument("--output", required=True, help="Path to output markdown file")
    parser.add_argument("--start-date", required=True, help="Start date like 2026-03-17")
    parser.add_argument("--end-date", required=True, help="End date like 2026-03-23")
    parser.add_argument("--top-n", type=int, default=30, help="Maximum number of items to render")
    parser.add_argument("--title", default="航天情报简报：AI 与航天领域近期动态", help="Markdown title")
    args = parser.parse_args()

    raw_items = json.loads(Path(args.input).read_text(encoding="utf-8"))
    items = [normalize_item(item) for item in raw_items]
    items = [item for item in items if item is not None]

    today = dt.date.today()
    items.sort(key=lambda item: score_item(item, today), reverse=True)
    selected = items[: max(args.top_n, 1)]

    output = render_brief(selected, args.start_date, args.end_date, args.title)
    Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
