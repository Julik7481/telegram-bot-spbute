import json
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Загрузка базы FAQ
with open("faq.json", encoding="utf-8") as f:
    faq_data = json.load(f)

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🎓 Направления", "📆 Сроки"],
                ["📝 Вступительные", "💵 Стоимость"],
                ["🏠 Общежитие", "📞 Контакты"]]
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

# Запуск
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
app.run_polling()
