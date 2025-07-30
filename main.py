import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from call_functions import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    verbose = (
        False if "verbose" not in sys.argv[1] and "--verbose" not in sys.argv else True
    )
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
If the verbose flag is passed,
"""
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    contents = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    function_calls = contents.function_calls
    if function_calls is not None:
        for function_call in function_calls:
            function_call_result = call_function(function_call, verbose=verbose)
            try:
                response = function_call_result.parts[0].function_response.response
            except Exception as e:
                raise Exception(
                    f"Error: no response from function {function_call}. Error {e}"
                )
            if verbose:
                print(f"-> {response}")
    else:
        print(contents.text)
    print("\n")
    # print(f"Prompt tokens: {contents.usage_metadata.prompt_token_count}")
    # print(f"Response tokens: {contents.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
