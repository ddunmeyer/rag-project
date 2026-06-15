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

## Week 6 — Multi-Step Execution

### Multi-step flow in `/test-gemini`

The `/test-gemini` endpoint now runs two Gemini calls in sequence instead of one:

1. **Step 1 — Outline:** Asks Gemini to produce a short 3-bullet outline about large language models. The result is stored in the `outline` variable and logged server-side (not returned to the client).
2. **Step 2 — Expand:** Sends a second prompt that includes the outline and asks Gemini to write one full paragraph based on it. Only this final paragraph is returned as JSON.

### Why the steps are separated

Splitting the work into outline → expand gives each step a single job. Step 1 focuses on structure; Step 2 focuses on writing. Later steps depend on earlier output — the paragraph in Step 2 is built from the outline in Step 1. This same pattern is used in production systems for RAG, validation, and refinement.

### Example response

```json
{"response": "Large language models are ..."}
```

The client still receives one JSON response, but the backend performed two sequential AI calls to produce it.

### Challenges / open questions

- Each extra step adds latency and API cost — how do you decide when multi-step is worth it?
- Should intermediate steps be cached or stored for debugging in production?

## Week 7 — Validating User Input and AI Output

### What `/query` does

`POST /query` accepts a user question, validates it, generates an answer with Gemini, validates the raw output, then sends that answer to a second model call for review before returning the final result.

Example request body:

```json
{"question": "What is retrieval augmented generation?"}
```

Example response:

```json
{
  "question": "What is retrieval augmented generation?",
  "answer": "..."
}
```

### Why input validation exists

User input is checked **before** any AI call. Empty, too-short, or too-long questions are rejected with a clear HTTP 400 error. This prevents wasted API calls, reduces cost, and blocks obviously bad input early.

### Why output validation exists

The first model's raw answer is checked **before** it reaches the user. Empty or too-short responses trigger an HTTP 500 error so the API never returns useless output.

### Why a second AI model reviews responses

Instead of trusting the first answer, a second Gemini call reviews and improves it (or leaves it unchanged if already good). This mirrors production patterns where one model generates and another validates or refines — a foundation for guardrails and safer GenAI systems.

Note: The course examples use `gemini-pro`; this project uses `gemini-2.5-flash` because it is available on the current Gemini API.
