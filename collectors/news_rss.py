"""
News RSS Collector — Fetches AI articles from major tech news outlets.
Parses RSS feeds from TechCrunch, The Verge, Ars Technica, VentureBeat, etc.
"""

import requests
import feedparser
from datetime import datetime, timezone, timedelta
import config


def _has_ai_content(title, summary=""):
    """Check if an article is AI-related based on keywords."""
    text = f"{title} {summary}".lower()
    return any(kw in text for kw in config.HN_AI_KEYWORDS)


def fetch():
    """Fetch AI-related articles from configured news RSS feeds."""
    all_items = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    for source_name, feed_url in config.NEWS_RSS_FEEDS:
        try:
            headers = {"User-Agent": config.USER_AGENT}
            resp = requests.get(feed_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            resp.raise_for_status()

            feed = feedparser.parse(resp.text)

            for entry in feed.entries[:30]:  # Check last 30 entries
                title = entry.get("title", "")
                summary = entry.get("summary", "") or entry.get("description", "") or ""

                # Filter for AI content
                if not _has_ai_content(title, summary):
                    continue

                # Parse published date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

                if published and published < cutoff:
                    continue

                # Clean up description (remove HTML tags)
                from bs4 import BeautifulSoup
                clean_summary = BeautifulSoup(summary, "lxml").get_text()[:200].strip()

                item = {
                    "title": title,
                    "url": entry.get("link", ""),
                    "external_url": entry.get("link", ""),
                    "source": source_name,
                    "source_category": "News",
                    "score": 0,
                    "comments": 0,
                    "description": clean_summary,
                    "published_at": published.isoformat() if published else "",
                    "content_type": "article",
                    "engagement": 0,
                }
                all_items.append(item)

        except Exception as e:
            print(f"  ⚠ News feed {source_name} failed: {e}")
            continue

    print(f"  ✓ News RSS: {len(all_items)} articles collected")
    return all_items
