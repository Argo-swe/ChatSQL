from jsonschema import validate
from pathlib import Path
from core.port.incoming.schema_validator_use_case import SchemaValidatorUseCase
from tools.utils import Utils


class JsonSchemaValidatorAdapter(SchemaValidatorUseCase):

    def __init__(self):
        self._dictionary_schema_file_path = (
            Path(__file__).parent / "./dictionary_schema.json"
        )

    def validate(self, dictionary_content: str) -> bool:
        """Validate a JSON dictionary with base ChatSQL dictionary schema"""
        schema = Utils.read_json_file_content(self._dictionary_schema_file_path)

        if schema is None:
            return False

        try:
            validate(Utils.string_to_json(dictionary_content), schema)
            return True
        except Exception:
            return False
