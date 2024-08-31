import re
from typing import ClassVar, Optional
from pydantic import field_validator
from fastapi_camelcase import CamelModel, ConfigDict


class DictionaryDto(CamelModel):
    id: Optional[int] = None
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

    valid_pattern: ClassVar[re.Pattern] = re.compile(r"^[\w\s\-]+$")

    @field_validator("name", mode="before")
    def validate_name(cls, value: str) -> str:  # noqa: N805
        if not cls.valid_pattern.match(value):
            raise ValueError(
                "The field must contain only alphanumeric characters, spaces, hyphens (-), or underscores (_)."
            )
        return value