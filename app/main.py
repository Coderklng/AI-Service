from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys
import uuid
from langchain_core.output_parsers import JsonOutputParser
# Imports bina 'app.' prefix ke (kyunki file 'app' folder ke andar hai)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routes import router
from services.rag_service import RAGService
from services.llm_service import LLMService
from services.groq_service import GroqService
from vectorstores.faiss_store import VectorDB
from embeddings.ollama_embeddings import Embedding
from schemas.request import ChatRequest
from services.chat_service import ChatService
from services.quiz_generate import QuizGenerate
from services.notes_service import NotesService
from services.ats_service import ATSService
from loaders.pdf_loader import Loader
from services.support_service import SupportService
import uvicorn

load_dotenv()
api_key = os.getenv("API_KEY")

app = FastAPI()

app.include_router(router,prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize Services
embed = Embedding().get_embedding()
db = VectorDB(embed)
llm = GroqService(api_key=api_key)
chatbot = RAGService(vectorDb=db, llm=llm)
support = SupportService(llm=llm)
quiz = QuizGenerate(llm=llm)
serviceNotes = NotesService(llm=llm)
service = ChatService(llm=llm)

app.include_router(router, prefix="/api")

@app.get("/")
def wel():
    return {"message": "Hurray! I am created Backend API"}

@app.post("/chat")
def chat_generate(request: ChatRequest):
    return chatbot.chat(query=request.question)

@app.post("/chat-with_ai")
def AiChat(request: ChatRequest):
    return service.chat_with_ai(query=request.question)

@app.post("/quiz/generate")
def generateQuiz(request: ChatRequest):
    return quiz.generateQuiz(query=request.question)

@app.post("/notes/generator")
def generate(request: ChatRequest):
    return serviceNotes.notes_generator(query=request.question)

@app.post("/support")
def create_support(request: ChatRequest):
    return support.chat_team(query=request.question)

@app.post("/upload/resume")
def upload_resume(job_description: str = Form(...), file: UploadFile = File(...)):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    upload_dir = os.path.join(BASE_DIR, "..", "data", "raw")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{uuid.uuid4()}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    pdf_loader = Loader(path=file_path)
    ats = ATSService(vectorDb=db, llm=llm.llm, loader=pdf_loader, parser=JsonOutputParser())
    return {"message": "ATS processed", "result": ats.tracking(job_description=job_description)}

@app.get("/download/{file_id}")
def download_file(file_id: str):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads", f"notes_{file_id}.pdf")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type="application/pdf", filename=f"notes_{file_id}.pdf")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) # Render PORT variable dega, nahi toh default 10000
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)