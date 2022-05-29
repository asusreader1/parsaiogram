import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_first_mews():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
    }

    url = "https://www.ukrinform.ua/block-lastnews"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('article')

    news_dict = {}
    for artic in articles_cards:
        article_title = artic.find("h2").text.strip()
        article_descr = artic.findAllNext('p')
        description = article_descr[1]
        description = str(description)[3:][:-4]
        article_href = artic.find('a')
        article_url = f'https://www.ukrinform.ua{article_href.get("href")}'
        article_id = artic.get("data-id")

        article_date = artic.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(article_date)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
        article_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

        # print((description))

        # print(f'{article_title}  \n {article_descr[1]}  \n {article_url}  \n {article_timestamp} | {article_id}')

        news_dict[article_id] = {
            "article_timestamp": article_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "description": description
        }

    with open("news_dict.json", 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
        }

        url = "https://www.ukrinform.ua/block-lastnews"
        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        articles_cards = soup.find_all('article')

        fresh_news = {}
        for article in articles_cards:
            article_href = article.find('a')
            article_url = f'https://www.ukrinform.ua{article_href.get("href")}'
            article_id = article.get("data-id")

            if article_id in news_dict:
                continue
            else:
                article_title = article.find("h2").text.strip()
                article_descr = article.findAllNext('p')
                description = article_descr[1]
                description = str(description)[3:][:-4]

                article_date = article.find("time").get("datetime")
                date_from_iso = datetime.fromisoformat(article_date)
                date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
                article_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

                news_dict[article_id] = {
                    "article_timestamp": article_timestamp,
                    "article_title": article_title,
                    "article_url": article_url,
                    "description": description
                }

                fresh_news[article_id] = {
                    "article_timestamp": article_timestamp,
                    "article_title": article_title,
                    "article_url": article_url,
                    "description": description
                }

        with open("news_dict.json", 'w') as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)

        return fresh_news


def main():
    get_first_mews()
    check_news_update()
    print(f'{check_news_update()}')


if __name__ == '__main__':
    main()
