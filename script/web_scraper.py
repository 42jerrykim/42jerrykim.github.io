import requests
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import urljoin
import html2text

def get_readable_content(url):
    print(f"[INFO] Fetching content from URL: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    response.encoding = response.apparent_encoding
    doc = Document(response.text)
    readable_html = doc.summary()
    title = doc.title()

    soup = BeautifulSoup(readable_html, 'html.parser')
    for tag in soup(['style', 'script']):
        tag.decompose()

    for img in soup.find_all('img'):
        if img.has_attr('src'):
            img['src'] = urljoin(url, img['src'])

    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown = h.handle(soup.prettify())

    print(f"[INFO] Finished processing content from URL: {url}")
    return title, markdown

def get_web_content(url):
    print(f"[INFO] Getting web content from URL: {url}")
    title, content = get_readable_content(url)
    print(f"[INFO] Completed getting web content from URL: {url}")
    return content
