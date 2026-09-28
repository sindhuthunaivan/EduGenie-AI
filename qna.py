from dotenv import load_dotenv
load_dotenv()
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.8-flash")

def get_answer(text: str):
    try:
        response = model.generate_content(f"You are EduGenie, friendly AI tutor. Explain simply: {text}")
        return {"result": response.text}
    except Exception as e:
        return {"result": f"API Error: {e}"}