import balaboba_engine


async def get_balaboba_text(message: str) -> str:
    response = await balaboba_engine.balaboba(message)
    return response
