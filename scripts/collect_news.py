#!/usr/bin/env python3
"""Collect official project feeds and secondary mentions for Crypto Radar."""
from __future__ import annotations
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "sources.json"
OUTPUT = ROOT / "data" / "auto-news.json"
USER_AGENT = "CryptoRadarBot/1.0 (+https://github.com/pavel9213/crypto-radar)"
RUMOR_WORDS = re.compile(r"\b(rumou?rs?|speculation|speculative|unconfirmed|allegedly|leaked|leak|insider claims|not confirmed)\b", re.I)
CATEGORIES = [
    ("TGE", re.compile(r"\b(tge|token generation|token launch|launch date|token launch date|listing date)\b", re.I)),
    ("Snapshot", re.compile(r"\b(snapshot|snapshot date|eligibility check|checker)\b", re.I)),
    ("Airdrop", re.compile(r"\b(airdrop|claim tokens|claiming|claim window)\b", re.I)),
    ("Points", re.compile(r"\b(points|points program|points campaign|leaderboard|xp)\b", re.I)),
    ("Partnership", re.compile(r"\b(partner|partnership|integrat(?:e|ion)|collaboration)\b", re.I)),
]
TIMEOUT = 18

def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml, application/rss+xml, application/xml, text/html, application/json, */*;q=0.8", **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return response.read(), response.headers.get("Content-Type", "")

def normalize_date(value):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        try:
            parsed = parsedate_to_datetime(value)
        except (ValueError, TypeError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def local_date(iso):
    return iso[:10] if iso else dt.datetime.now(dt.timezone.utc).date().isoformat()

def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()

def category_for(title, summary=""):
    text = title + " " + summary
    for name, pattern in CATEGORIES:
        if pattern.search(text):
            return name
    return "News"

def host_is_official(url, project):
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    return any(host == domain or host.endswith("." + domain) for domain in project.get("official_domains", []))

def status_for(title, summary, official):
    if RUMOR_WORDS.search(title + " " + summary):
        return "Rumor"
    return "Confirmed" if official else "Unconfirmed"

def parse_feed(xml_bytes):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    items = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1].lower() not in ("item", "entry"):
            continue
        values = {}
        for child in list(node):
            key = child.tag.rsplit("}", 1)[-1].lower()
            if key == "link":
                href = child.attrib.get("href")
                rel = child.attrib.get("rel", "alternate")
                if href and rel in ("alternate", ""):
                    values.setdefault("link", href)
                elif child.text and child.text.strip():
                    values.setdefault("link", child.text.strip())
            elif key in ("title", "summary", "description", "published", "updated", "pubdate", "guid", "id", "source"):
                values[key] = "".join(child.itertext()).strip()
        link = values.get("link") or values.get("guid") or values.get("id")
        title = plain_text(values.get("title", ""))
        if not title or not link or not link.startswith(("http://", "https://")):
            continue
        pub = normalize_date(values.get("published") or values.get("pubdate") or values.get("updated"))
        items.append({"title": title, "url": link, "summary": plain_text(values.get("summary") or values.get("description", ""))[:800], "published_at": pub, "publisher": plain_text(values.get("source", ""))})
    return items

def discover_feed_urls(homepage):
    candidates = [urljoin(homepage, path) for path in ("/feed.xml", "/rss.xml", "/atom.xml", "/feed", "/rss", "/blog/feed", "/blog/rss.xml", "/news/feed.xml")]
    try:
        raw, _ = fetch(homepage)
        text = raw.decode("utf-8", "replace")
        for match in re.finditer(r"<link\b[^>]*>", text, re.I):
            tag = match.group(0)
            if re.search(r"application/(?:rss\+xml|atom\+xml|feed\+json)", tag, re.I):
                href = re.search(r"\bhref\s*=\s*['\"]([^'\"]+)", tag, re.I)
                if href:
                    candidates.insert(0, urljoin(homepage, html.unescape(href.group(1))))
    except Exception as exc:
        print(f"[feed-discovery] {homepage}: {type(exc).__name__}", file=sys.stderr)
    return list(dict.fromkeys(candidates))

def make_event(project, item, official, source_kind):
    title = item["title"][:240]
    summary = item.get("summary", "")
    published = item.get("published_at") or dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    url = item["url"]
    category = category_for(title, summary)
    status = status_for(title, summary, official)
    publisher = item.get("publisher") or (urlparse(url).hostname or "source")
    note = ("Published by an official project source; check the linked announcement for exact details." if official else f"Secondary source ({publisher}); not an official confirmation. Verify with the project before acting.")
    if status == "Rumor":
        note = f"Rumor/speculation wording detected in this source ({publisher}). Treat as unconfirmed until an official announcement appears."
    import hashlib
    event_id = "auto-" + hashlib.sha256((project["id"] + "|" + url.rstrip("/")).encode("utf-8")).hexdigest()[:20]
    return {"id": event_id, "projectId": project["id"], "project": project["name"], "category": category, "title": title, "status": status, "date": local_date(published), "publishedAt": published, "source": url, "sourceName": publisher, "sourceType": source_kind, "automatic": True, "notes": note}

def google_news_url(query):
    return "https://news.google.com/rss/search?q=" + urllib.parse.quote(query, safe="") + "&hl=en-US&gl=US&ceid=US:en"

def collect_google_news(project):
    items = []
    for keyword in project.get("keywords", [project["name"]]):
        try:
            raw, _ = fetch(google_news_url('"' + keyword + '"'))
            for item in parse_feed(raw):
                item["publisher"] = item.get("publisher") or (urlparse(item["url"]).hostname or "Google News")
                items.append(item)
        except Exception as exc:
            print(f"[news-search] {project['name']}: {type(exc).__name__}", file=sys.stderr)
    return items

def collect_x(project, bearer):
    if not bearer:
        return []
    items = []
    for handle in project.get("x_handles", []):
        query = urllib.parse.quote(f"from:{handle} -is:retweet", safe=":-")
        url = "https://api.x.com/2/tweets/search/recent?query=" + query + "&max_results=25&tweet.fields=created_at,lang,entities"
        try:
            raw, _ = fetch(url, {"Authorization": "Bearer " + bearer})
            body = json.loads(raw)
            for post in body.get("data", []):
                tweet_id = post.get("id")
                if tweet_id:
                    items.append({"title": plain_text(post.get("text", ""))[:240], "url": f"https://x.com/{handle}/status/{tweet_id}", "summary": plain_text(post.get("text", ""))[:800], "published_at": normalize_date(post.get("created_at")), "publisher": "@" + handle})
        except urllib.error.HTTPError as exc:
            print(f"[x-api] @{handle}: HTTP {exc.code} (check API access/token)", file=sys.stderr)
        except Exception as exc:
            print(f"[x-api] @{handle}: {type(exc).__name__}", file=sys.stderr)
    return items

def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    events = {}
    now = dt.datetime.now(dt.timezone.utc)
    bearer = os.environ.get("X_BEARER_TOKEN", "").strip()
    for project in config["projects"]:
        official_items = []
        seen_feed_urls = set()
        for homepage in project.get("official_urls", []):
            for feed_url in discover_feed_urls(homepage):
                if feed_url in seen_feed_urls:
                    continue
                seen_feed_urls.add(feed_url)
                try:
                    raw, content_type = fetch(feed_url)
                    if b"<html" in raw[:500].lower() and "xml" not in content_type.lower():
                        continue
                    for item in parse_feed(raw):
                        if host_is_official(item["url"], project):
                            official_items.append(item)
                except Exception:
                    continue
        official_items.extend(collect_x(project, bearer))
        for item in official_items:
            event = make_event(project, item, True, "official")
            events[event["id"]] = event
        for item in collect_google_news(project):
            if host_is_official(item["url"], project):
                continue
            event = make_event(project, item, False, "news-index")
            events.setdefault(event["id"], event)
        count = sum(1 for event in events.values() if event["projectId"] == project["id"])
        print(f"[collect] {project['name']}: {count} unique items")
        time.sleep(0.15)
    ordered = sorted(events.values(), key=lambda event: event.get("publishedAt") or "", reverse=True)[:int(config.get("max_events", 250))]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"updated_at": now.isoformat(timespec="seconds").replace("+00:00", "Z"), "source_mode": "official feeds + secondary news index" + (" + X API" if bearer else ""), "events": ordered}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[done] wrote {len(ordered)} events to {OUTPUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
