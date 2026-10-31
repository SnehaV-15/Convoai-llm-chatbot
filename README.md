# ConvoAI – LLM-Powered Chatbot

ConvoAI is a web-based conversational AI chatbot powered by Google's Gemini API. It allows users to interact with an AI assistant through a simple, responsive chat interface while maintaining conversation context across multiple messages.

## Features

- **AI-Powered Conversations:** Generates responses using Google's Gemini API.
- **Multi-Turn Conversations:** Maintains conversation history using unique conversation IDs.
- **Context Management:** Limits conversation history to manage context size.
- **Custom System Instructions:** Configures the chatbot's personality and response style.
- **Responsive User Interface:** Clean chat interface with user and assistant message bubbles.
- **Typing Indicator:** Displays an animated indicator while the chatbot generates a response.
- **New Chat:** Starts a separate conversation.
- **Clear Chat:** Clears the visible chat messages.
- **Error Handling:** Handles invalid requests, API errors, quota limits, and temporary service unavailability.
- **Secure API Configuration:** Stores API credentials in environment variables.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| AI Model | Google Gemini |
| AI Integration | Google Gen AI SDK |
| Frontend | HTML, CSS, JavaScript |
| Environment Configuration | python-dotenv |

## Project Structure

```text
convoai-llm-chatbot/
│
├── app.py
├── .gitignore
├── README.md
│
└── templates/
    └── index.html
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SnehaV-15/convoai-llm-chatbot.git
cd convoai-llm-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask google-genai python-dotenv
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get an API key from [Google AI Studio](https://aistudio.google.com/).

**Important:** Never share or upload your API key.

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## API Endpoint

### POST `/chat`

Accepts a user message and conversation ID, then returns an AI-generated response.

**Request:**

```json
{
  "message": "Hello!",
  "conversation_id": "conversation_1"
}
```

**Successful response:**

```json
{
  "conversation_id": "conversation_1",
  "user_message": "Hello!",
  "bot_response": "Hello! How can I help you today?"
}
```

## Context Management

ConvoAI maintains separate conversation histories using conversation IDs. It limits the number of stored messages and total character count to help manage the model's context window.

## Error Handling

The application handles:
- Invalid or empty user messages.
- Invalid JSON requests.
- API quota limits.
- Temporary Gemini service unavailability.
- Unexpected backend errors.

## Future Improvements

- Persistent conversation storage using a database.
- User authentication and personalized chat history.
- Conversation export functionality.
- Improved context management through conversation summarization.
- Support for additional LLM providers.

## Author

Developed as part of the **Valentius Kryptix AI / Gen AI Internship**.

---

*ConvoAI – Simple conversations, powered by AI.*
