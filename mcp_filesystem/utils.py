"""
Utility functions for MCP Filesystem Server
"""

import fnmatch
import os
from pathlib import Path


def matches_pattern(filename: str, pattern: str) -> bool:
    """Match filenames against patterns with wildcards"""
    return fnmatch.fnmatch(filename, pattern)


def resolve_path(file_path: str, working_directory: str = None) -> Path:
    """Resolve a file path relative to a working directory"""
    if working_directory is None:
        working_directory = os.getcwd()
    
    path = Path(file_path)
    if path.is_absolute():
        return path.resolve()
    else:
        return (Path(working_directory) / file_path).resolve()
