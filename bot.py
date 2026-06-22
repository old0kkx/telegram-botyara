import random
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "привет!\n\n"
        "я бот-игра ´угадай числo´\n\n"
        "правила:\n"
        "• я загадываю число от 1 до 100\n"
        "• вы пишете числа в чат(В ОТВЕТ МНЕ НА СООБЩЕНИЕ)\n"
        "• я отвечаю: больше / меньше / угадал\n"
        "• после угадывания начинается новый раунд\n\n"
        "команда для старта игры:\n"
        "/startgame "
    )

    await update.message.reply_text(text)


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    games[chat_id] = random.randint(1, 100)

    await update.message.reply_text(
        "игра началась!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
   
    if chat_id not in games:
        return

    text = update.message.text

    if not text or not text.isdigit():
        return

    guess = int(text)
    secret = games[chat_id]

    if guess < secret:
        await update.message.reply_text("больше ")
    elif guess > secret:
        await update.message.reply_text("меньше ")
    else:
        await update.message.reply_text(f"вау.... число было {secret}")

        games[chat_id] = random.randint(1, 100)


import asyncio

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("startgame", start_game))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
