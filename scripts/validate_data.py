#!/usr/bin/env python3
"""Validate Crypto Radar configuration and generated feed JSON."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "sources.json"
DEFAULT_FEED = ROOT / "data" / "auto-news.json"
VALID_STATUSES = {"Confirmed", "Unconfirmed", "Rumor", "Monitoring"}
VALID_CATEGORIES = {"TGE", "Snapshot", "Airdrop", "Points", "Partnership", "News", "Other"}


def read_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [f"{path}: cannot read file ({exc})"]
    except json.JSONDecodeError as exc:
        return None, [f"{path}:{exc.lineno}:{exc.colno}: invalid JSON ({exc.msg})"]


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.hostname)


def validate_config(config: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["config: expected a JSON object"]
    projects = config.get("projects")
    if not isinstance(projects, list) or not projects:
        errors.append("config.projects: expected a non-empty array")
        projects = []
    ids: set[str] = set()
    for i, project in enumerate(projects):
        prefix = f"config.projects[{i}]"
        if not isinstance(project, dict):
            errors.append(f"{prefix}: expected an object")
            continue
        project_id = project.get("id")
        if not isinstance(project_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", project_id):
            errors.append(f"{prefix}.id: expected a lowercase slug")
        elif project_id in ids:
            errors.append(f"{prefix}.id: duplicate project id {project_id!r}")
        else:
            ids.add(project_id)
        if not isinstance(project.get("name"), str) or not project["name"].strip():
            errors.append(f"{prefix}.name: expected a non-empty string")
        for field in ("keywords", "official_urls", "official_domains", "x_handles"):
            value = project.get(field)
            if not isinstance(value, list):
                errors.append(f"{prefix}.{field}: expected an array")
                continue
            for j, entry in enumerate(value):
                if not isinstance(entry, str) or not entry.strip():
                    errors.append(f"{prefix}.{field}[{j}]: expected a non-empty string")
                elif field == "official_urls" and not valid_http_url(entry):
                    errors.append(f"{prefix}.official_urls[{j}]: expected an HTTP(S) URL")
                elif field == "official_domains" and ("/" in entry or "://" in entry or " " in entry):
                    errors.append(f"{prefix}.official_domains[{j}]: expected a hostname, not a URL")
                elif field == "x_handles" and not re.fullmatch(r"[A-Za-z0-9_]{1,15}", entry):
                    errors.append(f"{prefix}.x_handles[{j}]: invalid X handle")
    for field, minimum, maximum in (("poll_interval_hours", 1, 24), ("max_events", 1, 5000)):
        value = config.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
            errors.append(f"config.{field}: expected an integer from {minimum} to {maximum}")
    return errors


def validate_feed(feed: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(feed, dict):
        return ["feed: expected a JSON object"]
    events = feed.get("events")
    if not isinstance(events, list):
        return ["feed.events: expected an array"]
    ids: set[str] = set()
    for i, event in enumerate(events):
        prefix = f"feed.events[{i}]"
        if not isinstance(event, dict):
            errors.append(f"{prefix}: expected an object")
            continue
        event_id = event.get("id")
        if not isinstance(event_id, str) or not event_id.strip():
            errors.append(f"{prefix}.id: expected a non-empty string")
        elif event_id in ids:
            errors.append(f"{prefix}.id: duplicate event id {event_id!r}")
        else:
            ids.add(event_id)
        for field in ("projectId", "project", "title", "source", "date", "status", "category"):
            if not isinstance(event.get(field), str) or not event[field].strip():
                errors.append(f"{prefix}.{field}: expected a non-empty string")
        if event.get("status") not in VALID_STATUSES:
            errors.append(f"{prefix}.status: unsupported value {event.get('status')!r}")
        if event.get("category") not in VALID_CATEGORIES:
            errors.append(f"{prefix}.category: unsupported value {event.get('category')!r}")
        if "source" in event and not valid_http_url(event["source"]):
            errors.append(f"{prefix}.source: expected an HTTP(S) URL")
        date = event.get("date")
        if isinstance(date, str):
            try:
                dt.date.fromisoformat(date)
            except ValueError:
                errors.append(f"{prefix}.date: expected ISO date YYYY-MM-DD")
        published = event.get("publishedAt")
        if published is not None:
            try:
                parsed = dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    errors.append(f"{prefix}.publishedAt: timestamp must include a timezone")
            except (ValueError, AttributeError):
                errors.append(f"{prefix}.publishedAt: expected an ISO-8601 timestamp")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--feed", type=Path, default=DEFAULT_FEED)
    args = parser.parse_args(argv)
    config, config_read_errors = read_json(args.config)
    feed, feed_read_errors = read_json(args.feed)
    errors = config_read_errors + feed_read_errors
    if config is not None:
        errors.extend(validate_config(config))
    if feed is not None:
        errors.extend(validate_feed(feed))
    if errors:
        print("Crypto Radar validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print(f"Validation passed: {args.config} and {args.feed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
