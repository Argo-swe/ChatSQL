from fastapi_camelcase import CamelModel, ConfigDict


class TableDto(CamelModel):
    """Data Transfer Object for representing table information within a database schema.

    Attributes:
        name (str): The name of the table in the database.
        description (str): The description of the table in the database.
    """

    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
