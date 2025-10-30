"""
System operation tools for MCP Filesystem Server
"""

import os
import subprocess
import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from mcp.types import TextContent
from .utils import matches_pattern

logger = logging.getLogger(__name__)

# Store the current working directory for the server
_current_working_directory = os.getcwd()


async def change_directory(args: Dict[str, Any]) -> List[TextContent]:
    """Change the working directory for subsequent operations"""
    global _current_working_directory
    
    path = args.get("path")
    logger.info(f"Changing directory to: {path}")
    
    try:
        # Resolve the path
        new_path = Path(path).resolve()
        
        if not new_path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Directory does not exist: {path}"
            }, indent=2))]
        
        if not new_path.is_dir():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Not a directory: {path}"
            }, indent=2))]
        
        # Change the directory
        os.chdir(new_path)
        _current_working_directory = str(new_path)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "current_directory": _current_working_directory,
            "message": f"Changed directory to: {_current_working_directory}"
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"Error changing directory: {str(e)}"
        }, indent=2))]


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
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "working_directory": working_directory
        }, indent=2))]
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "command": command,
            "error": "Command timed out after 30 seconds"
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "command": command,
            "error": str(e)
        }, indent=2))]


async def list_files(args: Dict[str, Any]) -> List[TextContent]:
    """List files in a directory"""
    dir_path = args.get("path", ".")
    include_preview = args.get("include_preview", False)
    preview_lines = args.get("preview_lines", 3)
    max_preview_size = args.get("max_preview_size", 1024)  # 1KB max for preview
    working_directory = args.get("working_directory", _current_working_directory)
    
    logger.info(f"Listing files in directory: {dir_path}")
    
    try:
        # Resolve path relative to working directory
        if Path(dir_path).is_absolute():
            path = Path(dir_path)
        else:
            path = Path(working_directory) / dir_path
        
        path = path.resolve()
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Path does not exist: {dir_path}"
            }, indent=2))]
        
        if not path.is_dir():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Not a directory: {dir_path}"
            }, indent=2))]
        
        items = []
        for item in path.iterdir():
            file_info = {
                "name": item.name,
                "type": "directory" if item.is_dir() else "file"
            }
            
            if item.is_file():
                file_info["size"] = item.stat().st_size
                
                # Add preview for small text files if requested
                if include_preview and item.stat().st_size <= max_preview_size:
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            lines = f.readlines()[:preview_lines]
                            if lines:
                                file_info["preview"] = [line.strip() for line in lines]
                    except (UnicodeDecodeError, PermissionError):
                        # Skip preview for binary files or permission issues
                        pass
            
            items.append(file_info)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "directory": str(path),
            "total_items": len(items),
            "items": items
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def search_files(args: Dict[str, Any]) -> List[TextContent]:
    """Search for files matching a pattern"""
    search_path = args.get("path", ".")
    pattern = args.get("pattern", "*")
    recursive = args.get("recursive", True)
    include_hidden = args.get("include_hidden", False)
    max_results = args.get("max_results", 100)
    working_directory = args.get("working_directory", _current_working_directory)
    
    logger.info(f"Searching for files matching {pattern} in {search_path}")
    
    try:
        matches = []
        
        # Resolve path relative to working directory
        if Path(search_path).is_absolute():
            path = Path(search_path)
        else:
            path = Path(working_directory) / search_path
        
        path = path.resolve()
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Path does not exist: {search_path}"
            }, indent=2))]
        
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
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "search_path": str(path),
            "pattern": pattern,
            "recursive": recursive,
            "total_matches": len(matches),
            "matches": matches,
            "message": f"Found {len(matches)} matching file(s)" if matches else "No matching files found"
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]
