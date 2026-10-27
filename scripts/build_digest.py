#!/usr/bin/env python3
"""Build a deterministic Markdown digest from Crypto Radar's JSON feed."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEED = ROOT / "data" / "auto-news.json"
DEFAULT_OUTPUT = ROOT / "data" / "latest-digest.md"


def build_digest(payload: dict) -> str:
    events = payload.get("events", [])
    updated = payload.get("updated_at") or "Unknown"
    ordered = sorted(events, key=lambda e: (e.get("publishedAt") or e.get("date") or ""), reverse=True)
    categories = Counter(e.get("category", "Other") for e in events)
    statuses = Counter(e.get("status", "Unknown") for e in events)
    lines = [
        "# Crypto Radar — Signal Digest",
        "",
        f"> Feed updated: {updated}",
        "",
        "## Overview",
        "",
        f"- Total signals: **{len(events)}**",
        f"- Projects represented: **{len({e.get('projectId') for e in events if e.get('projectId')})}**",
        f"- Confirmed source-origin items: **{statuses.get('Confirmed', 0)}**",
        f"- Unconfirmed items: **{statuses.get('Unconfirmed', 0)}**",
        f"- Rumors: **{statuses.get('Rumor', 0)}**",
        "",
        "## Categories",
        "",
    ]
    if categories:
        lines.extend(f"- {name}: {count}" for name, count in sorted(categories.items()))
    else:
        lines.append("- No signals collected yet.")
    lines.extend(["", "## Latest signals", ""])
    if not ordered:
        lines.append("No signals are available yet.")
    for event in ordered[:20]:
        title = str(event.get("title", "Untitled")).replace("\n", " ").strip()
        source = str(event.get("source", ""))
        date = event.get("date") or "date unknown"
        status = event.get("status") or "Unknown"
        project = event.get("project") or event.get("projectId") or "Unknown project"
        category = event.get("category") or "Other"
        lines.append(f"- **[{status}] {project} · {category} · {date}** — {title}")
        if source.startswith(("https://", "http://")):
            lines.append(f"  Source: <{source}>")
    lines.extend([
        "",
        "---",
        "Automatically generated from data/auto-news.json. Labels indicate source confidence, not investment advice.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feed", type=Path, default=DEFAULT_FEED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = json.loads(args.feed.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("events"), list):
        parser.error("feed must be a JSON object with an events array")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_digest(payload), encoding="utf-8")
    print(f"Wrote digest to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
