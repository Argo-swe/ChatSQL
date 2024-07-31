from typing import List
from fastapi_camelcase import CamelModel
from models.dictionary_internal_structure.table_dto import TableDto


class DictionaryPreviewDto(CamelModel):
    database_name: str
    database_description: str
    tables: List[TableDto]

    class Config:
        from_attributes = True
