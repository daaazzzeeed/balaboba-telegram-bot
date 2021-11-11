from aiobalaboba import balaboba as bb


async def get_balaboba_text(message: str) -> str:
    response = await bb(message)
    return response
