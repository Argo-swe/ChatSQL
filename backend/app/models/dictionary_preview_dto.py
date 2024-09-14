from typing import List
from fastapi_camelcase import CamelModel, ConfigDict
from models.dictionary_internal_structure.table_dto import TableDto


class DictionaryPreviewDto(CamelModel):
    """Data Transfer Object to preview the contents of a dictionary.

    Attributes:
        database_name (str): The name of the database.
        database_description (str): The description of the database.
        tables (List[TableDto]): A list of tables contained in the database.
    """

    database_name: str
    database_description: str
    tables: List[TableDto]

    model_config = ConfigDict(from_attributes=True)
