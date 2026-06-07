from langchain_ollama import ChatOllama


class LLMService:

    def __init__(self):
        self.llm = ChatOllama(
            model="tinyllama",
            temperature=0.7,
            top_p=0.95,
            top_k=50,
            do_sample=False
        )

    def invoke(self, prompt):

        response = self.llm.invoke(prompt)

        return response.content