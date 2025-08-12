#!/usr/bin/env python3
"""
Test script for MCP Filesystem Server
"""

import asyncio
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_filesystem import file_operations, system_operations

async def test_server():
    """Test basic server functionality"""
    print("Testing MCP Filesystem Server...")
    
    # Test list_files
    print("\n1. Testing list_files:")
    result = await system_operations.list_files({"path": "."})
    print(f"   Result: {result[0].text[:100]}...")
    
    # Test search_files  
    print("\n2. Testing search_files:")
    result = await system_operations.search_files({"path": ".", "pattern": "*.py"})
    print(f"   Result: {result[0].text[:100]}...")
    
    # Test create_text_file
    print("\n3. Testing create_text_file:")
    test_file = "/tmp/test_mcp_file.txt"
    result = await file_operations.create_text_file({
        "file_path": test_file,
        "contents": "Hello from MCP Filesystem Server!"
    })
    print(f"   Result: {result[0].text}")
    
    # Test get_text_file_contents
    print("\n4. Testing get_text_file_contents:")
    result = await file_operations.get_text_file_contents({
        "files": [{
            "file_path": test_file,
            "ranges": [{"start": 1, "end": None}]
        }]
    })
    result_data = json.loads(result[0].text)
    print(f"   Result: File read successfully, hash: {result_data[test_file]['file_hash']}")
    
    # Clean up
    os.remove(test_file)
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_server())
