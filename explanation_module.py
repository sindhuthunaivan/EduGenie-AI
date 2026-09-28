from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def explain_topic(topic: str):
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(f"Explain in detail: {topic}")
    return response.text