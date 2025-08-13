"""
Tool definitions for MCP Filesystem Server
"""

from mcp.types import Tool


def get_tools_list():
    """Return list of available tools with their schemas"""
    return [
        Tool(
            name="execute_command",
            description="Execute a shell command. Use this for quick file operations (sed, awk, grep), system commands, or when you need more flexibility than the hash-based tools. Consider using sed/awk for simple text replacements, or shell commands for batch operations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Directory to execute the command in (optional)"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="list_files",
            description="List files in a directory with optional file content previews",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path",
                        "default": "."
                    },
                    "include_preview": {
                        "type": "boolean",
                        "description": "Include preview of small text files",
                        "default": False
                    },
                    "preview_lines": {
                        "type": "integer",
                        "description": "Number of lines to show in preview",
                        "default": 3
                    },
                    "max_preview_size": {
                        "type": "integer",
                        "description": "Maximum file size for preview (bytes)",
                        "default": 1024
                    }
                }
            }
        ),
        Tool(
            name="search_files",
            description="Search for files matching a pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory to search in",
                        "default": "."
                    },
                    "pattern": {
                        "type": "string",
                        "description": "File pattern (e.g., '*.py', 'data*')",
                        "default": "*"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to search subdirectories",
                        "default": True
                    },
                    "include_hidden": {
                        "type": "boolean",
                        "description": "Whether to include hidden files",
                        "default": False
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 100
                    }
                }
            }
        ),
        Tool(
            name="get_text_file_contents",
            description="Read specific line ranges from text files and return hashes for safe editing. Use this when you need to read file content or when you plan to make precise, hash-validated edits to ensure data integrity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the text file"
                                },
                                "ranges": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "start": {
                                                "type": "integer",
                                                "description": "Starting line number (1-based)"
                                            },
                                            "end": {
                                                "type": ["integer", "null"],
                                                "description": "Ending line number (null for end of file)"
                                            }
                                        },
                                        "required": ["start"]
                                    }
                                }
                            },
                            "required": ["file_path", "ranges"]
                        }
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["files"]
            }
        ),
        Tool(
            name="create_text_file",
            description="Create a new text file with given content. Use this for creating new files from scratch or completely replacing file contents.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "contents": {
                        "type": "string",
                        "description": "Content to write to the file"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "contents"]
            }
        ),
        Tool(
            name="append_text_file_contents",
            description="Append content to the end of an existing file with hash validation. Use this when you need to safely add content to a file and want to ensure no concurrent modifications occurred. For simple appends without validation concerns, consider using 'echo \"content\" >> file' with execute_command.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "contents": {
                        "type": "string",
                        "description": "Content to append to the file"
                    },
                    "file_hash": {
                        "type": "string",
                        "description": "Hash of the file contents for concurrency control"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "contents", "file_hash"]
            }
        ),
        Tool(
            name="insert_text_file_contents",
            description="Insert content at a specific line position with hash validation. Use this for precise insertions when data integrity is critical. For simple insertions, consider using sed commands with execute_command (e.g., 'sed -i \"3i\\content\" file').",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "before": {
                        "type": "integer",
                        "description": "Line number before which to insert content"
                    },
                    "after": {
                        "type": "integer",
                        "description": "Line number after which to insert content"
                    },
                    "contents": {
                        "type": "string",
                        "description": "Content to insert"
                    },
                    "file_hash": {
                        "type": "string",
                        "description": "Hash of the file contents for concurrency control"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "contents", "file_hash"]
            }
        ),
        Tool(
            name="delete_text_file_contents",
            description="Delete specific line ranges from a file with hash validation. Use this for precise deletions when data integrity is critical. For simple line deletions, consider using sed commands with execute_command (e.g., 'sed -i \"5,10d\" file').",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "file_hash": {
                        "type": "string",
                        "description": "Hash of the file contents"
                    },
                    "ranges": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "integer",
                                    "description": "Starting line number (1-based)"
                                },
                                "end": {
                                    "type": ["integer", "null"],
                                    "description": "Ending line number"
                                },
                                "range_hash": {
                                    "type": "string",
                                    "description": "Hash of the content being deleted"
                                }
                            },
                            "required": ["start", "range_hash"]
                        }
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "file_hash", "ranges"]
            }
        ),
        Tool(
            name="patch_text_file_contents",
            description="Replace specific line ranges with new content using hash validation. Use this for complex, precise replacements when data integrity is critical. For simple find/replace operations, consider using sed commands with execute_command (e.g., 'sed -i \"s/old/new/g\" file').",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "file_hash": {
                        "type": "string",
                        "description": "Hash of the entire file"
                    },
                    "patches": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "integer",
                                    "description": "Starting line number (1-based)"
                                },
                                "end": {
                                    "type": "integer",
                                    "description": "Ending line number"
                                },
                                "contents": {
                                    "type": "string",
                                    "description": "New content to replace the range with"
                                },
                                "range_hash": {
                                    "type": "string",
                                    "description": "Hash of the content being replaced"
                                }
                            },
                            "required": ["start", "end", "contents", "range_hash"]
                        }
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "file_hash", "patches"]
            }
        ),
        Tool(
            name="execute_command_async",
            description="Execute a shell command asynchronously with timeout support",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Directory to execute the command in (optional)"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum execution time in seconds (default: 300)",
                        "default": 300
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="check_command_status",
            description="Check the status and results of an asynchronous command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "string",
                        "description": "The ID of the command to check"
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="list_running_commands",
            description="List all currently running or completed commands",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_completed": {
                        "type": "boolean",
                        "description": "Whether to include completed commands in the list",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="kill_command",
            description="Terminate a running command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "string",
                        "description": "The ID of the command to kill"
                    },
                    "signal": {
                        "type": "string",
                        "description": "Signal to send (e.g., SIGTERM, SIGKILL)",
                        "default": "SIGTERM"
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="cleanup_completed_commands",
            description="Clean up completed commands older than specified hours",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_age_hours": {
                        "type": "integer",
                        "description": "Maximum age of commands to keep in hours",
                        "default": 24
                    }
                }
            }
        ),
        Tool(
            name="quick_edit_line",
            description="Replace a specific line in a file by line number. Use this for simple line replacements when you don't need hash validation - faster than hash-based tools for straightforward edits.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "line_number": {
                        "type": "integer",
                        "description": "Line number to replace (1-based)"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "New content for the line"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "line_number", "new_content"]
            }
        ),
        Tool(
            name="quick_find_replace",
            description="Simple find and replace text in a file. Use this for straightforward text substitutions without hash validation - more convenient than sed for simple replacements.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file"
                    },
                    "find": {
                        "type": "string",
                        "description": "Text to find"
                    },
                    "replace": {
                        "type": "string",
                        "description": "Text to replace it with"
                    },
                    "line_start": {
                        "type": "integer",
                        "description": "Optional: start line for replacement range (1-based)"
                    },
                    "line_end": {
                        "type": "integer",
                        "description": "Optional: end line for replacement range (1-based)"
                    },
                    "max_replacements": {
                        "type": "integer",
                        "description": "Maximum number of replacements (0 for all)",
                        "default": 0
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    }
                },
                "required": ["file_path", "find", "replace"]
            }
        ),
        Tool(
            name="file_info",
            description="Get file metadata including size, modification time, and permissions. Use this to understand file characteristics before editing or to check if files might be modified by other processes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file"
                    },
                    "include_preview": {
                        "type": "boolean",
                        "description": "Include a small preview of file contents",
                        "default": False
                    }
                },
                "required": ["file_path"]
            }
        )
    ]