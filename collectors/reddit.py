"""
Reddit Collector — Fetches top AI posts from multiple subreddits.
Uses Reddit's public JSON API (no auth required for read-only access).
"""

import time
import requests
from datetime import datetime, timezone, timedelta
import config


def fetch():
    """Fetch top AI posts from configured subreddits in the last 24 hours."""
    all_items = []
    headers = {"User-Agent": config.USER_AGENT}

    for subreddit in config.REDDIT_SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=25"
            response = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            posts = data.get("data", {}).get("children", [])
            cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

            for post in posts:
                p = post.get("data", {})
                created = datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc)

                if created < cutoff:
                    continue

                score = p.get("score", 0)
                if score < config.REDDIT_MIN_SCORE:
                    continue

                # Determine content type
                content_type = "article"
                url_str = p.get("url", "")
                if "youtube.com" in url_str or "youtu.be" in url_str:
                    content_type = "video"

                item = {
                    "title": p.get("title", ""),
                    "url": f"https://www.reddit.com{p.get('permalink', '')}",
                    "external_url": url_str,
                    "source": f"r/{subreddit}",
                    "source_category": "Reddit",
                    "score": score,
                    "comments": p.get("num_comments", 0),
                    "description": (p.get("selftext", "") or "")[:200].strip(),
                    "published_at": created.isoformat(),
                    "content_type": content_type,
                    "engagement": score + p.get("num_comments", 0) * 2,
                }
                all_items.append(item)

            # Be respectful — wait between subreddit requests
            time.sleep(1)

        except Exception as e:
            print(f"  ⚠ Reddit r/{subreddit} failed: {e}")
            continue

    print(f"  ✓ Reddit: {len(all_items)} posts collected")
    return all_items
