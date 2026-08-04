"""MCP Server adapter for Claude Code integration"""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .types import BlackDuckInitInput, BlackDuckInitOutput
from .blackduck_init import blackduck_init
from .logger import get_logger

logger = get_logger(__name__)


# Initialize MCP server
server = Server("blackduck-ai-command")


# Define the blackduck_init tool
BLACKDUCK_INIT_TOOL = Tool(
    name="blackduck_init",
    description="Initialize BlackDuck security scanning for a project using Bridge CLI. "
    "This tool validates inputs, generates a scan ID, prepares configuration, "
    "and executes the Bridge CLI scanning process.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_path": {
                "type": "string",
                "description": "Path to the project directory to scan "
                "(e.g., /Users/me/myapp or ~/myproject)",
            },
            "polaris_token": {
                "type": "string",
                "description": "User-specific Polaris authentication token. "
                "Keep this secure and confidential.",
            },
            "server_url": {
                "type": "string",
                "description": "BlackDuck Hub server URL (must start with https://). "
                "Example: https://blackduck.company.com",
            },
            "api_token": {
                "type": "string",
                "description": "BlackDuck API authentication token (optional). "
                "Provide if required by your BlackDuck configuration.",
            },
            "include_dev_deps": {
                "type": "boolean",
                "description": "Include development dependencies in the scan. "
                "Default is false.",
                "default": False,
            },
        },
        "required": ["project_path", "polaris_token"],
    },
)


@server.list_tools()
async def list_tools():
    """List available tools for Claude"""
    logger.info("Listing available tools")
    return [BLACKDUCK_INIT_TOOL]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls from Claude"""

    if name != "blackduck_init":
        logger.error(f"Unknown tool requested: {name}")
        return TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}", "success": False}),
        )

    logger.info("blackduck_init tool called from Claude")

    try:
        # Parse input
        input_data = BlackDuckInitInput(
            project_path=arguments.get("project_path"),
            polaris_token=arguments.get("polaris_token"),
            server_url=arguments.get("server_url"),
            api_token=arguments.get("api_token"),
            include_dev_deps=arguments.get("include_dev_deps", False),
        )

        logger.debug(
            f"Tool called with project: {input_data.project_path}, "
            f"server: {input_data.server_url}"
        )

        # Execute
        result: BlackDuckInitOutput = blackduck_init(input_data)

        # Format response
        response = result.model_dump()

        logger.info(f"Tool execution completed. Success: {result.success}")

        return TextContent(
            type="text",
            text=json.dumps(response, indent=2),
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        error_response = {
            "error": "Validation error",
            "message": str(e),
            "success": False,
        }
        return TextContent(
            type="text",
            text=json.dumps(error_response),
        )
    except Exception as e:
        logger.error(f"Unexpected error in tool execution: {str(e)}", exc_info=True)
        error_response = {
            "error": "Execution error",
            "message": str(e),
            "success": False,
        }
        return TextContent(
            type="text",
            text=json.dumps(error_response),
        )


async def main():
    """Main entry point for MCP server"""
    logger.info("Starting MCP server for Claude Code...")
    async with stdio_server(server) as streams:
        logger.info("MCP server listening on stdio")
        await streams.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"MCP server error: {str(e)}", exc_info=True)
        raise
