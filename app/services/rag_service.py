from prompts.prompt_template import OwnTemplate

class RAGService:

    def __init__(
        self,
        vectorDb,
        llm
    ):
        self.vectorDb = vectorDb
        self.llm = llm
    def chat(self, query):
    
        docs = self.vectorDb.get_documents(query=query, k=3)

    # remove duplicates
        unique_docs = list({doc.page_content: doc for doc in docs}.values())

        context = "\n\n".join([
        doc.page_content.strip()
        for doc in unique_docs
        ])[:4000]

        prompt = OwnTemplate.message_prompt()

        messages = prompt.invoke({
        "context": context,
        "query": query
         })

        answer = self.llm.invoke(messages)
       
        return {
        "query": query,
        "answer": answer,
        "context": context
         }