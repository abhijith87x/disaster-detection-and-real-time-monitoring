from langchain_google_genai import ChatGoogleGenerativeAI
from ..mcp_tools.client import get_mcp_tools
from config import GOOGLE_GEMINI_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=GOOGLE_GEMINI_KEY,
    temperature=0
)

async def reports_agent(state):

    print("Reports Agent Running")

    tools = await get_mcp_tools()

    reports_tools = [
        tool
        for tool in tools
        if tool.name == "query_disaster_reports"
    ]

    llm_with_tools = llm.bind_tools(
        reports_tools
    )

    response = await llm_with_tools.ainvoke(
        state["messages"]
    )
    print("REPORT MODEL RESPONSE:", response)
    print("REPORT TOOL CALLS:", response.tool_calls)
    return {
        "messages": [response]
    }