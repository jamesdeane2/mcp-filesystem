#!/usr/bin/env python3
"""
CLI tool for testing MCP Filesystem Server operations
"""

import asyncio
import click
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_filesystem import file_operations, system_operations


@click.group()
def cli():
    """MCP Filesystem CLI Tool"""
    pass


@cli.command()
@click.argument('path', default='.')
def list_files(path):
    """List files in a directory"""
    async def run():
        result = await system_operations.list_files({"path": path})
        print(result[0].text)
    asyncio.run(run())


@cli.command()
@click.argument('pattern', default='*')
@click.option('--path', default='.', help='Directory to search in')
@click.option('--recursive/--no-recursive', default=True, help='Search recursively')
def search(pattern, path, recursive):
    """Search for files matching a pattern"""
    async def run():
        result = await system_operations.search_files({
            "path": path,
            "pattern": pattern,
            "recursive": recursive
        })
        print(result[0].text)
    asyncio.run(run())


@cli.command()
@click.argument('command')
@click.option('--cwd', default=None, help='Working directory')
def execute(command, cwd):
    """Execute a shell command"""
    async def run():
        args = {"command": command}
        if cwd:
            args["working_directory"] = cwd
        result = await system_operations.execute_command(args)
        print(result[0].text)
    asyncio.run(run())


@cli.command()
@click.argument('file_path')
@click.option('--start', default=1, help='Start line (1-based)')
@click.option('--end', default=None, help='End line (null for EOF)')
def read_file(file_path, start, end):
    """Read a text file"""
    async def run():
        result = await file_operations.get_text_file_contents({
            "files": [{
                "file_path": file_path,
                "ranges": [{"start": start, "end": end}]
            }]
        })
        data = json.loads(result[0].text)
        if file_path in data and 'ranges' in data[file_path]:
            for range_data in data[file_path]['ranges']:
                if 'content' in range_data:
                    print(range_data['content'])
                    print(f"\n[Hash: {data[file_path]['file_hash']}]")
        else:
            print(result[0].text)
    asyncio.run(run())


@cli.command()
@click.argument('file_path')
@click.argument('content')
def create_file(file_path, content):
    """Create a new text file"""
    async def run():
        result = await file_operations.create_text_file({
            "file_path": file_path,
            "contents": content
        })
        print(result[0].text)


# Import async_operations for async commands
from mcp_filesystem import async_operations

@cli.command()
@click.argument('command')
@click.option('--cwd', default=None, help='Working directory')
@click.option('--timeout', default=300, help='Timeout in seconds')
def execute_async(command, cwd, timeout):
    """Execute a shell command asynchronously"""
    async def run():
        args = {"command": command, "timeout": timeout}
        if cwd:
            args["working_directory"] = cwd
        result = await async_operations.execute_command_async(args)
        data = json.loads(result[0].text)
        print(f"Command started with ID: {data['command_id']}")
        print(f"Status: {data['status']}")
        print(f"Message: {data['message']}")
    asyncio.run(run())


@cli.command()
@click.argument('command_id')
def check_status(command_id):
    """Check status of an async command"""
    async def run():
        result = await async_operations.check_command_status({
            "command_id": command_id
        })
        data = json.loads(result[0].text)
        if 'error' in data:
            print(f"Error: {data['error']}")
        else:
            print(f"Command ID: {data['command_id']}")
            print(f"Status: {data['status']}")
            print(f"Command: {data['command']}")
            if 'runtime_seconds' in data:
                print(f"Runtime: {data['runtime_seconds']:.2f} seconds")
            if 'output' in data:
                print(f"\nOutput:\n{data['output']}")
            if 'error' in data and data['error']:
                print(f"\nError:\n{data['error']}")
            if 'exit_code' in data:
                print(f"\nExit code: {data['exit_code']}")
    asyncio.run(run())


@cli.command()
@click.option('--all', 'include_all', is_flag=True, help='Include completed commands')
def list_commands(include_all):
    """List running commands"""
    async def run():
        result = await async_operations.list_running_commands({
            "include_completed": include_all
        })
        data = json.loads(result[0].text)
        print(f"Total commands: {data['total_commands']}")
        for cmd in data['commands']:
            runtime = cmd.get('runtime_seconds', 0)
            print(f"- {cmd['command_id']}: {cmd['status']} ({runtime:.2f}s)")
            print(f"  Command: {cmd['command'][:50]}...")
    asyncio.run(run())


@cli.command()
@click.argument('command_id')
@click.option('--signal', default='SIGTERM', help='Signal to send')
def kill(command_id, signal):
    """Kill a running command"""
    async def run():
        result = await async_operations.kill_command({
            "command_id": command_id,
            "signal": signal
        })
        data = json.loads(result[0].text)
        if 'error' in data:
            print(f"Error: {data['error']}")
        else:
            print(f"Success: {data['message']}")
    asyncio.run(run())
    asyncio.run(run())


if __name__ == '__main__':
    cli()
