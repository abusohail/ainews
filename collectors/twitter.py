"""
Twitter/X Collector — Fetches AI tweets via RSS bridge services.
Uses Nitter instances as RSS bridges. Gracefully degrades if unavailable.
"""

import requests
import feedparser
from datetime import datetime, timezone, timedelta
import config


def _try_nitter_feed(account, instance):
    """Try to fetch tweets from a single Nitter instance."""
    try:
        feed_url = f"{instance}/{account}/rss"
        headers = {"User-Agent": config.USER_AGENT}
        resp = requests.get(feed_url, headers=headers, timeout=config.REQUEST_TIMEOUT)

        if resp.status_code != 200:
            return None

        feed = feedparser.parse(resp.text)
        if not feed.entries:
            return None

        return feed
    except Exception:
        return None


def fetch():
    """Fetch recent AI tweets from configured accounts via Nitter RSS."""
    all_items = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    for account in config.TWITTER_ACCOUNTS:
        feed = None

        # Try each Nitter instance until one works
        for instance in config.NITTER_INSTANCES:
            feed = _try_nitter_feed(account, instance)
            if feed:
                break

        if not feed:
            continue

        for entry in feed.entries[:5]:  # Last 5 tweets per account
            title = entry.get("title", "")
            if not title:
                continue

            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if published and published < cutoff:
                continue

            # Clean up tweet text
            description = title[:280]

            item = {
                "title": f"@{account}: {description[:100]}...",
                "url": entry.get("link", ""),
                "external_url": entry.get("link", ""),
                "source": f"@{account}",
                "source_category": "Twitter/X",
                "score": 0,
                "comments": 0,
                "description": description,
                "published_at": published.isoformat() if published else "",
                "content_type": "article",
                "engagement": 0,
            }
            all_items.append(item)

    if all_items:
        print(f"  ✓ Twitter/X: {len(all_items)} tweets collected")
    else:
        print("  ⚠ Twitter/X: No tweets collected (Nitter bridges may be down)")

    return all_items
