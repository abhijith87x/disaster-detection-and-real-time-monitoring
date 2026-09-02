from langchain_google_genai import ChatGoogleGenerativeAI
from ..tools import retrieve_disaster_info
from ...config import GOOGLE_GEMINI_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=GOOGLE_GEMINI_KEY,
    temperature=0
)

llm_with_tools = llm.bind_tools(
    [retrieve_disaster_info]
)


def disaster_agent(state):

    response = llm_with_tools.invoke(
        state["messages"]
    )
    print("DISASTER RESPONSE:", response)
    print("DISASTER CONTENT:", response.content)
    return {
        "messages": [response]
    }