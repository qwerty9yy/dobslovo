import requests, json
from bs4 import BeautifulSoup

response = requests.get(f'https://justbible.ru/api/search?translation=rst&search=Начало')
data = response.json()
l = len(data) - 1
print(f'Нашло {l} Совпадений')
for i in range(l):
    count = data[f'{i}']
    d = count['data']
    text = count['text']
    print(d)
    print(text)
    print()
    

# with open('bot/cache/bible.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# data = data['Матфей']
# data = data['1']
# for i in range(1, len(data) + 1):
#     print(i, data[f'{i}'])
#     print()
# # Перебор только названий книг (глав)
# print("📚 Все книги Библии:")
# for book_name in data.keys():
#     print(f"• {book_name}")

# # Или с нумерацией
# print("\n📚 Все книги Библии (с нумерацией):")
# for i, book_name in enumerate(data.keys(), 1):
#     print(f"{i}. {book_name}")
    

# import requests
# import json
# from datetime import datetime

# def get_daily_verse():
#     """Получить случайную библейскую цитату"""
#     try:
#         response = requests.get('https://bible-api.com/?random=verse')
#         data = response.json()
#         return {
#             'text': data['text'],
#             'reference': data['reference'],
#             'version': data['translation_id']
#         }
#     except Exception as e:
#         print(f"Ошибка получения цитаты: {e}")
#         return None

# def print_verse(verse):
#     """Красиво вывести цитату"""
#     if verse:
#         print(f"\n📖 Библейская цитата на {datetime.now().strftime('%d.%m.%Y')}")
#         print("=" * 50)
#         print(f"{verse['text']}")
#         print(f"\n— {verse['reference']} ({verse['version']})")
#         print("=" * 50)

# # Использование
# if __name__ == "__main__":
#     verse = get_daily_verse()
#     print_verse(verse)

# import requests
# from bs4 import BeautifulSoup

# # 2. Проверяем статус ответа
# url = 'https://dobslovo.ru/arhivy-gazety/'
# response = requests.get(url)

# # 2. Проверяем статус ответа
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     test = soup.find_all('div', class_='elementor-icon-wrapper')
#     for blog in test:
#         link = blog.find('a', class_='elementor-icon')
#         if link:
#             href = link.get('href')
#             if href:
#                 # Добавляем https если ссылка начинается с //
#                 if href.startswith('//'):
#                     href = 'https:' + href
#                 # Проверяем что это PDF файл
#                 if href.endswith('pdf'):
#                     filepapers = href.split('/')[-1].replace('.pdf', '')
#                     num_papers = filepapers.split('-')
#                     # Проверяем что массив имеет достаточно элементов
#                     if len(num_papers) >= 3:
#                         years = num_papers[1]
#                         count = num_papers[-2]
#                         text = f"{href}\n{filepapers}\n{years}-{count}\n-------------"
#                         print(text)
#         img_tag = blog.find_previous("img")
#         img_url = img_tag["src"] if img_tag else None
#         print('image: ' + img_url)
        
    
    # test = soup.find('span', class_='elementor-counter-number')
    # test = test.get('data-to-value')
    # print(test)
    
    # blog_items = soup.find_all('div', class_='elementor-toggle-item')
    # # print(blog_items)
    # for blog in blog_items:
    #     name = blog.find('a', class_='elementor-toggle-title').text.strip()
    #     text = blog.find('div', class_='elementor-tab-content').text.strip()
    #     print(name, '----', text)