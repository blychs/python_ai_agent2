import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(path)
    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    try:
        contents_of_dir = []
        for f in os.listdir(absolute_path):
            if not f.startswith("."):
                file_path = f"{absolute_path}/{f}"
                contents_of_dir.append(
                    f"- {f} file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
                )
        return "\n".join(contents_of_dir)
    except Exception as e:
        return f"Error listing files: {e}"


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
