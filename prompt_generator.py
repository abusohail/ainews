"""
Prompt Generator — Creates ready-to-use AI image prompts and Veo3 video prompts.
Generates 3 sets: Today (5), This Week (5), This Month (5).
All dialogues are in Roman Urdu (Urdu written in Roman script).
"""

import random
from datetime import datetime, timezone


# ─── Image Prompt Templates ──────────────────────────────────────────────────

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

VEO3_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        (
            'Close-up cinematic shot of a {subject} with an expressive animated face, sitting on a rustic wooden cutting board in a sunlit kitchen. '
            'The {subject} looks directly at camera with big eyes and starts speaking in a confident, friendly Urdu voice: '
            '"{dialogue}" '
            'Camera slowly dollies in. Warm natural lighting from a window. Audio: cheerful background music, crisp Urdu voice. (no subtitles)'
        ),
        (
            'Medium shot of a {subject} character with cartoon eyes and a mouth, standing on a kitchen counter next to a plate of junk food. '
            'The {subject} gestures dramatically and says in a sassy Urdu tone: "{dialogue}" '
            'Camera at eye level, slight handheld movement. Bright kitchen lighting. Audio: comedic background music, expressive Urdu voice. (no subtitles)'
        ),
        (
            'Wide angle shot of a farmer\'s market scene. A {subject} with a cute animated face sits on a display stand. '
            'It turns to camera and says enthusiastically in Urdu: "{dialogue}" '
            'Shallow depth of field, golden hour lighting. Audio: ambient market sounds, warm Urdu voice. (no subtitles)'
        ),
    ],
    "Health & Wellness Tips": [
        (
            'Cinematic tracking shot following a person as they demonstrate {subject}. '
            'The scene transitions from a dark, sluggish morning to an energetic, vibrant atmosphere. '
            'Voiceover narrates in Urdu: "{dialogue}" '
            'Warm golden lighting gradually increases. Audio: inspirational ambient music, calm Urdu narrator voice. (no subtitles)'
        ),
        (
            'Close-up slow motion of {subject} being practiced, with stunning visual details. '
            'Camera orbits around the subject. Beautiful natural lighting. '
            'A confident voice explains in Urdu: "{dialogue}" '
            'Audio: soft piano music, clear Urdu voice, subtle ASMR textures. (no subtitles)'
        ),
    ],
    "Talking Everyday Objects": [
        (
            'Close-up shot of a {subject} on a bedside table at 6 AM. The {subject} has a cartoon face that suddenly opens its eyes. '
            'Looking exasperated, it says in Urdu: "{dialogue}" '
            'Camera slow push-in. Early morning blue light transitioning to warm. Audio: alarm sound fading in, comedic Urdu voice. (no subtitles)'
        ),
        (
            'Medium shot of a {subject} sitting alone on a shelf. It comes to life with cartoon eyes and mouth. '
            'Looking at camera with a knowing expression, it says in Urdu: "{dialogue}" '
            'Soft room lighting, shallow depth of field. Audio: gentle background music, wise-sounding Urdu voice. (no subtitles)'
        ),
    ],
    "Animals Explaining Science": [
        (
            'Medium shot of a {subject} sitting at a tiny desk in a library setting, wearing miniature round glasses. '
            'It looks up from a book at the camera and says in a professorial Urdu tone: "{dialogue}" '
            'Warm library lighting, bookshelves in background. Camera slowly zooms in. Audio: gentle classical music, scholarly Urdu voice. (no subtitles)'
        ),
    ],
    "AI & Future Tech Visualizations": [
        (
            'Sweeping aerial shot descending into a futuristic city scene showing {subject}. '
            'Holographic interfaces glow in neon blue and purple. Everything feels sleek and advanced. '
            'A narrator says in an awe-inspired Urdu voice: "{dialogue}" '
            'Dramatic cinematic lighting. Audio: epic orchestral music, deep Urdu narrator voice. (no subtitles)'
        ),
    ],
    "Motivational & Startup Stories": [
        (
            'Cinematic close-up of a founder\'s face illuminated by a laptop screen in a dark garage. They\'re working on {subject}. '
            'The person looks at camera with determination and says in Urdu: "{dialogue}" '
            'Low-key dramatic lighting, shallow depth of field. Audio: emotional piano building, raw authentic Urdu voice. (no subtitles)'
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

# ─── Roman Urdu Dialogue Lines ───────────────────────────────────────────────

DIALOGUES = {
    "Talking Fruits & Vegetables": {
        "apple": [
            "Roz ek apple khao aur doctor ki zaroorat nahi. Yeh meri taraf se free mashwara hai!",
            "Mujh mein fiber hai, vitamins hain, aur tumhari chips ki aadat pe bohot dukh hai.",
            "Ek hafta ho gaya fruit bowl mein. Mujhe khao yaar, kharab ho jaunga!",
            "Tumhare jism ko meri zaroorat hai, lekin tum junk food ke peechay bhaag rahe ho.",
        ],
        "banana": [
            "Main perfect snack hoon bhai. Apna wrapper bhi saath laata hoon. Chips mein yeh baat hai?",
            "Potassium, energy, khushi — sab kuch hai mujh mein. Aur sirf sau calories. Khao mujhe!",
            "Phone rakh do aur mujhe cheel lo. Tumhare muscles baad mein shukriya kahenge.",
            "Subah ka pehla kaam — banana khao. Energy din bhar rahegi, promise!",
        ],
        "avocado": [
            "Haan bhai mehenga hoon. Lekin hospital ka bill dekha hai? Main sasta option hoon.",
            "Healthy fats, fiber, aur bees tarah ke vitamins. Main basically multivitamin hoon.",
            "Log kehtay hain mehenga hai. Bhai sehat ka koi mol nahi hota, samjho!",
            "Toast pe lagao, salad mein daalo — bas mujhe ignore mat karo!",
        ],
        "broccoli": [
            "Bachay mujhse nafrat karte hain, baray bardasht karte hain, lekin immunity MUJHSE pyaar karti hai!",
            "Orange se zyada vitamin C, doodh se zyada calcium. Phir bhi log mujhe ignore karte hain.",
            "Steam karo, roast karo, fry karo — mujhe parwah nahi kaise khate ho, bas khao!",
            "Main sabziyon ka king hoon. Lekin tum ne aaj bhi burger kha liya. Sharam karo!",
        ],
        "carrot": [
            "Tumhari dadi sahi kehti thi — main aankhon ke liye acha hoon. Aur skin, pet, dil ke liye bhi!",
            "Snack ban sakta hoon, juice ban sakta hoon, soup bhi. Itni versatile aur kaun si sabzi hai?",
            "Mujhe halwa bana lo, mujhe salad mein daalo — bas mujhe fridge mein akela mat chhoro!",
        ],
        "garlic": [
            "Vampires, bacteria, aur dil ki bimari — sab mujhse darte hain. Main superfood ka bouncer hoon!",
            "Haan saans mein boo aati hai. Lekin immunity itni strong ho jaati hai ke bimari bhaag jaati hai.",
            "Khana mein agar main nahi toh taste bhi nahi aur sehat bhi nahi. Sochlo!",
        ],
        "lemon": [
            "Subah garam paani mein mera ras daalo. Metabolism coffee se bhi pehle jaag jayega.",
            "Khatta hoon, pata hai. Lekin mera vitamin C tumhari immunity ke liye meetha hai!",
            "Nimbu paani piyo, taza raho. Yeh desi nuskha hai aur kaam karta hai!",
        ],
        "watermelon": [
            "Garmi mein mujhse behtar koi nahi. Paani bhi milega aur maza bhi!",
            "Dehydration ka ilaaj hoon main. Cold drink choro, mujhe khao!",
            "Bees rupay mein itna paani aur vitamins — koi deal itni achi nahi milegi!",
        ],
        "mango": [
            "Phalon ka badshah hoon main. Season aaye toh mujhe zaroor khana!",
            "Vitamin A, C, fiber — aur taste toh poochho hi mat. King of fruits hoon bhai!",
            "Log diet ke naam pe mujhse door bhagte hain. Arre moderation mein khao, maza aayega!",
        ],
        "spinach": [
            "Popeye ne mujhe kha ke taaqat payi thi. Tum kyun nahi khaate?",
            "Iron, calcium, vitamins — main chhota sa saag hoon lekin power bohot hai!",
            "Palak paneer bana lo, smoothie mein daalo — bas mujhe waste mat karo!",
        ],
        "tomato": [
            "Sabzi hoon ya fruit, yeh debate baad mein. Pehle mujhe khao, sehat banao!",
            "Lycopene mujh mein hai — dil ki sehat ke liye behtareen hoon main!",
            "Har khane mein main hoon. Salad, curry, chutney — versatile king hoon main!",
        ],
        "_default": [
            "Oye! Haan tum — jo processed food kha rahe ho. Idhar aao, mujhse baat karo!",
            "Aaj teen fruit ki video dekhi lekin ek bhi nahi khaya. Sharam karo yaar!",
            "Main sirf khana nahi hoon — main dawai hoon. Aise treat karo mujhe!",
            "Tumhari sehat tumhare haath mein hai. Aur main tumhare haath mein hona chahiye!",
        ],
    },
    "Health & Wellness Tips": {
        "_default": [
            "Yeh ek simple change ne meri poori energy badal di. Suno dhyan se!",
            "Science kehti hai yeh sabse underrated health habit hai. Aur koi nahi karta!",
            "Tumhara jism tumhe kuch batana chahta hai. Aao samjhte hain.",
            "Maine yeh 30 din kiya aur results ne mujhe bhi hairan kar diya!",
            "Jab tum yeh roz subah karna shuru karo ge, jism khud shukriya kahega.",
            "Yeh aadat chhoti si hai lekin asar bohot bada hai. Aaj se shuru karo!",
        ],
    },
    "Talking Everyday Objects": {
        "_default": [
            "Roz mujhe use karte ho lekin kabhi shukriya nahi bola. Chalo baat karte hain!",
            "Main tumhe dekh raha hoon, aur honestly? Humein baat karni chahiye.",
            "Agar main tumhe ek mashwara de sakta toh yeh hota — suno dhyan se!",
            "Tumhe andaza bhi nahi mein tumhare liye kitna karta hoon. Suno toh sahi!",
            "Tum mujhe galat tareeqe se use kar rahe ho! Aao batata hoon sahi tareeqa.",
        ],
    },
    "Animals Explaining Science": {
        "_default": [
            "Aaj ka fun fact — aur yeh waaqi mein dimagh hila dega tumhara!",
            "Insaan centuries se yeh galat kar rahe hain. Main batata hoon kyun!",
            "Is cheez ke peechay ka science bohot dilchasp hai. Chalo samjhte hain!",
            "Aksar log yeh nahi jaante, lekin yeh sab badal deta hai sehat ke baare mein!",
            "Kya tumhe pata hai yeh cheez kaise kaam karti hai? Nahi? Toh suno!",
        ],
    },
    "AI & Future Tech Visualizations": {
        "_default": [
            "Saal 2030 mein khush aamdeed! Dekho tumhari rozana ki zindagi ab kaisi hai.",
            "Paanch saal pehle yeh technology namumkin lagti thi. Ab har jagah hai!",
            "Mustaqbil aa nahi raha — yeh pehle se yahan hai. Main dikhata hoon!",
            "AI ne duniya badal di hai. Ab insaan aur machine saath kaam karte hain!",
        ],
    },
    "Motivational & Startup Stories": {
        "_default": [
            "Sab ne kaha yeh idea pagalpan hai. Woh galat the, bilkul galat!",
            "Cheh mahine pehle mere paas kuch nahi tha. Aaj? Ek faislay ne sab badal diya.",
            "Sabse mushkil kaam product banana nahi tha. Khud pe bharosa karna tha!",
            "Garage mein se shuru kiya, aaj duniya jaanti hai. Yeh meri kahani hai!",
            "Haar mat mano. Kamyaabi un logon ko milti hai jo rukne se inkaar karte hain!",
        ],
    },
    "Satisfying Process Videos": {
        "_default": [],  # No dialogue for satisfying videos — ASMR only
    },
}


# ─── Viral Categories ────────────────────────────────────────────────────────

VIRAL_CATEGORIES = [
    {
        "category": "Talking Fruits & Vegetables",
        "subjects": [
            "apple", "banana", "avocado", "strawberry", "blueberry", "mango",
            "watermelon", "lemon", "orange", "carrot", "broccoli", "spinach",
            "garlic", "ginger", "turmeric", "pomegranate", "kiwi", "pineapple",
            "tomato", "sweet potato", "beet", "cucumber", "celery",
        ],
        "angles": [
            "apne health benefits samjha raha hai insaanon ko",
            "junk food khaane walon ki class le raha hai",
            "doosre fruit se behas kar raha hai kaun zyada healthy hai",
            "nutrition ke baare mein motivational speech de raha hai",
            "kissi ne isko phenk diya aur yeh react kar raha hai",
            "fridge mein doosri sabziyon ka interview le raha hai",
            "fridge mein zyada der rehne ki shikayat kar raha hai",
            "bachay ko sabzi khane ke liye mana raha hai",
            "samjha raha hai ke yeh superfood kyun hai",
            "ek simple recipe sikhane ki cooking show kar raha hai",
        ],
    },
    {
        "category": "Health & Wellness Tips",
        "subjects": [
            "subah ki routine", "pet ki sehat", "neend ki optimization",
            "paani peena", "stress door karna", "immunity", "anti-aging khana",
            "dimagh ki sehat", "energy badhana", "detox", "wazan ghatana",
            "muscle recovery", "meditation", "cold therapy", "intermittent fasting",
        ],
        "angles": [
            "doctor simple alfaaz mein science samjha raha hai",
            "pehle aur baad ka transformation dikha raha hai",
            "day-in-the-life healthy aadat dikha raha hai",
            "aam ghaltfahmiyon ko door kar raha hai",
            "do tareeqon ka comparison kar raha hai",
        ],
    },
    {
        "category": "Talking Everyday Objects",
        "subjects": [
            "coffee mug", "alarm clock", "toothbrush", "joote",
            "smartphone", "paani ki bottle", "takiya", "sheeshe",
            "fridge", "vitamin ki bottle", "blender", "yoga mat",
            "kitaab", "mombatti",
        ],
        "angles": [
            "shikayat kar raha hai ke galat tareeqe se use ho raha hai",
            "apne nazariye se zindagi ka mashwara de raha hai",
            "doosri cheez se behas kar raha hai",
            "dramatic andaaz mein apni kahani suna raha hai",
            "apne maalik ki daily habits review kar raha hai",
        ],
    },
    {
        "category": "Animals Explaining Science",
        "subjects": [
            "samajhdar ullu", "curious billi", "golden retriever",
            "chhota haathi", "penguin", "dolphin", "lomri",
            "khargosh", "tota", "kachhua",
        ],
        "angles": [
            "professor ban ke science fact sikha raha hai",
            "samjha raha hai insaan ajeeb kaam kyun karte hain",
            "doosre jaanwaron ko TED talk de raha hai",
            "apne baare mein nature documentary suna raha hai",
            "insaani khane pe react kar ke nutrition samjha raha hai",
        ],
    },
    {
        "category": "AI & Future Tech Visualizations",
        "subjects": [
            "AI robot assistant", "2030 ka smart ghar",
            "AI doctor", "self-driving sheher", "insaan-AI saath kaam",
            "neural interface", "holographic display", "drone delivery",
            "AI art studio", "robot chef", "AI teacher", "space mein colony",
        ],
        "angles": [
            "2030 mein ek din kaisa hoga",
            "aaj ki technology vs AI-powered mustaqbil",
            "futuristic product ka advertisement",
            "technology simply samjha raha hai",
            "aaj se mustaqbil tak ka transformation dikha raha hai",
        ],
    },
    {
        "category": "Motivational & Startup Stories",
        "subjects": [
            "akela founder ka safar", "garage se lakhon tak",
            "reject hone ke baad kamyaabi", "side hustle se full-time",
            "AI startup idea", "no-code app launch",
            "pehla customer ka moment", "business ko pivot karna",
            "bootstrapped kamyaabi",
        ],
        "angles": [
            "dramatic cinematic safar ki kahani",
            "founder apna sabse mushkil waqt bata raha hai kamyaabi se pehle",
            "split screen — struggle vs reward",
            "business banana ka time-lapse",
            "naukri chhod ke apna sapna pursue karna",
        ],
    },
    {
        "category": "Satisfying Process Videos",
        "subjects": [
            "perfect khana banana", "messy jagah organize karna",
            "painting banana", "kuch scratch se banana",
            "3D printing", "mitti ke bartan banana", "calligraphy",
            "cake decorating", "lakri ka kaam", "app code karna",
        ],
        "angles": [
            "close-up ASMR style satisfying sounds ke saath",
            "shuru se aakhir tak time-lapse",
            "split screen — messy vs clean/finished",
            "intricate details mein zoom karna",
            "final reveal ka moment",
        ],
    },
]


def _get_dialogue(category, subject):
    """Get a random dialogue line for the given category and subject."""
    cat_dialogues = DIALOGUES.get(category, {})
    lines = cat_dialogues.get(subject, cat_dialogues.get("_default", []))
    if not lines:
        return "Kya tumhe pata hai? Tumhari roz ki aadatein tumhari sehat pe sabse zyada asar dalti hain!"
    return random.choice(lines)


def _generate_prompt_set(categories, count, seed_str):
    """Generate a specific number of prompts using the given seed."""
    random.seed(seed_str)
    prompts = []

    # Shuffle categories and cycle through them
    shuffled_cats = list(categories)
    random.shuffle(shuffled_cats)

    idx = 0
    while len(prompts) < count:
        cat = shuffled_cats[idx % len(shuffled_cats)]
        category_name = cat["category"]
        subjects = cat["subjects"]
        angles = cat["angles"]

        subject = random.choice(subjects)
        angle = random.choice(angles)
        style = random.choice(IMAGE_STYLES)
        dialogue = _get_dialogue(category_name, subject)

        # Image prompt
        img_templates = IMAGE_TEMPLATES.get(category_name, [])
        if img_templates:
            image_prompt = random.choice(img_templates).format(subject=subject, style=style)
        else:
            image_prompt = f"A stunning image of {subject}, {angle}, {style}"

        # Veo3 prompt
        veo3_templates = VEO3_TEMPLATES.get(category_name, [])
        if veo3_templates:
            veo3_prompt = random.choice(veo3_templates).format(subject=subject, dialogue=dialogue)
        else:
            veo3_prompt = (
                f'Cinematic medium shot of {subject}, {angle}. '
                f'A voice narrates in Urdu: "{dialogue}" '
                f'Beautiful lighting, smooth camera movement. Audio: ambient music, clear Urdu voice. (no subtitles)'
            )

        prompts.append({
            "category": category_name,
            "subject": subject,
            "angle": angle,
            "image_prompt": image_prompt,
            "veo3_prompt": veo3_prompt,
        })

        idx += 1

    return prompts


def generate_prompts(trending_data=None):
    """
    Generate prompts in 3 time-based sets:
    - Today (5 prompts) — changes daily
    - This Week (5 prompts) — changes weekly
    - This Month (5 prompts) — changes monthly

    Returns dict with keys: daily, weekly, monthly
    """
    now = datetime.now(timezone.utc)

    # Seeds for time-based rotation
    daily_seed = now.strftime("%Y-%m-%d")
    weekly_seed = f"{now.year}-W{now.isocalendar()[1]}"
    monthly_seed = now.strftime("%Y-%m")

    result = {
        "daily": _generate_prompt_set(VIRAL_CATEGORIES, 5, f"daily-{daily_seed}"),
        "weekly": _generate_prompt_set(VIRAL_CATEGORIES, 5, f"weekly-{weekly_seed}"),
        "monthly": _generate_prompt_set(VIRAL_CATEGORIES, 5, f"monthly-{monthly_seed}"),
    }

    total = sum(len(v) for v in result.values())
    print(f"  ✓ Generated {total} prompts (5 daily + 5 weekly + 5 monthly)")
    return result
