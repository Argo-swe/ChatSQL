import re
from typing import ClassVar, Optional
from pydantic import field_validator
from fastapi_camelcase import CamelModel, ConfigDict


class DictionaryDto(CamelModel):
    """Data Transfer Object for carrying dictionary information.

    Attributes:
        id (Optional[int]): The unique identifier of the dictionary, optional for creating new entries.
        name (str): The name of the dictionary.
        description (str): The description of the dictionary.    
    """
    id: Optional[int] = None
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

    # Regex pattern to validate the name field (alphanumeric, spaces, hyphens, underscores)
    valid_pattern: ClassVar[re.Pattern] = re.compile(r"^[\w\s\-]+$")

    @field_validator("name", mode="before")
    def validate_name(cls, value: str) -> str:  # noqa: N805
        """Validator method for the 'name' field that ensures it matches the allowed pattern.

        Args:
            value (str): The name to be validated.

        Raises:
            ValueError: If the 'name' field contains invalid characters.

        Returns:
            str: The validated name.
        """
        if not cls.valid_pattern.match(value):
            raise ValueError(
                "The field must contain only alphanumeric characters, spaces, hyphens (-), or underscores (_)."
            )
        return value
