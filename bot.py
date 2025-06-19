import json
import os
import threading
import requests
from time import sleep
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running!"

with open("faq.json", encoding="utf-8") as f:
    faq_data = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Направления", "Сроки"],
                ["Вступительные", "Стоимость"],
                ["Общежитие", "Контакты"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я — бот приёмной комиссии СПбУТУиЭ. Задайте вопрос или выберите тему:",
        reply_markup=reply_markup
    )

def find_answer(user_message):
    text = user_message.lower()
    for item in faq_data:
        if any(keyword in text for keyword in item["keywords"]):
            return item["answer"]
    return "Пожалуйста, уточните вопрос или выберите тему из меню."

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = find_answer(user_message)
    print(f"[LOG] Получено сообщение: {user_message} → Ответ: {response}")
    await update.message.reply_text(response)

def keep_alive():
    while True:
        try:
            requests.get("https://tg-bot-spbute.onrender.com")
        except:
            pass
        sleep(300)

def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Отсутствует переменная окружения TELEGRAM_BOT_TOKEN")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8000))
    server.run(host='0.0.0.0', port=port)
