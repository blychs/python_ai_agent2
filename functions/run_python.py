import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    absolute_path_wd = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(path)
    if not absolute_path.startswith(absolute_path_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_path):
        return f'Error: File "{file_path}" not found.'
    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        run_process = subprocess.run(
            ["uv", "run", file_path],
            timeout=30,
            capture_output=True,
            cwd=absolute_path_wd,
            *args,
        )
        stdout = f"STDOUT: {run_process.stdout}"
        stderr = f"STDERR: {run_process.stderr}"
        output = stdout + stderr
        exit_code = run_process.returncode
        if exit_code != 0:
            output += str(exit_code)
        if stdout == "STDOUT: ":
            return "No output produced"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that should be run, relative to the working directory. If not provided, it returns an Error string.",
            ),
            # "args": types.Schema(
            #     type=types.Type.ARRAY,
            #     description="The list of arguments provided to the function",
            #     nullable=True,
            # ),
        },
    ),
)
