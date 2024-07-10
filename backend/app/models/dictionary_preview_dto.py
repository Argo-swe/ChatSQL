from typing import List
from pydantic import BaseModel
from models.dictionary_internal_structure.table_dto import TableDto

class DictionaryPreviewDto(BaseModel):
    database_name: str
    database_description: str
    tables: List[TableDto]

    class Config:
        from_attributes = True