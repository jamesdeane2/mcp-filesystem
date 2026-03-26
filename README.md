![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-compatible-purple)

# MCP Filesystem Server

A modular Python MCP (Model Context Protocol) server for filesystem operations with Claude Desktop.

## Features

This server provides comprehensive filesystem operations through MCP tools:

### Core Tools
- **execute_command** - Execute shell commands with optional working directory
- **list_files** - List files in a directory
- **search_files** - Search for files by pattern with glob support

### File Reading & Writing
- **get_text_file_contents** - Read specific line ranges from files
- **create_text_file** - Create new text files
- **append_text_file_contents** - Append content to files
- **quick_edit_line** - Replace specific lines in files  
- **quick_find_replace** - Find and replace text in files
- **file_info** - Get file metadata and information


### Async Command Execution (NEW!)
- **execute_command_async** - Execute long-running commands asynchronously with timeout support
- **check_command_status** - Check the status and output of async commands
- **list_running_commands** - List all running or completed commands
- **kill_command** - Terminate a running command with signal support
- **cleanup_completed_commands** - Clean up old completed commands

## Project Structure

```
mcp-filesystem/
├── mcp_filesystem/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # Main server entry point
│   ├── tools.py              # Tool definitions and schemas
│   ├── utils.py              # Utility functions (hashing, pattern matching)
│   ├── file_operations.py   # File manipulation tools
│   ├── async_operations.py   # Async command execution tools
│   └── system_operations.py # System and directory tools
├── pyproject.toml            # Project configuration
├── README.md                 # This file
└── test_server.py           # Test script
```

## Installation

### Using UV (Recommended)

1. Install UV if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
cd /path/to/mcp-filesystem
uv pip install mcp aiofiles click
```

### Using pip

```bash
cd /path/to/mcp-filesystem
pip install mcp aiofiles click
```

## Configuration

Add to your Claude Desktop configuration file at `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-filesystem": {
      "command": "/path/to/mcp-filesystem/venv/bin/python",
      "args": [
        "-m",
        "mcp_filesystem.server"
      ],
      "cwd": "/path/to/mcp-filesystem"
    }
  }
}
```

### Alternative: Using UV

If you prefer to use UV instead of the virtual environment:

```json
{
  "mcpServers": {
    "mcp-filesystem": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp-filesystem",
        "python",
        "-m",
        "mcp_filesystem.server"
      ]
    }
  }
}
```

## Usage

Once configured, you can interact with the filesystem through Claude:

- "List files in my home directory"
- "Search for all Python files in the project"
- "Create a new file called test.txt with some content"
- "Read lines 10-20 from config.py"
- "Append a new log entry to logfile.txt"

## File Operations

The server provides straightforward file operations without hash validation for simplicity:

- `create_text_file` - Create or overwrite entire files
- `append_text_file_contents` - Append content to files 
- `quick_edit_line` - Replace specific lines by line number
- `quick_find_replace` - Find and replace text patterns
- `get_text_file_contents` - Read file contents or specific line ranges
- `file_info` - Get file metadata, size, permissions, etc.

For complex file operations, you can also use shell commands via `execute_command`.

## Development

The server is built using:
- Python 3.10+
- MCP SDK for Python
- Async/await for non-blocking operations
- Hash validation for safe concurrent editing
- Modular architecture for maintainability

### Testing

Run the test script to verify functionality:

```bash
cd /path/to/mcp-filesystem
uv run python test_server.py
```

## Architecture

The server is organized into modules for better maintainability:

- **server.py**: Main entry point and request routing
- **tools.py**: Tool definitions and JSON schemas
- **file_operations.py**: All file manipulation functions
- **system_operations.py**: System commands and directory operations
- **utils.py**: Shared utilities like pattern matching

Each module is focused on a specific aspect of functionality, making it easy to:
- Add new tools
- Modify existing functionality
- Test individual components
- Understand the codebase

## License

MIT
