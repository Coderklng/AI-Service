from dotenv import load_dotenv
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__),"..")
    )
)


from app.services.groq_service import GroqService
from app.loaders.pdf_loader import Loader
from app.utils.text_splitter import TextSplitter
from app.embeddings.ollama_embeddings import Embedding
from app.vectorstores.faiss_store import VectorDb
from app.retriever.langchain_retriever import LangchainRetriever
from app.prompts.prompt_template import OwnTemplate

# ==========================
# ENV
# ==========================

load_dotenv()

PATH = "../app/data/raw/MBA  QT & FM New(1) (1).pdf";


API_KEY = os.getenv("API_KEY")


# ==========================
# LLM
# ==========================

llm = GroqService(api_key=API_KEY)

# ==========================
# LOAD DOCUMENT
# ==========================

loader = Loader(PATH)

docs = loader.load_with_pdf()

# ==========================
# SPLIT DOCUMENT
# ==========================

splitter = TextSplitter(
    chunk_size=300,
    overlap=200
)

chunks = splitter.text_split(docs)

# ==========================
# EMBEDDING + FAISS
# ==========================

embedding = Embedding()



vector_db = VectorDb(embedding)

db = vector_db.storeDb(chunks)

# ==========================
# RETRIEVER
# ==========================

retriever = LangchainRetriever(db)

# ==========================
# USER QUERY
# ==========================

user_query = "What is financial management?"

retrieved_docs = retriever.retrieval(user_query)

# ==========================
# CONTEXT
# ==========================

context = "\n".join(
    [doc.page_content for doc in retrieved_docs]
)

# ==========================
# PROMPT
# ==========================

prompt = OwnTemplate.build_prompt(context=context,query=user_query)

# ==========================
# LLM RESPONSE
# ==========================

response = llm.invoke(prompt)

print(response)

