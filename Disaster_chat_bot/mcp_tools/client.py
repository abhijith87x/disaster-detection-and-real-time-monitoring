from langchain_mcp_adapters.client import MultiServerMCPClient
import sys
import os 

client = MultiServerMCPClient(
    {
        "disaster": {
            "transport": "stdio",
            "command":  sys.executable,
            "args": [
                "-m",
                "Disaster_chat_bot/mcp_tools/disaster_server.py"
            ],
        }
    }
)


async def get_mcp_tools():

    tools = await client.get_tools()

    return tools