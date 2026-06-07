from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
import uuid
import os 

UPLOAD_DIR = "../uploads"

os.makedirs(UPLOAD_DIR,exist_ok=True)

class PDFService:
    def __init__(self, filename=f"../uploads/notes_{uuid.uuid4()}.pdf"):
       self.doc = SimpleDocTemplate(filename=filename) 
       self.filename = filename
       self.styles = getSampleStyleSheet()
       self.custom_style = ParagraphStyle(
           "Custom",
           parent=self.styles["BodyText"],
           leading=14,
           fontSize=14,
           spaceAfter=8
       )

    def _build_story(self, title, content):
        story = []
        #title
        title_style = ParagraphStyle(
        "TitleStyle",
        parent=self.styles["Title"],
        alignment=1,  # center
        fontSize=20,
        spaceAfter=20
    )

        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        
        body_style = ParagraphStyle(
        "BodyStyle",
        parent=self.styles["BodyText"],
        fontSize=12,
        leading=18,   # IMPORTANT: line spacing
        spaceAfter=10
        )
        
        heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=self.styles["Heading2"],
        fontSize=14,
        textColor=colors.darkblue,
        spaceBefore=12,
        spaceAfter=8,
        leading=16
        )
        # Content lines
        for line in content.split("\n"):
            line = line.strip()

            if not line:
                continue

            # Heading (simple rule: uppercase lines)
            if line.isupper():
                heading_style = ParagraphStyle(
                    "Heading",
                    parent=self.styles["Heading2"],
                    textColor=colors.darkblue,
                    spaceAfter=6,
                )
                story.append(Paragraph(line, heading_style))
            else:
                story.append(Paragraph(line, self.custom_style))

            story.append(Spacer(1, 4))

        return story

    def create_pdf(self, title, content):
        file_id = str(uuid.uuid4())
        file_name = os.path.join(UPLOAD_DIR,f"notes_{file_id}.pdf")
        doc = SimpleDocTemplate(file_name)
        story = self._build_story(title,content)
        doc.build(story)
        return file_id,file_name