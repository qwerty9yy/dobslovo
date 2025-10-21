from aiogram import Router, types
from aiogram.filters import Command
from bot.db import crud
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import time
from collections import defaultdict
from bot.handlers.user.menu_command import show_donate_menu, show_menu_about_us, show_menu_contacts, show_menu_newspaper, show_products_menu, show_start_menu
from bot.utils.states import NewsPapers

router = Router()
user_last_request = defaultdict(float)

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    current_time = time.time()
    if current_time - user_last_request[user_id] < 3:
        try:
            await message.answer("⏳ Пожалуйста, подождите немного...")
        except:
            pass
        return
    
    user_last_request[user_id] = current_time
    await state.clear()
    await crud.add_user(tg_id=message.from_user.id, username=message.from_user.username)
    await show_start_menu(message) # Без edit=True (новое сообщение)

@router.message(Command("contacts"))
async def contacts_handler(message: Message, state: FSMContext):
    await state.clear()
    """Обработчик команды /contacts"""
    await show_menu_contacts(message)
    
@router.message(Command('about'))
async def about_handler(message: Message, state: FSMContext):
    await state.clear()
    """Обработчик команды /about"""
    await show_menu_about_us(message)

@router.message(Command('donate'))
async def donate_handler(message: Message, state: FSMContext):
    await state.clear()
    """Обработчик команды /donate"""
    await show_donate_menu(message)

@router.message(Command('products'))
async def products_handler(message: Message, state: FSMContext):
    await state.clear()
    """Обработчик команды /products"""
    await show_products_menu(message)

@router.message(Command('newspaper'))
async def menu_newspaper(message: Message, state: FSMContext):
    """Обработчик команды /newspaper"""
    await show_menu_newspaper(message)
    await state.set_state(NewsPapers.newspapers)
