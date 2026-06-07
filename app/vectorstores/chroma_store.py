from langchain_community.vectorstores import Chroma
import chromadb

class ChromaStore:
    def __init__(self):
        self.client  = chromadb.PersistentClient(
            path="vector_db"
        )
        self.collection = self.client.get_or_create_collection(
            name="rag_collection"
        )
        
        
    def add_documents(self,chunks,embedding):
         ids = [str(i) for i in range(len(chunks))]
         self.collection.add(
           documents=chunks,
           embeddings=embedding.tolist(),
           ids=ids  
         )       
         
    def search(self,query_embedding,n_results=3):
        results = self.collection.query(
           query_embeddings=[query_embedding.tolist()],
           n_results=n_results 
        )
        return results 
    
    def chromaFire(self,chunks,embedding):
         db = Chroma.from_documents(chunks,embedding)
         return db 