from flask import Flask,request,jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
from pathlib import Path


dotenv_loaded = load_dotenv(dotenv_path=Path ('.env'))
print("dotenv loaded:", dotenv_loaded)


api_key = os.getenv("OPENROUTER_API_KEY")


print("API Key loaded:", bool(api_key))
print("API Key value:", api_key if api_key else "None")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask backend is running!"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    prompt = data.get("text", "")
    print("Prompt received:", prompt)
    print("API Key loaded at request time:", bool(api_key))

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model":"gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful summarizer."},
                {"role": "user", "content": f"Summarize this: {prompt}"}
            ]
        }

        print("Sending request to OpenRouter...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        print("Response status code:", response.status_code)
        result = response.json()
        print("Response JSON:", result)

        if "choices" in result:
            summary = result["choices"][0]["message"]["content"]
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

