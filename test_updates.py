#!/usr/bin/env python3
"""
Test script for MCP Filesystem Server updates
"""

import asyncio
import json
import sys
import os

# Add parent directory to path to import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_filesystem import file_operations, system_operations, async_operations


async def test_standardized_responses():
    """Test that all responses are now JSON formatted"""
    
    print("Testing standardized JSON responses...")
    print("=" * 50)
    
    # Test system operations
    print("\n1. Testing change_directory:")
    result = await system_operations.change_directory({"path": "/tmp"})
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Current dir: {data.get('current_directory')}")
    
    print("\n2. Testing execute_command:")
    result = await system_operations.execute_command({"command": "echo 'Hello World'"})
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Exit code: {data.get('exit_code')}")
    print(f"   Output: {data.get('stdout', '').strip()}")
    
    print("\n3. Testing list_files:")
    result = await system_operations.list_files({"path": "/tmp"})
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Total items: {data.get('total_items')}")
    
    print("\n4. Testing search_files:")
    result = await system_operations.search_files({"path": "/tmp", "pattern": "*.txt"})
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Total matches: {data.get('total_matches')}")
    
    # Test file operations
    test_file = "/tmp/test_mcp_file.txt"
    
    print("\n5. Testing write_file:")
    result = await file_operations.write_file({
        "file_path": test_file,
        "contents": "Test content\nLine 2\nLine 3"
    })
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Action: {data.get('action')}")
    
    print("\n6. Testing read_file (with complex schema):")
    result = await file_operations.read_file({
        "files": [{
            "file_path": test_file,
            "ranges": [{"start": 1, "end": 2}]
        }]
    })
    data = json.loads(result[0].text)
    print(f"   Lines read: {data.get('lines_read')}")
    print(f"   Content: {data.get('content')}")
    
    print("\n7. Testing append_to_file:")
    result = await file_operations.append_to_file({
        "file_path": test_file,
        "contents": "\nLine 4 appended"
    })
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Appended size: {data.get('appended_size')}")
    
    print("\n8. Testing replace_line:")
    result = await file_operations.replace_line({
        "file_path": test_file,
        "line_number": 2,
        "new_content": "Line 2 REPLACED"
    })
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Old: {data.get('old_content')}")
    print(f"   New: {data.get('new_content')}")
    
    print("\n9. Testing find_replace:")
    result = await file_operations.find_replace({
        "file_path": test_file,
        "find": "Test",
        "replace": "MODIFIED"
    })
    data = json.loads(result[0].text)
    print(f"   Success: {data.get('success')}")
    print(f"   Replacements made: {data.get('replacements_made')}")
    
    print("\n10. Testing file_info:")
    result = await file_operations.file_info({
        "file_path": test_file,
        "include_preview": True
    })
    data = json.loads(result[0].text)
    print(f"   Exists: {data.get('exists')}")
    print(f"   Size: {data.get('size_human')}")
    print(f"   Lines: {data.get('line_count')}")
    
    # Test async operations
    print("\n11. Testing execute_command_async:")
    result = await async_operations.execute_command_async({
        "command": "sleep 1 && echo 'Async done'",
        "timeout": 5
    })
    data = json.loads(result[0].text)
    command_id = data.get('command_id')
    print(f"   Command ID: {command_id}")
    print(f"   Status: {data.get('status')}")
    
    # Wait a bit then check status
    await asyncio.sleep(1.5)
    
    print("\n12. Testing check_command_status:")
    result = await async_operations.check_command_status({
        "command_id": command_id
    })
    data = json.loads(result[0].text)
    print(f"   Status: {data.get('status')}")
    print(f"   Output: {data.get('output', '').strip()}")
    
    # Clean up
    os.remove(test_file)
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("All responses are now JSON formatted.")


if __name__ == "__main__":
    asyncio.run(test_standardized_responses())
