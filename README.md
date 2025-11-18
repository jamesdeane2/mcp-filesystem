# MCP Filesystem Server

A production-ready Python MCP (Model Context Protocol) server for filesystem operations with Claude Desktop. Built with **FastMCP 2.0** for enhanced performance, cleaner code, and enterprise-grade features.

## Features

This server provides comprehensive filesystem operations through MCP tools:

### Core Tools
- **execute_command** - Execute shell commands with optional working directory
- **change_directory** - Change the working directory for subsequent operations
- **list_files** - List files in a directory
- **search_files** - Search for files by pattern with glob support

### File Reading & Writing
- **get_text_file_contents** - Read specific line ranges from files
- **create_text_file** - Create new text files
- **append_text_file_contents** - Append content to files
- **quick_edit_line** - Replace specific lines in files
- **quick_find_replace** - Find and replace text in files
- **file_info** - Get file metadata and information

### Async Command Execution
- **execute_command_async** - Execute long-running commands asynchronously with timeout support
- **check_command_status** - Check the status and output of async commands
- **list_running_commands** - List all running or completed commands
- **kill_command** - Terminate a running command with signal support
- **cleanup_completed_commands** - Clean up old completed commands

## What's New in v0.2.0

### FastMCP 2.0 Integration
- **Cleaner Architecture**: Decorator-based tool registration using `@mcp.tool()`
- **Type Safety**: Full type hints with automatic schema generation
- **Better Performance**: Optimized async operations and reduced boilerplate
- **Production Ready**: Enterprise-grade authentication and deployment support

### Bug Fixes
- Fixed missing `tools.py` file that was causing import errors
- Fixed tool naming consistency with `FileSystem_` prefix
- Removed deprecated hash-based validation tools

## Project Structure

```
mcp-filesystem/
├── mcp_filesystem/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # Main FastMCP 2.0 server with tool decorators
│   ├── tools.py              # Tool schema definitions
│   ├── utils.py              # Utility functions (path resolution, pattern matching)
│   ├── file_operations.py   # File manipulation tools
│   ├── async_operations.py   # Async command execution tools
│   └── system_operations.py # System and directory tools
├── pyproject.toml            # Project configuration with FastMCP 2.0
├── README.md                 # This file
└── test_server.py           # Test script
```

## Installation

### Using UV (Recommended)

1. Install UV if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install the server:
```bash
cd mcp-filesystem
uv pip install -e .
```

### Using pip

```bash
cd mcp-filesystem
pip install -e .
```

This will automatically install:
- `fastmcp>=2.0.0` - The FastMCP framework
- `aiofiles>=24.0.0` - Async file operations

## Configuration

Add to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-filesystem": {
      "command": "python",
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

If you prefer to use UV:

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

### Alternative: Using FastMCP CLI

FastMCP 2.0 provides a built-in CLI for running servers:

```json
{
  "mcpServers": {
    "mcp-filesystem": {
      "command": "fastmcp",
      "args": [
        "run",
        "/path/to/mcp-filesystem/mcp_filesystem/server.py"
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
- "Change directory to /path/to/project"
- "Replace line 5 in app.py with a new import statement"

## File Operations

The server provides straightforward file operations:

- `create_text_file` - Create or overwrite entire files
- `append_text_file_contents` - Append content to files
- `quick_edit_line` - Replace specific lines by line number
- `quick_find_replace` - Find and replace text patterns
- `get_text_file_contents` - Read file contents or specific line ranges
- `file_info` - Get file metadata, size, permissions, etc.

For complex file operations, you can also use shell commands via `execute_command`.

## Development

The server is built using:
- **Python 3.10+**
- **FastMCP 2.0** - Production-ready MCP framework
- **Async/await** - Non-blocking operations
- **Modular architecture** - Easy to maintain and extend

### Why FastMCP 2.0?

FastMCP provides several advantages over the standard MCP SDK:

1. **Cleaner Code**: Decorator-based tool registration eliminates boilerplate
2. **Type Safety**: Full type hints with automatic JSON schema generation
3. **Better DX**: Pythonic API that feels natural to Python developers
4. **Production Features**: Built-in auth, deployment tools, testing utilities
5. **Active Development**: Regular updates and improvements

### Testing

Test the server functionality:

```bash
python -c "from mcp_filesystem.server import mcp; print('Server loaded:', mcp.name)"
```

Run with FastMCP dev mode for debugging:

```bash
fastmcp dev mcp_filesystem/server.py
```

## Architecture

The server is organized into modules for better maintainability:

- **server.py**: FastMCP 2.0 server with decorator-based tool registration
- **tools.py**: Tool schema definitions for MCP protocol
- **file_operations.py**: All file manipulation functions
- **system_operations.py**: System commands and directory operations
- **async_operations.py**: Async command execution tools
- **utils.py**: Shared utilities like pattern matching and path resolution

Each module is focused on a specific aspect of functionality, making it easy to:
- Add new tools
- Modify existing functionality
- Test individual components
- Understand the codebase

### Adding New Tools

With FastMCP 2.0, adding new tools is simple:

```python
@mcp.tool(name="FileSystem_my_new_tool")
async def my_new_tool(
    param1: str,
    param2: int = 10
) -> str:
    """Description of what this tool does"""
    # Your implementation here
    return "result"
```

FastMCP automatically:
- Generates the JSON schema from type hints
- Validates input parameters
- Registers the tool with the MCP server

## Changelog

### v0.2.0 (2025-01-XX)
- **[BREAKING]** Migrated to FastMCP 2.0 framework
- **[ADDED]** Restored missing `tools.py` file
- **[FIXED]** Tool naming consistency with `FileSystem_` prefix
- **[REMOVED]** Deprecated hash-based validation tools
- **[IMPROVED]** Cleaner codebase with decorator-based tool registration
- **[IMPROVED]** Better type safety and automatic schema generation

### v0.1.0
- Initial release with standard MCP SDK
- Basic filesystem operations
- Async command execution

## Migration from v0.1.0

If you're upgrading from v0.1.0:

1. Update dependencies: `pip install --upgrade fastmcp`
2. No client-side changes needed - tool names and behaviors are identical
3. Server code is now cleaner and easier to maintain

## Contributing

Contributions are welcome! The codebase is now easier to work with thanks to FastMCP 2.0's cleaner architecture.

## License

MIT

## Support

For issues or questions:
- Check the [FastMCP documentation](https://gofastmcp.com/)
- Review the code in this repository
- Open an issue on GitHub
