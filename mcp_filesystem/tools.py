"""
Tool definitions for MCP Filesystem Server
"""

from mcp.types import Tool


def get_tools_list():
    """Return list of available tools with their schemas"""
    return [
        Tool(
            name="execute_command",
            description="Execute a shell command",
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
            description="List files in a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path",
                        "default": "."
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
            description="Read specific line ranges from text files and return hashes for safe editing",
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
            description="Create a new text file with given content",
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
            description="Append content to the end of an existing file",
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
            description="Insert content at a specific line position",
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
            description="Delete specific line ranges from a file",
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
            description="Replace specific line ranges with new content",
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
        )
    ]
