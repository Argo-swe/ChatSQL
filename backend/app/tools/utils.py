import json


class Utils:
    """A class used for general utility methods."""

    @staticmethod
    def read_file_content(file_path):
        """Reads the content of a file given its path.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file if the file is found, None otherwise.
        """
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print("File not found.")

    @staticmethod
    def read_json_file_content(file_path):
        """Reads and parses the content of a JSON file given its path.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict or list: The parsed JSON content.
            None: If the file content is not valid JSON or the file is not found.
        """
        content = Utils.read_file_content(file_path)
        if content is not None and Utils.is_json(content):
            return json.loads(content)
        else:
            return None

    @staticmethod
    def string_to_json(json_string):
        """Convert a JSON string to a JSON object.

        Args:
            json_string (str): A string containing JSON data.

        Returns:
            dict or list: The parsed JSON string.
            None: If the string is not valid JSON.
        """
        if Utils.is_json(json_string):
            return json.loads(json_string)
        else:
            return None

    @staticmethod
    def is_json(string):
        """Validate if JSON string represents a valid JSON.

        Args:
            string (str): The string to validate.

        Returns:
            bool: True if the string is valid JSON, False otherwise.
        """
        try:
            json.loads(string)
        except ValueError:
            return False
        return True
