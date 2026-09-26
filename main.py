import asyncio
import aiohttp
import requests

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
        "User-Agent"
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


async def search_git(query: str) -> str:
    try:
        response = await asyncio.to_thread(
            requests.get,
            "https://api.github.com/search/repositories",
            params={"q": query, "per_page": 5},
            timeout=15,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        return "Не удалось дождаться ответа GitHub. Попробуй позже."

    except requests.exceptions.HTTPError:
        return f"GitHub не смог выполнить поиск. Код: {response.status_code}."

    except requests.exceptions.RequestException:
        return "Не удалось связаться с GitHub. Попробуй позже."

    data = response.json()
    repositories = data["items"]
    messages = []  # Здесь будем накапливать строки

    for repo in repositories:
        text = (
            f"Название: {repo['full_name']}\n"
            f"Описание: {repo['description'] or 'Нет описания'}\n"
            f"Звёзды: {repo['stargazers_count']}\n"
            f"Язык: {repo['language'] or 'Не определён'}\n"
            f"Ссылка: {repo['html_url']}"
        )

        messages.append(text)

    return "\n\n".join(messages)

async def search_stack_overflow(query: str) -> str:
    try:
        response = await asyncio.to_thread(
            requests.get,
            "https://api.stackexchange.com/2.3/search/advanced",
            params={
                "site": "stackoverflow",
                "q": query,
                "sort": "relevance",
                "order": "desc",
                "pagesize": 5,
                "filter": "!-.GhDIMmjQBUYO5FtPM-qKIu"
            },
            timeout=15,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        return "Не удалось дождаться ответа Stack Overflow. Попробуй позже."

    except requests.exceptions.ConnectionError:
        return "Не удалось установить соединение со Stack Overflow. Попробуй позже."

    except requests.exceptions.HTTPError:
        return f"Stack Overflow не смог выполнить поиск. Код: {response.status_code}."

    except requests.exceptions.RequestException:
        return "Произошла ошибка запроса к Stack Overflow. Попробуй позже."

    data = response.json()
    discussions = data["items"]
    messages = []

    for discussion in discussions:
        text = (
            f"Заголовок: {discussion["title"] or "Нет заголовка"} \n"
            f"Ссылка: {discussion["link"] or 'Нет ссылки'}\n"
            f"Кол-во ответов: {discussion["answer_count"]}\n"
            f"Рейтинг: {discussion['score']}\n"
            f"Принятый ответ: {'Есть' if 'accepted_answer_id' in discussion else 'Нет'}\n"
        )
        messages.append(text)

    return "\n\n".join(messages)

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

    # result = await search_wiki(query)
    result = await asyncio.gather(
        search_wiki(query),
        search_git(query),
        search_stack_overflow(query),
    )
    await message.answer("\n\n".join(result))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())