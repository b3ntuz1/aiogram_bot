import requests
import datetime
from lxml import html

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}


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
                    result.append(f"**{item['title']}**")
                    url = self._get_url(item)
                    print(f"[get_games] {url}")
                    result.append(url)
                    result.append(f"{self._get_description(url)}\n")

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

    def _get_url(self, item):
        base = "https://www.epicgames.com/store/en-US/p/"
        url_slug = base + item['urlSlug']
        product_slug = base + item['productSlug']
        print(url_slug, product_slug)

        if url_slug == product_slug:
            return url_slug

        for i in (item['urlSlug'], item['productSlug']):
            result = self._probe(base + i, i)
            if result:
                return result

    def _probe(self, url, name):
        resp = requests.get(url, headers=headers)
        data = html.fromstring(resp.text)

        for probe_url in data.findall('head')[0].findall("link"):
            print(probe_url.attrib.get('href'))
            page = probe_url.attrib.get('href')
            if "not-found" in page:
                return ''
            if name in page:
                return page


if __name__ == "__main__":
    efg = EFG()
    print(efg.get_games())
