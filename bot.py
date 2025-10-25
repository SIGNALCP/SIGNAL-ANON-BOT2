import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from flask import Flask
import threading
import os

# Токен и ID администратора (из Render Environment)
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

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

# Приём любых типов сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text or ""
    caption = f"📩 Новое анонимное сообщение:\n\n{user_text}"

    # Если есть фото
    if message.photo:
        photo = message.photo[-1]  # берём фото максимального качества
        await bot.send_photo(ADMIN_ID, photo.file_id, caption=caption or "📩 Новое фото")

    # Если есть видео
    elif message.video:
        await bot.send_video(ADMIN_ID, message.video.file_id, caption=caption or "📩 Новое видео")

    # Если есть документ (например, скриншоты, PDF и т.п.)
    elif message.document:
        await bot.send_document(ADMIN_ID, message.document.file_id, caption=caption or "📩 Новый файл")

    # Если просто текст
    elif message.text:
        await bot.send_message(ADMIN_ID, caption)

    # Ответ пользователю
    await message.answer("✅ Спасибо! Ваше сообщение отправлено.")

# Flask для Render
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
