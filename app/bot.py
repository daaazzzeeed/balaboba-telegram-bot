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

WEBHOOK_URL = settings.APP_URL

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


@dp.message_handler(commands=["mode"])
async def switch_mode(message: types.Message):
    if settings.APP_MODE == AppModes.Webhook:
        settings.APP_MODE = AppModes.Polling
        await message.reply("Mode switched to polling")
        await bot.delete_webhook()
        executor.start_polling(dp)
    else:
        settings.APP_MODE = AppModes.Webhook
        await message.reply("Mode switched to webhooks")
        settings.WEBHOOK_IS_SET = True
        print("Webhook was set...")
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_URL,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=int(os.environ.get('PORT', 5000)),
        )


@dp.message_handler(content_types=["text"])
async def response_to_user(message: types.Message):
    text = await get_balaboba_text(message.text)
    await message.reply(text)


async def on_startup(dispatcher: Dispatcher) -> None:
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()


def setup_webhook():
    settings.WEBHOOK_IS_SET = True
    print("Webhook was set...")
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=int(os.environ.get('PORT', 5000)),
    )


def start_bot():
    settings.WEBHOOK_IS_SET = True
    print("Webhook was set...")
    setup_webhook()


if __name__ == "__main__":
    if settings.WEBHOOK_IS_SET:
        bot.delete_webhook()
    start_bot()
