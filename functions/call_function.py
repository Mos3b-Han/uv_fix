from collections.abc import Callable
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


available_functions = [
    {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                }
            },
        },
    },
    {
        "name": "get_file_content",
        "description": "Reads and returns the contents of a file at the specified path, relative to the working directory",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                }
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "run_python_file",
        "description": "Executes a Python file and returns stdout and stderr output",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments",
                },
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "write_file",
        "description": "Writes or overwrites a file with the given content",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_name: str, tool_input: dict, verbose: bool = False) -> str:
    if verbose:
        print(f"Calling function: {tool_name}({tool_input})")
    else:
        print(f" - Calling function: {tool_name}")

    if tool_name not in function_map:
        return f"Error: Unknown function: {tool_name}"

    args = dict(tool_input)
    args["working_directory"] = "./calculator"

    return function_map[tool_name](**args)
