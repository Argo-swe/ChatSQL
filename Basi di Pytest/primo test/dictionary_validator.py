from jsonschema import validate
from pathlib import Path
from utils.utils import Utils


class DictionaryValidator:
    __dictionary_schema_file_path = (
        Path(__file__).parent / "./assets/dictionary_schema.json"
    )

    @staticmethod
    def validate(json_dictionary) -> bool:
        """Validate a JSON object dictionary with base ChatSQL dictionary schema"""
        print(DictionaryValidator.__dictionary_schema_file_path)
        schema = Utils.read_json_file_content(
            DictionaryValidator.__dictionary_schema_file_path
        )

        try:
            validate(json_dictionary, schema)
            print("dictionary is valid")
            return True
        except Exception as error:
            print("dictionary is invalid", error)
            return False
