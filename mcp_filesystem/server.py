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
                if name == "execute_command":
                    return await system_operations.execute_command(arguments)
                elif name == "change_directory":
                    return await system_operations.change_directory(arguments)
                elif name == "list_files":
                    return await system_operations.list_files(arguments)
                elif name == "search_files":
                    return await system_operations.search_files(arguments)
                elif name == "get_text_file_contents":
                    return await file_operations.get_text_file_contents(arguments)
                elif name == "create_text_file":
                    return await file_operations.create_text_file(arguments)
                elif name == "append_text_file_contents":
                    return await file_operations.append_text_file_contents(arguments)

                # Async command operations
                elif name == "execute_command_async":
                    return await async_operations.execute_command_async(arguments)
                elif name == "check_command_status":
                    return await async_operations.check_command_status(arguments)
                elif name == "list_running_commands":
                    return await async_operations.list_running_commands(arguments)
                elif name == "kill_command":
                    return await async_operations.kill_command(arguments)
                elif name == "cleanup_completed_commands":
                    return await async_operations.cleanup_completed_commands(arguments)
                # Quick edit operations
                elif name == "quick_edit_line":
                    return await file_operations.quick_edit_line(arguments)
                elif name == "quick_find_replace":
                    return await file_operations.quick_find_replace(arguments)
                elif name == "file_info":
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
                    capabilities=ServerCapabilities()
                )
            )

def main():
    """Main entry point for the server"""
    server = FilesystemServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
