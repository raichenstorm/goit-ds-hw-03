import requests
from bs4 import BeautifulSoup
import json

def get_page_text(url):
    html_doc = requests.get(url)
    return html_doc.text

def scrape_quotes(url):
    html = get_page_text(url)
    soup = BeautifulSoup(html, 'html.parser')
    quotes = []
    for quote in soup.select('.quote'):
        text = quote.select_one('.text').get_text()
        author = quote.select_one('author').get_text()
        tags = [tag.get_text() for tag in quote.select('.tag')]
        quotes.append({
            'quote': text,
            'author': author,
            'tags': tags
        })
    return quotes

def scrape_authors(url):
    html = get_page_text(url)
    soup = BeautifulSoup(html, 'html.parser')
    authors = []
    for author in soup.select('.author'):
        name = author.get_text()
        born_date = author.find_next_sibling(class_='author-born-date').get_text()
        born_location = author.find_next_sibling(class_='author-born-location').get_text()
        description = author.find_next_sibling(class_='author-description').get_text()
        authors.append({
            'fullname': name,
            'born_date': born_date,
            'born_location': born_location,
            'description': description.strip()
        })
    return authors



def main():
    url = 'https://quotes.toscrape.com/'
    quotes_url = f'{url}/page/1'
    authors_url = f'{url}/author'

    all_quotes = []
    for page in range(1, 11):
        quotes_url = f'{url}/page/{page}'
        all_quotes.extend(scrape_quotes(quotes_url))

        with open('quotes.json', 'w') as f:
            json.dump(all_quotes, f, indent=2, ensure_ascii=False)
            return('Quotes data saved to json file')
        
    all_authors = []
    for quote in all_quotes:
        all_authors.append(quote['author'])
    unique_authors = set(all_authors)
    for author in unique_authors:
        author_url = f'{authors_url}{author}'
        all_authors.extend(scrape_authors(author_url))

    with open('authors.json', 'w') as f:
        json.dump(all_authors, f, indent=2, ensure_ascii=False)
    return('Authors data saved to json file')

if __name__ == "__main__":
    main()