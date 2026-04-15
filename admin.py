from aiogram import Router, F
from aiogram.types import Message
from config import config
from db import cursor

router = Router()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return await message.answer("Нет доступа")

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    await message.answer(f"Товаров в системе: {count}")

@router.message(F.text.startswith("/disable"))
async def disable_product(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return

    product_id = int(message.text.split()[1])

    cursor.execute("UPDATE products SET active=0 WHERE id=?", (product_id,))
    await message.answer("Товар отключен")