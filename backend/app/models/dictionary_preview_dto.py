from typing import List
from fastapi_camelcase import CamelModel, ConfigDict
from models.dictionary_internal_structure.table_dto import TableDto

class DictionaryPreviewDto(CamelModel):
    database_name: str
    database_description: str
    tables: List[TableDto]

    model_config = ConfigDict(from_attributes=True)
