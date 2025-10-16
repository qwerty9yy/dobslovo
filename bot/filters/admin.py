from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union
from bot.config.settings import settings

class IsAdmin(BaseFilter):
    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        """Фильтр проверяет, является ли пользователь администратором"""
        user_id = obj.from_user.id
        return user_id in settings.ADMIN_IDS