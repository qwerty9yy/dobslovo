import asyncio
from bot.utils.logger import logger
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError, TelegramBadRequest


class AntiFloodMiddleware(BaseMiddleware):
    """
    Middleware для защиты от Flood control (Too Many Requests)
    Автоматически перехватывает TelegramRetryAfter и ждёт нужное время.
    """

    def __init__(self, min_delay: float = 0.5):
        # минимальная задержка между сообщениями в один чат (секунды)
        self.min_delay = min_delay
        self.last_message_time = {}
        super().__init__()

    async def __call__(self, handler, event: TelegramObject, data: dict):
        chat_id = getattr(getattr(event, "chat", None), "id", None)
        if chat_id:
            # проверяем, прошло ли нужное время между сообщениями
            last_time = self.last_message_time.get(chat_id, 0)
            now = asyncio.get_event_loop().time()
            elapsed = now - last_time

            if elapsed < self.min_delay:
                await asyncio.sleep(self.min_delay - elapsed)

            self.last_message_time[chat_id] = now

        # перехватываем TelegramRetryAfter внутри самого вызова
        while True:
            try:
                return await handler(event, data)
            except TelegramRetryAfter as e:
                wait = getattr(e, "retry_after", 5)
                logger.info(f"⚠️ Flood control: жду {wait} сек (chat_id={chat_id})")
                await asyncio.sleep(wait)
            except TelegramForbiddenError:
                logger.error(f"🚫 Пользователь {chat_id} заблокировал бота.")
                return
            except TelegramBadRequest as e:
                logger.error(f"⚠️ Ошибка TelegramBadRequest: {e}", exc_info=True)
                return
            except Exception as e:
                logger.error(f"⚠️ Неожиданная ошибка в middleware: {e}", exc_info=True)
                await asyncio.sleep(1)
                return
