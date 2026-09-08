import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
print("Токен загружен:", bool(token))