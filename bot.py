import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
import threading
import os

# Твой токен и ID
TOKEN = os.getenv("BOT_TOKEN")  # добавь токен в Render -> Environment
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

# Команда /start
@dp.message(Command("start"))
async def start_message(message: types.Message):
    text = (
        "📡 *Приветствуем вас в проекте SIGNAL!*\n\n"
        "Этот бот управляется МВД по Чеченской Республике и предназначен "
        "для приёма анонимных сообщений о правонарушениях.\n\n"
        "Пожалуйста, опишите ваше сообщение как можно подробнее:\n"
        "— что произошло\n"
        "— где и когда\n"
        "— есть ли фото/видео доказательства\n\n"
        "Ваша личность остаётся полностью анонимной."
    )
    await message.answer(text, parse_mode="Markdown")

# Приём сообщений от пользователей
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    await bot.send_message(ADMIN_ID, f"📩 Новое анонимное сообщение:\n\n{user_text}")
    await message.answer("✅ Спасибо! Ваше сообщение отправлено.")

# Запуск Flask (для Render)
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
