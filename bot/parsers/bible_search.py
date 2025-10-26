import requests
from bot.utils.logger import logger
from bs4 import BeautifulSoup

from bot.parsers.products_parser import get_random_headers

async def parse_bible_search(search_word: str):
    """ Прасинг API для поиска по библии
        Возвращает список словарей с результатами и количество совпадений.
    """
    headers = get_random_headers()
    URL = f'https://justbible.ru/api/search?translation=rst&search={search_word}'
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"⚠️ Ошибка при запросе страницы для поиска по Библии: {e}", exc_info=True)
        return None
    
    try:
        data = response.json()
    except ValueError:
        logger.error("⚠️ Ошибка: неверный формат ответа API (не JSON).", exc_info=True)
        return None
    
    # Проверяем, что это словарь и содержит ключ "info"
    if not isinstance(data, dict) or 'info' not in data:
        logger.error("⚠️ Ошибка: структура данных неожиданна.", exc_info=True)
        return None
    
    # Берём данные о поиске
    info = data["info"]
    search_word = info.get("searched", "—")
    coincidences = info.get("count", 0)
    
    # Создаём список результатов
    bible_search = {
        "searched": search_word,
        "coincidences": coincidences,
        "results": []
    }
    
    for i in range(coincidences):
        key = str(i)
        if key not in data:
            continue
        item = data[key]
        text = item.get('text', 'Без текста')
        from_where = item.get('data', 'Неизвестно где')
        
        bible_search['results'].append({
            "from_where": from_where,
            "text": text
        })
        
    return bible_search
        
        
        
    