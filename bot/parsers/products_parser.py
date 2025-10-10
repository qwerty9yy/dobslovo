import os 
import json
import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

URL = 'https://dobslovo.ru/kupit-gazetu/'
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache_products.json")
CACHE_TTL = 24 * 60 * 60 # 24 часа

def get_random_headers():
    """Возвращает заголовки с случайным User-Agent"""
    ua = UserAgent()
    return {
        "User-Agent": ua.random,
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    }


def parse_products_page():
    """
    Парсит страницу 'Купить газету' с кешированием на 24 часа.
    Использует случайный User-Agent для маскировки под браузер.
    """
    
    # Проверяем кеш
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        if time.time() - cached['timestamp'] < CACHE_TTL:
            return cached['data']
    
    # Если кеш устарел — делаем новый запрос
    headers = get_random_headers()
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Парсим OZON ссылку
    ozon_link_tag = soup.find('a', href=lambda h: h and 'ozon.ru' in h)
    ozon_link = ozon_link_tag['href'] if ozon_link_tag else None
    
    # Парсим цену
    price_block = soup.find('p', string=lambda s: s and 'Цена газеты' in s)
    price_text = price_block.get_text(strip=True) if price_block else "Цена не найдена"
    
    # Парсим Цены с пересылкой по России
    faq_blocks = soup.find_all('li', class_='elementor-price-list-item')
    faq = []
    for block in faq_blocks:
        count_copy = block.find('span', class_='elementor-price-list-title').text.strip()
        price_count_copy = block.find('span', class_='elementor-price-list-price').text.strip()
        faq.append((count_copy, price_count_copy))
    
    
    
    
    data = {
        'ozon_link': ozon_link,
        'price': price_text,
        'price_delivery': faq,
    }
    
    # Сохраняем кеш
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'timestamp': time.time(), 'data': data}, f, ensure_ascii=False, indent=2)
        
    return data
    