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