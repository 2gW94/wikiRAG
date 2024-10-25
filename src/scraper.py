import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from loguru import logger
from tqdm import tqdm
import time


class OSDevScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.session = requests.Session()

        logger.add(
            "logs/scraper.log",
            rotation="100 MB",
            level="INFO",
            format="{time} {level} {message}"
        )

    def get_page_content(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Получаем основной контент
        content = soup.find('div', {'id': 'content'})
        if not content:
            return None, []

        # Удаляем ненужные элементы
        for element in content.select('div.printfooter, div#catlinks, div#footer'):
            element.decompose()

        # Извлекаем текст и ссылки
        text = content.get_text(strip=True, separator=' ')
        links = [
            urljoin(self.base_url, a['href'])
            for a in content.find_all('a', href=True)
            if a['href'].startswith('/') and ':' not in a['href']
        ]

        return text, links

    def scrape(self, start_url, max_pages=100):
        documents = []
        urls_to_visit = [start_url]

        with tqdm(total=max_pages) as pbar:
            while urls_to_visit and len(self.visited_urls) < max_pages:
                url = urls_to_visit.pop(0)

                if url in self.visited_urls:
                    continue

                logger.info(f"Scraping: {url}")
                html = self.get_page_content(url)
                if not html:
                    continue

                text, new_links = self.parse_page(html)
                if text:
                    documents.append({
                        'content': text,
                        'metadata': {'source': url}
                    })

                self.visited_urls.add(url)
                urls_to_visit.extend([l for l in new_links if l not in self.visited_urls])
                pbar.update(1)

                time.sleep(1)  # Задержка между запросами

        logger.info(f"Scraping completed. Collected {len(documents)} documents")
        return documents