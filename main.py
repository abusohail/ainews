"""
Viral Content Prompts — Main Orchestrator

Generates daily viral content prompts (image + Veo3 video) and sends
them via email. Designed to run via cron at 10:00 AM PKT daily.

Usage:
    python main.py           # Full run: generate prompts → email
    python main.py --dry-run # Generate prompts but don't send email
    python main.py --test    # Send a test email with sample prompts
"""

import sys
import time
from datetime import datetime, timezone, timedelta

from prompt_generator import generate_prompts
from email_builder import build_email
from email_sender import send_email


def run(dry_run=False):
    """Main pipeline: generate prompts → build email → send."""
    tz = timezone(timedelta(hours=5))
    now = datetime.now(tz)
    print(f"\n{'='*60}")
    print(f"  🎬 Viral Content Prompts — {now.strftime('%A, %B %d, %Y %I:%M %p PKT')}")
    print(f"{'='*60}\n")

    # Step 1: Generate prompts
    print("🎬 Generating viral content prompts...\n")
    start = time.time()

    try:
        prompts_data = generate_prompts()
    except Exception as e:
        print(f"  ✗ Prompt generation failed: {e}")
        return

    elapsed = time.time() - start
    total = sum(len(v) for v in prompts_data.values())
    print(f"\n  📊 Total: {total} prompts in {elapsed:.1f}s\n")

    # Step 2: Build email
    print("📧 Building email...")
    html = build_email(prompts_data)

    if dry_run:
        print("\n🔍 DRY RUN — Prompts generated:\n")
        for period, label in [("daily", "Aaj Ke"), ("weekly", "Is Hafte Ke"), ("monthly", "Is Maheene Ke")]:
            items = prompts_data.get(period, [])
            if items:
                print(f"  ── {label} Viral Prompts ({len(items)}) ──")
                for p in items:
                    print(f"  [{p['category']}] {p['subject']}")
                    print(f"      Angle: {p['angle']}")
                    print(f"      Image: {p['image_prompt'][:80]}...")
                    print(f"      Veo3:  {p['veo3_prompt'][:80]}...")
                    print()
        print("  ✓ Dry run complete. No email sent.")
        return

    # Step 3: Send email
    print("📮 Sending email...")
    success = send_email(html)

    if success:
        print(f"\n{'='*60}")
        print(f"  ✅ Prompts sent successfully!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f"  ❌ Failed to send. Check errors above.")
        print(f"{'='*60}\n")
        sys.exit(1)


def send_test():
    """Send a test email with sample prompts."""
    print("\n📧 Sending test email with sample prompts...")

    test_data = {
        "daily": [
            {
                "category": "Talking Fruits & Vegetables",
                "subject": "avocado",
                "angle": "junk food khaane walon ki class le raha hai",
                "image_prompt": "A giant avocado with a sassy expression and raised eyebrow, sitting next to junk food it disapproves of, 3D Pixar-style render, vibrant colors, soft lighting, cute character design",
                "veo3_prompt": 'Medium shot of an avocado character with cartoon eyes and a mouth, standing on a kitchen counter next to a plate of junk food. The avocado gestures dramatically and says in a sassy Urdu tone: "Haan bhai mehenga hoon. Lekin hospital ka bill dekha hai? Main sasta option hoon." Camera at eye level, slight handheld movement. Bright kitchen lighting. Audio: comedic background music, expressive Urdu voice. (no subtitles)',
            },
            {
                "category": "Animals Explaining Science",
                "subject": "samajhdar ullu",
                "angle": "professor ban ke science fact sikha raha hai",
                "image_prompt": "A wise owl wearing a tiny lab coat and round glasses, standing at a chalkboard with science diagrams, cinematic film still, shallow depth of field, warm golden hour lighting",
                "veo3_prompt": 'Medium shot of a wise owl sitting at a tiny desk in a library setting, wearing miniature round glasses. It looks up from a book at the camera and says in a professorial Urdu tone: "Aaj ka fun fact — aur yeh waaqi mein dimagh hila dega tumhara!" Warm library lighting, bookshelves in background. Camera slowly zooms in. Audio: gentle classical music, scholarly Urdu voice. (no subtitles)',
            },
            {
                "category": "Health & Wellness Tips",
                "subject": "subah ki routine",
                "angle": "doctor simple alfaaz mein science samjha raha hai",
                "image_prompt": "Split-screen visual: left side showing a tired person in gray tones, right side showing an energetic person in vibrant colors, with 'subah ki routine' text overlay, hyperrealistic photography, 8K, studio lighting, sharp focus",
                "veo3_prompt": 'Cinematic tracking shot following a person as they demonstrate morning routine. The scene transitions from a dark, sluggish morning to an energetic, vibrant atmosphere. Voiceover narrates in Urdu: "Yeh ek simple change ne meri poori energy badal di. Suno dhyan se!" Warm golden lighting gradually increases. Audio: inspirational ambient music, calm Urdu narrator voice. (no subtitles)',
            },
            {
                "category": "Motivational & Startup Stories",
                "subject": "akela founder ka safar",
                "angle": "dramatic cinematic safar ki kahani",
                "image_prompt": "Cinematic shot of a solo founder journey, dramatic lighting, determination on the face, laptop glowing in a dark garage, editorial magazine photography, clean background, professional lighting",
                "veo3_prompt": 'Cinematic close-up of a founder\'s face illuminated by a laptop screen in a dark garage. They\'re working on their startup. The person looks at camera with determination and says in Urdu: "Sab ne kaha yeh idea pagalpan hai. Woh galat the, bilkul galat!" Low-key dramatic lighting, shallow depth of field. Audio: emotional piano building, raw authentic Urdu voice. (no subtitles)',
            },
            {
                "category": "Talking Everyday Objects",
                "subject": "alarm clock",
                "angle": "apne maalik ki daily habits review kar raha hai",
                "image_prompt": "A alarm clock with an animated cartoon face, sitting on a nightstand, looking annoyed at its owner, hyper-detailed macro photography, dramatic lighting, rich textures",
                "veo3_prompt": 'Close-up shot of an alarm clock on a bedside table at 6 AM. The alarm clock has a cartoon face that suddenly opens its eyes. Looking exasperated, it says in Urdu: "Roz mujhe use karte ho lekin kabhi shukriya nahi bola. Chalo baat karte hain!" Camera slow push-in. Early morning blue light transitioning to warm. Audio: alarm sound fading in, comedic Urdu voice. (no subtitles)',
            },
        ],
        "weekly": [
            {
                "category": "AI & Future Tech Visualizations",
                "subject": "AI robot assistant",
                "angle": "2030 mein ek din kaisa hoga",
                "image_prompt": "Futuristic scene of AI robot assistant, glowing holographic interfaces, neon blue and purple lighting, cyberpunk aesthetic, cinematic film still, shallow depth of field, warm golden hour lighting",
                "veo3_prompt": 'Sweeping aerial shot descending into a futuristic city scene showing AI robot assistant. Holographic interfaces glow in neon blue and purple. A narrator says in an awe-inspired Urdu voice: "Saal 2030 mein khush aamdeed! Dekho tumhari rozana ki zindagi ab kaisi hai." Dramatic cinematic lighting. Audio: epic orchestral music, deep Urdu narrator voice. (no subtitles)',
            },
        ],
        "monthly": [
            {
                "category": "Satisfying Process Videos",
                "subject": "perfect khana banana",
                "angle": "close-up ASMR style satisfying sounds ke saath",
                "image_prompt": "Top-down view of cooking a perfect meal, perfectly organized, satisfying symmetry, clean workspace, editorial magazine photography, clean background, professional lighting",
                "veo3_prompt": "Top-down close-up shot of hands precisely cooking a perfect meal. Every movement is deliberate and satisfying. The camera slowly pulls back to reveal the full workspace. Audio: crisp ASMR sounds of the activity, soft lo-fi background music. No voice. (no subtitles)",
            },
        ],
    }

    html = build_email(test_data)
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
