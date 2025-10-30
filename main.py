import os
from flask import Flask, request, jsonify, Response
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
