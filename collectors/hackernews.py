"""
Hacker News Collector — Fetches top AI-related stories.
Uses the free HN API (https://github.com/HackerNews/API).
"""

import requests
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import config


def _is_ai_related(title):
    """Check if a story title is AI-related based on keywords."""
    title_lower = title.lower()
    return any(kw in title_lower for kw in config.HN_AI_KEYWORDS)


def _fetch_story(story_id):
    """Fetch a single HN story by ID."""
    try:
        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        resp = requests.get(url, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def fetch():
    """Fetch top AI-related stories from Hacker News in the last 24 hours."""
    all_items = []

    try:
        # Get top 200 story IDs
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        resp = requests.get(url, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        story_ids = resp.json()[:200]

        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

        # Fetch stories in parallel (max 10 threads)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(_fetch_story, sid): sid for sid in story_ids}

            for future in as_completed(futures):
                story = future.result()
                if not story or story.get("type") != "story":
                    continue

                title = story.get("title", "")
                if not _is_ai_related(title):
                    continue

                created = datetime.fromtimestamp(story.get("time", 0), tz=timezone.utc)
                if created < cutoff:
                    continue

                score = story.get("score", 0)
                if score < config.HN_MIN_SCORE:
                    continue

                story_url = story.get("url", "")
                hn_url = f"https://news.ycombinator.com/item?id={story.get('id')}"

                item = {
                    "title": title,
                    "url": story_url or hn_url,
                    "external_url": story_url,
                    "source": "Hacker News",
                    "source_category": "Hacker News",
                    "score": score,
                    "comments": story.get("descendants", 0),
                    "description": f"{score} points · {story.get('descendants', 0)} comments",
                    "published_at": created.isoformat(),
                    "content_type": "article",
                    "engagement": score + story.get("descendants", 0) * 2,
                }
                all_items.append(item)

    except Exception as e:
        print(f"  ⚠ Hacker News failed: {e}")

    print(f"  ✓ Hacker News: {len(all_items)} stories collected")
    return all_items
