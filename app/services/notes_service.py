from prompts.notes_template import NotesTemplate
from services.create_pdf import PDFService
import re

class NotesService:
    def __init__(self, llm):
        self.llm = llm
        self.pdf = PDFService()

    def clean_text(self, text):
        """
        Preserve markdown formatting while removing unwanted noise.
        """

        # remove markdown emphasis symbols only
        text = re.sub(r"[*`_]+", "", text)

        # remove long separator lines
        text = re.sub(r"=+", "", text)

        # limit excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def notes_generator(self, query):
        prompt = NotesTemplate.notes_template()

        response = prompt.invoke({
            "text": query
        })

        model_output = self.llm.invoke(response)

        # clean output but preserve markdown
        cleaned_text = self.clean_text(model_output)

        title = " ".join(query.strip().split()[:3]) or "Notes"

        file_id, filename = self.pdf.create_pdf(
            title=title,
            content=cleaned_text
        )

        return {
            "message": "PDF created successfully",
            "download_url": f"https://ai-service-production-558b.up.railway.app/download/{file_id}",
            "filename": filename,
            "notes": cleaned_text
        }
