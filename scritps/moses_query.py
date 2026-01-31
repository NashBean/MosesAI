#!/usr/bin/env python3
# moses_query.py - BDH + watsonx query on Moses knowledge
# Run: python3 moses_query.py "Moses' Exodus path"

import argparse
import json
from bdh_stub import generate_text  # In-house BDH
from ibm_watsonx_ai.foundation_models import Model  # pip install ibm-watsonx-ai

MAJOR_VERSION = 0
MINOR_VERSION = 1
FIX_VERSION = 0

KNOWLEDGE_FILE = "../data/moses_knowledge.json"

def load_knowledge():
    with open(KNOWLEDGE_FILE, 'r') as f:
        return json.load(f)

def bdh_query(knowledge, user_query):
    prompt = f"""You are MosesAI, a reverent assistant helping people understand the Biblical prophet Moses.
Base every answer first on Scripture. Use historical and archaeological information only as supporting context.
Never contradict the Bible. Be humble and truthful, emphasizing Moses' humility and God's sovereignty.

Knowledge base summary: {json.dumps(knowledge, indent=2)}

Question: {user_query}

Answer:"""
    return generate_text(prompt)

def watsonx_enhance(text, api_key, project_id):
    model = Model(model_id='ibm/granite-13b-chat-v2', credentials={"api_key": api_key, "url": "https://us-south.ml.cloud.ibm.com"}, project_id=project_id)
    prompt = f"Summarize/enhance this Moses info for accuracy and reverence: {text}"
    response = model.generate_text(prompt)
    return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Ask about Moses")
    parser.add_argument("--watsonx-key", default=os.getenv("WATSONX_API_KEY"))
    parser.add_argument("--project-id", default=os.getenv("PROJECT_ID"))
    args = parser.parse_args()

    knowledge = load_knowledge()
    bdh_response = bdh_query(knowledge, args.query)
    print(f"BDH Response: {bdh_response}")

    if args.watsonx_key and args.project_id:
        enhanced = watsonx_enhance(bdh_response, args.watsonx_key, args.project_id)
        print(f"Watsonx Enhanced: {enhanced}")

    print("Query done—sharing knowledge for deeper faith!")

if __name__ == "__main__":
    main()