from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph import create_graph
from mcp_tools.client import get_mcp_tools
from fastapi.middleware.cors import CORSMiddleware
from strip_markdown import strip_markdown

router = APIRouter()

chatbot = None


@router.on_event("startup")
async def startup():

    global chatbot

    tools = await get_mcp_tools()

    chatbot = await create_graph(tools)

    print("LangGraph initialized")

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request : ChatRequest):
    question = request.message
    user_id = 1
    config = {
        "configurable": {
            "thread_id": str(user_id)
        }
    }
    
    result = await chatbot.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        },
        config=config
    )

    text = result["messages"][-1].text
    
    return{
        "response": strip_markdown(text)
    }