# D-Starix Chat Assistant

A web-based AI chat assistant powered by Google's Gemini API. Built with Flask for the backend and vanilla HTML/CSS/JS for the frontend. Gemini's free tier requires no credit card, so this runs at zero cost.

## Features

- Web chat interface (type a message, get a response)
- Maintains conversation context during a session
- "New chat" button to reset the conversation
- Errors (missing key, API failures) shown clearly in the UI

## Tech Stack

- Python 3.9+
- Flask
- `google-generativeai` (official Gemini SDK)
- python-dotenv for environment variables

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd chatbot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

1. Get a free Gemini API key (no credit card required) at https://aistudio.google.com/apikey
2. Copy the example env file and fill in your key:
   ```bash
   cp .env.example .env
   ```
   ```
   GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxx
   GEMINI_MODEL=gemini-2.5-flash
   ```

### 5. Run the app

```bash
python3 app.py
```

Open your browser at http://127.0.0.1:5000

## Project Structure

```
chatbot/
├── app.py                  # Flask backend, Gemini chat logic
├── templates/
│   └── index.html          # Chat UI markup
├── static/
│   ├── style.css            # Chat UI styling
│   └── script.js            # Chat UI behavior (fetch calls to /api/chat)
├── requirements.txt         # Python dependencies
├── .env.example              # Template for your Gemini API key
├── .env                       # Gemini API key (not committed)
├── .gitignore
└── README.md
```

## How It Works

1. The user types a message in the browser and hits Send.
2. The frontend (`static/script.js`) sends a POST request to `/api/chat`.
3. Flask (`app.py`) appends the message to an in-memory conversation history and calls `gemini-2.5-flash` via `google.generativeai`, with the full history passed each time so the model has conversational context.
4. The reply is appended to the history and returned as JSON, then rendered in the chat window.

## Usage Guide

1. Make sure the app is running (see Setup Instructions above) and http://127.0.0.1:5000 is open in your browser.
2. Type a message in the input box at the bottom and press Send (or hit Enter).
3. The assistant's response will appear in the chat window above.
4. Continue the conversation — the assistant remembers earlier messages in the same session.
5. Click "New chat" at the top to clear the conversation and start fresh.

## Notes

- Chat history is kept in-memory per server process (single-session demo, not multi-user safe) — it resets if the server restarts.
- Gemini's free tier has per-minute and per-day request limits. If you see a `429` or rate-limit error, wait a bit before sending another message, or check current usage at https://ai.dev/rate-limit.
- **Model note:** This project uses `gemini-2.5-flash`. If you get a 404 saying the model isn't found, your API key's supported model list may have changed — run `genai.list_models()` to see what's available and update `GEMINI_MODEL` in your `.env` accordingly.
