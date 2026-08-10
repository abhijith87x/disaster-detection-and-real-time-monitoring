from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from state import AgentState

from agents.supervisor import supervisor
from agents.disaster_agent import disaster_agent
from agents.weather_agent import weather_agent
from agents.reports_agent import reports_agent

from langgraph.checkpoint.memory import MemorySaver


async def create_graph(mcp_tools):

    # -------------------------
    # Get MCP tools
    # -------------------------

    weather_tools = [
        tool
        for tool in mcp_tools
        if tool.name == "get_weather"
    ]

    reports_tools = [
        tool
        for tool in mcp_tools
        if tool.name == "query_disaster_reports"
    ]

    disaster_tools = [
        tool
        for tool in mcp_tools
        if tool.name == "retrieve_disaster_info"
    ]

    graph = StateGraph(AgentState)

    # -------------------------
    # Agents
    # -------------------------

    graph.add_node(
        "supervisor",
        supervisor
    )

    graph.add_node(
        "disaster_agent",
        disaster_agent
    )

    graph.add_node(
        "weather_agent",
        weather_agent
    )

    graph.add_node(
        "reports_agent",
        reports_agent
    )

    # -------------------------
    # MCP Tool Nodes
    # -------------------------

    graph.add_node(
        "weather_tools",
        ToolNode(weather_tools)
    )

    graph.add_node(
        "reports_tools",
        ToolNode(reports_tools)
    )

    graph.add_node(
        "disaster_tools",
        ToolNode(disaster_tools)
    )

    # -------------------------
    # START
    # -------------------------

    graph.add_edge(
        START,
        "supervisor"
    )

    # -------------------------
    # SUPERVISOR
    # -------------------------

    def route_from_supervisor(state):

        return state["next_agent"]

    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "disaster_agent": "disaster_agent",
            "weather_agent": "weather_agent",
            "reports_agent": "reports_agent",
            "FINISH": END
        }
    )

    # -------------------------
    # DISASTER
    # -------------------------

    def route_disaster(state):

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "disaster_tools"

        return "FINISH"

    graph.add_conditional_edges(
        "disaster_agent",
        route_disaster,
        {
            "disaster_tools": "disaster_tools",
            "FINISH": END
        }
    )

    graph.add_edge(
        "disaster_tools",
        "disaster_agent"
    )

    # -------------------------
    # WEATHER
    # -------------------------

    def route_weather(state):

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "weather_tools"

        return "FINISH"

    graph.add_conditional_edges(
        "weather_agent",
        route_weather,
        {
            "weather_tools": "weather_tools",
            "FINISH": END
        }
    )

    graph.add_edge(
        "weather_tools",
        "weather_agent"
    )

    # -------------------------
    # REPORTS
    # -------------------------

    def route_reports(state):

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "reports_tools"

        return "FINISH"

    graph.add_conditional_edges(
        "reports_agent",
        route_reports,
        {
            "reports_tools": "reports_tools",
            "FINISH": END
        }
    )

    graph.add_edge(
        "reports_tools",
        "reports_agent"
    )

    # -------------------------
    # Compile
    # -------------------------

    checkpointer = MemorySaver()

    return graph.compile(
        checkpointer=checkpointer
    )