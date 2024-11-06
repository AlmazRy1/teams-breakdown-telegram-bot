import os
from dotenv import load_dotenv
load_dotenv()
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Проверим, если токен не найден
if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Isasdasss'm your bot. How can I help you?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Добавляем команду /start
    app.add_handler(CommandHandler("start", start))
    
    # Добавляем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    app.run_polling()
