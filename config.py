"""
Configuration for AI News Digest Automation.
All tunable settings live here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── Email ────────────────────────────────────────────────────────────────────
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "abusohail783@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
EMAIL_RECIPIENT = "abusohail783@gmail.com"
EMAIL_SUBJECT_PREFIX = "🤖 AI Daily Digest"

# ─── Timezone ─────────────────────────────────────────────────────────────────
TIMEZONE = "Asia/Karachi"

# ─── Reddit ───────────────────────────────────────────────────────────────────
REDDIT_SUBREDDITS = [
    "artificial",
    "MachineLearning",
    "ChatGPT",
    "LocalLLaMA",
    "singularity",
    "OpenAI",
    "StableDiffusion",
    "ArtificialIntelligence",
    "nocode",
    "SaaS",
    "startup",
    "startups",
    "Entrepreneur",
    "AItools",
    "automation",
]
REDDIT_MIN_SCORE = 50  # Minimum upvotes to qualify

# ─── Hacker News ──────────────────────────────────────────────────────────────
HN_AI_KEYWORDS = [
    # Core AI
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "gpt", "openai", "anthropic", "claude", "gemini", "mistral",
    "transformer", "neural network", "chatbot", "copilot", "diffusion",
    "stable diffusion", "midjourney", "dall-e", "sora",
    "agent", "rag", "fine-tuning", "fine tuning", "lora", "hugging face",
    "langchain", "vector database", "embedding", "nlp", "computer vision",
    "generative ai", "gen ai",
    # No-code & Automation
    "no-code", "nocode", "low-code", "automation", "automate", "workflow",
    "zapier", "make.com", "n8n", "ai tool", "ai app",
    # Startups & Business
    "startup", "saas", "launch", "founder", "venture", "funding",
    "business", "entrepreneur", "product", "side project",
    "monetize", "revenue", "bootstrapped", "yc", "y combinator",
    # Ideas & Tools
    "ai idea", "use case", "prompt", "ai workflow", "ai agent",
    "cursor", "bolt", "lovable", "replit", "v0",
]
HN_MIN_SCORE = 30  # Minimum HN points to qualify

# ─── Product Hunt ─────────────────────────────────────────────────────────────
PH_AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "gpt", "llm",
    "automation", "automate", "chatbot", "no-code", "nocode", "low-code",
    "copilot", "agent", "workflow", "generative", "neural", "deep learning",
    "startup", "saas", "productivity", "tool", "builder",
]
PH_MIN_VOTES = 20

# ─── YouTube Channels (RSS) ──────────────────────────────────────────────────
# Format: (channel_name, channel_id)
YOUTUBE_CHANNELS = [
    ("Matt Wolfe", "UCJMUBx-bTIRqIIrjkbHGl0A"),
    ("AI Explained", "UCNJ1Ymd5yFuUPtn21xtRbbw"),
    ("Two Minute Papers", "UCbfYPyITQ-7l4upoX8nvctg"),
    ("Fireship", "UCsBjURrPoezykLs9EqgamOA"),
    ("The AI Advantage", "UCjq4FLKoNkmezyBPaqNOGew"),
    ("AI Jason", "UCrMPMOHBep3ZqXAE0VHPttg"),
    ("WorldofAI", "UCW3rlGUQrKvRsGFSHcFchVw"),
    ("Matthew Berman", "UCRI0sn7u0mq1WLDi7gQN2Xg"),
    ("Wes Roth", "UCaGSqN3YxMqd_-uu4UG4YKg"),
    ("AI Advantage", "UCjq4FLKoNkmezyBPaqNOGew"),
]

# ─── News RSS Feeds ───────────────────────────────────────────────────────────
NEWS_RSS_FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("Ars Technica AI", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
    ("Analytics India Mag", "https://analyticsindiamag.com/feed/"),
]

# ─── Twitter / X (RSS bridges) ───────────────────────────────────────────────
# Nitter instances for RSS (may change; will fallback gracefully)
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
]
TWITTER_ACCOUNTS = [
    "elaborateplease",  # AI news
    "TheAIGRID",
    "ai_for_success",
    "NicolaCrawford",
    "rowaborat",
]

# ─── Ranking ──────────────────────────────────────────────────────────────────
MAX_ITEMS_PER_SOURCE = 10  # Max items to include per source
MAX_TOTAL_ITEMS = 30       # Max total items in the digest

# ─── Request Settings ─────────────────────────────────────────────────────────
REQUEST_TIMEOUT = 15  # seconds
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
