from lxml import html
from setup_db import KVStorage
import urllib.request

base_url = "https://www.apkmirror.com"
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) \
    AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}


def get_data(url):
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req)
    xml = data.read()
    return xml


def save_to_db(latest_version):
    try:
        kvs = KVStorage.select().where(KVStorage.key == "apkmirror").get()
    except KVStorage.DoesNotExist:
        kvs = KVStorage(key="apkmirror", value="0")

    kvs.value = latest_version
    kvs.save()


def get_latest_version():
    try:
        kvs = KVStorage.select().where(KVStorage.key == "apkmirror").get()
    except KVStorage.DoesNotExist:
        return 0
    return kvs.value


def html_parse():
    url = base_url + '/apk/niantic-inc/pokemon-go/'
    xml = get_data(url)

    root = html.fromstring(xml)
    apk = root.xpath('//div/h5/a[@href]')[0]

    latest_version_str = apk.text.replace('Pokémon GO', '').replace(' ', '')
    latest_version = int(latest_version_str.replace('.', ''))

    saved_lv = int(get_latest_version())
    save_to_db(latest_version)

    if saved_lv < latest_version:
        return f"Latest version is {latest_version_str}.\n\n {base_url + apk.attrib['href']}"
    return ""


if __name__ == "__main__":
    print(html_parse())
