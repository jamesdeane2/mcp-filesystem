"""
System operation tools for MCP Filesystem Server
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Any, Dict, List
from mcp.types import TextContent
from .utils import matches_pattern

logger = logging.getLogger(__name__)


async def execute_command(args: Dict[str, Any]) -> List[TextContent]:
    """Execute a shell command"""
    command = args.get("command")
    working_directory = args.get("working_directory", os.getcwd())
    
    logger.info(f"Executing command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        return [TextContent(type="text", text=output)]
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="Command timed out after 30 seconds")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def list_files(args: Dict[str, Any]) -> List[TextContent]:
    """List files in a directory"""
    dir_path = args.get("path", ".")
    include_preview = args.get("include_preview", False)
    preview_lines = args.get("preview_lines", 3)
    max_preview_size = args.get("max_preview_size", 1024)  # 1KB max for preview
    
    logger.info(f"Listing files in directory: {dir_path}")
    
    try:
        path = Path(dir_path)
        if not path.exists():
            return [TextContent(type="text", text=f"Path does not exist: {dir_path}")]
        
        if not path.is_dir():
            return [TextContent(type="text", text=f"Not a directory: {dir_path}")]
        
        items = []
        for item in path.iterdir():
            if item.is_dir():
                items.append(f"{item.name} (directory)")
            else:
                file_info = f"{item.name} (file)"
                
                # Add preview for small text files if requested
                if include_preview and item.is_file():
                    try:
                        if item.stat().st_size <= max_preview_size:
                            with open(item, 'r', encoding='utf-8') as f:
                                lines = f.readlines()[:preview_lines]
                                if lines:
                                    preview = ' | '.join(line.strip() for line in lines)
                                    file_info += f" - Preview: {preview[:100]}{'...' if len(preview) > 100 else ''}"
                    except (UnicodeDecodeError, PermissionError):
                        # Skip preview for binary files or permission issues
                        pass
                
                items.append(file_info)
        
        return [TextContent(type="text", text="\n".join(items) if items else "Empty directory")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def search_files(args: Dict[str, Any]) -> List[TextContent]:
    """Search for files matching a pattern"""
    search_path = args.get("path", ".")
    pattern = args.get("pattern", "*")
    recursive = args.get("recursive", True)
    include_hidden = args.get("include_hidden", False)
    max_results = args.get("max_results", 100)
    
    logger.info(f"Searching for files matching {pattern} in {search_path}")
    
    try:
        matches = []
        path = Path(search_path)
        
        if not path.exists():
            return [TextContent(type="text", text=f"Path does not exist: {search_path}")]
        
        if recursive:
            for item in path.rglob(pattern):
                if not include_hidden and any(part.startswith('.') for part in item.parts):
                    continue
                matches.append(str(item))
                if len(matches) >= max_results:
                    break
        else:
            for item in path.glob(pattern):
                if not include_hidden and item.name.startswith('.'):
                    continue
                matches.append(str(item))
                if len(matches) >= max_results:
                    break
        
        return [TextContent(type="text", text="\n".join(matches) if matches else "No matching files found.")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
