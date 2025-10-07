import asyncio
from aiogram import Bot, Dispatcher
from bot.config.settings import settings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers.admin import admin
from bot.utils.logger import logger
from bot.handlers.user import message
from bot.handlers.user import callback
from bot.db.models import Base
from bot.db.base import engine
from bot.db.base import init_db

async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")

async def main():
    # Создаём экземпляр бота
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_routers(message.router, admin.router, callback.router)
    
    # Инициализация базы данных
    await init_db()

    await on_startup()
    logger.info("Bot started!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
