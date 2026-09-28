import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-3.8-flash")

def generate_quiz(topic):
    prompt = f"""
    Generate 3 quiz questions about {topic}.
    Each question has 4 options.
    Return ONLY JSON array: [{{"question": "...", "options": ["A","B","C","D"], "answer": "A"}}]
    """
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json","").replace("```","").strip()
        s = text.find("[")
        e = text.rfind("]")+1
        return json.loads(text[s:e])
    except Exception as ex:
        print(ex)
        return [
            {"question": f"What is {topic}?", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "Option A"},
            {"question": f"Second question about {topic}?", "options": ["A", "B", "C", "D"], "answer": "B"},
            {"question": f"Third question about {topic}?", "options": ["A", "B", "C", "D"], "answer": "C"}
        ]