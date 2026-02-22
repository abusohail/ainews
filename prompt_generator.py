"""
Prompt Generator — Creates AI image + Veo3 video prompts for viral content.
Focus: Fruits, Vegetables, Health, Junk Food, Everyday Life.
All dialogues in Urdu script. All images/videos in 9:16 vertical (Reels) format.

Generates:
- Aaj Ke Viral Prompts (5)
- Fruits & Vegetables Special (5)
- Video Series (3-5 connected clips for longer videos)
- Is Hafte Ke Viral Prompts (5)
- Is Maheene Ke Viral Prompts (5)
"""

import random
from datetime import datetime, timezone


# ─── Image Styles ─────────────────────────────────────────────────────────────

# All images must be 9:16 vertical for Reels/TikTok/Shorts
ASPECT_RATIO = "9:16 vertical aspect ratio, portrait orientation, mobile-first, optimized for Instagram Reels and TikTok"

IMAGE_STYLES = [
    f"hyperrealistic photography, 8K, studio lighting, sharp focus, {ASPECT_RATIO}",
    f"3D Pixar-style render, vibrant colors, soft lighting, cute character design, {ASPECT_RATIO}",
    f"cinematic film still, shallow depth of field, warm golden hour lighting, {ASPECT_RATIO}",
    f"editorial magazine photography, clean background, professional lighting, {ASPECT_RATIO}",
    f"whimsical illustration style, pastel colors, dreamy atmosphere, {ASPECT_RATIO}",
    f"hyper-detailed macro photography, dramatic lighting, rich textures, {ASPECT_RATIO}",
    f"modern minimalist design, clean composition, vibrant accent colors, {ASPECT_RATIO}",
]

# ─── Categories (user's interests only) ──────────────────────────────────────

VIRAL_CATEGORIES = [
    {
        "category": "Talking Fruits & Vegetables",
        "subjects": [
            "apple", "banana", "avocado", "mango", "watermelon", "lemon",
            "orange", "strawberry", "pomegranate", "kiwi", "pineapple",
            "carrot", "broccoli", "spinach", "garlic", "ginger", "turmeric",
            "tomato", "sweet potato", "cucumber", "onion", "potato",
        ],
        "angles": [
            "apne health benefits samjha raha hai",
            "junk food khaane walon ki class le raha hai",
            "doosre fruit se behas kar raha hai kaun zyada healthy hai",
            "bachay ko sabzi khane ke liye mana raha hai",
            "superfood hone ka proof de raha hai",
            "ek simple recipe sikha raha hai",
            "insaanon ko daant raha hai ke mujhe kyun nahi khaate",
        ],
    },
    {
        "category": "Health & Wellness",
        "subjects": [
            "subah ki routine", "pet ki sehat", "neend", "paani peena",
            "stress door karna", "immunity", "wazan ghatana", "energy badhana",
            "aankhon ki hifazat", "haddiyon ki mazbooti", "dil ki sehat",
            "skin care", "baalon ki hifazat", "sugar control",
            "cholesterol", "BP control", "digest karna",
        ],
        "angles": [
            "simple alfaaz mein science samjha raha hai",
            "pehle aur baad ka transformation dikha raha hai",
            "aam ghaltfahmiyon ko door kar raha hai",
            "do tareeqon ka comparison kar raha hai",
            "doctor ki tarah mashwara de raha hai",
        ],
    },
    {
        "category": "Fayde aur Nuqsanat",
        "subjects": [
            "mobile phone", "social media", "junk food", "cold drinks",
            "chai", "coffee", "ac mein rehna", "late night jaagna",
            "exercise na karna", "screen time", "online shopping",
            "earphones", "fast food", "processed food", "sugar",
            "gaming", "WiFi", "microwave", "plastic bottles",
        ],
        "angles": [
            "advantages aur disadvantages bata raha hai",
            "zyada use ke nuksan samjha raha hai",
            "healthy alternative suggest kar raha hai",
            "shocking facts bata raha hai",
            "common misconceptions door kar raha hai",
            "limit mein use karne ki advice de raha hai",
        ],
    },
    {
        "category": "Kitchen & Cooking Tips",
        "subjects": [
            "haldi doodh", "nimbu paani", "shahad", "desi ghee",
            "adrak ki chai", "khajoor", "badam", "akhrot",
            "lassi", "dahi", "pudina", "ajwain", "kalonji",
            "zeera paani", "saunf", "methi daana",
        ],
        "angles": [
            "desi nuskha bata raha hai",
            "recipe aur benefits ek saath",
            "yeh cheez roz khaani chahiye kyun",
            "yeh combination health ke liye best hai",
            "nani/dadi ka totka samjha raha hai",
        ],
    },
    {
        "category": "Satisfying Food Videos",
        "subjects": [
            "perfect biryani banana", "fruit salad banana",
            "smoothie banana", "sabzi katna", "roti banana",
            "chutney banana", "juice banana", "salad sajana",
            "masala mix karna", "chai banana", "paratha banana",
        ],
        "angles": [
            "close-up ASMR style satisfying sounds ke saath",
            "shuru se aakhir tak time-lapse",
            "ingredients sajana symmetry mein",
            "final reveal ka moment",
            "step by step recipe slow motion mein",
        ],
    },
    {
        "category": "Junk Food Nuqsanat",
        "subjects": [
            "burger", "pizza", "fries", "cold drink", "chips",
            "instant noodles", "hot dog", "fried chicken",
            "donuts", "ice cream", "chocolate bar", "energy drink",
            "processed meat", "packaged juice", "cookies",
        ],
        "angles": [
            "صحت پر سب سے بڑا نقصان بتا رہا ہے",
            "صحت مند متبادل تجویز کر رہا ہے",
            "چونکا دینے والے حقائق بتا رہا ہے",
            "جسم پر اثرات کا موازنہ کر رہا ہے",
            "ایک ہفتہ کھانے کے بعد کیا ہوتا ہے",
            "بچوں کو کیوں نہیں دینا چاہیے",
        ],
    },
]

# ─── Image Templates ─────────────────────────────────────────────────────────

IMAGE_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        "A {subject} with an expressive cartoon face (big eyes, wide smile), sitting on a kitchen counter, looking directly at camera, tall vertical frame, {style}",
        "Anthropomorphic {subject} character wearing tiny glasses, standing at a podium giving a speech about health, centered portrait composition, {style}",
        "A giant {subject} with a friendly face, arms and legs, pointing at a health facts poster in a kitchen, full-body vertical shot, {style}",
        "Close-up of a {subject} with a sassy expression and raised eyebrow, sitting next to junk food it disapproves of, vertical centered, {style}",
        "A {subject} character dressed as a doctor with a tiny stethoscope, giving health advice, portrait vertical frame, {style}",
    ],
    "Health & Wellness": [
        "Split-screen vertical: top half showing a tired person in gray tones, bottom half showing an energetic person in vibrant colors, topic: {subject}, {style}",
        "A beautiful flat lay of {subject} items, shot top-down on marble, portrait orientation, {style}",
        "Infographic-style vertical poster showing the benefits of {subject}, clean medical design, mobile format, {style}",
        "A person practicing {subject} in a beautiful natural setting at sunrise, full-body portrait shot, {style}",
    ],
    "Fayde aur Nuqsanat": [
        "A vertical split poster: top half green check marks showing advantages of {subject}, bottom half red crosses showing disadvantages, {style}",
        "An anthropomorphic {subject} with an animated face, angel wings on one side and devil horns on the other, vertical centered, {style}",
        "A dramatic vertical scene showing {subject} with angel on left and devil on right, portrait frame, {style}",
        "A vertical balance scale visual about {subject}, benefits vs harms, clean infographic, {style}",
    ],
    "Kitchen & Cooking Tips": [
        "A beautiful top-down portrait shot of {subject} ingredients laid out on a rustic wooden table, {style}",
        "An anthropomorphic {subject} character wearing an apron and chef hat, vertical centered portrait, {style}",
        "Close-up portrait shot of {subject} being prepared, steam rising, warm cozy kitchen background, {style}",
    ],
    "Satisfying Food Videos": [
        "Top-down portrait view of {subject}, perfectly organized, satisfying symmetry, clean workspace, {style}",
        "Close-up portrait of hands doing {subject}, shallow depth of field, warm lighting, ASMR aesthetic, {style}",
        "Ingredients for {subject} laid out beautifully in vertical rows, ready to begin, {style}",
    ],
    "Junk Food Nuqsanat": [
        "A dramatic vertical poster showing {subject} with a red warning sign, skull symbol overlay, dark moody lighting, {style}",
        "Split vertical image: top half shows appealing {subject}, bottom half shows its damage to the body with X-ray style visuals, {style}",
        "An evil-looking anthropomorphic {subject} with devil horns and a sneaky grin, dark background, {style}",
        "A vertical infographic showing {subject} ingredients with toxic warning labels and health damage stats, {style}",
    ],
}

# ─── Veo3 Templates — all 9:16 vertical for Reels ────────────────────────────

VEO3_ASPECT = "Vertical 9:16 frame, portrait orientation for Instagram Reels and TikTok."

VEO3_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        (
            f'{VEO3_ASPECT} Close-up cinematic portrait shot of a {{subject}} with an expressive animated face on a rustic cutting board in a sunlit kitchen. '
            'The {subject} looks at camera and speaks in confident Urdu: "{dialogue}" '
            'Camera slowly dollies in. Warm natural lighting. Audio: cheerful music, crisp Urdu voice. (no subtitles)'
        ),
        (
            f'{VEO3_ASPECT} Medium portrait shot of a {{subject}} with cartoon eyes standing on a kitchen counter next to junk food. '
            'It gestures dramatically and says in sassy Urdu: "{dialogue}" '
            'Camera at eye level. Bright kitchen lighting. Audio: comedic music, expressive Urdu voice. (no subtitles)'
        ),
    ],
    "Health & Wellness": [
        (
            f'{VEO3_ASPECT} Cinematic vertical tracking shot following a person demonstrating {{subject}}. '
            'Scene transitions from dark sluggish morning to vibrant energy. '
            'Voiceover in Urdu: "{dialogue}" '
            'Warm golden lighting. Audio: inspirational music, calm Urdu voice. (no subtitles)'
        ),
    ],
    "Fayde aur Nuqsanat": [
        (
            f'{VEO3_ASPECT} Vertical split screen: top half shows benefits of {{subject}} in bright warm colors, bottom half shows harms in dark cold tones. '
            'A narrator explains in Urdu: "{dialogue}" '
            'Dramatic lighting contrast. Audio: tense background music, clear Urdu voice. (no subtitles)'
        ),
    ],
    "Kitchen & Cooking Tips": [
        (
            f'{VEO3_ASPECT} Close-up portrait shot of hands preparing {{subject}} on a rustic wooden surface. '
            'Steam rises beautifully. A warm Urdu voice narrates: "{dialogue}" '
            'Golden kitchen lighting. Audio: gentle cooking sounds, soothing Urdu voice. (no subtitles)'
        ),
    ],
    "Satisfying Food Videos": [
        (
            f'{VEO3_ASPECT} Top-down portrait close-up of hands precisely doing {{subject}}. Every movement is satisfying. '
            'Camera slowly pulls back. '
            'Audio: crisp ASMR sounds, soft lo-fi music. No voice. (no subtitles)'
        ),
    ],
    "Junk Food Nuqsanat": [
        (
            f'{VEO3_ASPECT} Dramatic vertical cinematic shot of {{subject}} on a table, lit with dark red warning lighting. '
            'It slowly transforms to show its harmful effects inside the body. '
            'Narrator says in Urdu: "{dialogue}" '
            'Tense dramatic music, serious Urdu voice. (no subtitles)'
        ),
        (
            f'{VEO3_ASPECT} Medium portrait shot of a person happily eating {{subject}}, then cut to showing the damage it causes — side by side comparison. '
            'Narrator warns in Urdu: "{dialogue}" '
            'Audio: shocking music sting, urgent Urdu voice. (no subtitles)'
        ),
    ],
}

# ─── Urdu Script Dialogues (for proper Veo3 pronunciation) ───────────────────

DIALOGUES = {
    "Talking Fruits & Vegetables": {
        "apple": [
            "روز ایک سیب کھاؤ اور ڈاکٹر کی ضرورت نہیں۔ یہ میری طرف سے فری مشورہ ہے!",
            "مجھ میں فائبر ہے، وٹامنز ہیں، اور تمہاری چپس کی عادت پر بہت دکھ ہے۔",
            "تمہارے جسم کو میری ضرورت ہے، لیکن تم جنک فوڈ کے پیچھے بھاگ رہے ہو۔",
        ],
        "banana": [
            "میں پرفیکٹ سنیک ہوں بھائی۔ اپنا ریپر بھی ساتھ لاتا ہوں۔ چپس میں یہ بات ہے؟",
            "پوٹاشیم، انرجی، خوشی — سب کچھ ہے مجھ میں۔ اور صرف سو کیلوریز۔ کھاؤ مجھے!",
            "صبح کا پہلا کام — کیلا کھاؤ۔ انرجی دن بھر رہے گی، پرامس!",
        ],
        "avocado": [
            "ہاں بھائی مہنگا ہوں۔ لیکن ہسپتال کا بل دیکھا ہے؟ میں سستا آپشن ہوں۔",
            "ہیلتھی فیٹس، فائبر، اور بیس طرح کے وٹامنز۔ میں بنیادی طور پر ملٹی وٹامن ہوں۔",
            "ٹوسٹ پر لگاؤ، سلاد میں ڈالو — بس مجھے نظرانداز مت کرو!",
        ],
        "mango": [
            "پھلوں کا بادشاہ ہوں میں۔ سیزن آئے تو مجھے ضرور کھانا!",
            "وٹامن اے، سی، فائبر — اور ذائقہ تو پوچھو ہی مت۔ پھلوں کا بادشاہ ہوں بھائی!",
            "لوگ ڈائیٹ کے نام پر مجھ سے دور بھاگتے ہیں۔ ارے اعتدال میں کھاؤ!",
        ],
        "watermelon": [
            "گرمی میں مجھ سے بہتر کوئی نہیں۔ پانی بھی ملے گا اور مزا بھی!",
            "پانی کی کمی کا علاج ہوں میں۔ کولڈ ڈرنک چھوڑو، مجھے کھاؤ!",
        ],
        "lemon": [
            "صبح گرم پانی میں میرا رس ڈالو۔ میٹابولزم کافی سے بھی پہلے جاگ جائے گا۔",
            "نیمبو پانی پیو، تازہ رہو۔ یہ دیسی نسخہ ہے اور کام کرتا ہے!",
        ],
        "orange": [
            "وٹامن سی کا بادشاہ ہوں میں۔ بیمار ہونے سے پہلے مجھے کھاؤ، بعد میں نہیں!",
            "مجھے جوس بنا کر مت پیو، سیدھا کھاؤ۔ فائبر بھی ملے گا!",
        ],
        "pomegranate": [
            "خون بڑھانا ہے؟ مجھ سے پوچھو۔ انار کا جوس روز پیو، فرق دکھ جائے گا!",
            "اینٹی آکسیڈنٹس اتنے ہیں مجھ میں کہ بیماریاں دور ہی رہتی ہیں۔",
        ],
        "carrot": [
            "تمہاری دادی صحیح کہتی تھیں — میں آنکھوں کے لیے اچھا ہوں۔ اور جلد کے لیے بھی!",
            "سنیک بن سکتا ہوں، جوس بن سکتا ہوں، حلوہ بھی۔ ورسٹائل بادشاہ ہوں!",
        ],
        "broccoli": [
            "بچے مجھ سے نفرت کرتے ہیں، لیکن قوت مدافعت مجھ سے پیار کرتی ہے!",
            "سنترے سے زیادہ وٹامن سی، دودھ سے زیادہ کیلشیم۔ پھر بھی نظرانداز؟",
        ],
        "spinach": [
            "پوپائی نے مجھے کھا کر طاقت پائی تھی۔ تم کیوں نہیں کھاتے؟",
            "پالک پنیر بنا لو، سموتھی میں ڈالو — بس مجھے ضائع مت کرو!",
        ],
        "garlic": [
            "ہاں سانس میں بو آتی ہے۔ لیکن قوت مدافعت اتنی مضبوط ہو جاتی ہے!",
            "کھانے میں اگر میں نہیں تو ذائقہ بھی نہیں اور صحت بھی نہیں!",
        ],
        "ginger": [
            "گلا خراب ہے؟ ادرک کی چائے پیو۔ میں قدرتی دوائی ہوں!",
            "ہاضمے کا مسئلہ؟ ادرک کھاؤ۔ صدیوں سے کام کر رہا ہوں!",
        ],
        "turmeric": [
            "ہلدی کے بغیر نہ کھانا مکمل ہے نہ صحت۔ میں سب کا علاج ہوں!",
            "سوزش ختم کرنے والی، جراثیم کش — بھائی میں تو دوائیوں کی ماں ہوں!",
        ],
        "tomato": [
            "لائکوپین مجھ میں ہے — دل کی صحت کے لیے بہترین ہوں میں!",
            "ہر کھانے میں میں ہوں — سلاد، سالن، چٹنی۔ مجھ سے بڑھ کر کون؟",
        ],
        "onion": [
            "رلاتا ہوں، پتا ہے۔ لیکن قوت مدافعت ایسی بناتا ہوں کہ بیماری روئے!",
            "کچا کھاؤ یا پکاؤ، دونوں طریقے سے فائدہ مند ہوں۔ سوچ لو!",
        ],
        "cucumber": [
            "گرمی میں مجھے کھاؤ۔ پانی، وٹامنز، اور ٹھنڈک — سب ملے گا!",
            "وزن کم کرنا ہے؟ میں تمہارا بہترین دوست ہوں۔ کم کیلوریز، زیادہ فائدہ!",
        ],
        "_default": [
            "اوئے! ہاں تم — جو پراسیسڈ فوڈ کھا رہے ہو۔ ادھر آؤ، مجھ سے بات کرو!",
            "میں صرف کھانا نہیں ہوں — میں دوائی ہوں۔ ایسے ٹریٹ کرو مجھے!",
            "تمہاری صحت تمہارے ہاتھ میں ہے۔ اور میں تمہارے ہاتھ میں ہونا چاہیے!",
        ],
    },
    "Health & Wellness": {
        "_default": [
            "یہ ایک سادہ تبدیلی نے میری پوری انرجی بدل دی۔ سنو دھیان سے!",
            "سائنس کہتی ہے یہ سب سے کم سمجھی جانے والی صحت کی عادت ہے۔",
            "میں نے یہ تیس دن کیا اور نتائج نے مجھے بھی حیران کر دیا!",
            "جب تم یہ روز کرنا شروع کرو گے، جسم خود شکریہ کہے گا۔",
            "یہ عادت چھوٹی سی ہے لیکن اثر بہت بڑا ہے۔ آج سے شروع کرو!",
            "تمہارا جسم تمہیں کچھ بتانا چاہتا ہے۔ سنو تو سہی!",
        ],
    },
    "Fayde aur Nuqsanat": {
        "mobile phone": [
            "ایک طرف دنیا مٹھی میں ہے، دوسری طرف آنکھیں، نیند، اور صحت خراب۔ سوچ لو!",
            "موبائل تمہارا نوکر ہے یا تم اس کے؟ زیادہ استعمال کا یہ ہے نقصان!",
            "دو گھنٹے سے زیادہ سکرین ٹائم؟ تمہارے دماغ اور آنکھوں کو خطرہ ہے!",
        ],
        "social media": [
            "جوڑتا ہے لیکن ذہنی طور پر الگ بھی کر دیتا ہے۔ بیلنس رکھو!",
            "سکرولنگ میں وقت گزر جاتا ہے، لیکن کیا سچ میں کچھ حاصل ہوتا ہے؟",
            "موازنے کی بیماری سوشل میڈیا سے آتی ہے۔ اپنی زندگی پر فوکس کرو!",
        ],
        "junk food": [
            "ذائقہ ایک منٹ کا، لیکن صحت کا نقصان زندگی بھر کا۔ یہ سودا ٹھیک نہیں!",
            "برگر، پیزا، فرائز — سب ملا کر تمہارے جسم کو کیا دے رہے ہو؟ صرف فیٹ!",
        ],
        "cold drinks": [
            "ایک گلاس میں دس چمچ چینی۔ یہ تم روز پی رہے ہو۔ سوچ لو!",
            "ٹھنڈا پینا ہے تو پانی پیو۔ کولڈ ڈرنک تمہاری ہڈیوں کو کمزور کرتی ہے!",
        ],
        "chai": [
            "ایک دو کپ ٹھیک ہے، لیکن دن میں چھ؟ تمہارا پیٹ اور نیند دونوں خراب!",
            "چائے کے فائدے بھی ہیں — اینٹی آکسیڈنٹس۔ لیکن بغیر چینی پیو تو اور اچھا!",
        ],
        "coffee": [
            "صبح کی کافی سے انرجی ملتی ہے، لیکن رات کو پیو تو نیند اڑ جاتی ہے!",
            "ایک کپ کافی ہے — لٹرلی۔ زیادہ کافی اینگزائٹی اور ایسیڈیٹی کرتا ہے۔",
        ],
        "earphones": [
            "دن بھر ایئرفونز لگائے ہو؟ تمہاری سماعت خطرے میں ہے۔ والیوم کم کرو!",
            "میوزک سننا اچھا ہے لیکن ایک گھنٹے سے زیادہ ایئرفونز مت لگاؤ۔ کان کا خیال رکھو!",
        ],
        "sugar": [
            "چینی میٹھی ہے لیکن اثر کڑوا ہے۔ ذیابیطس، موٹاپا، دل کا مسئلہ — سب اس کا کام!",
            "دن میں چھ چمچ سے زیادہ شوگر؟ تم اپنے جسم کے ساتھ ظلم کر رہے ہو!",
        ],
        "screen time": [
            "دن بھر سکرین دیکھنے سے آنکھیں، نیند، دماغ — سب متاثر ہوتا ہے۔ بریک لو!",
            "ہر بیس منٹ میں بیس سیکنڈ کے لیے بیس فٹ دور دیکھو۔ بیس بیس بیس کا اصول یاد رکھو!",
        ],
        "fast food": [
            "جلدی ملتا ہے، جلدی کھایا جاتا ہے، لیکن جسم کو جلدی خراب بھی کرتا ہے!",
            "ایک ہفتہ فاسٹ فوڈ بند کرو۔ فرق خود محسوس کرو گے!",
        ],
        "_default": [
            "ہر چیز کے دو پہلو ہوتے ہیں۔ آؤ دیکھتے ہیں فائدے اور نقصانات!",
            "یہ چیز کتنی فائدہ مند ہے اور کتنی نقصاندہ — آج جانتے ہیں!",
            "حد میں استعمال کرو تو فائدہ، زیادہ کرو تو نقصان۔ یہ ہے اصلی بات!",
        ],
    },
    "Kitchen & Cooking Tips": {
        "_default": [
            "یہ دیسی نسخہ سالوں سے کام کر رہا ہے۔ آج تم بھی آزماؤ!",
            "نانی کہتی تھیں روز یہ کھاؤ۔ سائنس نے بھی صحیح ثابت کر دیا!",
            "صبح خالی پیٹ یہ لو — دن بھر انرجی رہے گی، پکا!",
            "یہ کمبینیشن صحت کے لیے کمال ہے۔ آج سے شروع کرو!",
            "کچن میں یہ چیز ہے؟ تو تم ڈاکٹر کے پاس جانا بھول جاؤ!",
        ],
    },
    "Satisfying Food Videos": {
        "_default": [],  # No dialogue — ASMR only
    },
    "Junk Food Nuqsanat": {
        "burger": [
            "یہ برگر جتنا لذیذ ہے، اتنا ہی تمہارے دل کے لیے خطرناک ہے ۔ سوچلو!",
            "ایک برگر میں اتنی کیلوریز ہیں جو آدھے دن کی ضرورت ہے۔ روز کھاؤ تو سوچو کیا ہوگا!",
        ],
        "pizza": [
            "پیزہ کی ئیک سلائس میں تمہارہ پورے دن کی شوگر سے زیادہ چینی ہے۔ ہوش کرو!",
            "ہفتے میں ایک سے زیادہ پیزہ کھانا وزن بڑھانے کی سب سے آسان راہ ہے!",
        ],
        "cold drink": [
            "ایک گلاس میں دس چمچ چینی۔ یہ تم روز پی رہے ہو۔ سوچلو!",
            "کولڈ ڈرنک تمہاری ہڈیوں، دانتوں، اور پیٹ کو خراب کر رہی ہے۔ پانی پیو!",
        ],
        "chips": [
            "چپس میں کیا ہے; نمک، تیل، اور خالی کیلوریز۔ تمہارے جسم کو کچھ نہیں ملتا!",
            "چپس کی بیگ کھول کے بیٹھ جاؤ تو رکنا مشکل ہو جاتا ہے۔ یہی ہے مسئلہ!",
        ],
        "instant noodles": [
            "فوری نوڈلز میں سوڈیم اتنا زیادہ ہے کہ آپ کی کدمبندی متاثر ہو سکتی ہے!",
            "جلدی تیار ہونے والی یہ چیز تمہارے جسم کو آہستہ آہستہ خراب کر رہی ہے!",
        ],
        "_default": [
            "یہ چیز جتنی لذیذ ہے، اتنی ہی تمہاری صحت کی دشمن ہے۔ سوچلو!",
            "ایک ہفتہ یہ کھانا بند کرو۔ تمہارا جسم خود شکریہ کہے گا!",
            "یہ فوڈ تمہیں خوش کرتا ہے لیکن تمہاری صحت برباد کرتا ہے۔ آگاہ رہو!",
        ],
    },
}

# ─── Video Series Templates (3-5 connected clips for longer video) ───────────────────

SERIES_ASPECT = "Vertical 9:16 portrait frame, optimized for Reels and TikTok."

VIDEO_SERIES = [
    {
        "title": "Fruit ki Kahani — {subject}",
        "category": "Talking Fruits & Vegetables",
        "clips": [
            {
                "clip_title": "Part 1: Taaruf",
                "prompt": (
                    f'{SERIES_ASPECT} Close-up of a {{subject}} with cute cartoon face sitting alone in a dark fridge. '
                    'It opens its eyes, looks at camera and says in Urdu: "{intro_dialogue}" '
                    'Blue refrigerator light. Camera slowly pushes in. Audio: mysterious music, curious Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Assalam o alaikum! Main hoon {subject}, aur aaj main tumhe apni kahani sunaata hoon.",
                    "Suno yaar, main {subject} hoon. Aur tumhe mujhse milna chahiye tha bohot pehle!",
                ],
            },
            {
                "clip_title": "Part 2: Fayde",
                "prompt": (
                    'Medium shot of {subject} with animated face now standing proudly on a kitchen counter in bright sunlight. '
                    'It puffs up with pride and says: "{benefit_dialogue}" '
                    'Warm kitchen lighting, camera at eye level. Audio: upbeat happy music, confident Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Mujh mein itne vitamins hain ke list sunao ge toh thak jao ge. Main tumhari sehat ka bodyguard hoon!",
                    "Doctor se bachna hai? Mujhe roz khao. Main tumhare jism ka best friend hoon!",
                    "Immunity chahiye? Energy chahiye? Sab mujh mein hai. Khaao aur dekho kamal!",
                ],
            },
            {
                "clip_title": "Part 3: Junk Food ko Daant",
                "prompt": (
                    'Wide shot of {subject} angrily confronting a burger and fries on the counter. '
                    '{subject} points at them and says: "{roast_dialogue}" '
                    'Dramatic lighting, split warm/cold tones. Audio: dramatic music sting, angry Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Tum! Burger! Tum ne insaanon ki sehat barbaad kar di hai! Sharam karo!",
                    "Chips aur cold drinks — tum log fraud ho! Taste dete ho lekin sehat lete ho!",
                    "Junk food se door raho. Woh dost nahi hai, dushman hai tumhari sehat ka!",
                ],
            },
            {
                "clip_title": "Part 4: Khatma — Final Message",
                "prompt": (
                    'Close-up of {subject} looking warmly at camera, gentle smile on its animated face. '
                    'Soft golden sunset light through kitchen window. It says softly: "{final_dialogue}" '
                    'Camera slowly dollies out. Audio: emotional soft music, warm Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Yaad rakhna — tumhari sehat tumhare haath mein hai. Aur main tumhare haath mein hona chahiye. Khuda hafiz!",
                    "Roz thoda sa healthy khao. Chhoti si aadat badi tabdili laati hai. Allah hafiz dosto!",
                    "Mujhe kha ke dekho, fark mehsoos karo ge. Yeh vaada hai mera. Phir milte hain!",
                ],
            },
        ],
    },
    {
        "title": "Fayde aur Nuqsanat — {subject}",
        "category": "Fayde aur Nuqsanat",
        "clips": [
            {
                "clip_title": "Part 1: Introduction",
                "prompt": (
                    'Cinematic medium shot of {subject} placed dramatically on a podium with spotlight on it. '
                    'A narrator voice in Urdu says: "{intro_dialogue}" '
                    'Dark background, single dramatic spotlight. Audio: suspenseful music, deep Urdu narrator. (no subtitles)'
                ),
                "dialogues": [
                    "Aaj hum baat karenge {subject} ke baare mein. Kitna faydamand hai aur kitna nuqsandeh? Chalo dekhte hain!",
                    "{subject} — har ghar mein hai, har koi use karta hai. Lekin kya tum jaante ho iske asli fayde aur nuqsanat?",
                ],
            },
            {
                "clip_title": "Part 2: Fayde bataao",
                "prompt": (
                    'Bright, warm-toned scene showing positive uses of {subject} with green check marks appearing. '
                    'Narrator explains happily in Urdu: "{benefit_dialogue}" '
                    'Warm golden lighting, upbeat energy. Audio: positive uplifting music, enthusiastic Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "{subject} ke bohot se fayde hain. Yeh connect karta hai, seekhne mein madad karta hai, aur time bachata hai!",
                    "Sahi tareeqe se use karo toh {subject} tumhara sabse acha saathi ban sakta hai!",
                ],
            },
            {
                "clip_title": "Part 3: Nuqsanat bataao",
                "prompt": (
                    'Dark, cold-toned scene showing negative effects of {subject} with red warning signs appearing. '
                    'Narrator warns seriously in Urdu: "{harm_dialogue}" '
                    'Harsh cold lighting, tense atmosphere. Audio: dramatic warning music, serious Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Lekin zyada use karo toh? Neend kharab, sehat kharab, rishtay kharab. Yeh hai doosra pehlu!",
                    "Limit se bahar jao toh {subject} fayde ki jagah nuqsan dena shuru kar deta hai. Khabardar!",
                ],
            },
            {
                "clip_title": "Part 4: Balance — Final Advice",
                "prompt": (
                    'Balanced scene with warm and cool tones side by side. {subject} in the center. '
                    'Narrator gives final advice in Urdu: "{final_dialogue}" '
                    'Balanced lighting. Audio: calming resolve music, wise Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Koi bhi cheez limit mein achi hai. {subject} bhi isi usool pe chalta hai. Balance rakho, sehatmand raho!",
                    "Toh yaad rakhna — {subject} ko samajhdaari se use karo. Har cheez ka balance zaroori hai. Shukriya!",
                ],
            },
        ],
    },
    {
        "title": "Desi Nuskha Series — {subject}",
        "category": "Kitchen & Cooking Tips",
        "clips": [
            {
                "clip_title": "Part 1: Intro & Ingredients",
                "prompt": (
                    'Top-down shot of {subject} ingredients beautifully arranged on a rustic table. '
                    'A warm Urdu voice says: "{intro_dialogue}" '
                    'Warm morning light. Audio: gentle music, friendly Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Aaj ka desi nuskha — {subject}! Nani ka totka jo science ne bhi sahi maana. Chalo banaate hain!",
                    "Yeh hai {subject} ka nuskha. Simple hai, asardaar hai, aur ghar mein sab kuch mojood hai!",
                ],
            },
            {
                "clip_title": "Part 2: Banaane ka tareeqa",
                "prompt": (
                    'Close-up of hands carefully preparing {subject}. Steam rising, beautiful textures visible. '
                    'Narrator guides in Urdu: "{method_dialogue}" '
                    'Warm kitchen lighting. Audio: cooking ASMR sounds, calm instructive Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Pehle yeh lo, phir yeh milaao. Dhyan se — quantity bilkul sahi honi chahiye!",
                    "Ek chamach yeh, do chamach woh, aur thoda sa pyaar — ban gaya perfect {subject}!",
                ],
            },
            {
                "clip_title": "Part 3: Fayde bataao",
                "prompt": (
                    'Medium shot of the finished {subject} looking beautiful and appetizing. '
                    'Narrator proudly explains in Urdu: "{benefit_dialogue}" '
                    'Golden warm lighting. Audio: satisfying reveal sound, proud Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Roz istemaal karo toh immunity badhe gi, energy aaye gi, aur bimari door rahegi!",
                    "Yeh nuskha tumhari sehat ke liye kamaal karega. Bus ek hafta try karo!",
                ],
            },
        ],
    },
    {
        "title": "Health Transformation — {subject}",
        "category": "Health & Wellness",
        "clips": [
            {
                "clip_title": "Part 1: Problem",
                "prompt": (
                    'Dark moody shot of a tired, exhausted person struggling with effects of not doing {subject}. '
                    'Narrator says in Urdu: "{problem_dialogue}" '
                    'Gray tones, low energy atmosphere. Audio: somber music, empathetic Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Thakawat, kamzori, mood swings — yeh sab hota hai jab tum {subject} ignore karte ho.",
                    "Kya tum bhi roz yeh mehsoos karte ho? Thaka hua, bejan, energy zero? Iska hal hai!",
                ],
            },
            {
                "clip_title": "Part 2: Solution",
                "prompt": (
                    'Scene brightens dramatically. Same person now energetic, practicing {subject}. '
                    'Narrator explains in Urdu: "{solution_dialogue}" '
                    'Warm bright lighting transition. Audio: uplifting music, motivating Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Bas yeh ek kaam shuru karo — {subject}. Aur dekho kaise zindagi badal jaati hai!",
                    "{subject} shuru karo. Pehle haftay mushkil lagega. Doosre haftay fark dikhega. Teesre mein log poochenge!",
                ],
            },
            {
                "clip_title": "Part 3: Result & Motivation",
                "prompt": (
                    'Inspirational wide shot of the transformed person, confident and glowing, outdoors in sunrise. '
                    'Person looks at camera and says in Urdu: "{result_dialogue}" '
                    'Beautiful golden sunrise. Audio: triumphant music, inspired Urdu voice. (no subtitles)'
                ),
                "dialogues": [
                    "Aaj se shuru karo. Kal ka tumhara version tumhe shukriya kahega. Yeh vaada hai!",
                    "Chhoti si aadat, bada fark. {subject} ne meri zindagi badal di. Ab tumhari baari hai!",
                ],
            },
        ],
    },
]


def _get_dialogue(category, subject):
    """Get a random dialogue for given category and subject."""
    cat = DIALOGUES.get(category, {})
    lines = cat.get(subject, cat.get("_default", []))
    if not lines:
        return "Kya tumhe pata hai? Tumhari roz ki aadatein tumhari sehat pe sabse zyada asar dalti hain!"
    return random.choice(lines)


def _generate_prompt_set(categories, count, seed_str):
    """Generate prompts for a specific time period."""
    random.seed(seed_str)
    prompts = []
    shuffled = list(categories)
    random.shuffle(shuffled)

    idx = 0
    while len(prompts) < count:
        cat = shuffled[idx % len(shuffled)]
        category_name = cat["category"]
        subject = random.choice(cat["subjects"])
        angle = random.choice(cat["angles"])
        style = random.choice(IMAGE_STYLES)
        dialogue = _get_dialogue(category_name, subject)

        img_templates = IMAGE_TEMPLATES.get(category_name, [])
        image_prompt = random.choice(img_templates).format(subject=subject, style=style) if img_templates else f"Stunning image of {subject}, {style}"

        veo3_templates = VEO3_TEMPLATES.get(category_name, [])
        if veo3_templates:
            veo3_prompt = random.choice(veo3_templates).format(subject=subject, dialogue=dialogue)
        else:
            veo3_prompt = f'Cinematic shot of {subject}. Urdu voiceover: "{dialogue}" Audio: music, Urdu voice. (no subtitles)'

        prompts.append({
            "category": category_name,
            "subject": subject,
            "angle": angle,
            "image_prompt": image_prompt,
            "veo3_prompt": veo3_prompt,
        })
        idx += 1

    return prompts


def _generate_fruits_section(seed_str):
    """Generate 5 prompts specifically for Fruits & Vegetables."""
    fruits_cat = [c for c in VIRAL_CATEGORIES if c["category"] == "Talking Fruits & Vegetables"]
    return _generate_prompt_set(fruits_cat, 5, f"fruits-{seed_str}")


def _generate_video_series(seed_str):
    """Generate a connected video series (3-5 clips that make a longer video)."""
    random.seed(f"series-{seed_str}")

    series_template = random.choice(VIDEO_SERIES)
    category = series_template["category"]

    # Pick a subject from the matching category
    matching_cats = [c for c in VIRAL_CATEGORIES if c["category"] == category]
    if matching_cats:
        subject = random.choice(matching_cats[0]["subjects"])
    else:
        subject = "apple"

    series_title = series_template["title"].format(subject=subject)
    clips = []

    for clip_tmpl in series_template["clips"]:
        dialogue_key = [k for k in clip_tmpl if k.endswith("_dialogue")]
        # Pick random dialogues for each slot
        filled_prompt = clip_tmpl["prompt"]
        for key in ["intro_dialogue", "benefit_dialogue", "roast_dialogue", "final_dialogue",
                     "harm_dialogue", "method_dialogue", "problem_dialogue", "solution_dialogue",
                     "result_dialogue"]:
            if "{" + key + "}" in filled_prompt:
                lines = clip_tmpl.get("dialogues", [])
                chosen = random.choice(lines) if lines else "Yeh bohot zaroori hai, dhyan se suno!"
                chosen = chosen.format(subject=subject)
                filled_prompt = filled_prompt.replace("{" + key + "}", chosen)

        filled_prompt = filled_prompt.replace("{subject}", subject)

        clips.append({
            "clip_title": clip_tmpl["clip_title"],
            "veo3_prompt": filled_prompt,
        })

    # Generate one image prompt for the series thumbnail
    style = random.choice(IMAGE_STYLES)
    img_templates = IMAGE_TEMPLATES.get(category, [])
    if img_templates:
        image_prompt = random.choice(img_templates).format(subject=subject, style=style)
    else:
        image_prompt = f"Stunning image of {subject}, {style}"

    return {
        "title": series_title,
        "subject": subject,
        "category": category,
        "image_prompt": image_prompt,
        "clips": clips,
        "total_duration": f"~{len(clips) * 8} seconds",
    }


def generate_prompts(trending_data=None, fresh_seed=None):
    """
    Generate all prompt sections.
    Pass fresh_seed (any string/number) to get different results on demand.
    Without fresh_seed: daily/weekly/monthly slots rotate on schedule.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    week_str = f"{now.year}-W{now.isocalendar()[1]}"
    month_str = now.strftime("%Y-%m")

    # fresh_seed lets the refresh button produce varied prompts within same day
    extra = f"-{fresh_seed}" if fresh_seed else ""

    daily_seed   = f"daily-{date_str}{extra}"
    weekly_seed  = f"weekly-{week_str}{extra}"
    monthly_seed = f"monthly-{month_str}{extra}"
    fruits_seed  = f"fruits-{date_str}{extra}"
    series_seed  = f"series-{date_str}{extra}"

    result = {
        "daily":   _generate_prompt_set(VIRAL_CATEGORIES, 5, daily_seed),
        "fruits":  _generate_prompt_set(
            [c for c in VIRAL_CATEGORIES if c["category"] == "Talking Fruits & Vegetables"],
            5, fruits_seed
        ),
        "series":  _generate_video_series(series_seed.replace("series-", "")),
        "weekly":  _generate_prompt_set(VIRAL_CATEGORIES, 5, weekly_seed),
        "monthly": _generate_prompt_set(VIRAL_CATEGORIES, 5, monthly_seed),
    }

    total = sum(len(v) for k, v in result.items() if isinstance(v, list))
    series_clips = len(result["series"].get("clips", []))
    print(f"  ✓ Generated {total} prompts + 1 video series ({series_clips} clips) [seed={extra or 'scheduled'}]")
    return result
