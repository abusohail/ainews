"""
Flask app — serves the viral prompts dashboard.
Run: python app.py
Visit: http://localhost:5000
"""

from flask import Flask, jsonify, send_from_directory, request
import os
import random
from prompt_generator import generate_prompts, IMAGE_STYLES, VEO3_ASPECT, SERIES_ASPECT

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/prompts")
def api_prompts():
    try:
        # fresh_seed passed from frontend refresh button — gives different prompts each click
        fresh_seed = request.args.get("fresh", None)
        data = generate_prompts(fresh_seed=fresh_seed)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/custom", methods=["POST"])
def api_custom():
    try:
        body = request.get_json()
        name = body.get("name", "").strip()
        mode = body.get("mode", "both")          # "advantage", "disadvantage", "both"
        instructions = body.get("instructions", "").strip()
        series = body.get("series", False)        # bool: generate series of clips

        if not name:
            return jsonify({"success": False, "error": "Name is required"}), 400

        style = random.choice(IMAGE_STYLES)

        # Build context string
        if mode == "advantage":
            angle_en = f"showing the advantages and benefits of {name}"
            angle_ur = f"{name} کے فائدے اور فوائد بتا رہا ہے"
            tone = "positive and enthusiastic"
        elif mode == "disadvantage":
            angle_en = f"showing the dangers and disadvantages of {name}"
            angle_ur = f"{name} کے نقصانات اور خطرات بتا رہا ہے"
            tone = "serious and warning"
        else:
            angle_en = f"comparing advantages vs disadvantages of {name}"
            angle_ur = f"{name} کے فائدے اور نقصانات کا موازنہ"
            tone = "balanced and informative"

        extra = f" Additional context: {instructions}" if instructions else ""

        # Generate image prompt
        image_prompt = (
            f"A dramatic vertical 9:16 portrait image about {name}. "
            f"Theme: {angle_en}.{extra} "
            f"Style: {style}"
        )

        # Build Urdu dialogue based on mode
        if mode == "advantage":
            dialogue = f"{name} کے فائدے جان کر آپ حیران رہ جائیں گے! آج سے اسے اپنی زندگی میں شامل کریں۔"
        elif mode == "disadvantage":
            dialogue = f"کیا آپ جانتے ہیں {name} آپ کی صحت کو کتنا نقصان پہنچا رہا ہے؟ ابھی سنیں!"
        else:
            dialogue = f"{name} — فائدہ بھی ہے، نقصان بھی۔ آج جانتے ہیں اصلی سچائی!"

        # Generate single Veo3 prompt
        veo3_prompt = (
            f"{VEO3_ASPECT} Cinematic vertical portrait shot focused on {name}. "
            f"{angle_en.capitalize()}.{extra} "
            f"Narrator speaks in Urdu: \"{dialogue}\" "
            f"Tone: {tone}. Dramatic lighting. Audio: matching background music, clear Urdu voice. (no subtitles)"
        )

        result = {
            "name": name,
            "mode": mode,
            "angle": angle_ur,
            "image_prompt": image_prompt,
            "veo3_prompt": veo3_prompt,
        }

        # Generate a series if requested
        if series:
            if mode == "advantage":
                clips_data = [
                    {
                        "clip_title": "Part 1 — Introduction",
                        "dialogue": f"آج ہم بات کریں گے {name} کے بارے میں۔ یہ سن کر آپ حیران رہ جائیں گے!",
                        "scene": f"Close-up of {name} with dramatic spotlight, mysterious reveal."
                    },
                    {
                        "clip_title": "Part 2 — Core Benefits",
                        "dialogue": f"{name} کے فائدے اتنے ہیں کہ گنتے گنتے تھک جاؤ گے۔ سنو دھیان سے!",
                        "scene": f"Bright warm scene showing {name} in positive light with green check marks."
                    },
                    {
                        "clip_title": "Part 3 — How to Use",
                        "dialogue": f"صحیح طریقے سے {name} استعمال کرو، اور دیکھو زندگی کیسے بدلتی ہے!",
                        "scene": f"Step by step demonstration of using {name} correctly."
                    },
                    {
                        "clip_title": "Part 4 — Final Message",
                        "dialogue": f"آج سے {name} کو اپنی زندگی میں شامل کرو۔ یہ وعدہ ہے تمہاری صحت سے!",
                        "scene": f"Warm inspiring shot of {name} with sunrise lighting, motivational close."
                    },
                ]
            elif mode == "disadvantage":
                clips_data = [
                    {
                        "clip_title": "Part 1 — Lure",
                        "dialogue": f"{name} دیکھنے میں اچھا لگتا ہے۔ لیکن اصلی کہانی آگے ہے!",
                        "scene": f"Tempting close-up of {name} in warm appealing light."
                    },
                    {
                        "clip_title": "Part 2 — Hidden Dangers",
                        "dialogue": f"کیا آپ جانتے ہیں {name} کے اندر کیا ہے؟ یہ جان کر آپ ڈر جائیں گے!",
                        "scene": f"Dark X-ray style reveal showing harmful elements inside {name}."
                    },
                    {
                        "clip_title": "Part 3 — Body Impact",
                        "dialogue": f"باقاعدہ {name} استعمال سے جسم پر یہ اثرات ہوتے ہیں۔ خبردار!",
                        "scene": f"Before/after comparison showing health damage from {name}."
                    },
                    {
                        "clip_title": "Part 4 — Better Alternative",
                        "dialogue": f"{name} چھوڑو، صحت مند متبادل اپناؤ۔ آج سے فیصلہ کرو!",
                        "scene": f"Bright green scene showing healthy alternatives to {name}."
                    },
                ]
            else:
                clips_data = [
                    {
                        "clip_title": "Part 1 — Introduction",
                        "dialogue": f"آج {name} کے فائدے اور نقصانات دونوں جانتے ہیں — مکمل سچائی!",
                        "scene": f"Dramatic split-screen intro of {name} with balanced lighting."
                    },
                    {
                        "clip_title": "Part 2 — Advantages",
                        "dialogue": f"{name} کے فائدے ہیں، اور یہ واقعی کام آتے ہیں جب صحیح استعمال کرو!",
                        "scene": f"Bright warm half showing positive uses of {name} with green tones."
                    },
                    {
                        "clip_title": "Part 3 — Disadvantages",
                        "dialogue": f"لیکن زیادہ استعمال کرو تو {name} نقصان بھی دیتا ہے۔ خبردار!",
                        "scene": f"Dark cold half showing negative effects of {name} with red warning signs."
                    },
                    {
                        "clip_title": "Part 4 — Balance Advice",
                        "dialogue": f"ہر چیز حد میں اچھی ہے۔ {name} بھی اسی اصول پر — بیلنس رکھو!",
                        "scene": f"Balanced warm/cool tones with {name} centered, final wise advice."
                    },
                ]

            series_clips = []
            for i, c in enumerate(clips_data):
                prompt = (
                    f"{SERIES_ASPECT} {c['scene']}"
                    + (f" {instructions}" if instructions else "")
                    + f" Narrator says in Urdu: \"{c['dialogue']}\" "
                    + f"Tone: {tone}. Audio: matching music, clear Urdu voice. (no subtitles)"
                )
                series_clips.append({
                    "clip_title": c["clip_title"],
                    "veo3_prompt": prompt,
                })

            result["series"] = {
                "title": f"{name} — Complete Series",
                "clips": series_clips,
                "total_duration": f"~{len(series_clips) * 8} seconds",
            }

        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)
