import aiohttp


async def _fetch(query: str, style: int, session: aiohttp.ClientSession) -> str:
    async with session.post(
        "https://yandex.ru/lab/api/yalm/text3",
        json={"query": query, "intro": style, "filter": 1},
    ) as resp:
        r = await resp.json()
    return r["query"] + r["text"]


async def balaboba(
    query: str, *, style: int = 0
) -> str:
    """Отправка запроса Яндекс Балабобе.
    Args:
        query (str): Текст для Балабобы.
        intro (int, optional): Вариант стилизации.
            0 - Без стиля. По умолчанию.
            1 - Теории заговора.
            2 - ТВ-репортажи.
            3 - Тосты.
            4 - Пацанские цитаты.
            5 - Рекламные слоганы.
            6 - Короткие истории.
            7 - Подписи в Instagram.
            8 - Короче, Википедия.
            9 - Синопсисы фильмов.
            10 - Гороскоп.
            11 - Народные мудрости.
            12 - Балабоба x Garage.
        session (ClientSession, optional): По умолчанию None.
    Returns:
        str: Ответ Балабобы
    """
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        return await _fetch(query, style, session)
