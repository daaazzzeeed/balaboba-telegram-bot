from fastapi import FastAPI, Request
import telebot
from app.config import BOT_TOKEN, APP_URL
from app.balaboba_handler import get_balaboba_text
import app.text_responses as text_responses

app = FastAPI()
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, text_responses.hello_message(message.from_user.first_name))
    bot.reply_to(message, text_responses.bot_description())
    bot.reply_to(message, text_responses.get_help())


@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, text_responses.get_help())


@bot.message_handler(content_types=["text"])
def response_to_user(message):
    text = get_balaboba_text(message.text)
    bot.reply_to(message, text)


@app.get("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL+BOT_TOKEN)
    return "webhook successfully set"


@app.post("/"+BOT_TOKEN, status_code=200)
async def get_message(request: Request):
    data = await request.json()
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return {"message": str(update)}
