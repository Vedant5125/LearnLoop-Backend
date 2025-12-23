from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend Running"}

ECON_CONTENT = """
Demand refers to the quantity of a good that consumers are willing
and able to purchase at different prices during a given period.

Law of Demand: As price increases, quantity demanded falls,
assuming other factors remain constant.
"""

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    prompt = f"""
You are an Economics teacher.
Use ONLY the content below to answer.

Content:{ECON_CONTENT}

Question:{query.question}

Explain clearly in simple terms.
"""
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role":"user", "content": prompt}]
    )

    return {"answer": response.choices[0].message.content}

