from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_GEMINI_KEY
from tools import get_weather,retrieve_disaster_info


llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=GOOGLE_GEMINI_KEY
)


llm_with_tools = llm.bind_tools(
    [
        get_weather,
        retrieve_disaster_info
    ]
)


def agent(state):

    print("Agent Node Running")

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages":[response]
    }