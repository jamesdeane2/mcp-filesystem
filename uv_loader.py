#!/usr/bin/env python3
"""
UV loader script for MCP Filesystem Server
"""

import subprocess
import sys
import os

def main():
    """Run the MCP server using UV"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run with UV
    cmd = [
        sys.executable,
        "-m",
        "mcp_filesystem.server"
    ]
    
    # Execute the command
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

