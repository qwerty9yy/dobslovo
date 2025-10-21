import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault
from bot.config.settings import settings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.core.bot_commands import get_bot_commands
from bot.handlers.admin import admin
from bot.utils.logger import logger
from bot.handlers.user import bible, message
from bot.handlers.user import callback
from bot.db.models import Base
from bot.db.base import engine
from bot.db.base import init_db

async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")
    
async def setup_bot_commands(bot: Bot):
    # Устанавливает команды бота в Telegram.
    # Безопасная инициализация с логированием.
    try:
        commands = get_bot_commands()
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault(), language_code='ru')
        logger.success("Команды бота успешно установлены")
    except Exception as e:
        logger.error(f"Ошибка при установке команд бота: {e}")

async def main():
    # Создаём экземпляр бота
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_routers(message.router, callback.router, bible.router)
    dp.include_routers(admin.admin_router)
    
    # Инициализация базы данных
    await init_db()
    
    await setup_bot_commands(bot)

    await on_startup()
    logger.info("Bot started!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
