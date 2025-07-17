import os


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(path)
    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    contents_of_dir = []
    for f in os.listdir(absolute_path):
        if not f.startswith("."):
            file_path = f"{absolute_path}/{f}"
            contents_of_dir.append(
                f"- {f} file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
            )
    return "\n".join(contents_of_dir)
