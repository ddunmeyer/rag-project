README.md
# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course.

This project will be built incrementally each week.


## Git Commands Used So Far

- git clone  
- git status  
- git add  
- git commit  
- git push

In week 4 we updated the rap_app.py file which is the main application file for the RAG project. It serves as the central backbone of your entire application. 

Core Purposes:

Start the Web Server
Creates a FastAPI application (app = FastAPI())
This is why you run it with uvicorn rag_app:app --reload

Securely Load the Gemini API Key
Loads .env file
Reads GEMINI_API_KEY safely
Validates that the key exists

Initialize the Gemini Model
Connects to Google Gemini (gemini-1.5-flash or pro)

Handle All Routes / Endpoints
Defines what the app can do (e.g., /, /generate, chat, document upload, etc.)

Implement the RAG Logic (in later stages)
Load documents
Create embeddings
Retrieve relevant chunks
Generate answers using Gemini + retrieved context

## Week 5 — First Backend API + Gemini Call

### What `/test-gemini` does

`GET /test-gemini` sends a hardcoded prompt to Google Gemini and returns the model's text response as JSON. The API key stays in `.env` on the server — the client never sees it.

Example response:

```json
{"response": "A large language model is ..."}
```

### Where the Gemini call lives

The Gemini call is inside the `test_gemini()` function in `rag_app.py`. It:

1. Creates a `GenerativeModel` (`gemini-1.5-flash`)
2. Calls `generate_content()` with a fixed prompt
3. Returns `response.text` as JSON

### What I learned from the Gemini documentation

- `genai.configure(api_key=...)` must run once before any model calls (already set up at the top of `rag_app.py`)
- `GenerativeModel("gemini-1.5-flash")` picks which Gemini model to use
- `model.generate_content(prompt)` sends text to Gemini and returns a response object
- `response.text` holds the generated text

Docs: https://ai.google.dev/gemini-api/docs/get-started/python

### Questions I still have

- When should we switch from `google-generativeai` to the newer `google.genai` SDK?