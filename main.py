import asyncio
import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

BOT_TOKEN = "8898587484:AAFQFYWF9h_bVhQFFSv6_lM7qkBpbZCcy_I"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def search_wiki(query: str) -> str:
    url = "https://ru.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": query,
        "limit": 1,
        "format": "json",
    }
    headers = {
        "User-Agent": "MyLearningBot/1.0 (contact: your_email@example.com)"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()

    titles = data[1]
    descriptions = data[2]
    links = data[3]

    if not titles:
        return f"По запросу '{query}' ничего не найдено."

    return f"{titles[0]}\n\n{descriptions[0]}\n\n{links[0]}"


@dp.message(Command('start'))
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет!\n"
        "Отправь команду вида: /search asyncio, где asyncio - поисковой запрос\n"
    )


@dp.message(Command('search'))
async def handle_search(message: Message, command: CommandObject) -> None:
    query = command.args
    if not query:
        await message.answer("Укажи запрос, например: /search asyncio")
        return

    result = await search_wiki(query)
    await message.answer(result)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())