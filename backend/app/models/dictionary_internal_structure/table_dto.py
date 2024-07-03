from pydantic import BaseModel

class TableDto(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True
