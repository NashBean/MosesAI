#!/usr/bin/env python3
# MosesAI_Server.py - Modular AI Server
# Run with: python3 app.py

from flask import Flask, request, jsonify
import jsonimport sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-lib')))

# Import shared from ai-lib (your submodule)
from ai_lib.CommonAI import (
    get_version, 
    load_config, # save_config,
    setup_logging, logger,
    load_data, update_data, send_alert,
    check_system_limits,  
    self_research, self_update,
    understand_language, get_culture, speak,
    get_response
    )
from ai_lib.bdh_wrapper import load_bdh_model, bdh_generate, bdh_self_learn

app = Flask(__name__)

# Version
MAJOR_VERSION = 0
MINOR_VERSION = 3
FIX_VERSION = 0
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

#AI
AI_NAME = "MosesAI"  
PORT = 5002  
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "moses_data.json")

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

KNOWLEDGE = load_data(DATA_FILE)
BDH_MODEL = load_bdh_model(DATA_FILE)  

# Use shared from BDH_MODEL
def get_response(query):
    # Use BDH for deep response
    prompt = f"Explain {query} in context of MosesAI's law: {KNOWLEDGE.get(q, '')}"
    app = LLMApp()
    pathway_response = app(prompt)
    return pathway_response

def self_learn(topic):

    research = self_research(topic)  # From ai-lib
    update_data({"learned": {topic: research}}, DATA_FILE)
    bdh_self_learn(BDH_MODEL, topic, KNOWLEDGE)  # Update BDH model
    KNOWLEDGE = load_data(DATA_FILE)
    return f"Learned '{topic}' via BDH: {research[:200]}..."

# Use shared from ai-lib
def research_topic(topic):
    if not CONFIG.get("RESEARCH_ENABLED", False):
        return "Research disabled."
    if not check_system_limits(CONFIG):
        return "System limits reached — research skipped."
    research = self_research(topic)  # From ai-lib
    update_data({"learned": {topic: research}}, DATA_FILE)  # From ai-lib
    global KNOWLEDGE
    KNOWLEDGE = load_data(DATA_FILE)
    logger.info(f"Researched and learned: {topic}")
    return f"Learned '{topic}': {research[:200]}..."  # Truncate

# Handle client
def handle_client(client_socket, addr):
    print(f"Connection from {addr}")
    try:
        welcome = f"{AI_NAME} Server {VERSION_STRING} \n"
        client_socket.send(welcome.encode('utf-8'))

        current_ai = None
        buffer = ""

        while True:
            data = client_socket.recv(1024)# Import shared from ai-lib (your submodule)
            if not data:
                break
            buffer += data.decode('utf-8', errors='ignore')

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                message = line.strip()
                if not message:
                    continue
                if message.lower() == "exit":
                    client_socket.send(b"Grace and peace - until next time!\n")
                    return

                if current_ai is None:
                    if message.lower().startswith("learn "):
                        topic = message[6:].strip()
                        resp = self_learn(topic)
                        full_resp = f"{current_ai.upper()}AI: {resp}\n"
                        client_socket.send(full_resp.encode('utf-8'))
                        speak(resp)
                        continue
                response = get_ai_response(message)
                full_resp = f"{current_ai.upper()}AI: {response}\n"
                client_socket.send(full_resp.encode('utf-8'))
                speak(response)
    except:
        pass
    finally:
        client_socket.close()
        print(f"Disconnected: {addr}")

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