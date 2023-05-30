import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_article(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title_element = soup.find('h1', class_='entry-title')
    author_element = soup.find('div', class_='td-post-author-name')
    date_element = soup.find('time', class_='entry-date')
    image_element = soup.find('img', class_='entry-thumb')
    video_element = soup.find('div', class_='youtube-embed')
    content_div = soup.find('div', class_='td-post-content')
    content_paragraphs = content_div.find_all('p') if content_div else []

    data = {}

    if title_element:
        data['Title'] = title_element.text.strip()

    if author_element and author_element.find('a'):
        data['Author'] = author_element.find('a').text.strip()

    if date_element:
        data['Date'] = date_element.text.strip()

    if image_element:
        data['Image URL'] = image_element['src']

    if content_paragraphs:
        content = '\n'.join([p.text.strip() for p in content_paragraphs])
        data['Content'] = content

    if video_element:
        video_id = video_element['data-video_id']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        data['Video URL'] = video_url

    categories = soup.find('ul', class_='td-category').find_all('a')
    category_names = [category.text.strip() for category in categories]
    data['Category'] = category_names

    return data
