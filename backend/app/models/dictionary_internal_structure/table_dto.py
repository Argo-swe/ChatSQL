from fastapi_camelcase import CamelModel, ConfigDict

class TableDto(CamelModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
