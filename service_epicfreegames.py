import requests
import json
from lxml import html
from sys import exit

def get_data(url) -> dict:
    try:
        data = requests.get(url)
        data.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("ERROR")
        print(e)
        exit(0)
    return data


def get_game_descr(url) -> str:
    data = html.fromstring(get_data(url).text).cssselect('div.css-pfxkyb')
    if data:
        return data[0].text
    return f"Description not found. Please check manualy."

def purifyMarkdown(text):
    symbols = "()'*_.+-#{}[]\!"
    for s in symbols:
        if s in text:
            text = text.replace(s, f"\\{s}")
    return text

def get_games(msg) -> str:
    result = ""
    for item in msg:
        if(item['productSlug'] == '[]'): continue
        url = "https://www.epicgames.com/store/en-US/p/" + item['productSlug']

        result += "**" + item['title'] + "**\n"
        result += get_game_descr(url) + "\n"
        result += url + "\n\n"

    return result[:-2]

def main() -> str:
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=UA&allowCountries=UA"
    data = get_data(url).json()['data']['Catalog']['searchStore']['elements']
    games = get_games(data)
    return games


def service() -> str:
    from setup_db import KVStorage
    from hashlib import md5
    try:
        kvs = KVStorage.select().where(KVStorage.key=="epicgames").get()
    except KVStorage.DoesNotExist:
        kvs = KVStorage(key="epicgames", value="0")

    text = main()
    digest = md5(text.encode()).hexdigest()
    if(kvs.value != digest):
        kvs.value = digest
        kvs.save()
        return text
    return ""


if __name__ == "__main__":
    print(main())
