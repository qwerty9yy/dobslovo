import requests
from bs4 import BeautifulSoup

# 2. Проверяем статус ответа
url = 'https://dobslovo.ru/arhivy-gazety/'
response = requests.get(url)

# 2. Проверяем статус ответа
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    test = soup.find_all('div', class_='elementor-icon-wrapper')
    for blog in test:
        link = blog.find('a', class_='elementor-icon')
        if link:
            href = link.get('href')
            if href:
                # Добавляем https если ссылка начинается с //
                if href.startswith('//'):
                    href = 'https:' + href
                # Проверяем что это PDF файл
                if href.endswith('pdf'):
                    filepapers = href.split('/')[-1].replace('.pdf', '')
                    num_papers = filepapers.split('-')
                    # Проверяем что массив имеет достаточно элементов
                    if len(num_papers) >= 3:
                        years = num_papers[1]
                        count = num_papers[-2]
                        text = f"{href}\n{filepapers}\n{years}-{count}\n-------------"
                        print(text)
        img_tag = blog.find_previous("img")
        img_url = img_tag["src"] if img_tag else None
        print('image: ' + img_url)
        
    
    # test = soup.find('span', class_='elementor-counter-number')
    # test = test.get('data-to-value')
    # print(test)
    
    # blog_items = soup.find_all('div', class_='elementor-toggle-item')
    # # print(blog_items)
    # for blog in blog_items:
    #     name = blog.find('a', class_='elementor-toggle-title').text.strip()
    #     text = blog.find('div', class_='elementor-tab-content').text.strip()
    #     print(name, '----', text)