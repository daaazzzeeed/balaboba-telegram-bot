from fastapi import FastAPI, Request
from telebot import TeleBot
from app.config import BOT_TOKEN

app = FastAPI()
bot = TeleBot(BOT_TOKEN)


@app.get("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook()



@app.post("/")
def get_message(request: Request):
    pass
