from aiogram import Bot, Dispatcher
from app.telegram.handlers import router
from app.db import init_db
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
# check
# print(f"Bot token: {TOKEN}")

async def main():
    init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
