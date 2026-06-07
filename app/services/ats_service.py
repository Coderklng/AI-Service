from prompts.ats_prompt import ATSTemplate

class ATSService:
    def __init__(self,vectorDb,llm,loader,parser):
           self.vectorDb = vectorDb
           self.llm = llm 
           self.parser = parser
           self.loader = loader
           
    def tracking(self, job_description):
      docs = self.loader.load_with_pdf()
      resume_text = "\n".join([d.page_content for d in docs])
      prompt = ATSTemplate.ats_prompt()
      chain = prompt | self.llm | self.parser 
      result = chain.invoke({
        "context":resume_text,
         "format_instruction":self.parser.get_format_instructions(),
        "job_text":job_description
      })

      return {"result": result}