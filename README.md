# AI Chat Assistant (Gemini API + Flask) (CHATBOT I AM)

A simple web-based AI chat assistant that lets users ask questions and get
responses from Google's Gemini API. Built with Flask (Python) for the
backend and vanilla HTML/CSS/JS for the frontend. Gemini's free tier
requires no credit card, so this runs at zero cost.

## Features

- Web chat interface (type a message, get a response)
- Maintains conversation context during a session
- "New chat" button to reset the conversation
- Errors (missing key, API failures) shown clearly in the UI

## Tech Stack

- Python 3.9+
- Flask
- Google Gen AI SDK (`google-genai`)
- python-dotenv for environment variables

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-chat-assistant
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
python3 -m pip install -r requirements.txt
```

### 4. Configure your API key

1. Get a **free** Gemini API key (no credit card required) at
   https://aistudio.google.com/apikey
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and paste your key:
   ```
   GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxx
   ```

### 5. Run the app

```bash
python3 app.py
```

Open your browser at **http://127.0.0.1:5000**

## Project Structure

```
ai-chat-assistant/
├── app.py                 # Flask backend, calls the Gemini API
├── templates/
│   └── index.html          # Chat UI markup
├── static/
│   ├── style.css            # Chat UI styling
│   └── script.js            # Frontend chat logic (fetch calls)
├── requirements.txt        # Python dependencies
├── .env.example             # Template for environment variables
├── .gitignore
└── README.md
```

## How It Works

1. The user types a message in the browser and hits Send.
2. The frontend (`script.js`) sends a POST request to `/api/chat`.
3. Flask (`app.py`) forwards the message to a Gemini chat session
   (`client.chats.create(...)` / `chat_session.send_message(...)`), which
   keeps track of conversation history automatically.
4. Gemini's reply is returned as JSON and rendered in the chat window.

## Usage Guide

1. Make sure the app is running (see Setup Instructions above) and
   `http://127.0.0.1:5000` is open in your browser.
2. Type a message in the input box at the bottom and press **Send** (or hit Enter).
3. The assistant's response will appear in the chat window above.
4. Continue the conversation — the assistant remembers earlier messages
   in the same session.
5. Click **New chat** at the top to clear the conversation and start fresh.
