"""MCP Server adapter for Claude Code integration - Simplified working version"""

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .types import BlackDuckInitInput, BlackDuckInitOutput
from .blackduck_init import blackduck_init
from .logger import get_logger

logger = get_logger(__name__)


async def main():
    """Main MCP server implementation"""

    server = Server("blackduck-ai-command")

    @server.list_tools()
    async def list_tools():
        """Return list of available tools"""
        logger.info("Listing available tools")
        return [
            Tool(
                name="blackduck_init",
                description="Initialize BlackDuck security scanning for a project using Bridge CLI.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Path to project directory",
                        },
                        "polaris_token": {
                            "type": "string",
                            "description": "Polaris authentication token",
                        },
                        "server_url": {
                            "type": "string",
                            "description": "BlackDuck server URL (HTTPS)",
                        },
                        "api_token": {
                            "type": "string",
                            "description": "BlackDuck API token (optional)",
                        },
                        "include_dev_deps": {
                            "type": "boolean",
                            "description": "Include dev dependencies",
                            "default": False,
                        },
                    },
                    "required": ["project_path", "polaris_token"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        """Execute tool calls"""

        if name != "blackduck_init":
            logger.error(f"Unknown tool: {name}")
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}", "success": False})
            )]

        logger.info("blackduck_init called")

        try:
            # Parse input
            input_data = BlackDuckInitInput(
                project_path=arguments.get("project_path"),
                polaris_token=arguments.get("polaris_token"),
                server_url=arguments.get("server_url"),
                api_token=arguments.get("api_token"),
                include_dev_deps=arguments.get("include_dev_deps", False),
            )

            logger.debug(f"Tool input: project={input_data.project_path}")

            # Execute
            result: BlackDuckInitOutput = blackduck_init(input_data)
            response = result.model_dump()

            logger.info(f"Tool completed: success={result.success}")

            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2)
            )]

        except Exception as e:
            logger.error(f"Tool error: {str(e)}", exc_info=True)
            error = {
                "error": str(e),
                "success": False,
            }
            return [TextContent(
                type="text",
                text=json.dumps(error)
            )]

    # Start server
    logger.info("Starting MCP server...")
    async with stdio_server(server) as streams:
        logger.info("MCP server listening on stdio")
        await streams.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise
