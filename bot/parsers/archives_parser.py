import requests
from bs4 import BeautifulSoup
from bot.utils.cache import cache_json
from bot.parsers.products_parser import get_random_headers

URL = "https://dobslovo.ru/arhivy-gazety/"

@cache_json(ttl=86400)
async def parse_archives_page():
    """Парсит страницу архивов газет «Доброе Слово»."""
    headers = get_random_headers()

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Ошибка при запросе страницы: {e}")
        return {"newspapers": []}

    soup = BeautifulSoup(response.text, "lxml")
    
    # Собираем все уникальные PDF
    pdf_urls = set()
    pdf_data = {}
    
    # Находим все PDF ссылки
    for link in soup.find_all('a', href=lambda h: h and h.endswith('.pdf') and 'Номер' in h):
        pdf_url = link['href']
        if pdf_url.startswith('//'):
            pdf_url = 'https:' + pdf_url
            
        if pdf_url in pdf_urls:
            continue
            
        pdf_urls.add(pdf_url)
        
        # Извлекаем информацию из URL
        filename = pdf_url.split("/")[-1].replace(".pdf", "")
        parts = filename.split("-")
        
        if len(parts) >= 3:
            year = parts[1]
            issue = parts[2]
            name = parts[-1]
            title = f"Газета {year}-{issue}-{name}"
            
            pdf_data[pdf_url] = {
                'title': title,
                'year': year,
                'issue': issue,
                'name': name
            }

    # Теперь ищем изображения для каждого PDF
    newspapers = []
    all_images = soup.find_all('img', src=lambda s: s and 'Номер' in s)
    
    for pdf_url, data in pdf_data.items():
        img_url = None
        year = data['year']
        issue = data['issue']
        
        # Ищем соответствующее изображение
        for img in all_images:
            src = img.get('src', '')
            if year in src and issue in src:
                img_url = src
                break
        
        newspapers.append({
            "title": data['title'],
            "year": data['year'],
            "issue": data['issue'],
            "pdf_url": pdf_url,
            "img_url": img_url
        })

    return {"newspapers": newspapers}