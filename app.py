from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag.generator import generate_response 
from rag.podcast import generate_podcast

app = FastAPI(title="LearnLoop RAG API")

@app.get("/")
def home():
    return {"message": "LearnLoop API is running"}

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    try:
        user_text = query.question
        
        result = generate_response(user_text)
        
        return {
            "status": "success",
            "question": user_text,
            "answer": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/podcast")
async def process_script(query: Query):
    try:
        podcast_result = generate_podcast(query.question)
        return {
            "status": "success",
            "data": podcast_result
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))