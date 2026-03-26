#!/usr/bin/env python3
"""Merge and deduplicate multiple space-news candidate JSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize_text(value: str) -> str:
    return " ".join((value or "").lower().split()).strip()


def build_key(item: dict) -> tuple[str, str, str]:
    title = normalize_text(str(item.get("title", "")))
    url = normalize_text(str(item.get("url", "")))
    date = normalize_text(str(item.get("date", "")))
    return (title, url, date)


def merge_items(paths: list[str]) -> list[dict]:
    seen: dict[tuple[str, str, str], dict] = {}
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, list):
            continue
        for item in data:
            if not isinstance(item, dict):
                continue
            key = build_key(item)
            if key not in seen:
                seen[key] = item
                continue

            existing = seen[key]
            for field in ("summary", "impact", "entities"):
                if not existing.get(field) and item.get(field):
                    existing[field] = item[field]
            if existing.get("source_type") == "media" and item.get("source_type") in {"official", "academic", "opensource"}:
                existing["source_type"] = item["source_type"]
            if not existing.get("cross_confirmed") and item.get("cross_confirmed"):
                existing["cross_confirmed"] = True
    return list(seen.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge and deduplicate multiple space-news JSON candidate files")
    parser.add_argument("inputs", nargs="+", help="Input JSON files")
    parser.add_argument("--output", required=True, help="Output merged JSON file")
    args = parser.parse_args()

    merged = merge_items(args.inputs)
    Path(args.output).write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
