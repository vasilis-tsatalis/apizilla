from typing import Optional
from pydantic import BaseModel

class QRData(BaseModel):
    name: Optional[str] = None
    logo64: Optional[str] = None
    data: dict

class QRContent(BaseModel):
    name: Optional[str] = None
    content: str
