#!/usr/bin/env python3
# AbrahamAI_Console.py 
# Talks to server, changes setting, supports "learn [topic]"
# Version

import requests

MAJOR_VERSIOM = 0
MINOR_VERSION = 3
FIX_VERSION = 0
# Added self-update via GitHub API, research controls, config
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

# AI constants
AI_NAME = "MosesAI"  
PORT = 5002  # MosesAI port
CONFIG_FILE = "{AI_NAME}_config.json"
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "{AI_NAME}_data.json")

SERVER_URL = f"http://localhost:{PORT}"

def main():
    print(f"{AI_NAME} Console {VERSION_STRING} - Type 'exit' to quit")
    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break
        if query.lower().startswith("set "):
            # Send to server as is
            r = requests.post(f"{SERVER_URL}/ask", json={"query": query})
            print(r.json()["response"])
            continue
        if query.lower().startswith("learn "):
            topic = query[6:].strip()
            query = f"learn {topic}"  # Send to server self-learn
        try:
            r = requests.post(f"{SERVER_URL}/ask", json={"query": query}, timeout=10)
            response = r.json().get("response", "No response")
            print(f"{AI_NAME}: {response}")
        except Exception as e:
            print(f"Error: {e}")

        r = requests.post(f"{SERVER_URL}/ask", json={"query": query})
        print(f"{AI_NAME}: {r.json()['response']}")

if __name__ == "__main__":
    main()
