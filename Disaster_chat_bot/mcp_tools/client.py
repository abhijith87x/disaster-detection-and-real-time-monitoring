from langchain_mcp_adapters.client import MultiServerMCPClient
import sys

client = MultiServerMCPClient(
    {
        "disaster": {
            "transport": "stdio",
            "command":  sys.executable,
            "args": [
                "Disaster_chat_bot/mcp_tools/disaster_server.py"
            ],
        }
    }
)


async def get_mcp_tools():

    tools = await client.get_tools()

    return tools