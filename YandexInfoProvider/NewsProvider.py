import requests
from bs4 import BeautifulSoup

newsUrl = "https://yandex.ru/news"


def getNews(amount):
    response = requests.get(url=newsUrl)
    soup = BeautifulSoup(str(response.text), 'lxml')
    news = []
    count = 0
    for news_block in soup.findAll("div", "mg-grid__row_gap_8"):
        link = news_block.a.attrs['href'].split("?")[:1]
        title = news_block.find("h2", "mg-card__title").text
        annotation = news_block.find("div", "mg-card__annotation").text

        element = {'title': title, 'annotation': annotation, 'link': link}
        if element not in news:
            news.append(element)
            count += 1

        if count == amount:
            break
    return news
