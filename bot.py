import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import os
from config import TOKEN, COLORS, FONTS, POSITIONS
from database import init_db, get_user, update_user
from watermark import add_watermark_image

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔒 Администратор и белый список пользователей
ADMIN_ID = 800577446  # Замени на свой Telegram ID
ALLOWED_USERS = [ADMIN_ID]

init_db()

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🖋 Текст", callback_data="text")
    kb.button(text="🎨 Цвет", callback_data="color")
    kb.button(text="📍 Позиция", callback_data="position")
    kb.button(text="🔠 Шрифт", callback_data="font")
    kb.button(text="💧 Прозрачность", callback_data="transparency")
    kb.button(text="📏 Размер", callback_data="size")
    kb.adjust(2)
    return kb.as_markup()

@dp.message(Command("start"))
async def start_cmd(msg: Message):
    if msg.from_user.id not in ALLOWED_USERS:
        await msg.answer("⛔ У вас нет доступа к этому боту.")
        return
    get_user(msg.from_user.id)
    await msg.answer("👋 Привет, мастер! Отправь фото, и я нанесу водяной знак.", reply_markup=main_menu())

@dp.message(Command("adduser"))
async def add_user_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔ У вас нет прав администратора.")
        return

    try:
        user_id = int(msg.text.split()[1])
        if user_id not in ALLOWED_USERS:
            ALLOWED_USERS.append(user_id)
            await msg.answer(f"✅ Пользователь {user_id} добавлен в whitelist!")
        else:
            await msg.answer("⚠️ Этот пользователь уже есть в списке.")
    except (IndexError, ValueError):
        await msg.answer("❌ Использование: /adduser <id>")

@dp.message(Command("listusers"))
async def list_users_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔ Нет доступа.")
        return
    users = "\n".join([str(u) for u in ALLOWED_USERS])
    await msg.answer(f"👥 Список разрешённых пользователей:\n{users}")

@dp.message(F.photo)
async def add_mark(msg: Message):
    if msg.from_user.id not in ALLOWED_USERS:
        await msg.answer("⛔ У вас нет доступа к этому боту.")
        return
    user = get_user(msg.from_user.id)
    photo = await msg.photo[-1].download(destination_dir=".")
    output_path = f"out_{msg.from_user.id}.jpg"
    add_watermark_image(photo.name, output_path, user[1], user[2], user[3], user[4], user[5], user[6])
    await msg.answer_photo(FSInputFile(output_path))
    os.remove(photo.name)
    os.remove(output_path)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
