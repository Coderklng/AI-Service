from pydantic import BaseModel
from typing import List,Optional    

class CodeResponse(BaseModel):
    summary : str
    language : str
    code : str
    explanation : Optional[str] = None
    notes : Optional[str] = None