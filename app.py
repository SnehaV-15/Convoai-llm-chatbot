
import os
import time

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env")

# Initialize Gemini
client = genai.Client(api_key=api_key)

# Flask application
app = Flask(__name__)

# Conversation storage
conversations = {}

MAX_HISTORY_MESSAGES = 10
MAX_HISTORY_CHARS = 12000


# Manage conversation context
def manage_context(history):

    history = history[-MAX_HISTORY_MESSAGES:]

    while history and history[0]["role"] != "user":
        history.pop(0)

    while history:
        total_chars = sum(
            len(part.get("text", ""))
            for message in history
            for part in message.get("parts", [])
        )

        if total_chars <= MAX_HISTORY_CHARS:
            break

        history = history[2:] if len(history) >= 2 else []

    return history


# Generate Gemini response with retries

def generate_with_retry(history, max_retries=1):

    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model="gemini-3.8-flash",
                contents=history,
                config={
                    "system_instruction": (
                        "You are a helpful and friendly chatbot. "
                        "Give clear and simple answers."
                    )
                }
            )

        except errors.ServerError:
            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt

            print(
                f"Gemini unavailable. Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


# Home page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON request."}), 400

    user_message = data.get("message")
    conversation_id = data.get("conversation_id", "default")

    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "Message cannot be empty."}), 400

    if not isinstance(conversation_id, str) or not conversation_id.strip():
        return jsonify({"error": "Invalid conversation ID."}), 400

    conversation_id = conversation_id.strip()

    # Create conversation if new
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    history = conversations[conversation_id]

    # Add user message
    history.append({
        "role": "user",
        "parts": [{"text": user_message.strip()}]
    })

    # Manage context
    history = manage_context(history)
    conversations[conversation_id] = history

    try:
        response = generate_with_retry(history)

        bot_reply = response.text

        if not bot_reply:
            raise ValueError("Gemini returned an empty response.")

        # Save bot response
        history.append({
            "role": "model",
            "parts": [{"text": bot_reply}]
        })

        return jsonify({
            "conversation_id": conversation_id,
            "user_message": user_message,
            "bot_response": bot_reply
        }), 200

    except errors.ServerError:
        app.logger.exception("Gemini server error")
        history.pop()

        return jsonify({
            "error": "Gemini is temporarily unavailable. Please try again."
        }), 503

    except errors.APIError as e:
        app.logger.exception("Gemini API error")
        history.pop()

        if e.code == 429:
            return jsonify({
                "error": "Gemini API quota exceeded. Please try later."
            }), 429

        return jsonify({
            "error": "Gemini API request failed."
        }), 502

    except Exception:
        app.logger.exception("Unexpected backend error")
        history.pop()

        return jsonify({
            "error": "An unexpected error occurred. Check the server logs."
        }), 500


# Run application
if __name__ == "__main__":
    print("Starting Flask chatbot...")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
