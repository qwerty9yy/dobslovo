from bot.keyboards.user.bible import get_bible_search, get_bible_search_word, get_book_name_keyboard, get_chapter_help, get_chapter_help_by_testament, get_chapter_selection, get_menu_bible
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
import json
import asyncio
from aiogram.exceptions import TelegramRetryAfter

from bot.parsers.bible_search import parse_bible_search
from bot.utils.states import Bible

router = Router()

MAX_MESSAGE_LENGTH = 4000

@router.message(Command('bible'))
async def menu_newspaper(message: Message, state: FSMContext):
    await state.clear()
    """Обработчик команды /bible"""
    await show_menu_bible(message)

@router.callback_query(F.data == 'bible')
async def menu_bible(callback: CallbackQuery):
    """Обработчик кнопки 'Библия' из главного меню"""
    await show_menu_bible(callback, edit=True)

async def show_menu_bible(message_or_call, edit: bool = False):
    """Меню Библия"""
    text = (
    "📚 *СВЯЩЕННОЕ ПИСАНИЕ* • *Библия*\n\n"
    
    "✨ *Божие Слово для каждого человека*\n"
    "Библия — это не просто книга, а живое Слово Божие, "
    "способное преобразить вашу жизнь, дать мудрость и указать путь ко спасению.\n\n"
    
    "📖 *ВЕТХИЙ ЗАВЕТ* — подготовка к приходу Спасителя\n"
    "• 39 книг • История • Закон • Пророчества • Мудрость\n\n"
    
    "📘 *НОВЫЙ ЗАВЕТ* — исполнение обетований во Христе\n"
    "• 27 книг • Евангелия • Учение Апостолов • Пророчества\n\n"
    
    "💫 *Выберите раздел для чтения:*"
    )
    markup = get_menu_bible()
    
    await asyncio.sleep(0.3)
    
    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')
    else:
        await message_or_call.answer(text, reply_markup=markup, parse_mode='Markdown')
        
@router.callback_query(F.data == 'chapter_help')
async def menu_chapter_help(callback: CallbackQuery):
    """Меню Список глав"""
    text = (
"📚 *Список доступных книг Библии:*\n\n"
        "*ВЕТХИЙ ЗАВЕТ:*\n"
        "• Бытие, Исход, Левит, Числа, Второзаконие\n"
        "• Иисус Навин, Судей, Руфь, 1-4 Царств\n"
        "• 1-2 Паралипоменон, Ездра, Неемия, Есфирь\n"
        "• Иов, Псалтирь, Притчи, Екклесиаст, Песнь Песней\n"
        "• Исаия, Иеремия, Плач Иеремии, Иезекииль, Даниил\n"
        "• Осия, Иоиль, Амос, Авдий, Иона, Михей\n"
        "• Наум, Аввакум, Софония, Аггей, Захария, Малахия\n\n"
        "*НОВЫЙ ЗАВЕТ:*\n"
        "• Матфея, Марка, Луки, Иоанна, Деяния\n"
        "• Римлянам, 1-2 Коринфянам, Галатам, Ефесянам\n"
        "• Филиппийцам, Колоссянам, 1-2 Фессалоникийцам\n"
        "• 1-2 Тимофею, Титу, Филимону, Евреям\n"
        "• Иакова, 1-2 Петра, 1-3 Иоанна, Иуды, Откровение"   
    )
    markup = get_chapter_help()
    await callback.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')
    
@router.callback_query(F.data.startswith('chapter_page_'))
async def menu_chapter_page(callback: CallbackQuery):
    """Меню Новый или ветхий завет"""
    testament_text = {
        'old': (
            "📖 *ВЕТХИЙ ЗАВЕТ*\n\n"
            
            "🌅 *От сотворения мира до Рождества Христова*\n"
            "Здесь записана священная история от Адама до пророка Малахии, "
            "законы данные через Моисея, мудрые изречения Соломона "
            "и вдохновенные пророчества о грядущем Мессии.\n\n"
            
            "⭐ *Ключевые книги:*\n"
            "• 🏛️ *Пятикнижие Моисеево* — основа Закона\n"
            "• 💎 *Псалтирь* — золотые молитвы Давида\n"
            "• 📜 *Пророки* — голос Божий к народу\n"
            "• 🎓 *Учительные* — мудрость для жизни\n\n"
            
            "✨ *Начните с:* Бытие, Псалтирь или Притчи\n\n"
            
            "_«Всё Писание боговдохновенно и полезно для научения...»_\n"
            "— 2 Тимофею 3:16"
        ),
        'new': (
            "📘 *НОВЫЙ ЗАВЕТ*\n\n"
            
            "✨ *От Рождества Христова до вечности*\n"
            "Четыре Евангелия рассказывают о жизни, смерти и воскресении Иисуса Христа, "
            "а послания Апостолов открывают путь спасения и христианской жизни.\n\n"
            
            "⭐ *Ключевые разделы:*\n"
            "• ✝️ *Евангелия* — жизнь и учение Христа\n"
            "• 🌍 *Деяния* — рождение Церкви\n"
            "• 💌 *Послания* — письма первых христиан\n"
            "• 🔮 *Откровение* — пророчество о будущем\n\n"
            
            "✨ *Начните с:* Евангелие от Иоанна или Евангелие от Луки\n\n"
            
            "_«Ибо так возлюбил Бог мир, что отдал Сына Своего Единородного...»_\n"
            "— Иоанна 3:16"
        )
    }
    
    # Получаем тип завета из callback_data
    testament_type = callback.data.split('_')[-1]
    
    if testament_type in testament_text:
        # Отправляем описание завета
        await callback.message.edit_text(
            testament_text[testament_type],
            reply_markup=get_chapter_help_by_testament(testament_type),
            parse_mode="Markdown"
        )
    else:
        # Если тип завета не распознан, показываем меню выбора
        await callback.message.edit_text(
            "📖 *Выберите Завет:*",
            reply_markup=get_chapter_help(),
            parse_mode="Markdown"
        )
    
    await callback.answer()
    
@router.callback_query(F.data.startswith('book_name_'))
async def menu_book_name(callback: CallbackQuery):
    """Меню Выбор Глав"""
    parts = callback.data.split('_')
    book_name = parts[-1]
    testament_type = parts[2] if len(parts) > 3 else 'old'
    text = (
        f"📖 <b>{book_name}</b>\n\n"
        "👇 Выберите главу:"
    )
    markup = get_book_name_keyboard(book_name, testament_type)
    await callback.message.edit_text(
        text, reply_markup=markup
    )
    
@router.callback_query(F.data.startswith('chapter_'))
async def menu_chapter_selection(callback: CallbackQuery):
    """Меню Обработка выбраной главы"""
    parts = callback.data.split('_')
    chapter_count = parts[-1]
    book_name = parts[1]
    
    with open('bot/cache/bible.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    book_data = data.get(book_name, {})
    chapter_data = book_data.get(chapter_count, {})
    
    # Получаем общее количество глав в книге
    total_chapters = len(book_data)
    current_chapter = int(chapter_count)
    
    header = f"📖 <b>{book_name}</b> | Глава {chapter_count}\n\n"
    footer = f"\n📄 <i>Глава {current_chapter} из {total_chapters}</i>"

    # Формируем текст главы
    text_content = ""
    for i, verse in chapter_data.items():
        text_content += f"{i}. {verse}\n"    
    
    # Разделяем текст на части, если он превышает лимит
    parts = []
    while text_content:
        chunk = text_content[:MAX_MESSAGE_LENGTH]
        split_index = chunk.rfind('\n')
        if split_index == -1:
            split_index = len(chunk)
        parts.append(text_content[:split_index])
        text_content = text_content[split_index:].lstrip()
    
    markup = get_chapter_selection(book_name, current_chapter, total_chapters)
    
    # Если глава помещается в одно сообщение — просто редактируем
    if len(parts) == 1:
        text = header + parts[0] + footer
        try:
            await callback.message.edit_text(text, reply_markup=markup)
        except TelegramBadRequest:
            await callback.answer("Сообщение уже актуально ✅", show_alert=False)
        return

    # Иначе: несколько сообщений
    # 🔹 Первое сообщение — редактируем (без клавиатуры)
    first_message_text = header + parts[0]
    try:
        await callback.message.edit_text(first_message_text)
    except TelegramBadRequest:
        await callback.answer("Сообщение уже актуально ✅", show_alert=False)

    # 🔹 Промежуточные части — просто отправляем (без клавиатуры)
    for part in parts[1:-1]:
        await callback.message.answer(part)
        await asyncio.sleep(0.5)

    # 🔹 Последняя часть — с футером и клавиатурой
    last_part = parts[-1] + footer
    await callback.message.answer(last_part, reply_markup=markup)
    
@router.callback_query(F.data.startswith('chapters_page_'))
async def paginate_chapters(callback: CallbackQuery):
    """Обработка кнопок пагинации глав."""
    _, _, book_name, page = callback.data.split('_')
    page = int(page)
    markup = get_book_name_keyboard(book_name, page=page)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data.startswith('book_name_back_'))
async def menu_back_to_chapters(callback: CallbackQuery):
    """Возврат из главы к выбору глав."""
    book_name = callback.data.split('_')[-1]

    # Формируем сообщение с выбором глав
    text = (
        f"📖 <b>{book_name}</b>\n\n"
        "👇 Выберите главу:"
    )
    markup = get_book_name_keyboard(book_name, testament_type='old')
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == 'bible_search')
async def menu_bible_search(callback: CallbackQuery, state: FSMContext):
    """Меню Поиск по Библии"""
    text = (
        "🔍 *ПОИСК ПО БИБЛИИ*\n\n"
        
        "✨ *Найдите нужный отрывок Писания*\n"
        "Введите слово или фразу, которую хотите найти в Священном Писании:\n\n"
        
        "📖 *Примеры запросов:*\n"
        "• _любовь_ - поиск всех упоминаний\n"
        "• _нагорная проповедь_ - найти отрывок\n\n"
        
        "💫 *Совет:* Используйте конкретные слова для более точных результатов\n\n"
        
        "⬇️ *Введите ваш запрос ниже:*"
    )
    markup = get_bible_search()
    await callback.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')
    await state.set_state(Bible.bible_search)

@router.message(Bible.bible_search)
async def menu_process_bible_search(message: Message, state: FSMContext):
    """Обработчик кнопки 'Поиска по Библии'"""
    
    user_request = message.text.strip()
    
    # ⏳ Пока идёт поиск — информируем пользователя
    await message.answer("🔎 Ищу совпадения, подождите немного...", show_alert=False)
    
    data = await parse_bible_search(user_request)
    
    if not data:
        await message.answer('❌ Ошибка при выполнении поиска. Попробуйте позже.', 
                             reply_markup=get_bible_search())
        await state.clear()
        return
    
    results = data['results']
    coincidences = data['coincidences']
    
    markup = get_bible_search_word()
    
    if coincidences == 0 or not results:
        await message.answer(
            f"😔 Ничего не найдено по запросу: <b>{user_request}</b>",
            reply_markup=markup
        )
        await state.clear()
        return
    
    # Формируем текст
    text_search = (
        f"📖 <b>Результаты поиска по слову:</b> <i>{user_request}</i>\n"
        f"🔢 Найдено совпадений: <b>{coincidences}</b>\n\n"
    )
    
    text = text_search
    
    for idx, item in enumerate(results, start=1):
        text += f"{idx}. <b>{item['from_where']}</b>\n{item['text']}\n\n"
        
    # Делим текст на части (если он превышает лимит)
    parts = []
    while text:
        chunk = text[:MAX_MESSAGE_LENGTH]
        split_index = chunk.rfind('\n\n')
        if split_index == -1:
            split_index = len(chunk)
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
        
    # Если текст влезает
    if len(parts) == 1:
        try:
            await message.edit_text(parts[0], reply_markup=markup)
        except TelegramBadRequest:
            await message.answer(parts[0], reply_markup=markup)
    else:
        # Первое сообщение редактируем (без клавиатуры)
        try:
            await message.edit_text(parts[0])
        except TelegramBadRequest:
            await message.answer(parts[0])
            
        # Промежуточные части (без клавиатуры)
        for p in parts[1:-1]:
            try:
                await message.answer(p)
                await asyncio.sleep(0.5)
            except TelegramRetryAfter as e:
                await message.answer(f"🔎 Ищу совпадения, подождите {e.retry_after} сек...")
                print(f"⏳ Flood control: спим {e.retry_after} сек...")
                await asyncio.sleep(e.retry_after)
            
        # Последняя часть (с клавиатурой)
        results_searh = parts[-1]
        results_searh += text_search
        await message.answer(results_searh, reply_markup=markup)
        
    await state.clear()