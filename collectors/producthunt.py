"""
Product Hunt Collector — Fetches trending AI products.
Uses Product Hunt's RSS feed and homepage scraping.
"""

import requests
import feedparser
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import config


def _is_ai_product(title, tagline=""):
    """Check if a product is AI-related."""
    text = f"{title} {tagline}".lower()
    return any(kw in text for kw in config.PH_AI_KEYWORDS)


def _fetch_from_rss():
    """Try to fetch from Product Hunt RSS feed."""
    items = []
    try:
        feed_url = "https://www.producthunt.com/feed"
        headers = {"User-Agent": config.USER_AGENT}
        resp = requests.get(feed_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()

        feed = feedparser.parse(resp.text)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=48)  # PH posts last longer

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")

            if not _is_ai_product(title, summary):
                continue

            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if published and published < cutoff:
                continue

            item = {
                "title": title,
                "url": entry.get("link", ""),
                "external_url": entry.get("link", ""),
                "source": "Product Hunt",
                "source_category": "Product Hunt",
                "score": 0,
                "comments": 0,
                "description": (summary or "")[:200].strip(),
                "published_at": published.isoformat() if published else "",
                "content_type": "tool",
                "engagement": 0,
            }
            items.append(item)

    except Exception as e:
        print(f"  ⚠ Product Hunt RSS failed: {e}")

    return items


def _fetch_from_homepage():
    """Scrape Product Hunt homepage for AI products."""
    items = []
    try:
        headers = {"User-Agent": config.USER_AGENT}
        resp = requests.get(
            "https://www.producthunt.com/",
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        # Look for product cards — PH structure may change
        links = soup.find_all("a", href=True)
        seen_urls = set()

        for link in links:
            href = link.get("href", "")
            if "/posts/" not in href:
                continue

            full_url = f"https://www.producthunt.com{href}" if href.startswith("/") else href
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            title = link.get_text(strip=True)
            if not title or len(title) < 3:
                continue

            if not _is_ai_product(title):
                continue

            item = {
                "title": title,
                "url": full_url,
                "external_url": full_url,
                "source": "Product Hunt",
                "source_category": "Product Hunt",
                "score": 0,
                "comments": 0,
                "description": "",
                "published_at": datetime.now(timezone.utc).isoformat(),
                "content_type": "tool",
                "engagement": 0,
            }
            items.append(item)

    except Exception as e:
        print(f"  ⚠ Product Hunt homepage scraping failed: {e}")

    return items


def fetch():
    """Fetch trending AI products from Product Hunt."""
    items = _fetch_from_rss()

    # Fallback to homepage scraping if RSS yields few results
    if len(items) < 3:
        homepage_items = _fetch_from_homepage()
        # Merge, avoiding duplicates
        existing_urls = {i["url"] for i in items}
        for item in homepage_items:
            if item["url"] not in existing_urls:
                items.append(item)

    # Deduplicate by title similarity
    seen_titles = set()
    unique_items = []
    for item in items:
        title_key = item["title"].lower().strip()[:50]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_items.append(item)

    print(f"  ✓ Product Hunt: {len(unique_items)} AI products collected")
    return unique_items
