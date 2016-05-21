# -*- coding: utf-8 -*-
import re
#import json
import requests
from bs4 import BeautifulSoup
import time

URL = "http://www.bbc.com/culture"
DIRPATH = "articles"
PAGE_COUNTER = 31
# 1 страница - 4 месяца
# 3 страницы - 1 год
# 30 страниц - 10 лет
# приблизительно

def get_links():  # ф-ия получает ссылки со всех страниц
    # status_code = 200
    i = 1
    links = []
    # while status_code == 200 and i < PAGE_COUNTER:  # 200 - всё удачно, 404 - ошибка
    while i < PAGE_COUNTER:  # 200 - всё удачно, 404 - ошибка
        url = "{}/{}={}".format(URL, "data/search/story-by-section/wwculture/music?page", i)
        r = requests.get(url) # get запрос по ссылке url    (ответ от сервера)
        status_code = r.status_code
        print(i, url, "[{}]".format(status_code))
        i += 1
        if status_code == 404:
            continue
        links += get_links_from_page(r.json()) 
        # поставить паузу в 1 секунду
    return links

def get_links_from_page(jsn):  # ф-ия получает ссылки с одной страницы
    urls = []
    for new in jsn['results']:
        urls.append("{}/{}".format(URL, new['Metadata']['Id'][10:]))
    return urls

def get_text(url):  # ф-ия получает текст статьи
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    body_content = soup.find(class_="body-content")
    text = "\n".join(map(lambda x: x.text.strip(), body_content.find_all('p')))
    filename = r.url[r.url.rfind('/')+1:] # последняя часть в ссылке (slug) (примерное название статьи) 
    print(filename)
    with open("{}/{}".format(DIRPATH, filename), 'w') as f:
        f.write(text)
    # поставить паузу в одну секунду

links = get_links()
with open('links.txt', 'w') as f:  # f = open('links.txt', 'w')
    f.write("\n".join(links))

for url in links:
    get_text(url)
    time.sleep(1)
