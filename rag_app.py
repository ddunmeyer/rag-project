import os
from dotenv import load_dotenv
from fastapi import FastAPI

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
    return {"status": "healthy", "model": "gemini-1.5-flash"}

# Example endpoint to test Gemini
@app.post("/generate")
async def generate(prompt: str):
    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

print("🚀 FastAPI app created successfully!")