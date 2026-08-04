"""MCP Server adapter for Claude Code integration"""

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ListToolsRequest,
    ListToolsResult,
    CallToolRequest,
    CallToolResult,
)

from .types import BlackDuckInitInput, BlackDuckInitOutput
from .blackduck_init import blackduck_init
from .logger import get_logger

logger = get_logger(__name__)


# Initialize server
server = Server("blackduck-ai-command")


# Define the blackduck_init tool
BLACKDUCK_INIT_TOOL = Tool(
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


# Handle list_tools requests
async def handle_list_tools(request: ListToolsRequest) -> ListToolsResult:
    """Return list of available tools"""
    logger.info("Listing available tools")
    return ListToolsResult(tools=[BLACKDUCK_INIT_TOOL])


# Handle tool calls
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Execute tool calls"""

    if request.params.name != "blackduck_init":
        logger.error(f"Unknown tool: {request.params.name}")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {request.params.name}", "success": False})
            )],
            is_error=True
        )

    logger.info("blackduck_init called")

    try:
        # Parse input
        args = request.params.arguments or {}
        input_data = BlackDuckInitInput(
            project_path=args.get("project_path"),
            polaris_token=args.get("polaris_token"),
            server_url=args.get("server_url"),
            api_token=args.get("api_token"),
            include_dev_deps=args.get("include_dev_deps", False),
        )

        logger.debug(f"Tool input: project={input_data.project_path}")

        # Execute
        result: BlackDuckInitOutput = blackduck_init(input_data)
        response = result.model_dump()

        logger.info(f"Tool completed: success={result.success}")

        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps(response, indent=2)
            )],
            is_error=not result.success
        )

    except Exception as e:
        logger.error(f"Tool error: {str(e)}", exc_info=True)
        error = {
            "error": str(e),
            "success": False,
        }
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps(error)
            )],
            is_error=True
        )


# Register handlers
server.add_request_handler("tools/list", ListToolsRequest, handle_list_tools)
server.add_request_handler("tools/call", CallToolRequest, handle_call_tool)


async def main():
    """Run the MCP server"""
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
