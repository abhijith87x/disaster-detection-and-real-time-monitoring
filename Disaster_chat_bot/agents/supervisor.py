from typing import Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from config import GOOGLE_GEMINI_KEY

class Route(BaseModel):

    next: Literal[
        "disaster_agent",
        "weather_agent",
        "reports_agent",
        "FINISH"
    ] = Field(
        description="The next agent to execute, or FINISH when the task is complete."
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=GOOGLE_GEMINI_KEY,
    temperature=0
)


router = llm.with_structured_output(Route)


def supervisor(state):

    print("Supervisor running")

    messages = [
        SystemMessage(
            content="""
You are the supervisor of a disaster-management multi-agent system.

Your job is to decide which specialized agent should handle the user's request.

If you need extra information ask to user to provide eg location etc

Available agents:

1. disaster_agent

Use for:
- disaster safety
- evacuation procedures
- what to do during a disaster
- flood safety
- earthquake safety
- disaster preparedness
- disaster knowledge from the RAG knowledge base
- general disaster risk or safety guidance

2. weather_agent

Use for:
- current weather
- weather condition
- temperature
- humidity
- rainfall
- rain
- wind
- clouds
- weather forecast
- weather conditions for a location

Examples:
"weather in Kollam" -> weather_agent
"weather condition in Kollam" -> weather_agent
"temperature in Kollam" -> weather_agent
"will it rain in Kollam?" -> weather_agent

3. reports_agent

Use for:
- recent disaster reports
- reported floods
- reported earthquakes
- recent disaster incidents
- disaster reports for a particular location
- reports within a date range
- disaster reports stored in MySQL

Examples:
"recent floods in Kollam" -> reports_agent
"any flood reports in Kollam?" -> reports_agent
"recent disasters in Kollam" -> reports_agent

IMPORTANT:
"flood chances in Kollam" or "flood risk in Kollam" is a disaster-risk question.
Use disaster_agent unless the user specifically asks about rainfall/weather forecast.

Choose FINISH when the user's request has already been completely answered.

You can choose different agents on different steps if the user's request requires multiple types of information.

Return only the appropriate route.
"""
        )
    ]

    messages.extend(state["messages"])

    result = router.invoke(messages)

    print("Supervisor decision:", result.next)

    return {
        "next_agent": result.next
    }