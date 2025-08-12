#!/usr/bin/env python3
"""
Test script for async command functionality
"""

import asyncio
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_filesystem import async_operations

async def test_async_commands():
    """Test async command execution"""
    print("Testing Async Command Execution\n")
    print("=" * 50)
    
    # Test 1: Start a simple async command
    print("\n1. Starting async command (sleep 3)...")
    result = await async_operations.execute_command_async({
        "command": "sleep 3 && echo 'Command completed!'",
        "timeout": 10
    })
    result_data = json.loads(result[0].text)
    command_id = result_data["command_id"]
    print(f"   Command started with ID: {command_id}")
    
    # Test 2: Check status immediately (should be running)
    print("\n2. Checking status immediately...")
    result = await async_operations.check_command_status({
        "command_id": command_id
    })
    status_data = json.loads(result[0].text)
    print(f"   Status: {status_data['status']}")
    print(f"   Runtime: {status_data.get('runtime_seconds', 0):.2f} seconds")
    
    # Test 3: List running commands
    print("\n3. Listing running commands...")
    result = await async_operations.list_running_commands({
        "include_completed": False
    })
    list_data = json.loads(result[0].text)
    print(f"   Running commands: {list_data['total_commands']}")
    for cmd in list_data['commands']:
        print(f"   - {cmd['command_id']}: {cmd['command'][:30]}...")
    
    # Test 4: Start a command that will timeout
    print("\n4. Starting command with 2 second timeout (will timeout)...")
    result = await async_operations.execute_command_async({
        "command": "sleep 5",
        "timeout": 2
    })
    timeout_data = json.loads(result[0].text)
    timeout_id = timeout_data["command_id"]
    print(f"   Command started with ID: {timeout_id}")
    
    # Wait a bit for the first command to complete
    print("\n5. Waiting 4 seconds for commands to complete...")
    await asyncio.sleep(4)
    
    # Test 5: Check status of completed command
    print("\n6. Checking status of first command (should be completed)...")
    result = await async_operations.check_command_status({
        "command_id": command_id
    })
    final_status = json.loads(result[0].text)
    print(f"   Status: {final_status['status']}")
    print(f"   Output: {final_status.get('output', '').strip()}")
    print(f"   Exit code: {final_status.get('exit_code')}")
    
    # Test 6: Check timeout command
    print("\n7. Checking status of timeout command...")
    result = await async_operations.check_command_status({
        "command_id": timeout_id
    })
    timeout_status = json.loads(result[0].text)
    print(f"   Status: {timeout_status['status']}")
    print(f"   Error: {timeout_status.get('error', '')}")
    
    # Test 7: Start a long-running command to test kill
    print("\n8. Starting long-running command to test kill...")
    result = await async_operations.execute_command_async({
        "command": "sleep 30",
        "timeout": 60
    })
    kill_data = json.loads(result[0].text)
    kill_id = kill_data["command_id"]
    print(f"   Command started with ID: {kill_id}")
    
    # Wait a moment
    await asyncio.sleep(1)
    
    # Test 8: Kill the command
    print("\n9. Killing the long-running command...")
    result = await async_operations.kill_command({
        "command_id": kill_id
    })
    kill_result = json.loads(result[0].text)
    print(f"   Result: {kill_result.get('message', kill_result.get('error'))}")
    
    # Test 9: List all commands including completed
    print("\n10. Listing all commands (including completed)...")
    result = await async_operations.list_running_commands({
        "include_completed": True
    })
    all_commands = json.loads(result[0].text)
    print(f"    Total commands: {all_commands['total_commands']}")
    for cmd in all_commands['commands']:
        runtime = cmd.get('runtime_seconds', 0)
        print(f"    - {cmd['command_id']}: {cmd['status']} ({runtime:.2f}s)")
    
    # Test 10: Cleanup old commands
    print("\n11. Cleaning up completed commands...")
    result = await async_operations.cleanup_completed_commands({
        "max_age_hours": 0  # Clean up all completed commands
    })
    cleanup_result = json.loads(result[0].text)
    print(f"    Removed {cleanup_result['removed_count']} commands")
    print(f"    Remaining: {cleanup_result['remaining_commands']}")
    
    print("\n" + "=" * 50)
    print("✅ All async tests completed!")

if __name__ == "__main__":
    asyncio.run(test_async_commands())
