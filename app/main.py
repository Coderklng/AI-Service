from fastapi import FastAPI,UploadFile,File,Form,HTTPException
import uvicorn
from fastapi.responses import FileResponse
from api.routes import router
from services.rag_service import RAGService
from services.llm_service import LLMService
from services.groq_service import GroqService
from vectorstores.faiss_store import VectorDB
from embeddings.ollama_embeddings import Embedding
from schemas.request import ChatRequest
from  dotenv import load_dotenv  
import os 
from fastapi.middleware.cors import CORSMiddleware
from services.chat_service import ChatService
from services.quiz_generate import QuizGenerate
from services.notes_service import NotesService
from services.ats_service import ATSService
from schemas.ats_request import ATSRequest
from loaders.pdf_loader import Loader
from langchain_core.output_parsers import JsonOutputParser
from services.llm_service import LLMService
import uuid
import os
from services.support_service import SupportService

load_dotenv()

api_key = os.getenv("API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

embed = Embedding().get_embedding()

db = VectorDB(embed)
 

llm = GroqService(api_key=api_key)


chatbot = RAGService(vectorDb=db,llm=llm)

support = SupportService(llm=llm)

quiz = QuizGenerate(llm=llm)

serviceNotes  = NotesService(llm=llm)

model = LLMService()


service = ChatService(llm=llm)

app.include_router(router,prefix="/api")


@app.get("/")
def wel():
    return {
        "message":"Hurray ! I am created Backend API"
    }


@app.post("/chat")
def chat_generate(request:ChatRequest):
     query = request.question
     return  chatbot.chat(
        query=query 
     )


@app.post("/chat-with_ai")
def AiChat(request:ChatRequest):
    query = request.question 
    return service.chat_with_ai(
        query=query
    )
    
    
@app.post("/quiz/generate")
def generateQuiz(request: ChatRequest):
    query = request.question
    return quiz.generateQuiz(query=query)

@app.post("/notes/generator")
def generate(request: ChatRequest):
     query = request.question
     return serviceNotes.notes_generator(
         query=query
     )
     
     
     
@app.post("/support")
def create_support(request: ChatRequest):
    query = request.question 
    return support.chat_team(query=query)
     

@app.post("/upload/resume")
def upload_resume(
    job_description: str = Form(...),
    file: UploadFile = File(...)
):

    # 1. Safe upload directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    upload_dir = os.path.join(BASE_DIR, "..", "data", "raw")
    os.makedirs(upload_dir, exist_ok=True)

    # 2. Save file
    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 3. Load resume
    pdf_loader = Loader(path=file_path)
   
    parser = JsonOutputParser()
    # 4. ATS Service
    ats = ATSService(
        vectorDb=db,
        llm=llm.llm,
        loader=pdf_loader,
        parser=parser
    )

    # 5. Run ATS
    result = ats.tracking(
        job_description=job_description
    )

    return {
        "message": "ATS processed successfully",
        "result": result
    }
    
@app.get("/download/{file_id}")
def download_file(file_id:str):
    file_path = f"../uploads/notes_{file_id}.pdf"
    if not os.path.exists(file_path):
        return HTTPException(
            status_code=200,
            detail="File not found please regenerate your files"
        )
    return FileResponse(path=file_path,media_type="application/pdf",filename=f"notes_{file_id}.pdf")
