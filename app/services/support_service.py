from prompts.support_template import SupportTemplate
import re 

class SupportService:
    def __init__(self,llm):
        self.llm = llm 
        
        
    def clean_text(self, text):
        # proper cleanup
        text = re.sub(r"[*#`_]+", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"=+", "", text)
        text = re.sub(r"-{2,}", "", text)
        text = re.sub(r"\n\s*\n", "\n", text)
        return text.strip()
    
    
    def chat_team(self,query):
        prompt = SupportTemplate.support_team()
        query_base = prompt.invoke({
            "query":query
        })
        response = self.llm.invoke(query_base)
        cleaned_text = self.clean_text(response)
        return {
            "user_query":query,
            "response":cleaned_text
        }
        