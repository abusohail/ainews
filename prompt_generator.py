"""
Prompt Generator — Creates AI image + Veo3 video prompts for viral content.
Focus: Fruits, Vegetables, Health, Mobile/Tech, Everyday Objects.
All dialogues in Roman Urdu.

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

IMAGE_STYLES = [
    "hyperrealistic photography, 8K, studio lighting, sharp focus",
    "3D Pixar-style render, vibrant colors, soft lighting, cute character design",
    "cinematic film still, shallow depth of field, warm golden hour lighting",
    "editorial magazine photography, clean background, professional lighting",
    "whimsical illustration style, pastel colors, dreamy atmosphere",
    "hyper-detailed macro photography, dramatic lighting, rich textures",
    "modern minimalist design, clean composition, vibrant accent colors",
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
]

# ─── Image Templates ─────────────────────────────────────────────────────────

IMAGE_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        "A {subject} with an expressive cartoon face (big eyes, wide smile), sitting on a kitchen counter, looking directly at camera, {style}",
        "Anthropomorphic {subject} character wearing tiny glasses, standing at a podium giving a speech about health, {style}",
        "A giant {subject} with a friendly face, arms and legs, pointing at a health facts poster in a kitchen, {style}",
        "Close-up of a {subject} with a sassy expression and raised eyebrow, sitting next to junk food it disapproves of, {style}",
        "A {subject} character dressed as a doctor with a tiny stethoscope, giving health advice, {style}",
    ],
    "Health & Wellness": [
        "Split-screen visual: left side showing a tired person in gray tones, right side showing an energetic person in vibrant colors, topic: {subject}, {style}",
        "A beautiful flat lay arrangement related to {subject}, shot from above on a marble surface with natural light, {style}",
        "Infographic-style image showing the benefits of {subject}, with simple icons, clean medical design, {style}",
        "A person practicing {subject} in a beautiful natural setting at sunrise, {style}",
    ],
    "Fayde aur Nuqsanat": [
        "A split image: left side green check marks showing advantages of {subject}, right side red crosses showing disadvantages, clean infographic style, {style}",
        "An anthropomorphic {subject} with an animated face, looking both helpful and dangerous, dual personality, {style}",
        "A dramatic scene showing {subject} with angel wings on one side and devil horns on the other, {style}",
        "A balance scale with benefits on one side and harms on other side about {subject}, {style}",
    ],
    "Kitchen & Cooking Tips": [
        "A beautiful overhead shot of {subject} ingredients laid out on a rustic wooden table, warm lighting, {style}",
        "An anthropomorphic {subject} character wearing an apron and chef hat, proudly showing off its recipe, {style}",
        "Close-up of {subject} being prepared, steam rising, warm cozy kitchen background, {style}",
    ],
    "Satisfying Food Videos": [
        "Top-down view of {subject}, perfectly organized, satisfying symmetry, clean workspace, {style}",
        "Close-up of hands doing {subject}, shallow depth of field, warm lighting, ASMR aesthetic, {style}",
        "Ingredients for {subject} laid out beautifully in rows, ready to begin, {style}",
    ],
}

# ─── Veo3 Templates ──────────────────────────────────────────────────────────

VEO3_TEMPLATES = {
    "Talking Fruits & Vegetables": [
        (
            'Close-up cinematic shot of a {subject} with an expressive animated face on a rustic cutting board in a sunlit kitchen. '
            'The {subject} looks at camera and speaks in confident Urdu: "{dialogue}" '
            'Camera slowly dollies in. Warm natural lighting. Audio: cheerful music, crisp Urdu voice. (no subtitles)'
        ),
        (
            'Medium shot of a {subject} with cartoon eyes standing on a kitchen counter next to junk food. '
            'It gestures dramatically and says in sassy Urdu: "{dialogue}" '
            'Camera at eye level. Bright kitchen lighting. Audio: comedic music, expressive Urdu voice. (no subtitles)'
        ),
    ],
    "Health & Wellness": [
        (
            'Cinematic tracking shot following a person demonstrating {subject}. '
            'Scene transitions from dark sluggish morning to vibrant energy. '
            'Voiceover in Urdu: "{dialogue}" '
            'Warm golden lighting. Audio: inspirational music, calm Urdu voice. (no subtitles)'
        ),
    ],
    "Fayde aur Nuqsanat": [
        (
            'Split screen cinematic shot. Left side shows the benefits of {subject} in bright warm colors. '
            'Right side shows the harms in dark cold tones. '
            'A narrator explains in Urdu: "{dialogue}" '
            'Dramatic lighting contrast. Audio: tense background music, clear Urdu voice. (no subtitles)'
        ),
        (
            'Medium shot of an anthropomorphic {subject} sitting at a talk show desk. '
            'It looks at camera seriously and says in Urdu: "{dialogue}" '
            'Studio lighting. Audio: news-style background music, professional Urdu voice. (no subtitles)'
        ),
    ],
    "Kitchen & Cooking Tips": [
        (
            'Close-up overhead shot of hands preparing {subject} on a rustic wooden surface. '
            'Steam rises beautifully. A warm Urdu voice narrates: "{dialogue}" '
            'Golden kitchen lighting. Audio: gentle cooking sounds, soothing Urdu voice. (no subtitles)'
        ),
    ],
    "Satisfying Food Videos": [
        (
            'Top-down close-up of hands precisely doing {subject}. Every movement is satisfying. '
            'Camera slowly pulls back to reveal the full scene. '
            'Audio: crisp ASMR sounds, soft lo-fi music. No voice. (no subtitles)'
        ),
    ],
}

# ─── Roman Urdu Dialogues ────────────────────────────────────────────────────

DIALOGUES = {
    "Talking Fruits & Vegetables": {
        "apple": [
            "Roz ek apple khao aur doctor ki zaroorat nahi. Yeh meri taraf se free mashwara hai!",
            "Mujh mein fiber hai, vitamins hain, aur tumhari chips ki aadat pe bohot dukh hai.",
            "Tumhare jism ko meri zaroorat hai, lekin tum junk food ke peechay bhaag rahe ho.",
        ],
        "banana": [
            "Main perfect snack hoon bhai. Apna wrapper bhi saath laata hoon. Chips mein yeh baat hai?",
            "Potassium, energy, khushi — sab kuch hai mujh mein. Aur sirf sau calories. Khao mujhe!",
            "Subah ka pehla kaam — banana khao. Energy din bhar rahegi, promise!",
        ],
        "avocado": [
            "Haan bhai mehenga hoon. Lekin hospital ka bill dekha hai? Main sasta option hoon.",
            "Healthy fats, fiber, aur bees tarah ke vitamins. Main basically multivitamin hoon.",
            "Toast pe lagao, salad mein daalo — bas mujhe ignore mat karo!",
        ],
        "mango": [
            "Phalon ka badshah hoon main. Season aaye toh mujhe zaroor khana!",
            "Vitamin A, C, fiber — aur taste toh poochho hi mat. King of fruits hoon bhai!",
            "Log diet ke naam pe mujhse door bhagte hain. Arre moderation mein khao!",
        ],
        "watermelon": [
            "Garmi mein mujhse behtar koi nahi. Paani bhi milega aur maza bhi!",
            "Dehydration ka ilaaj hoon main. Cold drink choro, mujhe khao!",
        ],
        "lemon": [
            "Subah garam paani mein mera ras daalo. Metabolism coffee se bhi pehle jaag jayega.",
            "Nimbu paani piyo, taza raho. Yeh desi nuskha hai aur kaam karta hai!",
        ],
        "orange": [
            "Vitamin C ka king hoon main. Bimaar hone se pehle mujhe khao, baad mein nahi!",
            "Mujhe juice bana ke mat piyo, seedha khao. Fiber bhi milega!",
        ],
        "pomegranate": [
            "Khoon badhana hai? Mujhse poochho. Anaar ka juice roz piyo, fark dikh jayega!",
            "Antioxidants itne hain mujh mein ke bimariyan door hi rehti hain.",
        ],
        "carrot": [
            "Tumhari dadi sahi kehti thi — main aankhon ke liye acha hoon. Aur skin ke liye bhi!",
            "Snack ban sakta hoon, juice ban sakta hoon, halwa bhi. Versatile king hoon!",
        ],
        "broccoli": [
            "Bachay mujhse nafrat karte hain, lekin immunity MUJHSE pyaar karti hai!",
            "Orange se zyada vitamin C, doodh se zyada calcium. Phir bhi ignore?",
        ],
        "spinach": [
            "Popeye ne mujhe kha ke taaqat payi thi. Tum kyun nahi khaate?",
            "Palak paneer bana lo, smoothie mein daalo — bas mujhe waste mat karo!",
        ],
        "garlic": [
            "Haan saans mein boo aati hai. Lekin immunity itni strong ho jaati hai!",
            "Khana mein agar main nahi toh taste bhi nahi aur sehat bhi nahi!",
        ],
        "ginger": [
            "Gala kharab hai? Adrak ki chai piyo. Main natural dawai hoon!",
            "Digestion ka masla? Adrak khao. Centuries se kaam kar raha hoon!",
        ],
        "turmeric": [
            "Haldi ke baghair na khana mukammal hai na sehat. Main sab ka ilaaj hoon!",
            "Anti-inflammatory, antiseptic — bhai main toh dawaiyon ki maa hoon!",
        ],
        "tomato": [
            "Lycopene mujh mein hai — dil ki sehat ke liye behtareen hoon main!",
            "Har khane mein main hoon — salad, curry, chutney. Mujhse badhkar kaun?",
        ],
        "onion": [
            "Rulaata hoon, pata hai. Lekin immunity aisi banaata hoon ke bimari roye!",
            "Kachha khao ya pakao, dono tareeqe se faydemand hoon. Sochlo!",
        ],
        "cucumber": [
            "Garmi mein mujhe khao. Paani, vitamins, aur thandak — sab milega!",
            "Weight loss karna hai? Main tumhara best friend hoon. Kam calories, zyada fayda!",
        ],
        "_default": [
            "Oye! Haan tum — jo processed food kha rahe ho. Idhar aao, mujhse baat karo!",
            "Main sirf khana nahi hoon — main dawai hoon. Aise treat karo mujhe!",
            "Tumhari sehat tumhare haath mein hai. Aur main tumhare haath mein hona chahiye!",
        ],
    },
    "Health & Wellness": {
        "_default": [
            "Yeh ek simple change ne meri poori energy badal di. Suno dhyan se!",
            "Science kehti hai yeh sabse underrated health habit hai.",
            "Maine yeh 30 din kiya aur results ne mujhe bhi hairan kar diya!",
            "Jab tum yeh roz karna shuru karo ge, jism khud shukriya kahega.",
            "Yeh aadat chhoti si hai lekin asar bohot bada hai. Aaj se shuru karo!",
            "Tumhara jism tumhe kuch batana chahta hai. Suno toh sahi!",
        ],
    },
    "Fayde aur Nuqsanat": {
        "mobile phone": [
            "Ek taraf duniya mutthi mein hai, doosri taraf aankhein, neend, aur sehat kharab. Sochlo!",
            "Mobile tumhara naukar hai ya tum uske? Zyada use ka yeh hai nuksan!",
            "Do ghante se zyada screen time? Tumhare dimagh aur aankhon ko khatra hai!",
        ],
        "social media": [
            "Connect karta hai lekin mentally disconnect bhi kar deta hai. Balance rakho!",
            "Scrolling mein waqt guzar jaata hai, lekin kya sach mein kuch haasil hota hai?",
            "Comparison ki bimari social media se aati hai. Apni zindagi pe focus karo!",
        ],
        "junk food": [
            "Taste ek minute ka, lekin sehat ka nuqsan zindagi bhar ka. Yeh soudah theek nahi!",
            "Burger, pizza, fries — sab mila ke tumhare jism ko kya de rahe ho? Sirf fat!",
        ],
        "cold drinks": [
            "Ek glass mein das chamach cheeni. Yeh tum pi rahe ho roz. Sochlo!",
            "Thanda peena hai toh paani piyo. Cold drink tumhare haddiyon ko kamzor karti hai!",
        ],
        "chai": [
            "Ek do cup theek hai, lekin din mein cheh? Tumhara pet aur neend dono kharab!",
            "Chai ke fayde bhi hain — antioxidants. Lekin bina cheeni piyo toh aur acha!",
        ],
        "coffee": [
            "Subah ki coffee se energy milti hai, lekin raat ko piyo toh neend ud jaati hai!",
            "Ek cup kafi hai — literally. Zyada coffee anxiety aur acidity karta hai.",
        ],
        "earphones": [
            "Din bhar earphones lagaye ho? Tumhari hearing danger mein hai. Volume kam karo!",
            "Music sunna acha hai lekin ek ghante se zyada earphones mat lagao. Kaan ka khayal rakho!",
        ],
        "sugar": [
            "Cheeni meethi hai lekin asar kadwa hai. Diabetes, obesity, dil ka masla — sab iska kaam!",
            "Din mein cheh chamach se zyada sugar? Tum apne jism ke saath zulm kar rahe ho!",
        ],
        "screen time": [
            "Din bhar screen dekhne se aankhein, neend, dimagh — sab affect hota hai. Break lo!",
            "Har bees minute mein bees second ke liye bees feet door dekho. 20-20-20 rule yaad rakho!",
        ],
        "fast food": [
            "Jaldi milta hai, jaldi khaya jaata hai, lekin jism ko jaldi kharab bhi karta hai!",
            "Ek hafta fast food bandh karo. Fark khud mehsoos karo ge!",
        ],
        "_default": [
            "Har cheez ke do pehlu hote hain. Aao dekhte hain fayde aur nuqsanat!",
            "Yeh cheez kitni faydamand hai aur kitni nuqsandeh — aaj jaante hain!",
            "Limit mein use karo toh fayda, zyada karo toh nuksan. Yeh hai asli baat!",
        ],
    },
    "Kitchen & Cooking Tips": {
        "_default": [
            "Yeh desi nuskha saalon se kaam kar raha hai. Aaj tum bhi aazmaao!",
            "Nani kehti thi roz yeh khao. Science ne bhi sahi sabit kar diya!",
            "Subah khaali pet yeh lo — din bhar energy rahegi, pakka!",
            "Yeh combination sehat ke liye kamaal hai. Try karo aaj se!",
            "Kitchen mein yeh cheez hai? Toh tum doctor ke paas jaana bhool jao!",
        ],
    },
    "Satisfying Food Videos": {
        "_default": [],  # No dialogue — ASMR only
    },
}

# ─── Video Series Templates (3-5 connected clips for longer video) ───────────

VIDEO_SERIES = [
    {
        "title": "Fruit ki Kahani — {subject}",
        "category": "Talking Fruits & Vegetables",
        "clips": [
            {
                "clip_title": "Part 1: Introduction",
                "prompt": (
                    'Close-up of a {subject} with cute cartoon face sitting alone in a dark fridge. '
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


def generate_prompts(trending_data=None):
    """
    Generate all prompt sections:
    - daily: 5 mixed viral prompts
    - fruits: 5 fruits & vegetables prompts
    - series: 1 connected video series (3-5 clips)
    - weekly: 5 weekly prompts
    - monthly: 5 monthly prompts
    """
    now = datetime.now(timezone.utc)
    daily_seed = now.strftime("%Y-%m-%d")
    weekly_seed = f"{now.year}-W{now.isocalendar()[1]}"
    monthly_seed = now.strftime("%Y-%m")

    result = {
        "daily": _generate_prompt_set(VIRAL_CATEGORIES, 5, f"daily-{daily_seed}"),
        "fruits": _generate_fruits_section(daily_seed),
        "series": _generate_video_series(daily_seed),
        "weekly": _generate_prompt_set(VIRAL_CATEGORIES, 5, f"weekly-{weekly_seed}"),
        "monthly": _generate_prompt_set(VIRAL_CATEGORIES, 5, f"monthly-{monthly_seed}"),
    }

    total = len(result["daily"]) + len(result["fruits"]) + len(result["weekly"]) + len(result["monthly"])
    series_clips = len(result["series"]["clips"])
    print(f"  ✓ Generated {total} prompts + 1 video series ({series_clips} clips)")
    return result
