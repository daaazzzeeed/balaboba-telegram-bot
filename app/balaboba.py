from aiobalaboba import balaboba


async def get_balaboba_text(message: str) -> str:
    response = await balaboba(message)
    return response
