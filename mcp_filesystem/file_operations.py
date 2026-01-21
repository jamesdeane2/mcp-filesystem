"""
File operation tools for MCP Filesystem Server
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from mcp.types import TextContent
from .utils import resolve_path

logger = logging.getLogger(__name__)


async def write_file(args: Dict[str, Any]) -> List[TextContent]:
    """Write or overwrite a file with given content. Maps from create_text_file tool."""
    file_path = args.get("file_path")
    contents = args.get("contents", "")
    encoding = args.get("encoding", "utf-8")
    working_directory = args.get("working_directory")
    
    logger.info(f"Writing file: {file_path}")
    
    try:
        path = resolve_path(file_path, working_directory)
        
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file (overwrites if exists)
        with open(path, 'w', encoding=encoding) as f:
            f.write(contents)
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "action": "created" if not path.exists() else "overwritten",
            "size": len(contents),
            "message": f"File written successfully: {file_path}"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def append_to_file(args: Dict[str, Any]) -> List[TextContent]:
    """Append content to a file. Creates file if it doesn't exist."""
    file_path = args.get("file_path")
    contents = args.get("contents", "")
    encoding = args.get("encoding", "utf-8")
    working_directory = args.get("working_directory")
    
    logger.info(f"Appending to file: {file_path}")
    
    try:
        path = resolve_path(file_path, working_directory)
        
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Append content (creates file if doesn't exist)
        with open(path, 'a', encoding=encoding) as f:
            f.write(contents)
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "appended_size": len(contents),
            "message": f"Content appended successfully to: {file_path}"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def replace_line(args: Dict[str, Any]) -> List[TextContent]:
    """Replace a specific line in a file by line number."""
    file_path = args.get("file_path")
    line_number = args.get("line_number")
    new_content = args.get("new_content")
    verbose = args.get("verbose", False)
    encoding = args.get("encoding", "utf-8")
    working_directory = args.get("working_directory")
    
    logger.info(f"Replacing line {line_number} in file: {file_path}")
    
    try:
        path = resolve_path(file_path, working_directory)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"File does not exist: {file_path}",
                "suggestion": "Use write_file to create it first"
            }, indent=2))]
        
        # Read file
        with open(path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        
        # Validate line number
        if line_number < 1 or line_number > len(lines):
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Line number {line_number} out of range",
                "file_lines": len(lines),
                "valid_range": f"1-{len(lines)}"
            }, indent=2))]
        
        # Store old content for response
        old_content = lines[line_number - 1].rstrip('\n')
        
        # Replace the line (preserve newline if original had one)
        if lines[line_number - 1].endswith('\n'):
            lines[line_number - 1] = new_content + '\n'
        else:
            lines[line_number - 1] = new_content
        
        # Write back
        with open(path, 'w', encoding=encoding) as f:
            f.writelines(lines)
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "line_number": line_number
        }
        
        if verbose:
            result["old_content"] = old_content
            result["new_content"] = new_content
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def find_replace(args: Dict[str, Any]) -> List[TextContent]:
    """Find and replace text in a file. Maps from quick_find_replace tool."""
    file_path = args.get("file_path")
    find_text = args.get("find")
    replace_text = args.get("replace")
    count = args.get("max_replacements", 0)  # 0 means replace all
    verbose = args.get("verbose", False)
    encoding = args.get("encoding", "utf-8")
    working_directory = args.get("working_directory")
    
    logger.info(f"Find/replace in file: {file_path} - '{find_text}' -> '{replace_text}'")
    
    try:
        path = resolve_path(file_path, working_directory)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"File does not exist: {file_path}",
                "suggestion": "Use write_file to create it first"
            }, indent=2))]
        
        # Read file
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # Count occurrences
        occurrences = content.count(find_text)
        
        if occurrences == 0:
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "file_path": str(path.absolute()),
                "message": f"Text '{find_text}' not found in file",
                "occurrences": 0
            }, indent=2))]
        
        # Perform replacement
        if count > 0:
            # Limited replacements
            new_content = content
            for _ in range(min(count, occurrences)):
                new_content = new_content.replace(find_text, replace_text, 1)
            replacements_made = min(count, occurrences)
        else:
            # Replace all
            new_content = content.replace(find_text, replace_text)
            replacements_made = occurrences
        
        # Write back
        with open(path, 'w', encoding=encoding) as f:
            f.write(new_content)
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "replacements_made": replacements_made
        }
        
        if verbose:
            result["find"] = find_text
            result["replace"] = replace_text
            result["occurrences_found"] = occurrences
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def read_file(args: Dict[str, Any]) -> List[TextContent]:
    """Read a file with optional line range."""
    file_path = args.get("file_path")
    start_line = args.get("start_line", 1)
    end_line = args.get("end_line")
    encoding = args.get("encoding", "utf-8")
    working_directory = args.get("working_directory")
    
    logger.info(f"Reading file: {file_path}")
    
    try:
        path = resolve_path(file_path, working_directory)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"File does not exist: {file_path}"
            }, indent=2))]
        
        with open(path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # Adjust end_line if not specified
        if end_line is None:
            end_line = total_lines
        
        # Validate range
        if start_line < 1 or start_line > total_lines:
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Invalid start line {start_line}",
                "total_lines": total_lines,
                "valid_range": f"1-{total_lines}"
            }, indent=2))]
        
        if end_line < start_line or end_line > total_lines:
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Invalid end line {end_line}",
                "total_lines": total_lines,
                "valid_range": f"{start_line}-{total_lines}"
            }, indent=2))]
        
        # Extract requested lines
        content = ''.join(lines[start_line-1:end_line])
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "total_lines": total_lines,
            "lines_read": f"{start_line}-{end_line}",
            "content": content.rstrip('\n'),
            "file_size": path.stat().st_size
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def file_info(args: Dict[str, Any]) -> List[TextContent]:
    """Get file metadata and information"""
    file_path = args.get("file_path")
    include_preview = args.get("include_preview", False)
    working_directory = args.get("working_directory")
    
    logger.info(f"Getting file info for: {file_path}")
    
    try:
        path = resolve_path(file_path, working_directory)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"File does not exist: {file_path}"
            }, indent=2))]
        
        # Get file stats
        stat = path.stat()
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "exists": True,
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "size_bytes": stat.st_size,
            "size_human": _human_readable_size(stat.st_size),
            "modified_time": stat.st_mtime,
            "created_time": stat.st_ctime,
            "permissions": oct(stat.st_mode)[-3:]
        }
        
        # Add line count for text files
        if path.is_file() and stat.st_size < 10 * 1024 * 1024:  # Under 10MB
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    result["line_count"] = len(lines)
                    result["is_text_file"] = True
                    
                    if include_preview and lines:
                        preview_lines = min(5, len(lines))
                        result["preview"] = {
                            "first_lines": [line.rstrip('\n') for line in lines[:preview_lines]],
                            "total_lines": len(lines)
                        }
            except (UnicodeDecodeError, PermissionError):
                result["is_text_file"] = False
        
        # Check if file might be actively modified
        import time
        current_time = time.time()
        recently_modified = (current_time - stat.st_mtime) < 300  # Modified within 5 minutes
        result["recently_modified"] = recently_modified
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


def _human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"
