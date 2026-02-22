"""
AI News Digest — Main Orchestrator

Runs all collectors, ranks content, builds email, and sends the daily digest.
Designed to be run via cron at 10:00 AM PKT daily.

Usage:
    python main.py           # Full run: collect → rank → email
    python main.py --dry-run # Collect and rank, but don't send email (prints to console)
    python main.py --test    # Send a test email with sample data
"""

import sys
import time
from datetime import datetime, timezone, timedelta

from collectors import reddit, hackernews, producthunt, youtube, twitter, news_rss
from collectors.trending import get_daily_topics
from ranker import rank_and_filter, group_by_type
from prompt_generator import generate_prompts
from email_builder import build_email
from email_sender import send_email


def collect_all():
    """Run all collectors and return combined results."""
    all_items = []

    collectors = [
        ("Reddit", reddit.fetch),
        ("Hacker News", hackernews.fetch),
        ("Product Hunt", producthunt.fetch),
        ("YouTube", youtube.fetch),
        ("Twitter/X", twitter.fetch),
        ("News RSS", news_rss.fetch),
    ]

    for name, fetch_fn in collectors:
        try:
            items = fetch_fn()
            all_items.extend(items)
        except Exception as e:
            print(f"  ✗ {name} collector crashed: {e}")
            continue

    return all_items


def run(dry_run=False):
    """Main pipeline: collect → rank → build email → send."""

    tz = timezone(timedelta(hours=5))
    now = datetime.now(tz)
    print(f"\n{'='*60}")
    print(f"  🤖 AI Daily Digest — {now.strftime('%A, %B %d, %Y %I:%M %p PKT')}")
    print(f"{'='*60}\n")

    # Step 1: Collect
    print("📡 Collecting from all sources...")
    start = time.time()
    all_items = collect_all()
    elapsed = time.time() - start
    print(f"\n  📊 Total collected: {len(all_items)} items in {elapsed:.1f}s\n")

    if not all_items:
        print("  ⚠ No items collected from any source. Skipping email.")
        return

    # Step 2: Rank & Filter
    print("🏆 Ranking and filtering outperforming content...")
    top_items = rank_and_filter(all_items)
    print(f"  📊 After ranking: {len(top_items)} outperforming items\n")

    # Step 3: Group by type
    grouped = group_by_type(top_items)
    for category, items in grouped.items():
        if items:
            label = category.replace("_", " ").title()
            print(f"  • {label}: {len(items)} items")
    print()

    # Step 4: Get trending topics & generate prompts
    print("🎬 Generating viral content prompts...")
    try:
        trending_data = get_daily_topics()
        prompts = generate_prompts(trending_data)
    except Exception as e:
        print(f"  ⚠ Prompt generation failed: {e}")
        prompts = []
    print()

    # Step 5: Build email
    print("📧 Building email digest...")
    html = build_email(grouped, len(all_items), prompts=prompts)

    if dry_run:
        print("\n🔍 DRY RUN — Email would contain:\n")
        for category, items in grouped.items():
            if not items:
                continue
            label = category.replace("_", " ").title()
            print(f"  ── {label} ──")
            for item in items:
                score = item.get("score", 0)
                source = item.get("source", "")
                print(f"  [{source}] {item['title']}")
                if score:
                    print(f"         Score: {score:,}")
                print()
        if prompts:
            print("\n  ── Viral Content Prompts ──")
            for p in prompts:
                print(f"  [{p['category']}] {p['subject']}")
                print(f"         Image: {p['image_prompt'][:80]}...")
                print(f"         Veo3:  {p['veo3_prompt'][:80]}...")
                print()
        print("  ✓ Dry run complete. No email sent.")
        return

    # Step 6: Send email
    print("📮 Sending email...")
    success = send_email(html)

    if success:
        print(f"\n{'='*60}")
        print(f"  ✅ Digest sent successfully!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f"  ❌ Failed to send digest. Check errors above.")
        print(f"{'='*60}\n")
        sys.exit(1)


def send_test():
    """Send a test email with sample content to verify setup."""
    print("\n📧 Sending test email...")

    test_items = {
        "top_stories": [
            {
                "title": "OpenAI releases GPT-5 with groundbreaking reasoning",
                "url": "https://example.com/gpt5",
                "source": "r/artificial",
                "source_category": "Reddit",
                "score": 5420,
                "comments": 1243,
                "description": "OpenAI has announced the release of GPT-5, featuring improved reasoning capabilities...",
                "content_type": "article",
                "engagement": 7906,
            },
            {
                "title": "Show HN: I built an open-source AI coding assistant",
                "url": "https://news.ycombinator.com/item?id=12345",
                "source": "Hacker News",
                "source_category": "Hacker News",
                "score": 342,
                "comments": 89,
                "description": "342 points · 89 comments",
                "content_type": "article",
                "engagement": 520,
            },
        ],
        "videos": [
            {
                "title": "The AI Tool That Changes Everything (2025)",
                "url": "https://youtube.com/watch?v=test123",
                "source": "Matt Wolfe",
                "source_category": "YouTube",
                "score": 150000,
                "comments": 0,
                "description": "In this video, we explore the latest AI tool that's changing the game...",
                "content_type": "video",
                "engagement": 150000,
            },
        ],
        "tools": [
            {
                "title": "AutomateAI — No-code AI workflow builder",
                "url": "https://producthunt.com/posts/automateai",
                "source": "Product Hunt",
                "source_category": "Product Hunt",
                "score": 287,
                "comments": 0,
                "description": "Build AI automations without writing code. Connect APIs, models, and data sources.",
                "content_type": "tool",
                "engagement": 287,
            },
        ],
        "news": [
            {
                "title": "Google DeepMind achieves new breakthrough in protein folding",
                "url": "https://techcrunch.com/test",
                "source": "TechCrunch AI",
                "source_category": "News",
                "score": 0,
                "comments": 0,
                "description": "Researchers at Google DeepMind have announced significant improvements to AlphaFold...",
                "content_type": "article",
                "engagement": 0,
            },
        ],
    }

    test_prompts = [
        {
            "category": "Talking Fruits & Vegetables",
            "subject": "avocado",
            "angle": "roasting people for eating junk food instead",
            "image_prompt": "A giant avocado with a sassy expression and raised eyebrow, sitting next to junk food it disapproves of, 3D Pixar-style render, vibrant colors, soft lighting, cute character design",
            "veo3_prompt": 'Medium shot of an avocado character with cartoon eyes and a mouth, standing on a kitchen counter next to a plate of junk food. The avocado gestures dramatically and says in a sassy tone: "Yes, I\'m expensive. But have you seen your hospital bills? I\'m the cheaper option." Camera at eye level, slight handheld movement. Bright kitchen lighting. Audio: comedic background music, expressive voice. (no subtitles)',
            "trending_hook": "Trending tie-in: Connect this to 'Healthy Eating Week' for extra reach",
        },
        {
            "category": "AI & Future Tech Visualizations",
            "subject": "AI robot assistant",
            "angle": "a day in the life in the year 2030",
            "image_prompt": "Futuristic scene of AI robot assistant, glowing holographic interfaces, neon blue and purple lighting, cyberpunk aesthetic, cinematic film still, shallow depth of field, warm golden hour lighting",
            "veo3_prompt": 'Sweeping aerial shot descending into a futuristic city scene showing AI robot assistant. Holographic interfaces glow in neon blue and purple. A narrator says in an awe-inspired voice: "Welcome to the year 2030. This is what your daily life looks like now." Dramatic cinematic lighting. Audio: epic orchestral music, deep narrator voice. (no subtitles)',
            "trending_hook": "",
        },
    ]

    html = build_email(test_items, 42, prompts=test_prompts)
    success = send_email(html)

    if success:
        print("  ✅ Test email sent! Check your inbox.")
    else:
        print("  ❌ Test email failed. Fix the issues above and try again.")


if __name__ == "__main__":
    if "--dry-run" in sys.argv:
        run(dry_run=True)
    elif "--test" in sys.argv:
        send_test()
    else:
        run()
