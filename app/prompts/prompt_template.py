from langchain_core.prompts import ChatPromptTemplate


class OwnTemplate:

    @staticmethod
    def message_prompt():

        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an AI Study Assistant specialized in answering strictly from given context.

STRICT RULES:
1. You MUST use ONLY the provided context to answer.
2. Do NOT use outside knowledge or assumptions.
3. If answer is not in context, say:
   "I could not find the answer in the provided document."

4. Always try to:
   - Expand explanation using context
   - Make answer student-friendly
   - Keep structure clear (bullet points if needed)

5. If context contains definitions, explain them simply.
6. Never hallucinate information.

7. IMPORTANT:
   Always base every sentence on the context.
                    """
                ),
                (
                    "human",
                    """
CONTEXT:
{context}

QUESTION:
{query}

INSTRUCTIONS:
- Read context carefully
- Extract relevant information only
- Write a complete answer

ANSWER:
                    """
                )
            ]
        )