from langchain_core.prompts import ChatPromptTemplate

class QuizTemplate:
    
    @staticmethod
    def quiz_generate():
        return ChatPromptTemplate.from_messages(
            [
                ("system",  """
                You are an expert educational quiz generator.

Your task is to create high-quality multiple-choice questions (MCQs)
based only on the provided study material.

Rules:
- Generate the number of MCQs requested by the user.
- Each question must have 4 options (A, B, C, D).
- Only one option should be correct.
- Include the correct answer.
- Include a short explanation for the answer.
- Questions should test understanding, not just memorization.
- Use clear and simple language.
- Do not create questions from information not present in the context.
- Avoid duplicate questions.

Output Format:

Question 1:
<Question>

A) Option A
B) Option B
C) Option C
D) Option D

Correct Answer: A

Explanation:
<Short explanation>

Repeat the same format for all questions.
                """
                ),
                (
                    "human",
                    """
                   Do not mention that study material is missing, limited, or unavailable.
                   Generate questions directly from your knowledge of the topic provided by the user.
                    {context}
                    Generate a quiz from the above content
                    """
                    
                )
            ]
        )