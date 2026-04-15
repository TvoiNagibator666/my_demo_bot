from aiogram import Router, F
from aiogram.types import Message
from db import cursor, conn

router = Router()

@router.message(F.text == "/balance")
async def balance(message: Message):
    cursor.execute("SELECT balance FROM users WHERE id=?", (message.from_user.id,))
    bal = cursor.fetchone()[0]

    await message.answer(f"Баланс: {bal}₽")

@router.message(F.text.startswith("/pay"))
async def pay(message: Message):
    amount = int(message.text.split()[1])

    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE id=?",
        (amount, message.from_user.id)
    )
    conn.commit()

    await message.answer(f"Пополнено на {amount}₽")

# списание (эмуляция)
@router.message(F.text == "/charge")
async def charge(message: Message):
    cursor.execute(
        "UPDATE users SET balance = balance - 10 WHERE id=?",
        (message.from_user.id,)
    )
    conn.commit()

    await message.answer("Списано 10₽ за размещение")