from langchain_google_genai import ChatGoogleGenerativeAI
from ..mcp_tools.client import get_mcp_tools
from config import GOOGLE_GEMINI_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=GOOGLE_GEMINI_KEY,
    temperature=0
)

async def weather_agent(state):

    print("Weather Agent Running")

    # Get MCP tools
    tools = await get_mcp_tools()
    
    weather_tools = [
        tool
        for tool in tools
        if tool.name == "get_weather"
    ]
    
    # Give MCP tools to Gemini
    llm_with_tools = llm.bind_tools(weather_tools)

    # Ask Gemini
    response = await llm_with_tools.ainvoke(
        state["messages"]
    )
    print("MODEL RESPONSE:", response)
    print("TOOL CALLS:", response.tool_calls)
    return {
        "messages": [response]
    }