from typing import Optional
from fastapi_camelcase import CamelModel, ConfigDict

class DictionaryDto(CamelModel):
    id: Optional[int] = None
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
