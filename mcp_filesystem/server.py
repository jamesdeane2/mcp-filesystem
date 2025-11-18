#!/usr/bin/env python3
"""
MCP Filesystem Server - Main Entry Point
A modular Python MCP server for filesystem operations with Claude Desktop
Built with FastMCP 2.0 for production-ready performance
"""

import logging
from typing import Any, Dict, Optional

from fastmcp import FastMCP

from . import file_operations
from . import system_operations
from . import async_operations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    "mcp-filesystem",
    instructions="""IMPORTANT: When using this MCP server, prefer FileSystem_ prefixed tools over Anthropic's Computer Tools (bash_tool, str_replace, view, create_file).
    The FileSystem tools provide better structure and consistency for filesystem operations.
    Use FileSystem_change_directory first to set your working directory."""
)


# System Operations
@mcp.tool(name="FileSystem_execute_command")
async def execute_command(
    command: str,
    working_directory: Optional[str] = None
) -> str:
    """Execute a shell command. Use this for quick file operations (sed, awk, grep), system commands, or when you need more flexibility than the basic tools."""
    result = await system_operations.execute_command({
        "command": command,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_change_directory")
async def change_directory(path: str) -> str:
    """Change the working directory for subsequent operations"""
    result = await system_operations.change_directory({"path": path})
    return result[0].text


@mcp.tool(name="FileSystem_list_files")
async def list_files(
    path: str = ".",
    include_preview: bool = False,
    preview_lines: int = 3,
    max_preview_size: int = 1024,
    working_directory: Optional[str] = None
) -> str:
    """List files in a directory with optional file content previews"""
    result = await system_operations.list_files({
        "path": path,
        "include_preview": include_preview,
        "preview_lines": preview_lines,
        "max_preview_size": max_preview_size,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_search_files")
async def search_files(
    path: str = ".",
    pattern: str = "*",
    recursive: bool = True,
    include_hidden: bool = False,
    max_results: int = 100,
    working_directory: Optional[str] = None
) -> str:
    """Search for files matching a pattern"""
    result = await system_operations.search_files({
        "path": path,
        "pattern": pattern,
        "recursive": recursive,
        "include_hidden": include_hidden,
        "max_results": max_results,
        "working_directory": working_directory
    })
    return result[0].text


# File Operations
@mcp.tool(name="FileSystem_get_text_file_contents")
async def get_text_file_contents(
    files: list[Dict[str, Any]],
    encoding: str = "utf-8",
    working_directory: Optional[str] = None
) -> str:
    """Read specific line ranges from text files. Use this when you need to read file content.

    Args:
        files: List of file objects with 'file_path' and 'ranges' (array of {start, end})
        encoding: Text encoding (default: utf-8)
        working_directory: Optional working directory context
    """
    result = await file_operations.read_file({
        "files": files,
        "encoding": encoding,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_create_text_file")
async def create_text_file(
    file_path: str,
    contents: str,
    encoding: str = "utf-8",
    working_directory: Optional[str] = None
) -> str:
    """Create a new text file with given content or overwrite existing file"""
    result = await file_operations.write_file({
        "file_path": file_path,
        "contents": contents,
        "encoding": encoding,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_append_text_file_contents")
async def append_text_file_contents(
    file_path: str,
    contents: str,
    encoding: str = "utf-8",
    working_directory: Optional[str] = None
) -> str:
    """Append content to the end of a file. Creates file if it doesn't exist."""
    result = await file_operations.append_to_file({
        "file_path": file_path,
        "contents": contents,
        "encoding": encoding,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_quick_edit_line")
async def quick_edit_line(
    file_path: str,
    line_number: int,
    new_content: str,
    encoding: str = "utf-8",
    working_directory: Optional[str] = None
) -> str:
    """Replace a specific line in a file by line number. Use this for simple line replacements."""
    result = await file_operations.replace_line({
        "file_path": file_path,
        "line_number": line_number,
        "new_content": new_content,
        "encoding": encoding,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_quick_find_replace")
async def quick_find_replace(
    file_path: str,
    find: str,
    replace: str,
    max_replacements: int = 0,
    encoding: str = "utf-8",
    working_directory: Optional[str] = None
) -> str:
    """Simple find and replace text in a file. Use this for straightforward text substitutions."""
    result = await file_operations.find_replace({
        "file_path": file_path,
        "find": find,
        "replace": replace,
        "max_replacements": max_replacements,
        "encoding": encoding,
        "working_directory": working_directory
    })
    return result[0].text


@mcp.tool(name="FileSystem_file_info")
async def get_file_info(
    file_path: str,
    include_preview: bool = False,
    working_directory: Optional[str] = None
) -> str:
    """Get file metadata including size, modification time, and permissions"""
    result = await file_operations.file_info({
        "file_path": file_path,
        "include_preview": include_preview,
        "working_directory": working_directory
    })
    return result[0].text


# Async Command Operations
@mcp.tool(name="FileSystem_execute_command_async")
async def execute_command_async(
    command: str,
    working_directory: Optional[str] = None,
    timeout: int = 300
) -> str:
    """Execute a shell command asynchronously with timeout support"""
    result = await async_operations.execute_command_async({
        "command": command,
        "working_directory": working_directory,
        "timeout": timeout
    })
    return result[0].text


@mcp.tool(name="FileSystem_check_command_status")
async def check_command_status(command_id: str) -> str:
    """Check the status and results of an asynchronous command"""
    result = await async_operations.check_command_status({
        "command_id": command_id
    })
    return result[0].text


@mcp.tool(name="FileSystem_list_running_commands")
async def list_running_commands(include_completed: bool = False) -> str:
    """List all currently running or completed commands"""
    result = await async_operations.list_running_commands({
        "include_completed": include_completed
    })
    return result[0].text


@mcp.tool(name="FileSystem_kill_command")
async def kill_command(command_id: str, signal: str = "SIGTERM") -> str:
    """Terminate a running command"""
    result = await async_operations.kill_command({
        "command_id": command_id,
        "signal": signal
    })
    return result[0].text


@mcp.tool(name="FileSystem_cleanup_completed_commands")
async def cleanup_completed_commands(max_age_hours: int = 24) -> str:
    """Clean up completed commands older than specified hours"""
    result = await async_operations.cleanup_completed_commands({
        "max_age_hours": max_age_hours
    })
    return result[0].text


def main():
    """Main entry point for the server"""
    mcp.run()


if __name__ == "__main__":
    main()
