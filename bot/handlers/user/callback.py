import html
from pathlib import Path
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, InputMediaPhoto

from bot.handlers.user.menu_command import show_menu_about_us, show_menu_contacts, show_start_menu

router = Router()

@router.callback_query(F.data == "back_to_main")
async def back_to_menu(callback: CallbackQuery):
    """Обработчик кнопки 'Назад' в главное меню"""
    await show_start_menu(callback, edit=True)  # Редактируем существующее сообщение

@router.callback_query(F.data == "contacts")
async def menu_contacts(callback: CallbackQuery):
    """Обработчик кнопки 'Контакты'"""
    await show_menu_contacts(callback, edit=True)
    
@router.callback_query(F.data == "menu_about_us")
async def menu_about_us(callback: CallbackQuery):
    """Обработчик кнопки 'О нас'"""
    await show_menu_about_us(callback, edit=True)


