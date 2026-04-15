from aiogram import Router, F
from aiogram.types import Message
from db import cursor, conn

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (message.from_user.id,))
    conn.commit()

    await message.answer(
        "Добро пожаловать!\n\n"
        "/catalog — поиск товаров\n"
        "/add — добавить товар\n"
        "/balance — баланс"
    )