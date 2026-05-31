import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
db_password = os.getenv("db_password")
expire_minutes = os.getenv("TOKEN_EXPIRE_MINUTES")
algorithm = os.getenv("ALGORITHM")
