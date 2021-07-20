import requests
import datetime
from lxml import html


class EFG():
    def __init__(self):
        self.data = requests.get(
            "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
        ).json()

    def get_games(self) -> list:
        """ Return text with free games available now on epicgamesstore and next
        update """
        # Так як у python немає мутабельних stringʼів, а метод зберає результат
        # із шматочків, то вирішив юзати список рядків. Тим більше що "\n".join()
        # працює швидко та ефективно.
        result = [f"Update time is: {self.next_update().ctime()}", "\n"]

        for item in self.data["data"]["Catalog"]["searchStore"]["elements"]:
            # if originalPrice == discount game is available for free
            tmp = item['price']['totalPrice']
            if tmp['originalPrice'] == tmp['discount']:
                if tmp['originalPrice'] != 0:
                    result.append(f"** {item['title']} **")
                    url = f"https://www.epicgames.com/store/en-US/p/{item['urlSlug']}"
                    result.append(url)
                    result.append(f"{self._get_description(url)}")

        return "\n".join(result)

    def next_update(self) -> datetime:
        """ Return datetime object which represent next update on epicgamesstore """
        for item in self.data["data"]["Catalog"]["searchStore"]["elements"]:
            # if originalPrice == discount game is available for free
            tmp = item['price']['totalPrice']
            if tmp['originalPrice'] == tmp['discount']:
                if tmp['originalPrice'] != 0:
                    nu = item["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
                    nu = nu.split('.')[:-1][0]
                    return datetime.datetime.fromisoformat(nu)

    def _get_description(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("ERROR")
            print(e)

        data = html.fromstring(resp.text).cssselect('div.css-pfxkyb')
        if data:
            return data[0].text
        return "Description not found. Please check manualy."
