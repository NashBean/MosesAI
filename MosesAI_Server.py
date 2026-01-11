#!/usr/bin/env python3
# MosesAI_Server.py - Modular AI Server
# Run with: python3 app.py

from flask import Flask, request, jsonify
import os
import json
# Import shared from ai-lib (submodule)
from ai_lib.CommonAI import (
    setup_logging,load_config, save_config, check_system_limits, self_research, self_update,
    send_alert, setup_logging, get_response  
    ) 

app = Flask(__name__)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 2
FIX_VERSION = 0
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

#AI
AI_NAME = "MosesAI"  
PORT = 5002  
DATA_DIR = "data"

CONFIG = load_config()
logger = setup_logging(CONFIG)
logger.info(f"{AI_NAME} Server {VERSION_STRING} starting...")

#DATA
data = load_data()
response = get_response(data, query)

EXODUS = json.load(open(os.path.join(DATA_DIR, "moses_exodus_route.json")))
TABERNACLE = json.load(open(os.path.join(DATA_DIR, "moses_tabernacle.json")))
PLAGUES = json.load(open(os.path.join(DATA_DIR, "moses_plagues.json")))

MUSTARD_SEED = DATA["MUSTARD_SEED"]
PARABLES = DATA["PARABLES"]
RESPONSES = DATA["RESPONSES"]

# Use shared from ai-lib
def get_response(query):
    return get_response(query)  # Calls ai-lib's get_response

# Self-learn (updates data.json)
def self_learn(topic):
    research = self_research(topic)  # From {AI_NAME}_data.json as string - exec it if needed
    # Update data.json
    with open(os.path.join(DATA_DIR, f"{AI_NAME}_data.json"), "r") as f:
        data = json.load(f)
    data["new_knowledge"][topic] = research
    with open(os.path.join(DATA_DIR, f"{AI_NAME}_data.json"), "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    return jsonify({"ai": AI_NAME, "status": "ready"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query"}), 400
    response = get_response(query)
    return jsonify({"ai": AI_NAME, "response": response})

if __name__ == "__main__":
    print(f"{AI_NAME} {VERSION_STRING} server running on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=False)