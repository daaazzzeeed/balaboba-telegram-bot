from balaboba import balaboba as bb


def get_balaboba_text(message: str) -> str:
    response = bb(message)
    return response
