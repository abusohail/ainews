"""
YouTube Collector — Fetches recent AI videos from popular channels.
Uses YouTube's public RSS feeds (no API key needed).
"""

import requests
import feedparser
from datetime import datetime, timezone, timedelta
import config


def _parse_youtube_rss(channel_name, channel_id):
    """Fetch recent videos from a YouTube channel's RSS feed."""
    items = []
    try:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        headers = {"User-Agent": config.USER_AGENT}
        resp = requests.get(feed_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()

        feed = feedparser.parse(resp.text)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)  # Strict 24h window

        for entry in feed.entries[:10]:  # Last 10 videos per channel
            title = entry.get("title", "")

            # Parse published date
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if published and published < cutoff:
                continue

            # Get video URL and thumbnail
            video_url = entry.get("link", "")

            # Get view count from media stats if available
            views = 0
            if hasattr(entry, "media_statistics"):
                views = int(entry.media_statistics.get("views", 0))

            description = ""
            if hasattr(entry, "media_group") and hasattr(entry.media_group, "media_description"):
                description = str(entry.media_group.media_description)[:200]
            elif hasattr(entry, "summary"):
                description = (entry.get("summary", "") or "")[:200]

            item = {
                "title": title,
                "url": video_url,
                "external_url": video_url,
                "source": channel_name,
                "source_category": "YouTube",
                "score": views,
                "comments": 0,
                "description": description.strip(),
                "published_at": published.isoformat() if published else "",
                "content_type": "video",
                "engagement": views,
            }
            items.append(item)

    except Exception as e:
        print(f"  ⚠ YouTube {channel_name} failed: {e}")

    return items


def fetch():
    """Fetch recent AI videos from all configured YouTube channels."""
    all_items = []

    for channel_name, channel_id in config.YOUTUBE_CHANNELS:
        videos = _parse_youtube_rss(channel_name, channel_id)
        all_items.extend(videos)

    print(f"  ✓ YouTube: {len(all_items)} videos collected")
    return all_items
