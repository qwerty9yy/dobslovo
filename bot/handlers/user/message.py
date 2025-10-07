from aiogram import Router, types
from aiogram.filters import Command
from bot.db import crud
from aiogram.types import Message

from bot.handlers.user.menu_command import show_menu_about_us, show_menu_contacts, show_start_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    await crud.add_user(tg_id=message.from_user.id, username=message.from_user.username)
    await show_start_menu(message) # Без edit=True (новое сообщение)

@router.message(Command("contacts"))
async def contacts_handler(message: Message):
    """Обработчик команды /contacts"""
    await show_menu_contacts(message)
    
@router.message(Command('about'))
async def about_handler(message: Message):
    """Обработчик команды /about"""
    await show_menu_about_us(message)