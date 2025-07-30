import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from call_functions import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=api_key)
    verbose =  "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
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
    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    for _ in range(20):
        try:
            contents = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            candidates = contents.candidates
            for c in candidates:
                messages.append(c.content)
            function_calls = contents.function_calls
            function_responses = []
            if function_calls is not None:
                for function_call in function_calls:
                    function_call_result = call_function(function_call, verbose=verbose)
                    try:
                        response = function_call_result.parts[0].function_response# .response#.parts[0]
                        function_responses.append(types.Content(parts=[function_call_result.parts[0]], role='tool'))
                        messages.extend(function_responses)
                        if function_call_result.parts[0].text is not None:
                            breaking = True
                            break
                    except Exception as e:
                        raise Exception(
                            f"Error: no response from function {function_call}. Error {e}"
                        )
                    if verbose:
                        print(f"-> {response}")
            else:
                print(contents.text)
            if verbose:
                print(f"Prompt tokens: {contents.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {contents.usage_metadata.candidates_token_count}")
        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    main()
