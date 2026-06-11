from prompts.code_template import CoderTemplate

class CoderService:
    def __init__(self,llm,parser):
        self.llm = llm 
        self.parser = parser
        
    def generate_code(self,query):
        prompt = CoderTemplate.coder_prompt()
        chain = prompt | self.llm | self.parser 
        response = chain.invoke({
            "query":query,
            "format_instructions": self.parser.get_format_instructions()
        })    
        return response 
    