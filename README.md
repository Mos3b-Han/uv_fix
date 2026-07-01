# AI Coding Agent

A toy implementation of an AI coding agent (similar to Claude Code / Cursor) built with Python and the Anthropic Claude API.

## What it does

The agent accepts a natural language task, then autonomously:
1. Explores the project structure
2. Reads relevant files
3. Makes changes (write/fix code)
4. Runs tests to verify fixes
5. Reports results

## Architecture

Built on the **ReAct pattern** (Reasoning + Acting loop):
- LLM decides which tool to call based on context
- Tool executes and returns result
- LLM sees result and decides next step
- Loop continues until task is complete

## Tools available

| Tool | Description |
|------|-------------|
| `get_files_info` | List directory contents |
| `get_file_content` | Read file contents |
| `write_file` | Write/overwrite files |
| `run_python_file` | Execute Python scripts |

## Setup

```bash
# Install dependencies
uv venv
source .venv/bin/activate
uv add anthropic python-dotenv

# Set API key
echo "ANTHROPIC_API_KEY='your_key_here'" > .env

# Run
uv run main.py "your task here" --verbose
```

## Security

- All file operations are sandboxed to `./calculator` directory
- Path traversal attacks prevented via `os.path.commonpath()`
- 30-second timeout on Python execution
- Maximum 20 iterations per task

## Example

```bash
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20" --verbose
```
