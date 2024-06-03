from jsonschema import validate
import json

class Utils:
    """
    A class used for general utility methods
    """

    def read_file_content(file_path):
        """
        Read file content form path
        """
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("File not found.")

    def read_json_file_content(file_path):
        """
        Read JSON file content form path
        """
        content = Utils.read_file_content(file_path)
        #print(content)
        if Utils.is_json(content):
            #print("is json")
            print(json.loads(content))
            return json.loads(content)
        else:
            return

    def string_to_json(json_string):
        """
        Convert a JSON string to a JSON object
        """
        if Utils.is_json(json_string):
            #print("is json", json_string)
            return json.loads(json_string)
        else:
            return

    def is_json(string):
        """
        Validate if JSON string represents a valid JSON
        """
        try:
            json.loads(string)
        except ValueError:
            return False
        return True
