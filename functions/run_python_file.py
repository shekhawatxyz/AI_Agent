import os
import config
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    full_file_path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(full_file_path)
    absolute_working_dir = os.path.abspath(working_directory)
    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    command = ["python", absolute_file_path] + args
    try:
        completed_process = subprocess.run(
            command,
            cwd=absolute_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )
        output_parts = []
        completed_process_output = completed_process.stdout
        completed_process_error = completed_process.stderr
        completed_process_returncode = completed_process.returncode
        if completed_process_output.strip():
            output_parts.append(f"STDOUT:\n{completed_process_output.strip()}")
        if completed_process_error.strip():
            output_parts.append(f"STDERR:\n{completed_process_error.strip()}")
        if completed_process_returncode != 0:
            output_parts.append(
                f"Process exited with code {completed_process_returncode}"
            )
        if not output_parts:
            return "No output produced"
        return "\n\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
