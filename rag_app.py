import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ===================== SECURELY LOAD GEMINI API KEY =====================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY is missing!\n"
        "Create a .env file with: GEMINI_API_KEY=your_key_here"
    )

print(f"✅ GEMINI API Key loaded (starts with: {GEMINI_API_KEY[:8]}...)")

# ===================== INITIALIZE GEMINI =====================
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

# Single model for all endpoints (gemini-1.5-flash is no longer available on the current API)
GEMINI_MODEL = "gemini-2.5-flash"
model = genai.GenerativeModel(GEMINI_MODEL)

# ===================== CREATE FASTAPI APP =====================
app = FastAPI(title="RAG App with Gemini")


class QueryRequest(BaseModel):
    question: str


def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")

    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")


def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")

    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")


def review_model_output(original_answer: str):
    review_prompt = f"""
You are reviewing an AI-generated response.

Your job:
- If the response is unclear, incomplete, or poorly written, improve it.
- If the response is already good, return it unchanged.

AI response to review:
{original_answer}
"""

    review_response = model.generate_content(review_prompt)

    return review_response.text


@app.get("/")
async def root():
    return {"message": "Hello! Your RAG app with Gemini is running securely 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/test-gemini")
async def test_gemini():
    try:
        topic = "large language models"

        # Step 1: Generate a short outline
        outline_prompt = (
            f"Create a short 3-bullet outline explaining {topic}. "
            "Keep each bullet to one sentence."
        )
        outline_response = model.generate_content(outline_prompt)
        outline = outline_response.text
        print(f"Step 1 complete — outline ({len(outline)} chars): {outline[:120]}...")

        # Step 2: Expand the outline into a full paragraph
        expand_prompt = (
            f"Using this outline as your guide, write one clear paragraph "
            f"explaining {topic}:\n\n{outline}"
        )
        final_response = model.generate_content(expand_prompt)

        return {"response": final_response.text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API call failed: {str(e)}",
        )


# Example endpoint to test Gemini
@app.post("/generate")
async def generate(prompt: str):
    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}


@app.post("/query")
def query_ai(request: QueryRequest):
    validate_user_input(request.question)

    primary_response = model.generate_content(request.question)

    raw_answer = primary_response.text

    validate_model_output(raw_answer)

    reviewed_answer = review_model_output(raw_answer)

    return {
        "question": request.question,
        "answer": reviewed_answer,
    }

print("🚀 FastAPI app created successfully!")