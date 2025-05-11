from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from utils.pdf_processor import process_pdf
from utils.agent import create_agent
from typing import Dict
import os

app = FastAPI(title="PDF QA Agent", version="0.1.0")
agent = create_agent()

pdf_store: Dict[str, str] = {}

class ChatRequest(BaseModel):
    query: str
    filename: str = None

def format_context(context: str, max_tokens: int = 3000) -> str:
    return " ".join(context.split())[:max_tokens]


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF uploads with validation"""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, detail="Only PDF files are accepted")
    
    try:
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(413, detail="File too large (max 10MB)")
            
        text = process_pdf(content)
        pdf_store[file.filename] = text
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        raise HTTPException(500, detail=f"Processing failed: {str(e)}")


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not pdf_store:
        raise HTTPException(400, detail="Please upload a PDF first")

    # choose the PDF text
    context = (
        pdf_store.get(request.filename)
        if request.filename
        else next(iter(pdf_store.values()))
    )
    # build a flat list of messages
    messages = [
        {
            "role": "system",
            "content": f"PDF Context:\n\n{format_context(context)}"
        },
        {
            "role": "user",
            "content": request.query
        }
    ]

    try:
        answer = agent(messages)
    except Exception as e:
        # bubble up any validation / API errors
        raise HTTPException(500, detail=str(e))

    return {"response": answer}
