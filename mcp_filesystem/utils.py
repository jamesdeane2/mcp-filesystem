"""
Utility functions for MCP Filesystem Server
"""

import hashlib
import fnmatch


def generate_hash_for_content(content: str) -> str:
    """Generate a simple hash for content validation"""
    return hashlib.md5(content.encode()).hexdigest()[:8]


def matches_pattern(filename: str, pattern: str) -> bool:
    """Match filenames against patterns with wildcards"""
    return fnmatch.fnmatch(filename, pattern)
