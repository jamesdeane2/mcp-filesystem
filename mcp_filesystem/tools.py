"""
Tool definitions for MCP Filesystem Server
"""

from mcp.types import Tool


def get_tools_list():
    """Return list of available tools with their schemas"""
    return [
        Tool(
            name="FileSystem_execute_command",
            description="Execute a shell command. Use this for quick file operations (sed, awk, grep), system commands, or when you need more flexibility than the basic tools.",
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
            name="FileSystem_change_directory",
            description="Change the working directory for subsequent operations",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to change to"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="FileSystem_list_files",
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
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                }
            }
        ),
        Tool(
            name="FileSystem_search_files",
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
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                }
            }
        ),
        Tool(
            name="FileSystem_get_text_file_contents",
            description="Read specific line ranges from text files. Use this when you need to read file content.",
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
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                },
                "required": ["files"]
            }
        ),
        Tool(
            name="FileSystem_create_text_file",
            description="Create a new text file with given content or overwrite existing file",
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
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                },
                "required": ["file_path", "contents"]
            }
        ),
        Tool(
            name="FileSystem_append_text_file_contents",
            description="Append content to the end of a file. Creates file if it doesn't exist.",
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
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                },
                "required": ["file_path", "contents"]
            }
        ),
        Tool(
            name="FileSystem_execute_command_async",
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
            name="FileSystem_check_command_status",
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
            name="FileSystem_list_running_commands",
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
            name="FileSystem_kill_command",
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
            name="FileSystem_cleanup_completed_commands",
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
            name="FileSystem_quick_edit_line",
            description="Replace a specific line in a file by line number. Use this for simple line replacements.",
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
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                },
                "required": ["file_path", "line_number", "new_content"]
            }
        ),
        Tool(
            name="FileSystem_quick_find_replace",
            description="Simple find and replace text in a file. Use this for straightforward text substitutions.",
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
                    "max_replacements": {
                        "type": "integer",
                        "description": "Maximum number of replacements (0 for all)",
                        "default": 0
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding",
                        "default": "utf-8"
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                },
                "required": ["file_path", "find", "replace"]
            }
        ),
        Tool(
            name="FileSystem_file_info",
            description="Get file metadata including size, modification time, and permissions",
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
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Working directory context (optional)"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]
