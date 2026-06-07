from langchain_core.prompts import ChatPromptTemplate

class OwnTemplate:

    @staticmethod
    def message_prompt():

        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an AI Study Assistant.

Your job is to answer questions using ONLY the provided context.

Rules:
1. Use only the information present in the context.
2. Do not make up facts.
3. If the answer is not available in the context, reply:
   "I could not find the answer in the provided document."
4. Keep answers clear and concise.
5. When possible, explain in simple student-friendly language.
6. If the context contains definitions, concepts, or steps, present them in a structured format.
                    """
                ),
                (
                    "human",
                    """
Context:
{context}

Question:
{query}

Answer:
                    """
                )
            ]
        )