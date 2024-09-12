from typing import Optional
from fastapi_camelcase import CamelModel, ConfigDict


class AdminDto(CamelModel):
    """Data Transfer Object for carrying admin information.

    Attributes:
        id (Optional[int]): The unique identifier of the admin, optional for creating new users.
        username (str): The username of the admin.
        password (str): The password of the admin.
    """
    id: Optional[int] = None
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)
