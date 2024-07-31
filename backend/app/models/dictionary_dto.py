from typing import Optional
from fastapi_camelcase import CamelModel


class DictionaryDto(CamelModel):
    id: Optional[int] = None
    name: str
    description: str

    class Config:
        from_attributes = True
