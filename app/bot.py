from aiogram import Bot, Dispatcher, executor, types
from app.config import settings
from app.balaboba_handler import get_balaboba_text
import app.text_responses as text_responses

# app = FastAPI()
bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(text_responses.hello_message(message.from_user.first_name))
    await message.reply(text_responses.bot_description())
    await message.reply(text_responses.get_help())


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.reply(text_responses.get_help())


@dp.message_handler(content_types=["text"])
async def response_to_user(message):
    text = await get_balaboba_text(message.text)
    await message.reply(text)


# @app.get("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url=APP_URL+BOT_TOKEN)
#     return "webhook successfully set"
#
#
# @app.post("/"+BOT_TOKEN, status_code=200)
# async def get_message(request: Request):
#     data = await request.json()
#     update = telebot.types.Update.de_json(data)
#     bot.process_new_updates([update])
#     return {"message": str(update)}

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
