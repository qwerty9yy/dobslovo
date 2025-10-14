import os
import json
import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from bot.parsers.products_parser import get_random_headers
from bot.utils.cache import cache_json

URL = 'https://dobslovo.ru/'
# CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache_number_newspapers.json")
# CACHE_TTL = 24 * 60 * 60 # 24 часа

@cache_json(ttl=86400)
async def parse_number_newspapers():
    # Парсит количство газет отпечатано с 2002 года 
    # Проверяем кеш
    # if os.path.exists(CACHE_FILE):
    #     with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    #         cached = json.load(f)
    #     if time.time() - cached['timestamp'] < CACHE_TTL:
    #         return cached['data']       
    # # Если кеш устарел — делаем новый запрос
    
    headers = get_random_headers() # UserAgent c файла products_parser
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Ошибка при запросе: {e}")
        return {"count_newspapers": "Ошибка загрузки"}
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Парсим количество напечатаных газет
    count_block = soup.find('span', class_='elementor-counter-number')
    count_block = count_block.get('data-to-value')
    
    return {
        'count_newspapers': count_block,
    }
    
    # # Сохраняем кеш
    # with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    #     json.dump({'timestamp': time.time(), 'data': data}, f, ensure_ascii=False, indent=2)
        
    # return data
    