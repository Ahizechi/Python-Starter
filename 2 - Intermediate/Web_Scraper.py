from bs4 import BeautifulSoup
import requests
import pandas as pd

def web_scraper(url, element, class_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all(element, class_=class_name)

    extracted_data = []
    for item in items:
        text = item.get_text()
        link = item.find('a', href=True)
        link_url = link['href'] if link else 'No link'
        extracted_data.append({'text': text.strip(), 'link': link_url})

    return pd.DataFrame(extracted_data)

# Example usage
# df = web_scraper('https://example.com', 'div', 'some-class-name')
# print(df)
