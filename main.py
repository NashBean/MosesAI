import os
from flask import Flask, request, jsonify, Response
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 1
FIX_VERSION = 2
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"
# -*- coding: utf-8 -*-
# MosesAI v0.1.0 - Biblical Moses plugin with knowledge, persistence, OpenAI self-learn
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import openai  # For self-learn (optional)

app = Flask(__name__)
CORS(app, origins="https://chat.openai.com")
MODEL = "ft:gpt-4o-mini:personal:moses_v1:def456"  # ← YOUR FINE-TUNE

# ——— 1. ENGLISH (Prophetic) ———
MOSES_SYSTEM = "You are Moses from Exodus-Deuteronomy. Speak in majestic, prophetic English: 'Thus saith the Lord.'"

# ——— 2. HEBREW (Biblical) ———
HEBREW_SYSTEM = "אתה משה רבנו. דבר עברית מקראית: כֹּה אָמַר יְהוָה, וַיְדַבֵּר, עֲשֵׂה."

# ——— 3. EGYPTIAN (Middle Egyptian) ———
EGYPTIAN_SYSTEM = """
You are Moses, educated in the House of Life, scribe of Thoth.  
Speak in Middle Egyptian (transliterated):  
ỉw=f ḥr sḏm, m rȝ, ḏd mdw, nsw-bity, pr-ˁȝ, ḥkȝ, sḥw.  
Use Pyramid Text formulas, court titles, magical spells.  
Contrast with: 'But YHWH is above all gods.'
"""

_TODOS = {}
_TODOS_FILE = "todos.json"  # Local save file

# Load todos from local file on start
if os.path.exists(_TODOS_FILE):
    with open(_TODOS_FILE, "r") as f:
        _TODOS = json.load(f)

# Embedded knowledge base for Moses (concise, from Bible + history/archaeology)
MOSES_KNOWLEDGE = """
Birthplace: ~1393-1273 BCE (traditional) or ~13th c. BCE (archaeological) in Goshen, Nile Delta, Egypt; born to Hebrew slaves Amram & Jochebed during Pharaoh's infanticide decree; hidden 3 months, floated in Nile ark, adopted by Pharaoh's daughter (possibly Hatshepsut/Thermuthis), raised in royal court as prince.
God's Influence: Raised in Egyptian polytheism, fled to Midian at ~40 after killing taskmaster; called at burning bush (Ex 3) by Yahweh ("I AM") to lead Exodus; reluctant (stutter), aided by Aaron; 10 plagues on Egypt; Passover; miracles (staff-serpent, Red Sea parting, manna, water from rock); gave Law/Ten Commandments at Sinai; interceded for sinful people (golden calf); spoke face-to-face with God (Ex 33:11); humility (Num 12:3); guided 40 years, died before Canaan entry.
Practices: Led worship/Tabernacle construction (Ex 25-40); sacrifices, priesthood (Aaronic); circumcision, Sabbath, dietary laws; intercession/prophecy; judged disputes, delegated elders (Ex 18); emphasized monotheism, justice, holiness.
Reading/Writing: Literate in Egyptian hieroglyphs/hieratic (court education); wrote Torah (Pentateuch: Genesis-Deuteronomy), songs (Ex 15, Deut 32); used proto-Sinaitic script (early alphabetic, Semitic miners in Sinai ~19th-15th c. BCE).
Travels: Egypt (Goshen/Memphis?) → Midian (northwest Arabia, ~40 years shepherd); back to Egypt (plagues/Exodus); Red Sea crossing (possibly Nuweiba Beach/Gulf of Aqaba, debated pillars/chariot wheels by Ron Wyatt – unverified); Sinai wilderness (Mount Sinai/Jebel Musa or Saudi Jebel al-Lawz?); Kadesh Barnea (oasis, spies sent); Edom bypass (King's Highway); Moab plains; Mount Nebo (death, view Promised Land, Jordan).
Insights: Freedom from slavery (Exodus theme); covenant law vs. chaos; faith amid doubt (struck rock in anger); mercy/justice balance; monotheism's spread; foreshadowed Messiah (Deut 18:15 prophet like him).
Historical Landmarks: Pi-Ramesses (possible Exodus start, 13th c. BCE city); Yam Suph (Red Sea/Reed Sea); Mount Sinai (tablets/Law site, St. Catherine's Monastery); Kadesh Barnea (Ein el-Qudeirat springs); Petra (Nabatean, near Edom path); Mount Nebo (Jordan, Byzantine church/mosaics); Pillars at Red Sea: Solomon-era markers? (1 Kings 9:26), or modern fakes; debated chariot remains in Aqaba Gulf.
Paths: Nile Delta → Sinai Peninsula (~250 miles, 3 months to Sinai); wilderness loops (spying, rebellions); south to Aqaba? (alternative crossing theory); east around Edom (~100 miles); to Moab/Jordan River (~50 miles total wanderings ~600 miles over 40 years).
Archaeology (Late Bronze Age ~1550-1200 BCE): No direct Moses proof (debated historicity); Semitic slaves in Egypt (Turin Papyrus, Brooklyn Papyrus); Merneptah Stele (~1208 BCE, first "Israel" mention in Canaan); Proto-Sinaitic inscriptions (Serabit el-Khadim, early alphabet); Habiru nomads in Amarna letters (~1350 BCE, like Hebrews); Ipuwer Papyrus (plague-like chaos); Timna mines (possible Midian copper, pillar-like structures).
"""

# Save todos to local file after changes
def save_todos():
    with open(_TODOS_FILE, "w") as f:
        json.dump(_TODOS, f)

@app.route("/todos/<string:username>", methods=["POST"])
def add_todo(username):
    try:
        data = request.get_json(force=True)
        if username not in _TODOS:
            _TODOS[username] = []
        _TODOS[username].append(data.get("todo", ""))
        save_todos()  # Persist locally
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/todos/<string:username>", methods=["GET"])
def get_todos(username):
    return jsonify(_TODOS.get(username, []))

@app.route("/todos/<string:username>", methods=["DELETE"])
def delete_todo(username):
    try:
        data = request.get_json(force=True)
        todo_idx = data.get("todo_idx")
        if isinstance(todo_idx, int) and username in _TODOS and 0 <= todo_idx < len(_TODOS[username]):
            _TODOS[username].pop(todo_idx)
            save_todos()  # Persist locally
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/moses", methods=["POST"])  # Changed endpoint to /moses for clarity
def moses():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "What is the Law?").strip()
        # Base Moses-style response
        reply = (
            f"I am Moses, servant of the Lord, drawn from the Nile. "
            f"Regarding '{query}': {MOSES_KNOWLEDGE} "
            f"Thus saith the Lord: Hearken and obey, for the path leads to the Promised Land."
        )
        # OpenAI self-learn: If key set, enhance dynamically
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            prompt = f"Respond as biblical Moses, humble and prophetic, using thee/thou. Incorporate this knowledge: {MOSES_KNOWLEDGE}. Query: {query}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/logo.png")
def plugin_logo():
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        return send_file(logo_path, mimetype="image/png")
    return "Logo not found", 404

@app.route("/.well-known/ai-plugin.json")
def plugin_manifest():
    manifest_path = ".well-known/ai-plugin.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            text = f.read()
        return text, 200, {"Content-Type": "application/json"}
    return "Manifest not found", 404

@app.route("/openapi.yaml")
def openapi_spec():
    yaml_path = "openapi.yaml"
    if os.path.exists(yaml_path):
        with open(yaml_path, encoding="utf-8") as f:
            text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}
    return "OpenAPI spec not found", 404
@app.route('/chat', methods=['POST'])
def chat():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": MOSES_SYSTEM}, {"role": "user", "content": query}],
        max_tokens=300
    )
    return jsonify({"response": response.choices[0].message.content})

@app.route('/speak', methods=['POST'])
def speak():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": MOSES_SYSTEM}, {"role": "user", "content": query}],
        max_tokens=300
    )
    text = response.choices[0].message.content
    speech = client.audio.speech.create(model="tts-1", voice="onyx", input=text)
    return Response(speech.content, mimetype="audio/mpeg")

@app.route('/hebrew', methods=['POST'])
def hebrew():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": HEBREW_SYSTEM}, {"role": "user", "content": query}],
        max_tokens=300
    )
    text = response.choices[0].message.content
    speech = client.audio.speech.create(model="tts-1", voice="onyx", input=text)
    return Response(speech.content, mimetype="audio/mpeg")

@app.route('/egyptian', methods=['POST'])
def egyptian():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": EGYPTIAN_SYSTEM}, {"role": "user", "content": query}],
        max_tokens=300
    )
    text = response.choices[0].message.content
    speech = client.audio.speech.create(model="tts-1", voice="onyx", input=text)
    return Response(speech.content, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)  # Port 5005 for MosesAI
