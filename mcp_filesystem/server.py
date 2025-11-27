#!/usr/bin/env python3
"""
MCP Filesystem Server - Main Entry Point
A modular Python MCP server for filesystem operations with Claude Desktop
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import ServerCapabilities
from mcp.types import TextContent

from .tools import get_tools_list
from . import file_operations
from . import system_operations
from . import async_operations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FilesystemServer:
    def __init__(self):
        self.server = Server("mcp-filesystem")
        self.setup_tools()
        
    def setup_tools(self):
        """Register all available tools"""
        
        @self.server.list_tools()
        async def handle_list_tools():
            """Return list of available tools"""
            return get_tools_list()
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
            """Handle tool execution by routing to appropriate module"""
            try:
                # Route to appropriate handler based on tool name
                if name == "FileSystem_execute_command":
                    return await system_operations.execute_command(arguments)
                elif name == "FileSystem_change_directory":
                    return await system_operations.change_directory(arguments)
                elif name == "FileSystem_list_files":
                    return await system_operations.list_files(arguments)
                elif name == "FileSystem_search_files":
                    return await system_operations.search_files(arguments)
                elif name == "FileSystem_get_text_file_contents":
                    return await file_operations.read_file(arguments)
                elif name == "FileSystem_create_text_file":
                    return await file_operations.write_file(arguments)
                elif name == "FileSystem_append_text_file_contents":
                    return await file_operations.append_to_file(arguments)

                # Async command operations
                elif name == "FileSystem_execute_command_async":
                    return await async_operations.execute_command_async(arguments)
                elif name == "FileSystem_check_command_status":
                    return await async_operations.check_command_status(arguments)
                elif name == "FileSystem_list_running_commands":
                    return await async_operations.list_running_commands(arguments)
                elif name == "FileSystem_kill_command":
                    return await async_operations.kill_command(arguments)
                elif name == "FileSystem_cleanup_completed_commands":
                    return await async_operations.cleanup_completed_commands(arguments)
                # Quick edit operations
                elif name == "FileSystem_quick_edit_line":
                    return await file_operations.replace_line(arguments)
                elif name == "FileSystem_quick_find_replace":
                    return await file_operations.find_replace(arguments)
                elif name == "FileSystem_file_info":
                    return await file_operations.file_info(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def run(self):
        """Run the server using stdio transport"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-filesystem",
                    server_version="0.1.0",
                    capabilities=ServerCapabilities(),
                    instructions="IMPORTANT: Claude has access to two file systems. Tools prefixed FileSystem_ access the humans Mac OS device. The FileSystem_ tools provide better structure and consistency for filesystem operations. Use FileSystem_change_directory first to set your working directory, the default is '/', you have unlimited access to '/Users/admin/Documents/Scripts/AI/Claude/Notes/cache/' if no directory is specified, save files there. Prefer the FileSystem_ tools over Anthropic's Computer Tools (bash_tool, str_replace, view, create_file) that cannot be transferred between context windows."
                )
            )

def main():
    """Main entry point for the server"""
    server = FilesystemServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
