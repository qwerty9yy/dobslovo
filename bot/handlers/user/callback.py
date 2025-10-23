import html
from pathlib import Path
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from bot.handlers.user.menu_command import show_donate_menu, show_menu_about_us, show_menu_contacts, show_menu_newspaper, show_products_menu, show_start_menu
from bot.keyboards.user.keyboards import  get_menu_newspaper, get_show_bank
from bot.keyboards.user.products_keyboard import get_show_faq, get_show_price
from bot.parsers.archives_parser import parse_archives_page
from bot.parsers.products_parser import parse_products_page
from bot.utils.states import NewsPapers

router = Router()

@router.callback_query(F.data == "back_to_main")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Назад' в главное меню"""
    
    await state.clear()
    
    try:
        await show_start_menu(callback, edit=True)  # Редактируем существующее сообщение
    except TelegramBadRequest:
        # Если не получается отредактировать (сообщение без текста),
        # отправляем новое сообщение
        await show_start_menu(callback, edit=False)  
    await callback.answer()      

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

@router.callback_query(lambda c: c.data == 'menu_products')
async def menu_products(callback: CallbackQuery):
    """Обработчик кнопки 'Продукция' из главного меню"""
    await show_products_menu(callback, edit=True)

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

@router.callback_query(F.data == 'show_price')
async def menu_show_price(callback: CallbackQuery):
    """Обработчик кнопки 'Цена газеты' из Продукция"""
    data = await parse_products_page() or {}
    main_price = data.get('price', "Цена не найдена 😔")
    price_delivery = data.get('price_delivery', [])
    text = (
        "💰 <b>Информация о ценах</b>\n\n"
        f"{main_price}\n\n"
    )
    if price_delivery:
        text += "📦 <b>Цены с пересылкой по России:</b>\n"
        for count, price in price_delivery:
            text += f"• {html.escape(count)}: <b>{html.escape(price)}</b>\n"
            
    markup = get_show_price()
    try:
        await callback.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest:
        await callback.answer("Сообщение уже актуально ✅", show_alert=False)

@router.callback_query(F.data == 'show_faq')
async def menu_show_faq(callback: CallbackQuery):
    """Обработчик кнопки 'Популярные вопросы' из Продукция"""
    data = await parse_products_page() or {}
    questions = data.get('popular_questions', [])
    
    if not questions:
        await callback.answer('Популярные вопросы временно недоступны 😔', show_alert=True)
        return
    
    text = (
        '❓ <b>Популярные вопросы:</b>\n\n'
    )
    for question, answer in questions:
        text += f'🔹 <b>{html.escape(question)}</b>\n<blockquote>{html.escape(answer)}</blockquote>\n\n'
        
    markup = get_show_faq()
    try:
        await callback.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest:
        await callback.answer("Сообщение уже актуально ✅", show_alert=False)
    
@router.callback_query(F.data == 'newspaper')
async def menu_show_newspaper(callback: CallbackQuery): #, state: FSMContext
    """Обработчик кнопки 'Газета'"""
    await show_menu_newspaper(callback, edit=True)
    # await state.set_state(NewsPapers.newspapers)
        
# @router.message(NewsPapers.newspapers)
# async def menu_process_years(message: Message, state: FSMContext):
#     """Обработчик кнопки 'Введеного года'"""
    
#     if message.text.startswith('/'):
#         await state.clear()
#         return
    
#     data = await parse_archives_page()
#     newspapers = data.get('newspapers', [])
    
#     if not newspapers:
#         await message.answer('Архивы временно недоступны')
#         await state.clear()
#         return
    
#     max_year = max(int(item['year']) for item in newspapers)
#     user_text = message.text
#     markup = get_menu_newspaper_search()
#     # Проверки
#     if not user_text.isdigit():
#         await message.answer('❌ Введите число!', reply_markup=markup)
#         return
    
#     if len(user_text) != 4:
#         await message.answer('❌ Пожалуйста, введите корректный год (4 цифры)', reply_markup=markup)
#         return
    
#     year = int(user_text)
    
#     if year < 2018:
#         await message.answer('❌ Выпусков до 2018 года нет в архивах', reply_markup=markup)
#         return
    
#     if year > max_year:
#         await message.answer(f'❌ Выпуски доступны до {max_year} года', reply_markup=markup)
#         return
    
#     year_papers = [paper for paper in newspapers if int(paper['year']) == year]
    
#     if not year_papers:
#         await message.answer(f'❌ За {year} год выпусков не найдено', reply_markup=markup)
#         await state.clear()
#         return
    
#     # Показываем найденные газеты
#     text = f'📰 <b>Газеты за {year} год:</b>\n\n'
#     for paper in year_papers:
#         text += f"• {paper['title']}\n"
        
#     markup_papers = create_year_papers_keyboard(year_papers)
#     await message.answer(text, reply_markup=markup_papers)
#     await state.clear()

@router.callback_query(F.data.startswith('newspaper_'))
async def handle_newspaper_selection(callback: CallbackQuery):
    """Обработчик кнопки 'Выбора выпуска газеты введеного года'"""
    try:
        parts = callback.data.split('_')    # ["newspaper", "2024", "1"]

        year = parts[1]
        issue = parts[2]

        data = await parse_archives_page()
        papers = data.get('newspapers', [])

        # Ищем выбранную газету
        selected_paper = next(
            (paper for paper in papers 
                if paper['year'] == year and paper['issue'] == issue),
            None
        )

        if not selected_paper:
            await callback.answer("❌ Газета не найдена", show_alert=True)
            return

        markup = get_menu_newspaper()

        # Отправляем картинку газеты
        if selected_paper.get('img_url'):
            await callback.message.answer_photo(
                photo=selected_paper['img_url'],
                caption=(f"📰 <b>{selected_paper['title']}</b>"
            ))

        # Отправляем PDF файл
        try:
            await callback.message.answer_document(
                document=selected_paper['pdf_url'],
                caption=f"📄 <b>Газета в формате PDF</b>\n⬆️ Скачайте файл или вернитесь в меню",
                reply_markup=markup)
        except TelegramBadRequest as e:
            print(f"PDF Telegram error: {e}")
            # Специфичная обработка ошибок Telegram
            if "wrong file identifier" in str(e).lower() or "wrong type" in str(e).lower():
                await callback.message.answer(
                    f"❌ Неверный формат файла\n"
                    f"📰 <b>{selected_paper['title']}</b>\n"
                    f"🔗 <a href='{selected_paper['pdf_url']}'>Скачать по ссылке</a>",
                    reply_markup=markup
                )
            else:
                await callback.message.answer(
                    '❌ Не удалось загрузить PDF файл',
                    reply_markup=markup
                )
                
        except Exception as e:
            print(f"PDF general error: {e}")
            await callback.message.answer(
                '❌ Ошибка при загрузке файла',
                reply_markup=markup
            )
    except Exception as e:
        print(f"Unexpected error in newspaper selection: {e}")
        await callback.answer("❌ Произошла непредвиденная ошибка", show_alert=True)
