from aiogram import Bot, Dispatcher, types, executor
from app.config import settings
from app.balaboba_handler import get_balaboba_text
import app.text_responses as text_responses
import os
import logging
from app.consts import AppModes

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)
logger = logging.getLogger(__name__)
logger.info("STARTING............")

WEBHOOK_HOST = settings.APP_URL
WEBHOOK_PATH = f"/webhook/{settings.BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8443

logger.info(settings.BOT_TOKEN)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(text_responses.hello_message(message.from_user.first_name))
    await message.reply(text_responses.bot_description())
    await message.reply(text_responses.get_help())


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.reply(text_responses.get_help())


@dp.message_handler(commands=["stop"])
async def bye(message: types.Message):
    await bot.send_message(message.chat.id, "Пока-пока!")


@dp.message_handler(content_types=["text"])
async def response_to_user(message: types.Message):
    text = await get_balaboba_text(message.text)
    await message.reply(text)


@dp.message_handler(commands=["mode"])
async def switch_mode(message: types.Message):
    if settings.APP_MODE == AppModes.Webhook:
        settings.APP_MODE = AppModes.Polling
        await message.reply("Mode switched to polling")
    else:
        settings.APP_MODE = AppModes.Webhook
        await message.reply("Mode switched to webhooks")
    start_bot()


async def on_startup(dispatcher: Dispatcher) -> None:
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()


def start_bot():
    if "HEROKU" in list(os.environ.keys()) and settings.APP_MODE == AppModes.Webhook:
        print(list(os.environ.keys()))
        print("HEROKU in env")
        print("WH_HOST:", WEBHOOK_HOST)
        print("WA_HOST:", WEBAPP_HOST)
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=int(os.environ.get('PORT', 5000)),
        )
    else:
        print("no HEROKU in env")
        print(list(os.environ.keys()))
        executor.start_polling(dp)


if __name__ == "__main__":
    bot.delete_webhook()
    start_bot()
