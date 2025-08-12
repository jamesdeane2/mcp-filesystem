#!/bin/bash

# Start the MCP Filesystem Server
echo "Starting MCP Filesystem Server..."
cd /Users/admin/Documents/GitHub_James/mcp-filesystem
uv run python -m mcp_filesystem.server
