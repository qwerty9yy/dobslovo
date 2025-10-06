from aiogram import Router, types
from aiogram.filters import Command
from bot.config.settings import settings

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return await message.answer("🚫 У вас нет доступа.")
    await message.answer("✅ Добро пожаловать в админку!")



"""Объяснение:

Простейшая проверка прав администратора по ADMIN_ID.

Если ID не совпадает — отправляем отказ.

Легко расширяется до полноценной админ-панели."""