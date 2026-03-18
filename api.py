# File: api.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.agent import CommentAnalysisAgent
from src.response_generator import ResponseGenerator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading agent...")
agent     = CommentAnalysisAgent()
generator = ResponseGenerator()
print("✅ API ready")


def detect_language(text):
    """Simple heuristic — if mostly ASCII, reply in English"""
    if not text:
        return 'bengali'
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    return 'english' if ascii_chars / len(text) > 0.85 else 'bengali'


class CommentRequest(BaseModel):
    text:     str
    language: str = "bengali"
    user_id:  str = "demo_user"


@app.post("/analyze")
def analyze(req: CommentRequest):
    analysis = agent.analyze(req.text, user_id=req.user_id, use_rag=False)
    emotion  = analysis['final_prediction']['emotion']
    decision = analysis['final_prediction']['decision']
    lang     = detect_language(req.text)
    response = generator.generate(emotion, lang)
    return {
        "emotion":     emotion,
        "confidence":  analysis['final_prediction']['confidence'],
        "decision":    decision,
        "tools":       analysis['tools_used'],
        "adjustments": analysis['adjustments_made'],
        "base":        analysis['base_prediction'],
        "reply":       response['response_text'],
        "tone":        response['tone'],
    }


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("ui.html", encoding="utf-8") as f:
        return f.read()