from aiogram import Router, types
from aiogram.filters import Command
from bot.db import crud
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from bot.handlers.user.menu_command import show_donate_menu, show_menu_about_us, show_menu_contacts, show_menu_newspaper, show_products_menu, show_start_menu
from bot.utils.states import NewsPapers

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

@router.message(Command('donate'))
async def donate_handler(message: Message):
    """Обработчик команды /donate"""
    await show_donate_menu(message)

@router.message(Command('products'))
async def products_handler(message: Message):
    """Обработчик команды /products"""
    await show_products_menu(message)

@router.message(Command('newspaper'))
async def menu_newspaper(message: Message, state: FSMContext):
    """Обработчик команды /newspaper"""
    await show_menu_newspaper(message)
    await state.set_state(NewsPapers.newspapers)
