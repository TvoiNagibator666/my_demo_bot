from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import cursor

router = Router()

@router.message(F.text == "/catalog")
async def catalog(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Apple", callback_data="brand_Apple")
    kb.button(text="Samsung", callback_data="brand_Samsung")
    kb.adjust(2)

    await message.answer("Выбери бренд:", reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith("brand_"))
async def filter_brand(callback: CallbackQuery):
    brand = callback.data.split("_")[1]

    cursor.execute("SELECT name, price FROM products WHERE brand=? AND active=1", (brand,))
    items = cursor.fetchall()

    if not items:
        return await callback.message.answer("Нет товаров")

    text = "\n".join([f"{name} — {price}₽" for name, price in items])
    await callback.message.answer(text)