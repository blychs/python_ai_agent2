from google.genai import types
import functions as funcs

FUNCTIONS = {
    "get_files_info": funcs.get_files_info,
    "get_file_content": funcs.get_file_content,
    "run_python_file": funcs.run_python_file,
    "write_file": funcs.write_file,
}


def call_function(function_call_part: types.FunctionCall, verbose=False):
    function = FUNCTIONS.get(function_call_part.name, None)
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    if function_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_result = function(
        **{**function_call_part.args, **{"working_directory": "./calculator"}}
    )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    print(
        call_function(
            types.FunctionCall(name="get_files_info", args={"directory": "."})
        )
    )
    print(
        call_function(
            types.FunctionCall(name="get_files_infor", args={"directory": "."})
        )
    )
