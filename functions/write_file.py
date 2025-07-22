import os
from google.genai import types


def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    directory_path = "/".join(path.split("/")[:-1])
    exists = os.path.exists(directory_path)
    absolute_path = os.path.abspath(path)
    absolute_working_directory_path = os.path.abspath(working_directory)
    if not absolute_path.startswith(absolute_working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not exists:
        try:
            os.makedirs(directory_path)
        except Exception as e:
            return f"Error: something went wrong creating the file. Code error {e}"
    try:
        with open(absolute_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: something went wrong {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to show the contents from, relative to the working directory. If not provided, it will fail",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="Contents of the file"
            ),
        },
    ),
)
