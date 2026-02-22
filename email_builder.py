"""
Email Builder — Generates a beautiful, mobile-friendly HTML email
with viral content prompts organized by: Today, This Week, This Month.
Dark theme with modern design.
"""

from datetime import datetime, timezone, timedelta


def _render_prompt_card(prompt):
    """Render a single prompt set as a styled email card."""
    category = prompt.get("category", "")
    subject = prompt.get("subject", "")
    angle = prompt.get("angle", "")
    image_prompt = prompt.get("image_prompt", "")
    veo3_prompt = prompt.get("veo3_prompt", "")

    cat_colors = {
        "Talking Fruits & Vegetables": "#4CAF50",
        "Health & Wellness Tips": "#2196F3",
        "Talking Everyday Objects": "#FF9800",
        "Animals Explaining Science": "#9C27B0",
        "AI & Future Tech Visualizations": "#00BCD4",
        "Motivational & Startup Stories": "#F44336",
        "Satisfying Process Videos": "#E91E63",
    }
    color = cat_colors.get(category, "#666")

    return f"""
    <div style="background:#1E1E2E;border-radius:12px;padding:16px;margin-bottom:16px;border-left:4px solid {color};">
        <div style="margin-bottom:8px;">
            <span style="background:{color};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;">{category}</span>
            <span style="color:#888;font-size:13px;margin-left:8px;">Subject: <strong style="color:#E0E0FF;">{subject}</strong></span>
        </div>
        <p style="color:#A0A0B0;font-size:12px;margin:4px 0 12px;font-style:italic;">💡 {angle}</p>

        <div style="background:#15151F;border-radius:8px;padding:12px;margin-bottom:10px;">
            <p style="color:#4CAF50;font-size:11px;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:1px;">🖼️ Image Prompt (Midjourney / DALL-E / Flux)</p>
            <p style="color:#D0D0E0;font-size:13px;line-height:1.5;margin:0;">{image_prompt}</p>
        </div>

        <div style="background:#15151F;border-radius:8px;padding:12px;">
            <p style="color:#FF5722;font-size:11px;font-weight:700;margin:0 0 6px;text-transform:uppercase;letter-spacing:1px;">🎬 Veo3 Video Prompt</p>
            <p style="color:#D0D0E0;font-size:13px;line-height:1.5;margin:0;">{veo3_prompt}</p>
        </div>
    </div>
    """


def _render_section(title, emoji, prompts):
    """Render a time-based section of prompts."""
    if not prompts:
        return ""

    cards = "".join(_render_prompt_card(p) for p in prompts)

    return f"""
    <div style="margin-bottom:32px;">
        <h2 style="color:#E0E0FF;font-size:20px;font-weight:700;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #2A2A3A;">
            {emoji} {title}
        </h2>
        {cards}
    </div>
    """


def build_email(prompts_data):
    """
    Build the complete HTML email from prompts data.
    prompts_data has keys: daily, weekly, monthly — each with 5 prompt dicts.
    """
    tz = timezone(timedelta(hours=5))  # PKT
    today = datetime.now(tz).strftime("%A, %B %d, %Y")

    daily = prompts_data.get("daily", [])
    weekly = prompts_data.get("weekly", [])
    monthly = prompts_data.get("monthly", [])

    total = len(daily) + len(weekly) + len(monthly)

    # Build sections
    sections = ""
    sections += _render_section("Aaj Ke Viral Prompts", "🔥", daily)
    sections += _render_section("Is Hafte Ke Viral Prompts", "📅", weekly)
    sections += _render_section("Is Maheene Ke Viral Prompts", "📆", monthly)

    if not sections.strip():
        sections = """
        <div style="text-align:center;padding:40px;color:#888;">
            <p style="font-size:18px;">😴 Aaj ke liye prompts nahi ban sake</p>
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
                🎬 Viral Content Prompts
            </h1>
            <p style="color:#8888AA;font-size:14px;margin:0;">
                {today} · {total} ready-to-use prompts (Image + Veo3)
            </p>
            <p style="color:#666;font-size:12px;margin:8px 0 0;">
                Copy-paste karein aur viral content banayein! 🚀
            </p>
        </div>

        <!-- Sections -->
        {sections}

        <!-- Footer -->
        <div style="text-align:center;padding:24px;color:#555;font-size:12px;border-top:1px solid #1A1A2A;margin-top:20px;">
            <p style="margin:0;">
                Curated by your AI Automation 🤖<br>
                Roz subah 10 baje — fresh viral prompts!
            </p>
        </div>

    </div>
</body>
</html>
    """

    return html
