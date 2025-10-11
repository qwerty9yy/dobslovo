import requests
from bs4 import BeautifulSoup

# 2. Проверяем статус ответа
url = 'https://dobslovo.ru/kupit-gazetu/'
response = requests.get(url)

# 2. Проверяем статус ответа
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    blog_items = soup.find_all('div', class_='elementor-toggle-item')
    # print(blog_items)
    for blog in blog_items:
        name = blog.find('a', class_='elementor-toggle-title').text.strip()
        text = blog.find('div', class_='elementor-tab-content').text.strip()
        print(name, '----', text)