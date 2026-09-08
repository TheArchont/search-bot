import asyncio
import os

from aiogram import Bot
from dotenv import load_dotenv


async def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("Не задан BOT_TOKEN в .env")

    bot = Bot(token=token)

    try:
        me = await bot.get_me()
        print(f"Подключились к боту @{me.username}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())