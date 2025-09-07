#!/usr/bin/env python3
"""
Entry point for the Generic Data Analytics MCP Server.

This script initializes and runs the MCP server. It ensures that the `src`
directory is added to the Python path to make the `mcp_server` package
available for import and then executes the server's main run loop.
"""

import sys
import os

# Add src to Python path so we can import our server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server.server import mcp


def main():
    """
    Initializes and runs the FastMCP server.

    This function calls the `run` method on the imported `mcp` instance,
    starting the server and beginning its operation to handle MCP requests.
    """
    mcp.run()


if __name__ == "__main__":
    main()
