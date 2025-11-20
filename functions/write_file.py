import os
import config


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)
    parent_dir = os.path.dirname(absolute_path)

    if not absolute_path.startswith(absolute_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f"Error: Failed to create parent directory for {file_path}: {e}"
    try:
        with open(absolute_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error {e}"
