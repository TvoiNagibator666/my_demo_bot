from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import cursor, conn

router = Router()

class AddProduct(StatesGroup):
    name = State()
    brand = State()
    price = State()

@router.message(F.text == "/add")
async def add_start(message: Message, state: FSMContext):
    await state.set_state(AddProduct.name)
    await message.answer("Название товара:")

@router.message(AddProduct.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.brand)
    await message.answer("Бренд:")

@router.message(AddProduct.brand)
async def get_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("Цена:")

@router.message(AddProduct.price)
async def get_price(message: Message, state: FSMContext):
    data = await state.get_data()

    cursor.execute(
        "INSERT INTO products (user_id, name, brand, price) VALUES (?, ?, ?, ?)",
        (message.from_user.id, data["name"], data["brand"], int(message.text))
    )
    conn.commit()

    await state.clear()
    await message.answer("Товар добавлен!")