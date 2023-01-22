from typing import Optional, List
from pydantic import BaseModel, Field

class BarcodeNumber(BaseModel):
    value: str  = Field(
        ..., title="The value number of the Barcode (12 + 1)", max_length=13
    )
    name: Optional[str] = Field(
        None, title="The name of the Barcode", max_length=50
    )
