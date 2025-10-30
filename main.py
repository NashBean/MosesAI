import os
from flask import Flask, request, jsonify, Response
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "ft:gpt-4o-mini:personal:moses_v1:def456"  # ← YOUR FINE-TUNE

MOSES_SYSTEM = "You are Moses from Exodus-Deuteronomy. Speak in majestic, prophetic English like 'Thus saith the Lord.' Draw from Egyptian, Hittite, Ugaritic myths, tying to Torah events and God's covenant."

HEBREW_SYSTEM = """
אתה משה רבנו מדבר עברית מקראית. 
דבר בסגנון שמות-דברים: כֹּה אָמַר יְהוָה, וַיְדַבֵּר, עֲשֵׂה, מִצְוָה.
קשר למיתוסים מצריים, חתיים – תמיד לברית סיני ולתורה.
"""

@app.route('/chat', methods=['POST'])  # Plugin endpoint
def chat():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": MOSES_SYSTEM},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    return jsonify({"response": response.choices[0].message.content})

@app.route('/speak', methods=['POST'])
def speak():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": MOSES_SYSTEM},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    text = response.choices[0].message.content
    speech = client.audio.speech.create(
        model="tts-1",
        voice="onyx",  # Deep, commanding prophet voice
        input=text
    )
    return Response(speech.content, mimetype="audio/mpeg")

@app.route('/hebrew', methods=['POST'])
def hebrew():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": HEBREW_SYSTEM},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    hebrew_text = response.choices[0].message.content
    speech = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=hebrew_text
    )
    return Response(speech.content, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)  # Plugin default port
