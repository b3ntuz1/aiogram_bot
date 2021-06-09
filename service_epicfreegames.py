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
    data = html.fromstring(get_data(url).text)
    return data.cssselect('div.css-pfxkyb')[0].text


def get_games(msg) -> str:
    result = ""
    for item in msg:
        if(item['productSlug'] == '[]'): continue
        url = "https://www.epicgames.com/store/en-US/p/" + item['productSlug']

        result += "**" + item['title'] + "**\n"
        result += get_game_descr(url) + "\n"
        result += url + "\n\n"

    return result[:-2]


def main():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=UA&allowCountries=UA"
    data = get_data(url).json()['data']['Catalog']['searchStore']['elements']
    games = get_games(data)
    return games
 
