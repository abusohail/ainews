"""
Prompt Generator — Creates ready-to-use AI image prompts and Veo3 video prompts
based on trending topics and viral content categories.
Each day generates fresh, unique prompts for content creation.
"""

import random
from datetime import datetime, timezone


# ─── Image Prompt Templates ──────────────────────────────────────────────────
# Optimized for Midjourney, DALL-E, Ideogram, Flux

IMAGE_STYLES = [
    "hyperrealistic photography, 8K, studio lighting, sharp focus",
    "3D Pixar-style render, vibrant colors, soft lighting, cute character design",
    "cinematic film still, shallow depth of field, warm golden hour lighting",
    "editorial magazine photography, clean background, professional lighting",
    "whimsical illustration style, pastel colors, dreamy atmosphere",
    "hyper-detailed macro photography, dramatic lighting, rich textures",
    "modern minimalist design, clean composition, vibrant accent colors",
    "anime-inspired digital art, cel shading, dynamic composition",
]

IMAGE_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        "A {subject} with an expressive cartoon face (big eyes, wide smile), sitting on a kitchen counter, looking directly at camera, {style}",
        "Anthropomorphic {subject} character wearing tiny glasses, standing at a podium giving a speech, surrounded by other produce in the audience, {style}",
        "A giant {subject} with a friendly face, arms and legs, standing in a supermarket produce aisle, pointing at a health facts poster, {style}",
        "Close-up of a {subject} with a sassy expression and raised eyebrow, sitting next to junk food it disapproves of, {style}",
        "A {subject} character dressed as a doctor with a tiny stethoscope, examining a patient (another vegetable), in a miniature hospital, {style}",
    ],
    "Health & Wellness Tips": [
        "Split-screen visual: left side showing a tired person in gray tones, right side showing an energetic person in vibrant colors, with '{subject}' text overlay, {style}",
        "A beautiful flat lay arrangement related to {subject}, shot from above on a marble surface with natural light, {style}",
        "Infographic-style image showing the benefits of {subject}, with icons and a human body silhouette, clean medical design, {style}",
        "A serene scene of someone practicing {subject} in a beautiful natural setting at sunrise, {style}",
        "Before and after comparison showing the effects of {subject}, dramatic transformation, {style}",
    ],
    "Talking Everyday Objects": [
        "A {subject} with an animated cartoon face, sitting on a nightstand, looking annoyed at its owner, {style}",
        "Anthropomorphic {subject} standing with crossed arms, giving side-eye to the camera, in a cozy room, {style}",
        "A group of household objects including a {subject} having a meeting at a tiny conference table, {style}",
        "Close-up of a {subject} with a wise, elderly expression and tiny spectacles, sitting in a library, {style}",
    ],
    "Animals Explaining Science": [
        "A {subject} wearing a tiny lab coat and round glasses, standing at a chalkboard with science diagrams, {style}",
        "A {subject} professor character sitting in a leather armchair, holding a tiny book, fireplace in background, {style}",
        "A {subject} in a TED talk setting, on stage with a red circle underneath, screen behind it showing diagrams, {style}",
    ],
    "AI & Future Tech Visualizations": [
        "Futuristic scene of {subject}, glowing holographic interfaces, neon blue and purple lighting, cyberpunk aesthetic, {style}",
        "A split scene showing current technology on the left and {subject} on the right in a utopian future city, {style}",
        "Product advertisement for {subject}, sleek design, floating in a void with soft volumetric lighting, Apple-style aesthetic, {style}",
    ],
    "Motivational & Startup Stories": [
        "Cinematic shot of a {subject}, dramatic lighting, determination on the face, laptop glowing in a dark garage, {style}",
        "Split composition: left side showing struggle (dark, rain), right side showing success (bright, confetti), depicting {subject}, {style}",
        "A person experiencing the moment of {subject}, captured in slow motion, lens flare, emotional lighting, {style}",
    ],
    "Satisfying Process Videos": [
        "Top-down view of {subject}, perfectly organized, satisfying symmetry, clean workspace, {style}",
        "Close-up of hands doing {subject}, shallow depth of field, warm lighting, ASMR aesthetic, {style}",
        "Time-lapse start frame of {subject}, raw materials laid out beautifully, ready to begin, {style}",
    ],
}

# ─── Veo3 Video Prompt Templates ─────────────────────────────────────────────
# Optimized for Google Veo3 — includes camera, audio, and scene direction

VEO3_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        (
            'Close-up cinematic shot of a {subject} with an expressive animated face, sitting on a rustic wooden cutting board in a sunlit kitchen. '
            'The {subject} looks directly at camera with big eyes and starts speaking in a confident, friendly voice: '
            '"{dialogue}" '
            'Camera slowly dollies in. Warm natural lighting from a window. Audio: cheerful background music, crisp voice. (no subtitles)'
        ),
        (
            'Medium shot of a {subject} character with cartoon eyes and a mouth, standing on a kitchen counter next to a plate of junk food. '
            'The {subject} gestures dramatically and says in a sassy tone: "{dialogue}" '
            'Camera at eye level, slight handheld movement. Bright kitchen lighting. Audio: comedic background music, expressive voice. (no subtitles)'
        ),
        (
            'Wide angle shot of a farmer\'s market scene. A {subject} with a cute animated face sits on a display stand. '
            'It turns to camera and says enthusiastically: "{dialogue}" '
            'Shallow depth of field, golden hour lighting. Audio: ambient market sounds, warm voice. (no subtitles)'
        ),
    ],
    "Health & Wellness Tips": [
        (
            'Cinematic tracking shot following a person as they demonstrate {subject}. '
            'The scene transitions from a dark, sluggish morning to an energetic, vibrant atmosphere. '
            'Voiceover narrates: "{dialogue}" '
            'Warm golden lighting gradually increases. Audio: inspirational ambient music, calm narrator voice. (no subtitles)'
        ),
        (
            'Close-up slow motion of {subject} being practiced, with stunning visual details. '
            'Camera orbits around the subject. Beautiful natural lighting. '
            'A confident voice explains: "{dialogue}" '
            'Audio: soft piano music, clear voice, subtle ASMR textures. (no subtitles)'
        ),
    ],
    "Talking Everyday Objects": [
        (
            'Close-up shot of a {subject} on a bedside table at 6 AM. The {subject} has a cartoon face that suddenly opens its eyes. '
            'Looking exasperated, it says: "{dialogue}" '
            'Camera slow push-in. Early morning blue light transitioning to warm. Audio: alarm sound fading in, comedic voice. (no subtitles)'
        ),
        (
            'Medium shot of a {subject} sitting alone on a shelf. It comes to life with cartoon eyes and mouth. '
            'Looking at camera with a knowing expression, it says: "{dialogue}" '
            'Soft room lighting, shallow depth of field. Audio: gentle background music, wise-sounding voice. (no subtitles)'
        ),
    ],
    "Animals Explaining Science": [
        (
            'Medium shot of a {subject} sitting at a tiny desk in a library setting, wearing miniature round glasses. '
            'It looks up from a book at the camera and says in a professorial tone: "{dialogue}" '
            'Warm library lighting, bookshelves in background. Camera slowly zooms in. Audio: gentle classical music, scholarly voice. (no subtitles)'
        ),
    ],
    "AI & Future Tech Visualizations": [
        (
            'Sweeping aerial shot descending into a futuristic city scene showing {subject}. '
            'Holographic interfaces glow in neon blue and purple. Everything feels sleek and advanced. '
            'A narrator says in an awe-inspired voice: "{dialogue}" '
            'Dramatic cinematic lighting. Audio: epic orchestral music, deep narrator voice. (no subtitles)'
        ),
    ],
    "Motivational & Startup Stories": [
        (
            'Cinematic close-up of a founder\'s face illuminated by a laptop screen in a dark garage. They\'re working on {subject}. '
            'The person looks at camera with determination and says: "{dialogue}" '
            'Low-key dramatic lighting, shallow depth of field. Audio: emotional piano building, raw authentic voice. (no subtitles)'
        ),
    ],
    "Satisfying Process Videos": [
        (
            'Top-down close-up shot of hands precisely doing {subject}. Every movement is deliberate and satisfying. '
            'The camera slowly pulls back to reveal the full workspace. '
            'Audio: crisp ASMR sounds of the activity, soft lo-fi background music. No voice. (no subtitles)'
        ),
    ],
}

# ─── Dialogue Lines per Category ─────────────────────────────────────────────

DIALOGUES = {
    "Talking Fruits & Vegetables": {
        "apple": [
            "One of me a day and your doctor stays unemployed. You're welcome.",
            "You know what's in me? Fiber, vitamins, and pure disappointment that you chose chips instead.",
            "I've been sitting in your fruit bowl for a week. EAT ME before I go bad!",
        ],
        "banana": [
            "I'm literally the perfect snack. I come in my own wrapper. What's your excuse, candy bar?",
            "Potassium, energy, happiness — I bring it all. And I'm only 100 calories. You're welcome.",
            "Stop scrolling and peel me. Your muscles will thank you later.",
        ],
        "avocado": [
            "Yes, I'm expensive. But have you seen your hospital bills? I'm the cheaper option.",
            "Healthy fats, fiber, and twenty different vitamins. I'm basically a multivitamin with better branding.",
            "Millennials didn't ruin the economy — they just discovered I'm delicious on toast.",
        ],
        "broccoli": [
            "Kids hate me. Adults tolerate me. Your immune system LOVES me. Know your audience.",
            "More vitamin C than an orange, more calcium than milk. But sure, keep ignoring me.",
            "Steam me, roast me, stir-fry me — I don't care how you eat me, just eat me!",
        ],
        "carrot": [
            "Your grandma was right — I AM good for your eyes. Also your skin, your gut, and your heart.",
            "I can be a snack, a juice, a soup, or a cake. Name another vegetable that versatile.",
        ],
        "garlic": [
            "Vampires, bacteria, and heart disease all fear me. I'm basically a superfood bouncer.",
            "Yes, I make your breath smell. But I also make your immune system unstoppable. Trade-off accepted.",
        ],
        "lemon": [
            "Start your morning with my juice in warm water. Your metabolism will wake up faster than coffee.",
            "I'm sour, I know. But my vitamin C content is sweet for your immune system.",
        ],
        "_default": [
            "Hey you! Yeah, the one eating processed food. Come talk to me instead.",
            "You scrolled past three fruit videos today. Time to actually eat one of us.",
            "I'm not just food — I'm medicine. Start treating me like it.",
        ],
    },
    "Health & Wellness Tips": {
        "_default": [
            "This one simple change transformed my energy levels completely.",
            "Scientists say this is the most underrated health habit. And almost nobody does it.",
            "Your body is trying to tell you something. Here's what it means.",
            "I tried this for 30 days and the results shocked me.",
            "This is what happens to your body when you start doing this every morning.",
        ],
    },
    "Talking Everyday Objects": {
        "_default": [
            "You use me every day but never appreciate me. Let's talk about that.",
            "I've been watching you, and honestly? We need to have a conversation.",
            "If I could give you one piece of advice, it would be this.",
            "You have no idea how much I do for you. Let me explain.",
        ],
    },
    "Animals Explaining Science": {
        "_default": [
            "Fun fact of the day — and this one is absolutely mind-blowing.",
            "Humans have been doing this wrong for centuries. Let me explain why.",
            "The science behind this is actually fascinating. Let me break it down for you.",
            "Most people don't know this, but it changes everything about how you think about health.",
        ],
    },
    "AI & Future Tech Visualizations": {
        "_default": [
            "Welcome to the year 2030. This is what your daily life looks like now.",
            "This technology seemed impossible five years ago. Now it's everywhere.",
            "The future isn't coming — it's already here. Let me show you.",
        ],
    },
    "Motivational & Startup Stories": {
        "_default": [
            "Everyone said this idea was crazy. They were wrong.",
            "Six months ago I had nothing. Today? Everything changed because of one decision.",
            "The hardest part wasn't building the product. It was believing in myself.",
        ],
    },
    "Satisfying Process Videos": {
        "_default": [],  # No dialogue for satisfying videos
    },
}


def _get_dialogue(category, subject):
    """Get a random dialogue line for the given category and subject."""
    cat_dialogues = DIALOGUES.get(category, {})
    lines = cat_dialogues.get(subject, cat_dialogues.get("_default", []))
    if not lines:
        return "Did you know? Your daily habits shape your health more than genetics."
    return random.choice(lines)


def generate_prompts(trending_data):
    """
    Generate daily image + Veo3 video prompts based on trending data.

    Returns a list of prompt sets, each containing:
    - category: the viral category name
    - subject: specific subject
    - angle: the creative angle
    - image_prompt: ready-to-use image generation prompt
    - veo3_prompt: ready-to-use Veo3 video prompt
    - trending_hook: optional trending topic tie-in
    """
    prompts = []

    # Use today's date as seed for consistent daily output
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    random.seed(today)

    daily_categories = trending_data.get("daily_categories", [])
    google_trends = trending_data.get("google_trends", [])

    for cat in daily_categories:
        category_name = cat["category"]
        subjects = cat["subjects"]
        angles = cat["angles"]

        # Pick 2 subjects per category
        chosen_subjects = random.sample(subjects, min(2, len(subjects)))
        chosen_angle = random.choice(angles)
        chosen_style = random.choice(IMAGE_STYLES)

        for subject in chosen_subjects:
            # Get dialogue for Veo3
            dialogue = _get_dialogue(category_name, subject)

            # Generate image prompt
            img_templates = IMAGE_TEMPLATES.get(category_name, [])
            if img_templates:
                img_template = random.choice(img_templates)
                image_prompt = img_template.format(
                    subject=subject, style=chosen_style
                )
            else:
                image_prompt = f"A stunning image of {subject}, {chosen_angle}, {chosen_style}"

            # Generate Veo3 video prompt
            veo3_templates = VEO3_TEMPLATES.get(category_name, [])
            if veo3_templates:
                veo3_template = random.choice(veo3_templates)
                veo3_prompt = veo3_template.format(
                    subject=subject, dialogue=dialogue
                )
            else:
                veo3_prompt = (
                    f'Cinematic medium shot of {subject}, {chosen_angle}. '
                    f'A voice narrates: "{dialogue}" '
                    f'Beautiful lighting, smooth camera movement. Audio: ambient music, clear voice. (no subtitles)'
                )

            # Tie to a trending topic if available
            trending_hook = ""
            if google_trends:
                trend = random.choice(google_trends)
                trending_hook = f"Trending tie-in: Connect this to '{trend}' for extra reach"

            prompts.append({
                "category": category_name,
                "subject": subject,
                "angle": chosen_angle,
                "image_prompt": image_prompt,
                "veo3_prompt": veo3_prompt,
                "trending_hook": trending_hook,
            })

    print(f"  ✓ Generated {len(prompts)} image + Veo3 prompt sets")
    return prompts
