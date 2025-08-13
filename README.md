# MCP Filesystem Server

A modular Python MCP (Model Context Protocol) server for filesystem operations with Claude Desktop.

## Features

This server provides comprehensive filesystem operations through MCP tools:

### Core Tools
- **execute_command** - Execute shell commands with optional working directory
- **list_files** - List files in a directory
- **search_files** - Search for files by pattern with glob support

### File Reading & Writing
- **get_text_file_contents** - Read specific line ranges with hash support for safe editing
- **create_text_file** - Create new text files
- **append_text_file_contents** - Append content to files with hash validation
- **insert_text_file_contents** - Insert content at specific line positions
- **delete_text_file_contents** - Delete specific line ranges
- **patch_text_file_contents** - Replace line ranges with new content


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
cd /Users/admin/Documents/GitHub_James/mcp-filesystem
uv pip install mcp aiofiles click
```

### Using pip

```bash
cd /Users/admin/Documents/GitHub_James/mcp-filesystem
pip install mcp aiofiles click
```

## Configuration

Add to your Claude Desktop configuration file at `/Users/admin/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-filesystem": {
      "command": "/Users/admin/Documents/GitHub_James/mcp-filesystem/venv/bin/python",
      "args": [
        "-m",
        "mcp_filesystem.server"
      ],
      "cwd": "/Users/admin/Documents/GitHub_James/mcp-filesystem"
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
        "/Users/admin/Documents/GitHub_James/mcp-filesystem",
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

## File Editing Safety

The server uses a hash-based system to prevent conflicts when editing files:

1. **Simple operations** (recommended):
   - `append_text_file_contents` - Just needs file hash
   - `insert_text_file_contents` - Insert before/after a line, only needs file hash
   - `create_text_file` - Create or overwrite entire files

2. **Complex operations** (use carefully):
   - `patch_text_file_contents` - Replace specific line ranges (needs both file and range hashes)
   - `delete_text_file_contents` - Delete specific line ranges (needs both file and range hashes)

Always call `get_text_file_contents` before editing to get current hashes!

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
cd /Users/admin/Documents/GitHub_James/mcp-filesystem
uv run python test_server.py
```

## Architecture

The server is organized into modules for better maintainability:

- **server.py**: Main entry point and request routing
- **tools.py**: Tool definitions and JSON schemas
- **file_operations.py**: All file manipulation functions
- **system_operations.py**: System commands and directory operations
- **utils.py**: Shared utilities like hashing and pattern matching

Each module is focused on a specific aspect of functionality, making it easy to:
- Add new tools
- Modify existing functionality
- Test individual components
- Understand the codebase

## License

MIT
