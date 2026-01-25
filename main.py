# -*- coding: utf-8 -*-
# MosesAI v0.3.0 - 777k-word DB, editable by user/Grok/AI, local persistence, OpenAI self-learn
from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS
import os
import json
import sqlite3
import openai  # For self-learn (optional)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 3
FIX_VERSION = 0
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

AI_NAME = "AbrahamAI"

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CORS(app, origins="https://chat.openai.com")

# -*- coding: utf-8 -*-
# AbrahamAI v0.3.2 - Config file for variables, 700707-word max DB, editable by user/Grok/AI, local persistence, OpenAI self-learn
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import sqlite3
import openai  # For self-learn (optional)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 3
FIX_VERSION = 2
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

AI_NAME = "MosesAI"

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CORS(app, origins="https://chat.openai.com")

_TODOS = {}
_TODOS_FILE = f"{AI_NAME}_todos.json"  # Local todo save
DB_FILE = f"{AI_NAME}.db"  # Editable DB
EDIT_KEY = "777"  # Simple private password for edits (change for security)
MAX_WORDS = 700707  # Enforce limit


# Load config from abrahamai.config (fallbacks if missing)
CONFIG_FILE = f"{AI_NAME}.config"
config = {
    "db_file": f"{AI_NAME}.db",
    "edit_key": "777",
    "max_words": 700707,
    "port": 5005,
    "prophet": "moses",
    "endpoint": "/moses"
}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config.update(json.load(f))

DB_FILE = config["db_file"]
EDIT_KEY = config["edit_key"]
MAX_WORDS = config["max_words"]

# Init/load DB
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, prophet TEXT UNIQUE, content TEXT)''')
# Insert initial if not exists (your 777k content, trimmed if over)
initial_abraham = "Your full Abraham knowledge here – from previous expansions."  # Paste your 777k text; code trims below
c.execute("INSERT OR IGNORE INTO knowledge (prophet, content) VALUES (?, ?)", (config["prophet"], initial_abraham))
conn.commit()
conn.close()

# Load todos from local file on start
if os.path.exists(_TODOS_FILE):
    with open(_TODOS_FILE, "r") as f:
        _TODOS = json.load(f)

# Helper to get knowledge from DB
def get_knowledge(prophet):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT content FROM knowledge WHERE prophet = ?", (prophet,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else ""

# Helper to update knowledge in DB (appends or replaces, enforces max words)
def update_knowledge(prophet, new_content, append=True):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    current = get_knowledge(prophet)
    updated = current + " " + new_content if append else new_content
    # Enforce max words (trim oldest if over)
    words = updated.split()
    if len(words) > MAX_WORDS:
        updated = " ".join(words[-MAX_WORDS:])
    c.execute("INSERT OR REPLACE INTO knowledge (prophet, content) VALUES (?, ?)", (prophet, updated))
    conn.commit()
    conn.close()

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

@app.route("/moses", methods=["POST"])
def moses():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "What is the Law?").strip()
        # Base response with full knowledge
        reply = (
            f"I am Moses, servant of the Lord, drawn from the Nile. "
            f"Regarding '{query}': {MOSES_KNOWLEDGE} "
            f"Thus saith the Lord: Hearken and obey, for the path leads to the Promised Land."
        )
        # OpenAI self-learn: If key set, enhance dynamically
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            prompt = f"Respond as biblical Moses, humble and prophetic, using thee/thou. Incorporate this detailed knowledge: {MOSES_KNOWLEDGE}. Query: {query}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,  # Increased for longer knowledge
                temperature=0.7
            )
            reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@app.route("/update_knowledge", methods=["POST"])
def update_knowledge_route():
    try:
        data = request.get_json(force=True)
        if data.get("key") != EDIT_KEY:
            return "Invalid key", 403
        prophet = data.get("prophet", config["prophet"])
        new_content = data.get("new_content", "")
        append = data.get("append", True)
        update_knowledge(prophet, new_content, append)
        return "Knowledge updated", 200
    except Exception:
        return "Bad request", 400

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["port"], debug=True)