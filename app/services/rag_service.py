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

        # retrieve documents
        docs = self.vectorDb.get_documents(
            query=query,
            k=3
        )

        # context build
        context = "\n\n".join(
            [
                doc.page_content
                if hasattr(doc, "page_content")
                else str(doc)
                for doc in docs
            ]
        )

        # build prompt
        prompt = OwnTemplate.message_prompt()

        messages = prompt.invoke(
            {
                "context": context,
                "query": query
            }
        )

        # llm response
        answer = self.llm.invoke(messages)
        content = answer.content if hasattr(answer,"content") else str(answer)
        return {
            "query": query,
            "answer":content,
            "context": context
        } 