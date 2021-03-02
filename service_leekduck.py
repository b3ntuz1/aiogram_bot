from lxml import html
from setup_db import KVStorage
import urllib.request


headers = headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) \
    AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}
url = "https://leekduck.com"


def _get_root(category):
    category = '/' + category if category[0] != '/' else category
    category = category + '/' if category[-1] != '/' else category

    rq = urllib.request.Request(url + category, headers=headers)
    return html.fromstring(urllib.request.urlopen(rq).read())


def _get_image(category):
    root = _get_root(category)

    img = root.xpath("*//p[@id='graphic']/img")
    img = img[0].get('src')

    return(url + img.replace(" ", "%20").replace('../', '/'))


def _get_caption(category):
    result = ""
    root = _get_root(category)

    lis = root.xpath("*//article/div/div/div[2]/ul/li")
    for i in lis:
        if "Tier" in i.text_content():
            if len(result) > 6:
                result = result[:-2] + "\n"
            result += i.text_content() + "\n"
        else:
            p = i.xpath(".//*/p[@class='boss-name']")
            result += p[0].text_content() + ", " if len(p) != 0 else ""

    return result[:-2]


def _is_new(img, category):
    category = category.replace('/','')
    leekduck = "leekduck" + "_" + category
    try:
        kvs = KVStorage.select().where(KVStorage.key==leekduck).get()
    except KVStorage.DoesNotExist:
        kvs = KVStorage(key=leekduck, value="0")

    if kvs.value != img:
        kvs.value = img
        kvs.save()
        return True
    return False


def get_raid_bosses():
    img = _get_image('boss')
    return [img, _get_caption('boss'), _is_new(img, 'boss')]


def get_research():
    img = _get_image('research')
    return [img , _is_new(img, 'research')]


if __name__ == '__main__':
    print(get_raid_bosses())
    print(get_research())