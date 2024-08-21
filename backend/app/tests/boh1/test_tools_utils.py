import pytest
from tools.utils import Utils
from pathlib import Path


def test_read_file_content():
    file_path = Path(__file__).parent / "../assets/wrong_json.json"

    content = Utils.read_file_content(file_path)

    assert "Wrong JSON file content\n" == content


def test_read_file_content_wrong_path():
    file_path = Path(__file__).parent / "../assets/wrong_json_NO_EXISTS.json"

    content = Utils.read_file_content(file_path)

    assert content is None


def test_read_json_file_content():
    file_path = Path(__file__).parent / "../assets/simple_json.json"

    content = Utils.read_json_file_content(file_path)

    assert content is not None


def test_read_json_file_content_wrong_content():
    file_path = Path(__file__).parent / "../assets/wrong_json.json"

    content = Utils.read_json_file_content(file_path)

    assert content is None


def test_stirng_to_json_ok():
    json = '{ "prop": 1 }'
    json_str = Utils.string_to_json(json)
    print(json_str)
    assert json_str is not None


def test_stirng_to_json_wrong():
    json = "invalid json\n"
    json_str = Utils.string_to_json(json)
    assert json_str is None


def test_is_json_ok():
    json = '{ "prop": 1 }'
    is_json = Utils.is_json(json)
    assert is_json == True


def test_is_json_wrong():
    json = "invalid json\n"
    is_json = Utils.is_json(json)
    assert is_json == False
