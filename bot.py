import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from keep_alive import keep_alive  # анти-сон сервер

# 🚀 Запуск анти-сна
keep_alive()

# 🔐 Настройки
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🎯 Кнопка "Отправить сообщение"
send_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📨 Отправить сообщение", callback_data="send_message")]
])

# 📸 Приветствие и инструкция
@dp.message(commands=["start"])
async def start_message(message: types.Message):
    try:
        with open("logo.jpg", "rb") as photo:
            await message.answer_photo(
                photo=photo,
                caption=(
                    "📢 **Приветствуем вас в проекте SIGNAL**\n"
                    "Анонимная система для сообщений о правонарушениях.\n"
                    "Ваше имя не сохраняется — всё конфиденциально.\n\n"
                    "📝 **Как оформить обращение:**\n"
                    "1️⃣ Что произошло — опишите событие.\n"
                    "2️⃣ Где — адрес, ориентир или населённый пункт.\n"
                    "3️⃣ Когда — дата и время.\n"
                    "4️⃣ Кто причастен — люди, авто, организации.\n"
                    "5️⃣ Прикрепите фото, видео или голосовое сообщение (по желанию).\n\n"
                    "⚖️ Все обращения поступают напрямую сотрудникам **МВД по Чеченской Республике.**"
                ),
                reply_markup=send_button,
                parse_mode="Markdown"
            )
    except Exception:
        await message.answer(
            "📢 **Приветствуем вас в проекте SIGNAL**\n"
            "Анонимная система для сообщений о правонарушениях.\n"
            "Ваше имя не сохраняется — всё конфиденциально.",
            reply_markup=send_button,
            parse_mode="Markdown"
        )

# 📨 Когда пользователь нажимает кнопку
@dp.callback_query(lambda c: c.data == "send_message")
async def prompt_user(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "✍️ Опишите ваше сообщение ниже. Можете прикрепить фото, видео или голос."
    )

# 💬 Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    # Отправляем админу
    if message.text:
        await bot.send_message(ADMIN_ID, f"🕵️‍♂️ Анонимное сообщение:\n{message.text}")
    elif message.photo:
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption="📷 Анонимное фото")
    elif message.video:
        await bot.send_video(ADMIN_ID, message.video.file_id, caption="🎥 Анонимное видео")
    elif message.voice:
        await bot.send_voice(ADMIN_ID, message.voice.file_id, caption="🎙 Голосовое сообщение")
    else:
        await bot.send_message(ADMIN_ID, "📦 Получено вложение неизвестного типа")

    # Благодарим пользователя
    await message.answer(
        "✅ Ваше сообщение получено.\n"
        "Благодарим за вашу бдительность и гражданскую позицию. "
        "Все обращения передаются сотрудникам **МВД по Чеченской Республике** для проверки.",
        parse_mode="Markdown"
    )

# 🚀 Запуск
async def main():
    print("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
