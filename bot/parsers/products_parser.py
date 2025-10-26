import os 
import json
import time
from bs4 import BeautifulSoup
import requests
from bot.utils.logger import logger
from fake_useragent import UserAgent
from bot.utils.cache import cache_json

URL = 'https://dobslovo.ru/kupit-gazetu/'
# CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache_products.json")
# CACHE_TTL = 24 * 60 * 60 # 24 часа

def get_random_headers():
    """Возвращает заголовки с случайным User-Agent"""
    ua = UserAgent()
    return {'User-Agent': ua.random}

@cache_json(ttl=86400)
async def parse_products_page():
    """
    Парсит страницу 'Купить газету' с кешированием на 24 часа.
    Использует случайный User-Agent для маскировки под браузер.
    """
    
    # # Проверяем кеш
    # if os.path.exists(CACHE_FILE):
    #     with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    #         cached = json.load(f)
    #     if time.time() - cached['timestamp'] < CACHE_TTL:
    #         return cached['data']
    # Если кеш устарел — делаем новый запрос
    
    headers = get_random_headers()
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"⚠️ Ошибка при запросе: {e}", exc_info=True)
        return {"price": "Ошибка загрузки"}
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Парсим OZON ссылку
    # ozon_link_tag = soup.find('a', href=lambda h: h and 'ozon.ru' in h)
    # ozon_link = ozon_link_tag['href'] if ozon_link_tag else None
    
    # Парсим цену
    price_block = soup.find('p', string=lambda s: s and 'Цена газеты' in s)
    price_text = price_block.get_text(strip=True) if price_block else "Цена не найдена"
    
    # Парсим Цены с пересылкой по России
    price_blocks = soup.find_all('li', class_='elementor-price-list-item')
    price_delivery = []
    for block in price_blocks:
        title_tag = block.find('span', class_='elementor-price-list-title')
        price_tag = block.find('span', class_='elementor-price-list-price')
        if not (title_tag and price_tag):
            continue
        count_copy = title_tag.text.strip()
        price_count_copy = price_tag.text.strip()
        price_delivery.append((count_copy, price_count_copy))
        
    # Парсим Популярные вопросы и ответы 
    blog_items = soup.find_all('div', class_='elementor-toggle-item')
    popular_questions = []
    for blog in blog_items:
        title_tag = blog.find('a', class_='elementor-toggle-title')
        content_tag = blog.find('div', class_='elementor-tab-content')
        if not (title_tag and content_tag):
            continue
        question = title_tag.get_text(strip=True)
        answer = content_tag.get_text(strip=True)
        popular_questions.append((question, answer))
    
    
    return {
        # 'ozon_link': ozon_link,
        'price': price_text,
        'price_delivery': price_delivery,
        'popular_questions': popular_questions,
    }
    
    # # Сохраняем кеш
    # with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    #     json.dump({'timestamp': time.time(), 'data': data}, f, ensure_ascii=False, indent=2)
        
    # return data
    