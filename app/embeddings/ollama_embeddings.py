from langchain_community.embeddings import HuggingFaceEmbeddings 
from typing import List
class Embedding:
    def __init__(self):
        self.embed = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device":"cpu"}   
        )
        
    def get_embedding(self):
        return self.embed    
        
    def embed_query(self,query:str):
        return self.embed.embed_query(query)
    
    def embed_documents(self,texts:List[str]):
        return self.embed.embed_documents(texts)