from fastapi import FastAPI, Request
import telebot
from app.config import BOT_TOKEN, APP_URL
import uvicorn

app = FastAPI()
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello, " + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo(message):
    bot.reply_to(message, message.text)


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
