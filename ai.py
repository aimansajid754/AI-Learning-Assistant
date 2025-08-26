import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# pick a fast model for generation
MODEL_ID = "gemini-1.5-flash"

def _model():
    return genai.GenerativeModel(MODEL_ID)

def summarize_section(section_text: str, style: str = "concise"):
    prompt = f"""
You are a helpful study assistant.
Summarize the section below in {style} bullet points.
Use only facts from the text. If info is missing, say "Not in document".
Section:
\"\"\"{section_text}\"\"\""""
    resp = _model().generate_content(prompt)
    return resp.text.strip()

def generate_mcqs(section_text: str, n_questions: int = 8, difficulty: str = "medium"):
    system = (
        "Create multiple choice questions from the provided content only. "
        "Return valid JSON with this schema: "
        "{\"questions\":[{\"question\":\"...\",\"options\":[\"A\",\"B\",\"C\",\"D\"],"
        "\"answer_index\":0,\"explanation\":\"...\"}]}"
    )
    prompt = f"""
Content:
\"\"\"{section_text}\"\"\"
Rules:
- Make {n_questions} MCQs
- Difficulty: {difficulty}
- No outside knowledge
- Each question must have exactly 4 options and one correct answer_index
- Keep explanations short and grounded in the content
Return JSON only."""
    resp = _model().generate_content(
        [system, prompt],
        generation_config={"response_mime_type": "application/json"}
    )
    try:
        data = json.loads(resp.text)
        return data.get("questions", [])
    except Exception:
        # fallback: try to coerce
        txt = resp.text.strip()
        txt = txt[txt.find("{") : txt.rfind("}") + 1]
        return json.loads(txt).get("questions", [])

def generate_flashcards(section_text: str, n_cards: int = 12):
    system = (
        "Extract key concepts as Q&A flashcards based only on the content. "
        "Return JSON as {\"cards\":[{\"q\":\"...\",\"a\":\"...\"}]}"
    )
    prompt = f"""
Content:
\"\"\"{section_text}\"\"\"
Rules:
- Create {n_cards} concise Q&A pairs
- Focus on definitions, formulas, lists, contrasts
- Use simple language
Return JSON only."""
    resp = _model().generate_content(
        [system, prompt],
        generation_config={"response_mime_type": "application/json"}
    )
    try:
        data = json.loads(resp.text)
        return data.get("cards", [])
    except Exception:
        txt = resp.text.strip()
        txt = txt[txt.find("{") : txt.rfind("}") + 1]
        return json.loads(txt).get("cards", [])
