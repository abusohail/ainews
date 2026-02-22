"""
Email Builder — Generates a beautiful, mobile-friendly HTML email digest.
Dark theme with modern design, organized by content type.
"""

from datetime import datetime, timezone, timedelta


def _format_score(item):
    """Format engagement score as a readable badge."""
    score = item.get("score", 0)
    source = item.get("source_category", "")

    if source == "Reddit":
        comments = item.get("comments", 0)
        return f"⬆ {score:,} · 💬 {comments:,}"
    elif source == "Hacker News":
        comments = item.get("comments", 0)
        return f"▲ {score:,} · 💬 {comments:,}"
    elif source == "YouTube":
        if score > 0:
            if score >= 1_000_000:
                return f"👁 {score / 1_000_000:.1f}M views"
            elif score >= 1_000:
                return f"👁 {score / 1_000:.1f}K views"
            return f"👁 {score:,} views"
        return "📺 New"
    elif source == "Product Hunt":
        if score > 0:
            return f"⬆ {score:,} upvotes"
        return "🚀 New launch"
    else:
        return f"📰 {source}"


def _source_badge(source_category):
    """Get a colored badge for each source."""
    badges = {
        "Reddit": ("#FF4500", "Reddit"),
        "Hacker News": ("#FF6600", "HN"),
        "Product Hunt": ("#DA552F", "PH"),
        "YouTube": ("#FF0000", "YouTube"),
        "Twitter/X": ("#1DA1F2", "Twitter"),
        "News": ("#4A90D9", "News"),
    }
    color, label = badges.get(source_category, ("#888888", source_category))
    return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600;letter-spacing:0.5px;">{label}</span>'


def _render_item(item):
    """Render a single news item as an HTML card."""
    title = item.get("title", "Untitled")
    url = item.get("url", "#")
    source = item.get("source", "")
    source_category = item.get("source_category", "")
    description = item.get("description", "")
    score_text = _format_score(item)

    desc_html = ""
    if description:
        desc_html = f'<p style="margin:6px 0 0;color:#A0A0B0;font-size:13px;line-height:1.4;">{description}</p>'

    return f"""
    <div style="background:#1E1E2E;border-radius:12px;padding:16px;margin-bottom:12px;border:1px solid #2A2A3A;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
            {_source_badge(source_category)}
            <span style="color:#666;font-size:12px;">{source}</span>
        </div>
        <a href="{url}" style="color:#E0E0FF;text-decoration:none;font-size:15px;font-weight:600;line-height:1.3;display:block;">
            {title}
        </a>
        {desc_html}
        <div style="margin-top:8px;color:#888;font-size:12px;">
            {score_text}
        </div>
    </div>
    """


def _render_section(title, emoji, items):
    """Render a section of items."""
    if not items:
        return ""

    items_html = "".join(_render_item(item) for item in items)

    return f"""
    <div style="margin-bottom:32px;">
        <h2 style="color:#E0E0FF;font-size:20px;font-weight:700;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #2A2A3A;">
            {emoji} {title}
        </h2>
        {items_html}
    </div>
    """


def build_email(grouped_items, total_collected):
    """Build the complete HTML email from grouped items."""
    # Count items
    total_shown = sum(len(items) for items in grouped_items.values())

    # Get today's date
    tz = timezone(timedelta(hours=5))  # PKT
    today = datetime.now(tz).strftime("%A, %B %d, %Y")

    # Build sections
    sections = ""
    sections += _render_section("Top Stories", "🔥", grouped_items.get("top_stories", []))
    sections += _render_section("Trending Videos", "📺", grouped_items.get("videos", []))
    sections += _render_section("New AI Tools", "🚀", grouped_items.get("tools", []))
    sections += _render_section("News Roundup", "📰", grouped_items.get("news", []))

    # If nothing collected
    if not sections.strip():
        sections = """
        <div style="text-align:center;padding:40px;color:#888;">
            <p style="font-size:18px;">😴 Quiet day in AI land</p>
            <p>No outperforming content found in the last 24 hours.</p>
        </div>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#0D0D1A;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,sans-serif;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">

        <!-- Header -->
        <div style="text-align:center;padding:30px 20px;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);border-radius:16px;margin-bottom:24px;">
            <h1 style="color:#E0E0FF;font-size:28px;margin:0 0 8px;font-weight:800;">
                🤖 AI Daily Digest
            </h1>
            <p style="color:#8888AA;font-size:14px;margin:0;">
                {today} · {total_shown} outperforming items from {total_collected} scanned
            </p>
        </div>

        <!-- Content -->
        {sections}

        <!-- Footer -->
        <div style="text-align:center;padding:24px;color:#555;font-size:12px;border-top:1px solid #1A1A2A;margin-top:20px;">
            <p style="margin:0;">
                Curated by your AI News Automation 🤖<br>
                Sources: Reddit · Hacker News · Product Hunt · YouTube · Twitter · News RSS
            </p>
            <p style="margin:8px 0 0;color:#444;">
                Delivered daily at 10:00 AM PKT
            </p>
        </div>

    </div>
</body>
</html>
    """

    return html
