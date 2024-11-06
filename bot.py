import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка токена из переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Временное хранилище для игроков в памяти
players = []

# Команда для добавления игрока
async def add_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        name = context.args[0]
        coef = float(context.args[1])
        players.append((name, coef))
        await update.message.reply_text(f"Игрок {name} с коэффициентом {coef} добавлен!")
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /add_player <имя> <коэффициент>")

# Команда для просмотра игроков
async def view_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not players:
        await update.message.reply_text("Пока что список игроков пуст.")
        return
    response = "Список игроков:\n" + "\n".join(f"{name}: {coef}" for name, coef in players)
    await update.message.reply_text(response)

# Команда для распределения игроков по командам
async def split_teams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        num_teams = int(context.args[0])
        if num_teams <= 0:
            raise ValueError("Количество команд должно быть больше нуля.")
        
        # Инициализация команд
        teams = [[] for _ in range(num_teams)]
        team_sums = [0] * num_teams

        # Сортируем игроков по коэффициентам и распределяем по командам
        for player, coef in sorted(players, key=lambda x: -x[1]):  # Сортируем по убыванию коэффициента
            min_team_idx = team_sums.index(min(team_sums))
            teams[min_team_idx].append((player, coef))
            team_sums[min_team_idx] += coef

        # Формируем сообщение с разбивкой по командам
        response = ""
        for i, team in enumerate(teams, start=1):
            response += f"Команда {i}:\n" + "\n".join(f"{name}: {coef}" for name, coef in team) + "\n\n"
        await update.message.reply_text(response)
    
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /split <количество_команд>")

# Основной код бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Команды для добавления игрока, просмотра игроков и распределения по командам
    app.add_handler(CommandHandler("add_player", add_player))
    app.add_handler(CommandHandler("view_players", view_players))
    app.add_handler(CommandHandler("split", split_teams))

    # Запуск бота
    app.run_polling()
