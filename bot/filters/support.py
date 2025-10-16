# from aiogram.filters import BaseFilter
# from aiogram.types import Message, CallbackQuery
# from typing import Union
# from bot.config.settings import settings

# class IsSupport(BaseFilter):
#     async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
#         return obj.from_user.id == settings.SUPPORT_ID