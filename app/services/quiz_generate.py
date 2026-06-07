from prompts.quiz_generate_prompt import QuizTemplate

class QuizGenerate:
     def __init__(self,llm):
         self.llm = llm 
                  
     def generateQuiz(self,query):
          prompt = QuizTemplate.quiz_generate()
          response = prompt.invoke({
              "context":query
          })   
          response_model = self.llm.invoke(response)
          return {
              "query":query,
              "answer":response_model
          }
          