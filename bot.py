import json
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask
import threading
from telegram.error import Conflict
import threading

def run_bot():
    try:
        app.run_polling()
    except Conflict:
        print("⚠️ Бот уже запущен в другом месте!")

# Загрузка базы FAQ
with open("faq.json", encoding="utf-8") as f:
    faq_data = json.load(f)

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Направления", "Сроки"],
                ["Вступительные", "Стоимость"],
                ["Общежитие", "Контакты"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я — бот приёмной комиссии СПбУТУиЭ. Задайте вопрос или выберите тему:",
        reply_markup=reply_markup
    )

# Поиск ответа по ключевым словам
def find_answer(user_message):
    text = user_message.lower()
    for item in faq_data:
        if any(keyword in text for keyword in item["keywords"]):
            return item["answer"]
    return "Пожалуйста, уточните вопрос или выберите тему из меню."

# Обработка сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = find_answer(user_message)
    await update.message.reply_text(response)

# Функция для запуска бота
def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "7637716156:AAEL8ACVDiSjaGfplu_Z1yk_wH7lgJDKt4U")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

# HTTP-сервер для Render
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    threading.Thread(target=run_bot).start()
    # Запускаем Flask-сервер
    server.run(host='0.0.0.0', port=8000)