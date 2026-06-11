from fastapi import FastAPI,UploadFile,File,APIRouter
import uuid
import os
from loaders.pdf_loader import Loader 
from utils.text_splitter import TextSplitter
from embeddings.ollama_embeddings import Embedding
from vectorstores.faiss_store import VectorDB
import sys 
import os




router = APIRouter()

BASE_DIR =  os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR,"..","Uploader")

os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/upload")
async def uploaded_file(file: UploadFile = File(...)):

    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1. Load PDF
    loader = Loader(file_path)
    docs = loader.load_with_pdf()

    # 2. Split
    splitter = TextSplitter()
    chunks = splitter.split_text(docs)

    # 3. Store in FAISS
    embed = Embedding().get_embedding()
    db = VectorDB(embed)
    db.storeDb(chunks)

    return {
        "file_name": file_name,
        "message": "file uploaded & indexed successfully"
    }
    
