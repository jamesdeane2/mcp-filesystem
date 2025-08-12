"""
Asynchronous command execution tools for MCP Filesystem Server
"""

import asyncio
import logging
import subprocess
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp.types import TextContent
import json

logger = logging.getLogger(__name__)

# Store running commands
running_commands: Dict[str, Dict[str, Any]] = {}


async def execute_command_async(args: Dict[str, Any]) -> List[TextContent]:
    """Execute a command asynchronously with timeout support"""
    command = args.get("command")
    working_directory = args.get("working_directory")
    timeout = args.get("timeout", 300)  # Default 5 minutes
    
    command_id = str(uuid.uuid4())[:8]
    logger.info(f"Starting async command {command_id}: {command}")
    
    command_data = {
        "id": command_id,
        "command": command,
        "status": "running",
        "start_time": datetime.now().isoformat(),
        "output": "",
        "error": "",
        "process": None,
        "timeout": timeout,
        "exit_code": None
    }
    
    running_commands[command_id] = command_data
    
    # Start the command asynchronously
    async def run_command():
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_directory
            )
            command_data["process"] = process
            
            try:
                # Wait for command with timeout
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                command_data["output"] = stdout.decode() if stdout else ""
                command_data["error"] = stderr.decode() if stderr else ""
                command_data["exit_code"] = process.returncode
                command_data["status"] = "completed" if process.returncode == 0 else "error"
                
            except asyncio.TimeoutError:
                logger.warning(f"Command {command_id} timed out after {timeout} seconds")
                if process:
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), timeout=5)
                    except asyncio.TimeoutError:
                        process.kill()
                        await process.wait()
                
                command_data["status"] = "timeout"
                command_data["error"] = f"Command timed out after {timeout} seconds"
                
        except Exception as e:
            command_data["status"] = "error"
            command_data["error"] = str(e)
        finally:
            command_data["end_time"] = datetime.now().isoformat()
            if command_data["process"]:
                command_data["exit_code"] = command_data["process"].returncode
    
    # Start the command in the background
    asyncio.create_task(run_command())
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "command_id": command_id,
            "status": "started",
            "message": f"Command started with ID: {command_id}. Use check_command_status to monitor progress."
        }, indent=2)
    )]


async def check_command_status(args: Dict[str, Any]) -> List[TextContent]:
    """Check the status of an asynchronously running command"""
    command_id = args.get("command_id")
    
    logger.info(f"Checking status of command: {command_id}")
    
    if command_id not in running_commands:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "Command not found",
                "command_id": command_id,
                "available_commands": list(running_commands.keys())
            }, indent=2)
        )]
    
    command_data = running_commands[command_id]
    
    result = {
        "command_id": command_data["id"],
        "command": command_data["command"],
        "status": command_data["status"],
        "start_time": command_data["start_time"]
    }
    
    # Calculate runtime
    start_time = datetime.fromisoformat(command_data["start_time"])
    if "end_time" in command_data:
        end_time = datetime.fromisoformat(command_data["end_time"])
        result["end_time"] = command_data["end_time"]
        result["total_runtime_seconds"] = (end_time - start_time).total_seconds()
    else:
        result["runtime_seconds"] = (datetime.now() - start_time).total_seconds()
    
    # Add output based on status
    if command_data["status"] in ["completed", "error", "timeout"]:
        result["exit_code"] = command_data.get("exit_code")
        result["output"] = command_data["output"]
        result["error"] = command_data["error"]
    else:
        # For running commands, include partial output
        result["partial_output"] = command_data["output"]
        result["partial_error"] = command_data["error"]
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def list_running_commands(args: Dict[str, Any]) -> List[TextContent]:
    """List all running or completed commands"""
    include_completed = args.get("include_completed", False)
    
    logger.info(f"Listing {'all' if include_completed else 'running'} commands")
    
    commands = []
    for cmd_id, cmd_data in running_commands.items():
        if not include_completed and cmd_data["status"] != "running":
            continue
        
        command_info = {
            "command_id": cmd_data["id"],
            "command": cmd_data["command"],
            "status": cmd_data["status"],
            "start_time": cmd_data["start_time"]
        }
        
        # Calculate runtime
        start_time = datetime.fromisoformat(cmd_data["start_time"])
        if "end_time" in cmd_data:
            end_time = datetime.fromisoformat(cmd_data["end_time"])
            command_info["runtime_seconds"] = (end_time - start_time).total_seconds()
        else:
            command_info["runtime_seconds"] = (datetime.now() - start_time).total_seconds()
        
        commands.append(command_info)
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "total_commands": len(commands),
            "commands": commands
        }, indent=2)
    )]


async def kill_command(args: Dict[str, Any]) -> List[TextContent]:
    """Terminate a running command"""
    command_id = args.get("command_id")
    signal = args.get("signal", "SIGTERM")
    
    logger.info(f"Killing command {command_id} with signal {signal}")
    
    if command_id not in running_commands:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "Command not found",
                "command_id": command_id
            }, indent=2)
        )]
    
    command_data = running_commands[command_id]
    
    if command_data["status"] != "running":
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "Command is not running",
                "command_id": command_id,
                "status": command_data["status"]
            }, indent=2)
        )]
    
    try:
        process = command_data.get("process")
        if process and process.returncode is None:
            if signal == "SIGKILL":
                process.kill()
            else:
                process.terminate()
            
            # Wait a bit for the process to terminate
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                # Force kill if it doesn't terminate
                process.kill()
                await process.wait()
            
            command_data["status"] = "killed"
            command_data["end_time"] = datetime.now().isoformat()
            command_data["exit_code"] = process.returncode
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "command_id": command_id,
                    "signal": signal,
                    "message": f"Command {command_id} has been terminated"
                }, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "Process not found or already terminated",
                    "command_id": command_id
                }, indent=2)
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "command_id": command_id
            }, indent=2)
        )]


async def cleanup_completed_commands(args: Dict[str, Any]) -> List[TextContent]:
    """Clean up completed commands older than specified hours"""
    max_age_hours = args.get("max_age_hours", 24)
    
    logger.info(f"Cleaning up commands older than {max_age_hours} hours")
    
    current_time = datetime.now()
    removed_count = 0
    removed_commands = []
    
    # Create a list of command IDs to remove (can't modify dict during iteration)
    commands_to_remove = []
    
    for cmd_id, cmd_data in running_commands.items():
        if cmd_data["status"] in ["completed", "error", "timeout", "killed"]:
            if "end_time" in cmd_data:
                end_time = datetime.fromisoformat(cmd_data["end_time"])
                age_hours = (current_time - end_time).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    commands_to_remove.append(cmd_id)
                    removed_commands.append({
                        "command_id": cmd_id,
                        "command": cmd_data["command"][:50] + "..." if len(cmd_data["command"]) > 50 else cmd_data["command"],
                        "status": cmd_data["status"],
                        "age_hours": round(age_hours, 2)
                    })
    
    # Remove the commands
    for cmd_id in commands_to_remove:
        del running_commands[cmd_id]
        removed_count += 1
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "success": True,
            "removed_count": removed_count,
            "removed_commands": removed_commands,
            "remaining_commands": len(running_commands)
        }, indent=2)
    )]
