import easyocr
import pytesseract
from PIL import Image

class OCRServices:
    def __init__(self):
        self.ocr = easyocr.Reader(["en","hi"],gpu=False)
        
    def easy_ocr(self,image_path):
        results = self.ocr.readtext(image_path)
        texts = []
        for box,text,confidence in results:
              if confidence > 0.6:
                  texts.append(text)
        ocr_text = " ".join(texts)
        return ocr_text          
     
     
    def tesseract_ocr(self,image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)     