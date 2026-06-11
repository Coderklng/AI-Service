from langchain_community.vectorstores import FAISS 
import os

# Folder path define karo
PERSISTENT_DIR = "/tmp/vector_db"

# Ye ensure karega ki agar folder nahi hai, toh ban jaye
os.makedirs(PERSISTENT_DIR, exist_ok=True)
class VectorDB:
    def __init__(self, embedding):
        self.embedding = embedding
      # Path fix kar diya
        
    def storeDb(self, docs):
        db = FAISS.from_documents(docs, self.embedding)
        db.save_local(PERSISTENT_DIR)
        return db
    
    def localDb(self):
        return FAISS.load_local(
            PERSISTENT_DIR,
            self.embedding,
            allow_dangerous_deserialization=True
        )
        
    def get_documents(self,query,k=3):
        db = self.localDb()
        save_db =  db.as_retriever(
            search_type="similarity",
            search_kwargs={"k":k}
        )
        retriever_aug = save_db.invoke(query)
        return retriever_aug
    
    
        
    def get_search(self,query,k=3):
        db = self.localDb()
        return db.similarity_search(  
           query=query,
          k=k                         
         )
        
        