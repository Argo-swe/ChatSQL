from pydantic import BaseModel

class DictionaryDto(BaseModel):
    #id: int
    name: str
    description: str
