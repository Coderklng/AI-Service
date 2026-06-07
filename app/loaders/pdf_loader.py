from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
import pdfplumber


class Loader:
    def __init__(self, path: str):
        self.path = path

    # -------------------------
    # LangChain single PDF
    # -------------------------
    def load_with_pdf(self):
        try:
            loader = PyPDFLoader(self.path)
            return loader.load()
        except Exception as e:
            print(f"[PyPDFLoader Error]: {e}")
            return []

    # -------------------------
    # LangChain folder loader
    # -------------------------
    def load_with_directory(self):
        try:
            loader = PyPDFDirectoryLoader(self.path)
            return loader.load()
        except Exception as e:
            print(f"[DirectoryLoader Error]: {e}")
            return []

    # -------------------------
    # pdfplumber (best for raw text extraction)
    # -------------------------
    def load_with_plumber(self):
        try:
            text = ""

            with pdfplumber.open(self.path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:   # important fix
                        text += page_text + "\n"

            return text.strip() if text else None

        except Exception as e:
            print(f"[pdfplumber Error]: {e}")
            return None