from prompts.chat_prompt import ChatTemplate

class ChatService:
    def __init__(self,llm):
        self.llm = llm 
        
    def chat_with_ai(self,query):
        prompt = ChatTemplate.chatAi()
        messages = prompt.invoke({
            "query":query
        })  
        response = self.llm.invoke(messages)
        content  = response.content if hasattr(response,"content") else str(response)
        return {
            "query":query,
            "answer":response
        }