import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from typing import List, Tuple

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Проверим, если токен не найден
if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Пример списка игроков с коэффициентами
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
    teams = [[] for _ in range(num_teams)]
    team_sums = [0] * num_teams

    for player, coef in sorted(sorted_players, key=lambda x: x[1], reverse=True):
        min_team_idx = team_sums.index(min(team_sums))
        teams[min_team_idx].append((player, coef))
        team_sums[min_team_idx] += coef

    return teams, team_sums

# Команда /start с кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[str(i)] for i in range(2, 6)]  # Кнопки от 2 до 5 команд
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Choose the number of teams:", reply_markup=reply_markup)

# Обработчик выбора количества команд
async def split(update: Update, context: CallbackContext) -> None:
    try:
        num_teams = int(update.message.text)
        if num_teams < 2 or num_teams > len(sorted_players):
            await update.message.reply_text(f"Please choose a number between 2 and {len(sorted_players)}.")
            return
    except ValueError:
        await update.message.reply_text("Please select a valid number of teams.")
        return

    teams, team_sums = split_players(sorted_players, num_teams)
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
    
    # Обрабатываем выбранное количество команд через текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, split))
    
    # Запускаем бота
    app.run_polling()
