from pydantic import BaseModel
from typing import Optional

class TranscriptionResponse(BaseModel):
    status: str
    text: str
    filename: str

class ErrorResponse(BaseModel):
    detail: str
    status: str = "error"