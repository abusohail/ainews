"""
Email Builder — Beautiful HTML email with viral content prompts.
Sections: Aaj Ke, Fruits Special, Video Series, Hafte Ke, Maheene Ke.
Dark theme, mobile-friendly.
"""

from datetime import datetime, timezone, timedelta


def _render_prompt_card(prompt):
    """Render a single prompt card."""
    category = prompt.get("category", "")
    subject = prompt.get("subject", "")
    angle = prompt.get("angle", "")
    image_prompt = prompt.get("image_prompt", "")
    veo3_prompt = prompt.get("veo3_prompt", "")

    cat_colors = {
        "Talking Fruits & Vegetables": "#4CAF50",
        "Health & Wellness": "#2196F3",
        "Fayde aur Nuqsanat": "#FF9800",
        "Kitchen & Cooking Tips": "#E91E63",
        "Satisfying Food Videos": "#9C27B0",
    }
    color = cat_colors.get(category, "#666")

    return f"""
    <div style="background:#1E1E2E;border-radius:12px;padding:16px;margin-bottom:14px;border-left:4px solid {color};">
        <div style="margin-bottom:6px;">
            <span style="background:{color};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;">{category}</span>
            <span style="color:#888;font-size:13px;margin-left:8px;">Subject: <strong style="color:#E0E0FF;">{subject}</strong></span>
        </div>
        <p style="color:#A0A0B0;font-size:12px;margin:4px 0 10px;font-style:italic;">💡 {angle}</p>

        <div style="background:#15151F;border-radius:8px;padding:12px;margin-bottom:8px;">
            <p style="color:#4CAF50;font-size:10px;font-weight:700;margin:0 0 5px;text-transform:uppercase;letter-spacing:1px;">🖼️ IMAGE PROMPT</p>
            <p style="color:#D0D0E0;font-size:12px;line-height:1.5;margin:0;">{image_prompt}</p>
        </div>

        <div style="background:#15151F;border-radius:8px;padding:12px;">
            <p style="color:#FF5722;font-size:10px;font-weight:700;margin:0 0 5px;text-transform:uppercase;letter-spacing:1px;">🎬 VEO3 VIDEO PROMPT</p>
            <p style="color:#D0D0E0;font-size:12px;line-height:1.5;margin:0;">{veo3_prompt}</p>
        </div>
    </div>
    """


def _render_section(title, emoji, prompts):
    """Render a section of prompt cards."""
    if not prompts:
        return ""
    cards = "".join(_render_prompt_card(p) for p in prompts)
    return f"""
    <div style="margin-bottom:28px;">
        <h2 style="color:#E0E0FF;font-size:18px;font-weight:700;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #2A2A3A;">
            {emoji} {title}
        </h2>
        {cards}
    </div>
    """


def _render_video_series(series):
    """Render the connected video series section."""
    if not series:
        return ""

    title = series.get("title", "Video Series")
    subject = series.get("subject", "")
    category = series.get("category", "")
    image_prompt = series.get("image_prompt", "")
    clips = series.get("clips", [])
    duration = series.get("total_duration", "")

    # Render each clip
    clips_html = ""
    for i, clip in enumerate(clips):
        clip_title = clip.get("clip_title", f"Part {i+1}")
        veo3_prompt = clip.get("veo3_prompt", "")
        clip_num = i + 1
        clips_html += f"""
        <div style="background:#15151F;border-radius:8px;padding:12px;margin-bottom:8px;border-left:3px solid #FF5722;">
            <p style="color:#FF5722;font-size:11px;font-weight:700;margin:0 0 5px;">
                🎬 Clip {clip_num} — {clip_title} (8 sec)
            </p>
            <p style="color:#D0D0E0;font-size:12px;line-height:1.5;margin:0;">{veo3_prompt}</p>
        </div>
        """

    return f"""
    <div style="margin-bottom:28px;">
        <h2 style="color:#E0E0FF;font-size:18px;font-weight:700;margin:0 0 8px;padding-bottom:8px;border-bottom:2px solid #2A2A3A;">
            🎥 Video Series — Combine Karein!
        </h2>
        <p style="color:#888;font-size:12px;margin:0 0 14px;">
            Neeche ke {len(clips)} clips Veo3 se bana ke combine karo = ek lambi video ({duration})
        </p>

        <div style="background:#1E1E2E;border-radius:12px;padding:16px;margin-bottom:14px;border-left:4px solid #FF5722;">
            <h3 style="color:#E0E0FF;font-size:16px;margin:0 0 8px;font-weight:700;">
                📽️ {title}
            </h3>
            <p style="color:#888;font-size:12px;margin:0 0 12px;">
                Category: {category} · Subject: <strong style="color:#E0E0FF;">{subject}</strong> · {duration}
            </p>

            <div style="background:#15151F;border-radius:8px;padding:12px;margin-bottom:10px;">
                <p style="color:#4CAF50;font-size:10px;font-weight:700;margin:0 0 5px;text-transform:uppercase;letter-spacing:1px;">🖼️ THUMBNAIL IMAGE PROMPT</p>
                <p style="color:#D0D0E0;font-size:12px;line-height:1.5;margin:0;">{image_prompt}</p>
            </div>

            {clips_html}

            <div style="background:#2A1A1A;border-radius:8px;padding:10px;margin-top:8px;">
                <p style="color:#FF9800;font-size:11px;margin:0;text-align:center;">
                    ⚡ Tip: Har clip Veo3 se banao → phir CapCut/CapCut ya kisi editor mein combine karo = viral video ready!
                </p>
            </div>
        </div>
    </div>
    """


def build_email(prompts_data):
    """Build the complete HTML email."""
    tz = timezone(timedelta(hours=5))
    today = datetime.now(tz).strftime("%A, %B %d, %Y")

    daily = prompts_data.get("daily", [])
    fruits = prompts_data.get("fruits", [])
    series = prompts_data.get("series", {})
    weekly = prompts_data.get("weekly", [])
    monthly = prompts_data.get("monthly", [])

    total = len(daily) + len(fruits) + len(weekly) + len(monthly)
    series_clips = len(series.get("clips", [])) if series else 0

    sections = ""
    sections += _render_section("Aaj Ke Viral Prompts", "🔥", daily)
    sections += _render_section("Fruits & Vegetables Special", "🥑", fruits)
    sections += _render_video_series(series)
    sections += _render_section("Is Hafte Ke Viral Prompts", "📅", weekly)
    sections += _render_section("Is Maheene Ke Viral Prompts", "📆", monthly)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#0D0D1A;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,sans-serif;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">

        <div style="text-align:center;padding:30px 20px;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);border-radius:16px;margin-bottom:24px;">
            <h1 style="color:#E0E0FF;font-size:26px;margin:0 0 8px;font-weight:800;">
                🎬 Viral Content Prompts
            </h1>
            <p style="color:#8888AA;font-size:13px;margin:0;">
                {today} · {total} prompts + {series_clips}-clip video series
            </p>
            <p style="color:#666;font-size:11px;margin:6px 0 0;">
                Image + Veo3 prompts — copy-paste karein aur viral ho jayen! 🚀
            </p>
        </div>

        {sections}

        <div style="text-align:center;padding:20px;color:#555;font-size:11px;border-top:1px solid #1A1A2A;margin-top:16px;">
            <p style="margin:0;">Your AI Automation 🤖 · Roz subah 10 baje fresh prompts!</p>
        </div>

    </div>
</body>
</html>
    """

    return html
