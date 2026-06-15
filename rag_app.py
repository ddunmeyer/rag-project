import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

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
model = genai.GenerativeModel('gemini-1.5-flash')

# ===================== CREATE FASTAPI APP =====================
app = FastAPI(title="RAG App with Gemini")

@app.get("/")
async def root():
    return {"message": "Hello! Your RAG app with Gemini is running securely 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/test-gemini")
async def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
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

print("🚀 FastAPI app created successfully!")