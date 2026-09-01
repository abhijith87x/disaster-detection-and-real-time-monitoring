from fastapi import FastAPI
from Disaster_chat_bot.router import router as chatbot_router

app = FastAPI()

app.include_router(chatbot_router)