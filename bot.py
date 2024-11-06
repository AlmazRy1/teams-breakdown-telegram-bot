import os
from dotenv import load_dotenv
load_dotenv()
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from typing import List, Tuple

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Проверим, если токен не найден
if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Пример списка игроков с коэффициентами
# Это должно быть частью вашего кода, где вы передаете список игроков
sorted_players = [
    ("Player1", 1.1),
    ("Player2", 2.3),
    ("Player3", 3.5),
    ("Player4", 4.2),
    ("Player5", 0.9),
    ("Player6", 1.8),
    ("Player7", 2.6),
    ("Player8", 3.7),
    ("Player9", 1.2),
    ("Player10", 2.4),
    ("Player11", 3.0),
    ("Player12", 4.5),
]

# Функция для распределения игроков по командам
def split_players(sorted_players: List[Tuple[str, float]], num_teams: int):
    # Initialize teams and their sums
    teams = [[] for _ in range(num_teams)]
    team_sums = [0] * num_teams

    # Distribute players by adding the highest available coefficient to the team with the lowest sum
    for player, coef in sorted(sorted_players, key=lambda x: x[1], reverse=True):
        # Find the team with the minimum sum to add the next player
        min_team_idx = team_sums.index(min(team_sums))
        teams[min_team_idx].append((player, coef))
        team_sums[min_team_idx] += coef

    return teams, team_sums

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your bot. How can I help you?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def split(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем аргумент из команды
    try:
        num_teams = int(context.args[0])  # Читаем количество команд
    except (IndexError, ValueError):
        await update.message.reply_text("Please specify the number of teams (e.g. /split 4).")
        return

    if num_teams < 2 or num_teams > len(sorted_players):
        await update.message.reply_text("Please choose a number of teams between 2 and {}.".format(len(sorted_players)))
        return

    # Разбиваем игроков по командам
    teams, team_sums = split_players(sorted_players, num_teams)

    # Формируем сообщение с результатами
    response = f"Players have been split into {num_teams} teams:\n"
    for i, team in enumerate(teams):
        response += f"\nTeam {i + 1} (Sum: {team_sums[i]}):\n"
        for player, coef in team:
            response += f"  - {player} (Coefficient: {coef})\n"

    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем команду /start
    app.add_handler(CommandHandler("start", start))
    
    # Добавляем команду /split
    app.add_handler(CommandHandler("split", split))
    
    # Добавляем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    app.run_polling()
