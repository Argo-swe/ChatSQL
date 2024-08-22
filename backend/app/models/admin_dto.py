from typing import Optional
from fastapi_camelcase import CamelModel


class AdminDto(CamelModel):
    id: Optional[int] = None
    username: str
    password: str

    class Config:
        from_attributes = True
