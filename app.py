"""
AI Chat Assistant - Flask web app powered by the Gemini API (Google).

Run:
    python3 app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file (see .env.example) "
        "and add your Gemini API key."
    )

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Keep answers clear and concise."

model = genai.GenerativeModel(MODEL, system_instruction=SYSTEM_PROMPT)

app = Flask(__name__)

# Simple in-memory conversation history (per server process, single user demo)
# Gemini expects roles "user" and "model", with content under "parts"
conversation_history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    conversation_history.append({"role": "user", "parts": [user_message]})

    try:
        response = model.generate_content(conversation_history)
        assistant_reply = response.text
        conversation_history.append(
            {"role": "model", "parts": [assistant_reply]})
        return jsonify({"reply": assistant_reply})

    except Exception as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 500


@app.route("/api/reset", methods=["POST"])
def reset():
    conversation_history.clear()
    return jsonify({"status": "conversation reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
