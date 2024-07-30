from fastapi_camelcase import CamelModel


class TableDto(CamelModel):
    name: str
    description: str

    class Config:
        from_attributes = True
