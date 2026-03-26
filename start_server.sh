#!/bin/bash

# Start the MCP Filesystem Server
echo "Starting MCP Filesystem Server..."
cd /path/to/mcp-filesystem
uv run python -m mcp_filesystem.server
