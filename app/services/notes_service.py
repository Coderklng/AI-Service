from prompts.notes_template import NotesTemplate
from services.create_pdf import PDFService
import re
import uuid

class NotesService:
    def __init__(self, llm):
        self.llm = llm
        self.pdf = PDFService()

    def clean_text(self, text):
        # proper cleanup
        text = re.sub(r"[*#`_]+", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"=+", "", text)
        text = re.sub(r"-{2,}", "", text)
        text = re.sub(r"\n\s*\n", "\n", text)
        return text.strip()

    def notes_generator(self, query):
        prompt = NotesTemplate.notes_template()

        response = prompt.invoke({
            "text": query
        })

        model_output = self.llm.invoke(response)

        # clean LLM output
        cleaned_text = self.clean_text(model_output)

        # unique file name (VERY IMPORTANT)
    
        title = " ".join(query.strip().split()[:3]) or "Notes"

        file_id,filename = self.pdf.create_pdf(
            title=title,
            content=cleaned_text
        )
        
        return {
            "message": "PDF created successfully",
            "download_url": f"https://ai-service-production-558b.up.railway.app/download/{file_id}",
            "filename":filename,
            "notes": model_output
        }