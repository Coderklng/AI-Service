import numpy as np 

class Retrieval:
    def __init__(self,index,chunks,embedding):
        self.index = index 
        self.chunks = chunks 
        self.embedding = embedding
        
    def retrieveAug(self,user_query,k=3):
        
        query_vector = self.embedding.customEmbedding([user_query])
        
        query_vector = np.array(query_vector).astype("float32")
        
        distance,indices = self.index.search(query_vector,k)
        
        results = []
        
        for idx in indices[0]:
            
            results.append(self.chunks[idx])
            
        return results    