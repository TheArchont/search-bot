import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = "8898587484:AAFQFYWF9h_bVhQFFSv6_lM7qkBpbZCcy_I"

bot=Bot(token=BOT_TOKEN)
dp=Dispatcher()

@dp.message(Command('start'))
async def handle_start(message: Message):
    await message.answer("Hi!")

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())