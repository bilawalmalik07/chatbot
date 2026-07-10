"""
AI Chat Assistant - Flask web app powered by the Google Gemini API.

Run:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Load environment variables from .env
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file (see .env.example) "
        "and add your Gemini API key (free, no card needed, from "
        "https://aistudio.google.com/apikey)."
    )

client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Keep answers clear and concise."

# Simple in-memory chat session (per server process, single user demo)
chat_session = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})

    except APIError as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/reset", methods=["POST"])
def reset():
    global chat_session
    chat_session = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return jsonify({"status": "conversation reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
