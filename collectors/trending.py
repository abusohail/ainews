"""
Trending Topics Collector — Scrapes Google Trends, Reddit, and curated viral
categories to find what's hot today. Used to generate image + Veo3 prompts.
"""

import requests
import feedparser
import random
from datetime import datetime, timezone, timedelta
import config


# ─── Curated Viral Content Categories ────────────────────────────────────────
# These are proven viral formats that consistently perform on TikTok/Reels/Shorts.
# The system rotates through them daily and combines with trending topics.

VIRAL_CATEGORIES = [
    {
        "category": "Talking Fruits & Vegetables",
        "description": "Animated fruits/vegetables with faces giving health advice or roasting bad habits",
        "subjects": [
            "apple", "banana", "avocado", "strawberry", "blueberry", "mango",
            "watermelon", "lemon", "orange", "carrot", "broccoli", "spinach",
            "garlic", "ginger", "turmeric", "pomegranate", "kiwi", "pineapple",
            "tomato", "sweet potato", "beet", "cucumber", "celery",
        ],
        "angles": [
            "explaining its health benefits to skeptical humans",
            "roasting people for eating junk food instead",
            "having a debate with another fruit about who's healthier",
            "giving a motivational speech about nutrition",
            "reacting to someone throwing it away uneaten",
            "interviewing other produce in the fridge",
            "complaining about being left in the fridge too long",
            "trying to convince a kid to eat vegetables",
            "explaining why it's a superfood",
            "doing a cooking show teaching a simple recipe",
        ],
    },
    {
        "category": "Health & Wellness Tips",
        "description": "Quick health tips visualized with stunning imagery",
        "subjects": [
            "morning routine", "gut health", "sleep optimization", "hydration",
            "stress relief", "immune system", "anti-aging foods", "brain health",
            "energy boost", "detox", "weight loss", "muscle recovery",
            "meditation", "cold therapy", "intermittent fasting",
        ],
        "angles": [
            "a doctor explaining the science in simple terms",
            "before and after transformation visualization",
            "a day-in-the-life showing the healthy habit",
            "mythbusting common misconceptions",
            "comparing two approaches side by side",
        ],
    },
    {
        "category": "Talking Everyday Objects",
        "description": "Household objects come alive and share opinions or facts",
        "subjects": [
            "coffee mug", "alarm clock", "toothbrush", "running shoes",
            "smartphone", "water bottle", "pillow", "mirror", "fridge",
            "vitamin bottle", "blender", "yoga mat", "book", "candle",
        ],
        "angles": [
            "complaining about how it's being used wrong",
            "giving life advice based on its perspective",
            "having an argument with another object",
            "telling its origin story dramatically",
            "reviewing its owner's daily habits",
        ],
    },
    {
        "category": "Animals Explaining Science",
        "description": "Cute animals narrating scientific or health facts",
        "subjects": [
            "wise owl", "curious cat", "golden retriever", "baby elephant",
            "penguin", "dolphin", "fox", "rabbit", "parrot", "turtle",
        ],
        "angles": [
            "teaching a fun science fact as a professor",
            "explaining why humans do weird things",
            "giving a TED talk to other animals",
            "narrating a nature documentary about itself",
            "reacting to human food and explaining nutrition",
        ],
    },
    {
        "category": "AI & Future Tech Visualizations",
        "description": "Stunning visuals of futuristic AI and tech concepts",
        "subjects": [
            "AI robot assistant", "smart home of 2030", "AI doctor",
            "self-driving city", "human-AI collaboration", "neural interface",
            "holographic display", "drone delivery", "AI art studio",
            "robot chef", "AI teacher", "space colonization",
        ],
        "angles": [
            "a day in the life in the year 2030",
            "comparing today vs the AI-powered future",
            "a futuristic product advertisement",
            "explaining how the technology works simply",
            "showing the transformation from current to future",
        ],
    },
    {
        "category": "Motivational & Startup Stories",
        "description": "Inspirational entrepreneurship and startup content",
        "subjects": [
            "solo founder journey", "garage to millions", "rejected pitch to success",
            "side hustle to full-time", "AI startup idea", "no-code app launch",
            "first customer moment", "pivoting the business", "bootstrapped success",
        ],
        "angles": [
            "dramatic cinematic storytelling of the journey",
            "a founder narrating their darkest moment before success",
            "split screen showing the struggle vs the reward",
            "a time-lapse of building the business",
            "someone quitting their 9-5 to pursue their dream",
        ],
    },
    {
        "category": "Satisfying Process Videos",
        "description": "Oddly satisfying creation and transformation processes",
        "subjects": [
            "cooking a perfect meal", "organizing a messy space", "painting art",
            "building something from scratch", "3D printing", "pottery making",
            "calligraphy", "cake decorating", "woodworking", "coding an app",
        ],
        "angles": [
            "close-up ASMR-style with satisfying sounds",
            "time-lapse from start to finish",
            "split screen of messy vs clean/finished",
            "zooming into the intricate details",
            "the final reveal moment",
        ],
    },
]


def _get_google_trends():
    """Fetch current trending topics from Google Trends RSS."""
    trending = []
    try:
        feed_url = "https://trends.google.com/trending/rss?geo=US"
        headers = {"User-Agent": config.USER_AGENT}
        resp = requests.get(feed_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()

        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:15]:
            title = entry.get("title", "").strip()
            if title:
                trending.append(title)
    except Exception as e:
        print(f"  ⚠ Google Trends failed: {e}")

    return trending


def _get_trending_health_topics():
    """Fetch health-related trending topics from Reddit."""
    topics = []
    try:
        subreddits = ["HealthyFood", "nutrition", "wellness", "Fitness"]
        headers = {"User-Agent": config.USER_AGENT}

        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=5"
            resp = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                for post in data.get("data", {}).get("children", []):
                    title = post.get("data", {}).get("title", "")
                    if title:
                        topics.append(title)

            import time
            time.sleep(1)

    except Exception as e:
        print(f"  ⚠ Reddit health trends failed: {e}")

    return topics


def get_daily_topics():
    """
    Get today's trending topics and viral content ideas.
    Combines Google Trends, Reddit health topics, and curated categories.
    """
    # Fetch live trending data
    google_trends = _get_google_trends()
    health_topics = _get_trending_health_topics()

    # Use today's date as seed for consistent daily rotation
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    random.seed(today)

    # Pick 3-4 random categories for today
    daily_categories = random.sample(VIRAL_CATEGORIES, min(4, len(VIRAL_CATEGORIES)))

    result = {
        "google_trends": google_trends[:10],
        "health_topics": health_topics[:10],
        "daily_categories": daily_categories,
    }

    print(f"  ✓ Trending: {len(google_trends)} Google trends, {len(health_topics)} health topics")
    return result
