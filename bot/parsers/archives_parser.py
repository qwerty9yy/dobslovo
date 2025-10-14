import requests
from bs4 import BeautifulSoup
from bot.utils.cache import cache_json
from bot.parsers.products_parser import get_random_headers  # берём оттуда UA

URL = "https://dobslovo.ru/arhivy-gazety/"

@cache_json(ttl=86400)
async def parse_archives_page():
    """Парсит страницу архивов газет «Доброе Слово»."""
    headers = get_random_headers()

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Ошибка при запросе страницы: {e}")
        return {"newspapers": []}

    soup = BeautifulSoup(response.text, "lxml")
    newspapers = []

    containers = soup.find_all("div", class_="elementor-icon-wrapper")
    for block in containers:
        pdf_tag = block.find("a", href=lambda h: h and h.endswith(".pdf"))
        if not pdf_tag:
            continue

        pdf_url = pdf_tag["href"]
        if pdf_url.startswith("//"):
            pdf_url = "https:" + pdf_url

        filename = pdf_url.split("/")[-1].replace(".pdf", "")
        parts = filename.split("-")

        if len(parts) >= 3:
            year = parts[1]
            issue = parts[2]
            name = parts[-1]
            title = f"Газета {year}-{issue}-{name}"
        else:
            year, issue, title = "Неизвестно", "?", filename

        img_tag = block.find_previous("img")
        img_url = img_tag["src"] if img_tag else None

        newspapers.append({
            "title": title,
            "year": year,
            "issue": issue,
            "pdf_url": pdf_url,
            "img_url": img_url
        })

    return {"newspapers": newspapers}