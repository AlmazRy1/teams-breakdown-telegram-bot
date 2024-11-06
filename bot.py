from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7736749449:AAGExAxvHsMPDvFIvF59u0NjhuQ6QWFWpMc"  # Замени на твой токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your bot. How can I help you?")

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
