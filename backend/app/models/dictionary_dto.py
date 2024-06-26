from typing import Optional
from pydantic import BaseModel

class DictionaryDto(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

    class Config:
        from_attributes = True
