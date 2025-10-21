from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json

MAX_BUTTONS_PER_PAGE = 96  # Telegram лимит (немного меньше 100, с запасом)

@lru_cache
def get_menu_bible():
    ''' Клавиатура меню "Библия" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='📖 Библия', callback_data='chapter_help')
    builder.button(text='🔍 Поиск по Библии', callback_data='bible_search')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2, 1)
    return builder.as_markup()

@lru_cache
def get_chapter_help():
    ''' Клавиатура меню "Список глав" Telegram-бота «Доброе Слово». ''' 
    builder = InlineKeyboardBuilder()
    builder.button(text='📖 Ветхий Завет', callback_data='chapter_page_old')
    builder.button(text='📘 Новый Завет', callback_data='chapter_page_new')
    builder.button(text='🔍 Поиск по Библии', callback_data='bible_search')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2, 1, 1)
    return builder.as_markup()

@lru_cache
def get_chapter_help_by_testament(page_type: str = 'new', page: int = 0):
    ''' Клавиатура меню "Новый, Ветхий Завет" Telegram-бота «Доброе Слово». ''' 
    builder = InlineKeyboardBuilder()
    try:
        with open('bot/cache/bible.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        builder.button(text='🔙 Главное меню', callback_data='back_to_main')
        return builder.as_markup()
    
    all_books = list(data.keys())
    
    old_book = []
    new_book = []    
    
    # Разделяем на Ветхий и Новый Завет
    new_testament_start = None
    for i, book in enumerate(all_books):
        if book == 'Матфей':
            new_testament_start = i
            break
    
    if new_testament_start is not None:
        old_book = all_books[:new_testament_start]
        new_book = all_books[new_testament_start:]
    else:
        # Если все же не нашли, разделим пополам (резервный вариант)
        split_index = len(all_books) // 2
        old_book = all_books[:split_index]
        new_book = all_books[split_index:]
        
    # Выбираем книги в зависимости от типа завета
    if page_type == 'old':
        books_list = old_book
    else:
        books_list = new_book      
    
    for book_name in books_list:
        builder.button(text=f'{book_name}', callback_data=f'book_name_{page_type}_{book_name}')
    
    builder.button(text='🕊️ Выбор "Завета"', callback_data='chapter_help')
    builder.button(text='🔍 Поиск по Библии', callback_data='bible_search')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    if page_type == 'old':
        builder.adjust(*[2]*19, 1, 2, 1)
    else:
        builder.adjust(*[2]*13, 1, 2, 1)
    return builder.as_markup()

@lru_cache
def get_book_name_keyboard(book_name, testament_type='old', page: int = 1):
    ''' Клавиатура меню "С выбором глав" Telegram-бота «Доброе Слово». ''' 
    builder = InlineKeyboardBuilder()
    try:
        with open('bot/cache/bible.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        chapters = list(data[book_name].keys())
    except (FileNotFoundError, KeyError):
        # Обработка случая, когда файл не найден
        builder.button(text='🔙 Главное меню', callback_data='back_to_main')
        return builder.as_markup()
    
    total_chapters = len(chapters)
    total_pages = (total_chapters + MAX_BUTTONS_PER_PAGE - 1) // MAX_BUTTONS_PER_PAGE
    start = (page - 1) * MAX_BUTTONS_PER_PAGE
    end = start + MAX_BUTTONS_PER_PAGE
    page_chapters = chapters[start:end]
     
    for chapter in page_chapters:
        builder.button(text=f'{chapter}', callback_data=f'chapter_{book_name}_{chapter}')
    
    nav_row = []
    if page > 1:
        nav_row.append({"text": "⬅️ Назад", "data": f"chapters_page_{book_name}_{page - 1}"})
    if page < total_pages:
        nav_row.append({"text": "➡️ Далее", "data": f"chapters_page_{book_name}_{page + 1}"})
        
    for btn in nav_row:
        builder.button(text=btn["text"], callback_data=btn["data"])
    
    
    testament_text = "↩️ Ветхий Завет" if testament_type == 'old' else "↩️ Новый Завет"
    builder.button(text=testament_text, callback_data=f'chapter_page_{testament_type}')
    builder.button(text='🕊️ Выбор "Завета"', callback_data='chapter_help')
    builder.button(text='🔍 Поиск по Библии', callback_data='bible_search')
    builder.adjust(3) 
    return builder.as_markup()


@lru_cache
def get_chapter_selection(book_name, current_chapter, total_chapters):
    ''' Клавиатура меню "Просмотром глав" Telegram-бота «Доброе Слово». ''' 
    builder = InlineKeyboardBuilder()
    
    # Кнопки навигации по главам
    if current_chapter > 1:
        builder.button(text='⬅️ Предыдущая', callback_data=f'chapter_{book_name}_{current_chapter - 1}')
    if current_chapter < total_chapters:
        builder.button(text='Следующая ➡️', callback_data=f'chapter_{book_name}_{current_chapter + 1}')
    
    # Основные навигационные кнопки
    builder.button(text='⬅️ К главам', callback_data=f'book_name_back_{book_name}')
    builder.button(text='🕊️ Выбор "Завета"', callback_data='chapter_help')
    builder.button(text='🔍 Поиск по Библии', callback_data='bible_search')
    
       # Расположение кнопок
    if current_chapter > 1 and current_chapter < total_chapters:
        # Есть обе кнопки навигации
        builder.adjust(2, 2, 1)
    elif current_chapter > 1 or current_chapter < total_chapters:
        # Есть только одна кнопка навигации
        builder.adjust(1, 2, 1)
    else:
        # Нет кнопок навигации (только одна глава)
        builder.adjust(2, 1)
    
    return builder.as_markup()

@lru_cache
def get_bible_search():
    ''' Клавиатура меню "Поиск по Библии" Telegram-бота «Доброе Слово». ''' 
    builder = InlineKeyboardBuilder()
    builder.button(text='📖 Библия', callback_data='chapter_help')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(1)
    return builder.as_markup()

@lru_cache
def get_bible_search_word():
    ''' Клавиатура меню "Поиск по Библии введеного слова" Telegram-бота «Доброе Слово». ''' 
    builder = InlineKeyboardBuilder()
    builder.button(text='🔍 Новый поиск', callback_data='bible_search')
    builder.button(text='📖 Библия', callback_data='chapter_help')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(1)
    return builder.as_markup()