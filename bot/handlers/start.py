from aiogram import Router, types
from aiogram.filters import Command
from bot.db import crud

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await crud.add_user(tg_id=message.from_user.id, username=message.from_user.username)
    await message.answer("✅ Вы успешно зарегистрированы в базе!")
