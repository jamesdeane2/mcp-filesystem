"""
File operation tools for MCP Filesystem Server - Simplified version without hash validation
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from mcp.types import TextContent

logger = logging.getLogger(__name__)


async def write_file(args: Dict[str, Any]) -> List[TextContent]:
    """Write or overwrite a file with given content. No questions asked."""
    file_path = args.get("file_path")
    contents = args.get("contents", "")
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Writing file: {file_path}")
    
    try:
        path = Path(file_path)
        
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
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def append_to_file(args: Dict[str, Any]) -> List[TextContent]:
    """Append content to a file. Creates file if it doesn't exist."""
    file_path = args.get("file_path")
    contents = args.get("contents", "")
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Appending to file: {file_path}")
    
    try:
        path = Path(file_path)
        
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
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def replace_line(args: Dict[str, Any]) -> List[TextContent]:
    """Replace a specific line in a file by line number."""
    file_path = args.get("file_path")
    line_number = args.get("line_number")
    new_content = args.get("new_content")
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Replacing line {line_number} in file: {file_path}")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "error": f"File does not exist: {file_path}",
                "suggestion": "Use write_file to create it first"
            }, indent=2))]
        
        # Read file
        with open(path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        
        # Validate line number
        if line_number < 1 or line_number > len(lines):
            return [TextContent(type="text", text=json.dumps({
                "error": f"Line number {line_number} out of range",
                "file_lines": len(lines),
                "valid_range": f"1-{len(lines)}"
            }, indent=2))]
        
        # Store old content for response
        old_content = lines[line_number - 1].rstrip('\
')
        
        # Replace the line (preserve newline if original had one)
        if lines[line_number - 1].endswith('\
'):
            lines[line_number - 1] = new_content + '\
'
        else:
            lines[line_number - 1] = new_content
        
        # Write back
        with open(path, 'w', encoding=encoding) as f:
            f.writelines(lines)
        
        result = {
            "success": True,
            "file_path": str(path.absolute()),
            "line_number": line_number,
            "old_content": old_content,
            "new_content": new_content,
            "message": f"Line {line_number} replaced successfully"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def find_replace(args: Dict[str, Any]) -> List[TextContent]:
    """Find and replace text in a file."""
    file_path = args.get("file_path")
    find_text = args.get("find")
    replace_text = args.get("replace")
    count = args.get("count", 0)  # 0 means replace all
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Find/replace in file: {file_path} - '{find_text}' -> '{replace_text}'")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
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
            "find": find_text,
            "replace": replace_text,
            "occurrences_found": occurrences,
            "replacements_made": replacements_made,
            "message": f"Replaced {replacements_made} occurrence(s)"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


async def read_file(args: Dict[str, Any]) -> List[TextContent]:
    """Read a file or specific line ranges from a file."""
    file_path = args.get("file_path")
    start_line = args.get("start_line", 1)
    end_line = args.get("end_line")  # None means to end of file
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Reading file: {file_path}")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
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
                "error": f"Invalid start line {start_line}",
                "total_lines": total_lines,
                "valid_range": f"1-{total_lines}"
            }, indent=2))]
        
        if end_line < start_line or end_line > total_lines:
            return [TextContent(type="text", text=json.dumps({
                "error": f"Invalid end line {end_line}",
                "total_lines": total_lines,
                "valid_range": f"{start_line}-{total_lines}"
            }, indent=2))]
        
        # Extract requested lines
        content = ''.join(lines[start_line-1:end_line])
        
        result = {
            "file_path": str(path.absolute()),
            "total_lines": total_lines,
            "lines_read": f"{start_line}-{end_line}",
            "content": content.rstrip('\
'),  # Remove trailing newline for cleaner output
            "file_size": path.stat().st_size
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "file_path": file_path
        }, indent=2))]


# Keep these for backwards compatibility, but map them to the new simple functions
async def create_text_file(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - now just calls write_file"""
    return await write_file(args)


async def get_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - simplified version for backwards compatibility"""
    files = args.get("files", [])
    encoding = args.get("encoding", "utf-8")
    
    if not files:
        return [TextContent(type="text", text="No files specified")]
    
    # Handle the first file only for simplicity
    file_info = files[0]
    file_path = file_info.get("file_path")
    ranges = file_info.get("ranges", [])
    
    # If no ranges specified, read whole file
    if not ranges:
        return await read_file({"file_path": file_path, "encoding": encoding})
    
    # Read first range only
    range_info = ranges[0]
    return await read_file({
        "file_path": file_path,
        "start_line": range_info.get("start", 1),
        "end_line": range_info.get("end"),
        "encoding": encoding
    })


async def append_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - now ignores hash and just appends"""
    return await append_to_file({
        "file_path": args.get("file_path"),
        "contents": args.get("contents", ""),
        "encoding": args.get("encoding", "utf-8")
    })


async def quick_edit_line(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - now just calls replace_line"""
    return await replace_line(args)


async def quick_find_replace(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - now just calls find_replace"""
    return await find_replace({
        "file_path": args.get("file_path"),
        "find": args.get("find"),
        "replace": args.get("replace"),
        "count": args.get("max_replacements", 0),
        "encoding": args.get("encoding", "utf-8")
    })


# Stub functions for the hash-based operations that just redirect to simpler versions
async def insert_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - now just appends without hash check"""
    return await append_to_file({
        "file_path": args.get("file_path"),
        "contents": args.get("contents", ""),
        "encoding": args.get("encoding", "utf-8")
    })


async def delete_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - simplified to return error message"""
    return [TextContent(type="text", text=json.dumps({
        "error": "delete_text_file_contents is deprecated",
        "suggestion": "Use replace_line with empty content or find_replace to remove text"
    }, indent=2))]


async def patch_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Legacy function - simplified to return error message"""
    return [TextContent(type="text", text=json.dumps({
        "error": "patch_text_file_contents is deprecated", 
        "suggestion": "Use write_file to rewrite the entire file, or find_replace for specific changes"
    }, indent=2))]


async def file_info(args: Dict[str, Any]) -> List[TextContent]:
    """Get file metadata and information"""
    file_path = args.get("file_path")
    include_preview = args.get("include_preview", False)
    
    logger.info(f"Getting file info for: {file_path}")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return [TextContent(type="text", text=json.dumps({
                "error": f"File does not exist: {file_path}"
            }, indent=2))]
        
        # Get file stats
        stat = path.stat()
        
        result = {
            "file_path": str(path.absolute()),
            "exists": True,
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "size_bytes": stat.st_size,
            "size_human": _human_readable_size(stat.st_size),
            "modified_time": stat.st_mtime,
            "created_time": stat.st_ctime,
            "permissions": oct(stat.st_mode)[-3:],
            "owner_readable": bool(stat.st_mode & 0o400),
            "owner_writable": bool(stat.st_mode & 0o200),
            "owner_executable": bool(stat.st_mode & 0o100)
        }
        
        # Add line count for text files
        if path.is_file() and stat.st_size < 10 * 1024 * 1024:  # Under 10MB
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    result["line_count"] = len(lines)
                    result["is_text_file"] = True
                    
                    if include_preview and lines:
                        preview_lines = min(5, len(lines))
                        result["preview"] = {
                            "first_lines": [line.rstrip('\
') for line in lines[:preview_lines]],
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