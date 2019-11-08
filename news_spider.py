import requests
from bs4 import BeautifulSoup as bs
import json
import lxml

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
base_url = 'https://pasmi.ru/cat/news/page/1/'


def news_parser(base_url, headers):

    news = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')

        try:
            pagination = soup.find_all('a', attrs={'class' : 'page-numbers'})
            count = 3  # Just for illustration purpose to read only 2 pages
            # count = int(pagination[-2])+1 #this will get total number of pages from the web site
            for i in range(1, count):
                url = f'https://pasmi.ru/cat/news/page/{i}/'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        articles = soup.find_all('article')
        for article in articles:
            try:
                date = article.find('span', attrs={'class': "time"}).text
                title = article.find('a', attrs={'class': 'entry-title'}).text
                link = article.find('a')['href']
                img = img_parser(link, headers)
                paragraph = paragraph_parser(link, headers)

                news.append({
                    "date": date,
                    "title": title,
                    "link": link,
                    "image": img,
                    "content": str(paragraph),
                })
                print("[*]News Parsing: ", len(news))
            except:
                pass

        with open('data.json', 'w') as f:
            json.dump(news, f,  indent=2)

# This Function will get image for each article
def img_parser(article_url, headers):
    session = requests.Session()
    request = session.get(article_url, headers=headers)
    soup = bs(request.content, 'lxml')
    img = soup.find('img')['src']
    return img

# This Function will get only the first <p> tag for each article
def paragraph_parser(article_url, headers):
    session = requests.Session()
    request = session.get(article_url, headers=headers)
    soup = bs(request.content, 'lxml')
    paragraph = soup.find('p')
    return paragraph


news_parser(base_url, headers)


