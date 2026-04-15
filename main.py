import asyncio
from aiogram import Bot, Dispatcher

from config import config
from db import init_db
import start, filter, product, payment, admin
import logging
logging.basicConfig(level=logging.INFO)
async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    init_db()

    dp.include_router(start.router)
    dp.include_router(filter.router)
    dp.include_router(product.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
