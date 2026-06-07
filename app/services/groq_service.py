from langchain_groq import ChatGroq


class GroqService:

    def __init__(self, api_key):

        self.llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.3-70b-versatile"
        )

    def invoke(self, prompt):

        response = self.llm.invoke(prompt)

        return response.content