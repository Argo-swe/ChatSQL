from typing import Optional
from fastapi_camelcase import CamelModel, ConfigDict


class AdminDto(CamelModel):
    id: Optional[int] = None
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)
