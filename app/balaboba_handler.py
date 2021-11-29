import aiobalaboba


async def get_balaboba_text(message: str) -> str:
    response = await aiobalaboba.balaboba(message)
    print(response)
    return response
