import html
from pathlib import Path
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, InputMediaPhoto

from bot.handlers.user.menu_command import show_donate_menu, show_menu_about_us, show_menu_contacts, show_products_menu, show_start_menu
from bot.keyboards.user.keyboards import get_show_bank, get_support_us
from bot.keyboards.user.products_keyboard import get_show_faq, get_show_price
from bot.parsers.products_parser import parse_products_page

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
    
@router.callback_query(F.data == "donate")
async def menu_support_us(callback: CallbackQuery):
    """Обработчик кнопки 'Поддержать'"""
    await show_donate_menu(callback, edit=True)

@router.callback_query(F.data.startswith('bank_'))
async def support_us_callback(callback: CallbackQuery):
    """Отображает данные реквизитов при выборе банка."""
    bank_name = callback.data.split('_')[1]
    bank_description = {
        "sberbank": (
                    "🏦 <b>Сбербанк</b>\n\n"
                    "Получатель: <i>Сергей Иванович К.</i>\n"
                    "Карта: <code>4276 6800 1260 0464</code>\n"
                    "Телефон, привязанный к карте: <code>+7 950 173 48 38</code>"
        ),
        "mtsbank": (
                    "💳 <b>МТС Банк</b>\n\n"
                    "Вы можете перевести средства, пополнив баланс телефона:\n"
                    "<code>+7 912 756 82 80</code>"
        ),
        "mailrussia": (
                    "📮 <b>Почта России</b>\n\n"
                    "Адрес для почтовых переводов:\n"
                    "<i>427550, Удмуртская Республика,\n"
                    "п. Балезино, а/я 24,\n"
                    "Кощееву Сергею Ивановичу</i>"
        )
        }
    bank_info = bank_description.get(bank_name)
    markup = get_show_bank()
    if not bank_info:
        await callback.answer('❌ Способ не найден', show_alert=True)
        return
        
    await callback.message.edit_text(
    bank_info, reply_markup=markup
    )
    
@router.callback_query(lambda c: c.data == 'menu_products')
async def menu_products(callback: CallbackQuery):
    """Обработчик кнопки 'Продукция' из главного меню"""
    await show_products_menu(callback, edit=True)

@router.callback_query(F.data == 'show_price')
async def menu_show_price(callback: CallbackQuery):
    """Обработчик кнопки 'Цена газеты' из Продукция"""
    data = parse_products_page()
    main_price = data.get('price', "Цена не найдена 😔")
    price_delivery = data.get('price_delivery', [])
    text = (
        "💰 <b>Информация о ценах</b>\n\n"
        f"{main_price}\n\n"
    )
    if price_delivery:
        text += "📦 <b>Цены с пересылкой по России:</b>\n"
        for count, price in price_delivery:
            text += f"• {count}: <b>{price}</b>\n"
            
    markup = get_show_price()
    await callback.message.edit_text(text, reply_markup=markup)

@router.callback_query(F.data == 'show_faq')
async def menu_show_faq(callback: CallbackQuery):
    """Обработчик кнопки 'Популярные вопросы' из Продукция"""
    data = parse_products_page()
    questions = data.get('popular_questions', [])
    
    if not questions:
        await callback.answer('Популярные вопросы временно недоступны 😔', show_alert=True)
        return
    
    text = (
        '❓ <b>Популярные вопросы:</b>\n\n'
    )
    for question, answer in questions:
        text += f'🔹 <b>{question}</b>\n<blockquote>{answer}</blockquote>\n\n'
        
    markup = get_show_faq()
    await callback.message.edit_text(text, reply_markup=markup)
    