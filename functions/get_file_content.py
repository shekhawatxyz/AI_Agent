import os
import config


def get_file_content(working_directory, file_path):
    full_file_path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(full_file_path)
    absolute_working_dir = os.path.abspath(working_directory)
    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        MAX_CHARS = config.MAX_CHARS
        with open(absolute_file_path) as f:
            file_content_string = f.read(MAX_CHARS)
            remaining_char = f.read(1)
            if remaining_char:
                return f'{file_content_string}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            else:
                return file_content_string
    except Exception as e:
        return f"Error: {e}"
