from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-3.8-flash")

def ask_gemini(prompt):
    try:
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Error: {e} - Check API Key"

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return open("templates/index.html", encoding="utf-8").read()

@app.post("/ask")
def ask_question(question: str = Form(...)):
    prompt = f"Answer this student question in simple way: {question}"
    return {"answer": ask_gemini(prompt)}

@app.post("/explain")
def explain_topic(topic: str = Form(...)):
    prompt = f"Explain {topic} in simple English for college students with examples"
    return {"answer": ask_gemini(prompt)}

@app.post("/summarize")
def summarize(paragraph: str = Form(...)):
    prompt = f"Summarize this paragraph in 80 words: {paragraph}"
    return {"summary": ask_gemini(prompt)}

@app.post("/quiz")
def get_quiz(topic: str = Form(...)):
    prompt = f"Generate 3 quiz questions about {topic} with 4 options. Return ONLY JSON: [{{\"question\":\"...\",\"options\":[\"A\",\"B\",\"C\",\"D\"],\"answer\":\"A\"}}]"
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json","").replace("```","").strip()
        s=text.find("["); e=text.rfind("]")+1
        return {"quiz": json.loads(text[s:e])}
    except:
        return {"quiz": [{"question": f"What is {topic}?","options":["A","B","C","D"],"answer":"A"}]*3}

@app.post("/learning-plan")
def learning_plan(goal: str = Form(...)):
    prompt = f"Create a 7-day personalized learning plan for: {goal}. Give day wise tasks."
    return {"plan": ask_gemini(prompt)}