from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
      def __init__(self,chunk_size=500,chunk_overlap=300):
          self.chunk_size = chunk_size 
          self.chunk_overlap = chunk_overlap
          
      def split_text(self,doc):
          splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,chunk_overlap=self.chunk_overlap)
          docs = splitter.split_documents(doc)
          return docs 
      
      