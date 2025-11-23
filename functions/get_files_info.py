from google.genai import types
import os
from os.path import isdir


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)
    # Security check
    if not absolute_path.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    try:
        directory_contents = os.listdir(absolute_path)
        y = ""
        for d in directory_contents:
            item_path = os.path.join(absolute_path, d)
            y += f"- {d}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n"
        return y
    except Exception as e:
        return f"Error: A problem occurred: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
