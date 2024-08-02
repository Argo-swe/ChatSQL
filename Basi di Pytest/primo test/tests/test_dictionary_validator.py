from dictionary_validator import DictionaryValidator
import pytest
from pathlib import Path
from jsonschema.exceptions import ValidationError

def test_validate_successful(mocker):
    # Il valid_json è del JSON per cui andiamo a chiedere la verifica e che sappiamo già essere valido
    valid_json = {
        "database_name": "SampleDB",
        "database_description": "A sample database schema.",
        "tables": [
            {
                "name": "table1",
                "description": "A sample table",
                "table_synonyms": ["tbl1", "t1"],
                "columns": [
                    {
                        "name": "column1",
                        "type": "varchar",
                        "description": "A sample column",
                        "column_synonyms": ["col1", "c1"]
                    }
                ],
                "primary_key": ["column1"],
                "foreign_keys": [
                    {
                        "foreign_key_column_names": ["column1"],
                        "reference_table_name": "table2",
                        "reference_column_names": ["column2"]
                    }
                ]
            }
        ]
    }

    # Il nostro schema JSON, secondo il dizionario dati
    mock_schema = {
        "type": "object",
        "required": [
            "database_name",
            "database_description",
            "tables"
        ],
        "properties": {
            "database_name": {
                "type": "string"
            },
            "database_description": {
                "type": "string"
            },
            "tables": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": [
                        "name",
                        "description",
                        "columns",
                        "primary_key"
                    ],
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "table_synonyms": {
                            "type": [ "array", "null" ],
                            "items": {"type": "string"}
                        },
                        "columns": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": [
                                    "name",
                                    "type",
                                    "description"
                                ],
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    },
                                    "type": {
                                        "type": "string"
                                    },
                                    "description": {
                                        "type": "string"
                                    },
                                    "column_synonyms": {
                                        "type": [ "array", "null" ],
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        },
                        "primary_key": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1
                        },
                        "foreign_keys": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "foreign_key_column_names",
                                    "reference_table_name",
                                    "reference_column_names"
                                ],
                                "properties": {
                                    "foreign_key_column_names": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "reference_table_name": {
                                        "type": "string"
                                    },
                                    "reference_column_names": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Ora mettiamo il mock della lettura del JSON di Utils
    mocker.patch('utils.utils.Utils.read_json_file_content', return_value=mock_schema)
    
    # # Poi il mock di jsonschema.validate, che non fa nulla per simulare il successo
    mocker.patch('jsonschema.validate')

    # Il test viene eseguito da queste due righe
    result = DictionaryValidator.validate(valid_json)
    assert result is True, "The validator should return True for valid JSON input"
