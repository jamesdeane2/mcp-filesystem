"""
File operation tools for MCP Filesystem Server
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from mcp.types import TextContent
from .utils import generate_hash_for_content

logger = logging.getLogger(__name__)


async def get_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Read specific line ranges from text files"""
    files = args.get("files", [])
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Reading text file contents from {len(files)} files")
    
    result = {}
    
    for file_info in files:
        file_path = file_info.get("file_path")
        ranges = file_info.get("ranges", [])
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                lines = content.split('\n')
                file_hash = generate_hash_for_content(content)
                
                file_result = {
                    "ranges": [],
                    "file_hash": file_hash,
                    "_hash_info": {
                        "description": "Use file_hash for append/insert operations. Use range_hash for patch/delete operations.",
                        "warning": "Hashes change when file is modified. Always get fresh hashes before editing!"
                    }
                }
                
                for range_info in ranges:
                    start = range_info.get("start", 1)
                    end = range_info.get("end")
                    
                    if end is None:
                        end = len(lines)
                    
                    # Validate range
                    if start < 1 or start > len(lines) or end < start or end > len(lines):
                        file_result["ranges"].append({
                            "error": f"Invalid range {start}-{end}. File has {len(lines)} lines.",
                            "start": start,
                            "end": end
                        })
                        continue
                    
                    range_content = '\n'.join(lines[start-1:end])
                    range_hash = generate_hash_for_content(range_content)
                    
                    file_result["ranges"].append({
                        "content": range_content,
                        "start": start,
                        "end": end,
                        "range_hash": range_hash,
                        "total_lines": len(lines),
                        "content_size": len(range_content),
                        "_usage_hint": f'To patch/delete these exact lines, use start={start}, end={end}, range_hash="{range_hash}"'
                    })
                
                result[file_path] = file_result
        except Exception as e:
            result[file_path] = {
                "error": str(e),
                "_suggestion": "Check if file exists and you have read permissions"
            }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def create_text_file(args: Dict[str, Any]) -> List[TextContent]:
    """Create a new text file"""
    file_path = args.get("file_path")
    contents = args.get("contents", "")
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Creating text file at: {file_path}")
    
    try:
        path = Path(file_path)
        
        if path.exists():
            return [TextContent(type="text", text=f"Error: File already exists: {file_path}")]
        
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(path, 'w', encoding=encoding) as f:
            f.write(contents)
        
        return [TextContent(type="text", text=f"Successfully created file: {file_path}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error creating file: {str(e)}")]


async def append_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Append content to file"""
    file_path = args.get("file_path")
    contents = args.get("contents", "")
    file_hash = args.get("file_hash")
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Appending content to file: {file_path}")
    
    try:
        if not Path(file_path).exists():
            return [TextContent(type="text", text=f"Error: File does not exist: {file_path}")]
        
        # Read and verify hash
        with open(file_path, 'r', encoding=encoding) as f:
            current_content = f.read()
        
        current_hash = generate_hash_for_content(current_content)
        
        if current_hash != file_hash:
            return [TextContent(type="text", text="Error: File has been modified. Please use get_text_file_contents to get the current hash, then retry.")]
        
        # Append content
        with open(file_path, 'a', encoding=encoding) as f:
            f.write(contents)
        
        # Return new hash
        new_content = current_content + contents
        new_hash = generate_hash_for_content(new_content)
        
        result = {
            "success": True,
            "file_path": file_path,
            "new_file_hash": new_hash,
            "message": "Content appended successfully"
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error appending to file: {str(e)}")]


async def insert_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Insert content at specific line"""
    file_path = args.get("file_path")
    before = args.get("before")
    after = args.get("after")
    contents = args.get("contents", "")
    file_hash = args.get("file_hash")
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Inserting content into file: {file_path}")
    
    try:
        # Validate parameters
        if (before is None and after is None) or (before is not None and after is not None):
            return [TextContent(type="text", text='Error: You must specify either "before" or "after" (but not both)')]
        
        if not Path(file_path).exists():
            return [TextContent(type="text", text=f"Error: File does not exist: {file_path}")]
        
        # Read and verify hash
        with open(file_path, 'r', encoding=encoding) as f:
            current_content = f.read()
        
        current_hash = generate_hash_for_content(current_content)
        
        if current_hash != file_hash:
            return [TextContent(type="text", text="Error: File has been modified. Please use get_text_file_contents to get the current hash, then retry.")]
        
        # Split into lines
        lines = current_content.split('\n')
        
        # Calculate insert position
        if before is not None:
            insert_index = before - 1  # Convert to 0-based index
        else:
            insert_index = after  # After line N means index N
        
        # Validate line number
        if insert_index < 0 or insert_index > len(lines):
            return [TextContent(type="text", text=f"Error: Line number out of range. File has {len(lines)} lines.")]
        
        # Insert content
        content_lines = contents.split('\n')
        lines[insert_index:insert_index] = content_lines
        
        # Write back
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
        
        # Return new hash
        new_hash = generate_hash_for_content(new_content)
        
        result = {
            "success": True,
            "file_path": file_path,
            "new_file_hash": new_hash,
            "inserted_at_line": insert_index + 1,
            "message": "Content inserted successfully"
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error inserting content: {str(e)}")]


async def delete_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Delete specific line ranges"""
    file_path = args.get("file_path")
    file_hash = args.get("file_hash")
    ranges = args.get("ranges", [])
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Deleting content from file: {file_path}")
    
    try:
        if not Path(file_path).exists():
            return [TextContent(type="text", text=f"Error: File does not exist: {file_path}")]
        
        # Read and verify hash
        with open(file_path, 'r', encoding=encoding) as f:
            current_content = f.read()
        
        current_hash = generate_hash_for_content(current_content)
        
        if current_hash != file_hash:
            return [TextContent(type="text", text="Error: File has been modified. Please use get_text_file_contents to get the current hash, then retry.")]
        
        # Split into lines
        lines = current_content.split('\n')
        
        # Sort ranges by start line (descending) to delete from bottom to top
        sorted_ranges = sorted(ranges, key=lambda x: x['start'], reverse=True)
        
        # Delete each range
        for range_info in sorted_ranges:
            start = range_info['start'] - 1  # Convert to 0-based
            end = range_info.get('end')
            if end is None:
                end = len(lines) - 1
            else:
                end = end - 1
            
            range_hash = range_info.get('range_hash')
            
            # Validate range
            if start < 0 or start >= len(lines) or end < start or end >= len(lines):
                return [TextContent(type="text", text=f"Error: Invalid range {range_info['start']}-{range_info.get('end')}. File has {len(lines)} lines.")]
            
            # Verify range hash
            range_content = '\n'.join(lines[start:end + 1])
            actual_hash = generate_hash_for_content(range_content)
            
            if actual_hash != range_hash:
                return [TextContent(type="text", text=f"Error: Content mismatch at lines {range_info['start']}-{range_info.get('end')}. Please use get_text_file_contents to get current content and hashes.")]
            
            # Delete the range
            del lines[start:end + 1]
        
        # Write back
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
        
        # Return new hash
        new_hash = generate_hash_for_content(new_content)
        
        result = {
            "success": True,
            "file_path": file_path,
            "new_file_hash": new_hash,
            "deleted_ranges": len(ranges),
            "message": "Content deleted successfully"
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error deleting content: {str(e)}")]


async def patch_text_file_contents(args: Dict[str, Any]) -> List[TextContent]:
    """Patch specific line ranges"""
    file_path = args.get("file_path")
    file_hash = args.get("file_hash")
    patches = args.get("patches", [])
    encoding = args.get("encoding", "utf-8")
    
    logger.info(f"Patching file: {file_path} with {len(patches)} patches")
    
    try:
        if not Path(file_path).exists():
            return [TextContent(type="text", text=f"Error: File does not exist: {file_path}")]
        
        # Read and verify hash
        with open(file_path, 'r', encoding=encoding) as f:
            current_content = f.read()
        
        current_hash = generate_hash_for_content(current_content)
        
        if current_hash != file_hash:
            result = {
                "error": "File hash mismatch",
                "message": "The file has been modified since you last read it.",
                "suggestion": "Call get_text_file_contents again to get the current file_hash and range_hash values, then retry with the updated hashes.",
                "expected_hash": file_hash,
                "actual_hash": current_hash
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Split into lines
        lines = current_content.split('\n')
        
        # Sort patches by start line (descending) to apply from bottom to top
        sorted_patches = sorted(patches, key=lambda x: x['start'], reverse=True)
        
        # Apply each patch
        for patch in sorted_patches:
            start = patch['start'] - 1  # Convert to 0-based
            end = patch['end'] - 1
            
            # Validate range
            if start < 0 or start >= len(lines) or end < start or end >= len(lines):
                result = {
                    "error": "Invalid line range",
                    "message": f"Line range {patch['start']}-{patch['end']} is out of bounds",
                    "file_lines": len(lines),
                    "suggestion": "Check that your line numbers are correct (1-based) and within the file bounds"
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            # Verify range hash
            range_content = '\n'.join(lines[start:end + 1])
            actual_hash = generate_hash_for_content(range_content)
            
            if actual_hash != patch['range_hash']:
                result = {
                    "error": "Range hash mismatch",
                    "message": f"Content at lines {patch['start']}-{patch['end']} doesn't match expected hash",
                    "suggestion": "Call get_text_file_contents with the exact same start and end line numbers to get the current range_hash",
                    "expected_hash": patch['range_hash'],
                    "actual_hash": actual_hash,
                    "hint": "Make sure you use the EXACT same start and end values in both get_text_file_contents and patch_text_file_contents"
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            # Apply the patch
            new_lines = patch['contents'].split('\n')
            lines[start:end + 1] = new_lines
        
        # Write back
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
        
        # Return new hash
        new_hash = generate_hash_for_content(new_content)
        
        result = {
            "success": True,
            "file_path": file_path,
            "new_file_hash": new_hash,
            "patches_applied": len(patches),
            "message": "All patches applied successfully"
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error patching file: {str(e)}")]
