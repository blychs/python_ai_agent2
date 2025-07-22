import os
from google.genai import types


MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(path)
    absolute_working_path = os.path.abspath(working_directory)
    if not absolute_path.startswith(absolute_working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(absolute_path, "r") as f:
            file_contents = f.read(MAX_CHARS)
        if len(file_contents) >= MAX_CHARS:
            file_contents += f'\n[...File "{file_path}" truncated at 10000 characters]'
        return file_contents
    except Exception as e:
        return f"Error listing file contents: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents, up to 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to show the contents from, relative to the working directory. If not provided, it will fail",
            ),
        },
    ),
)
