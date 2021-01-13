from lxml import etree, html
from os.path import exists
import urllib.request

base_url = "https://www.apkmirror.com"
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) \
    AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}


def get_data(url):
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req)
    xml = data.read()
    return xml


def rss_parse():
    url = base_url + '/feed/'
    xml = get_data(url)
    root = etree.fromstring(xml)
    root.getroottree()
    for r in root.xpath('channel/item'):
        if("Pokémon GO" in r.xpath('title')[0].text):
            return r.xpath('link')[0].text
    return "On RSS channel update not found"


def html_parse():
    url = base_url + '/apk/niantic-inc/pokemon-go/'
    xml = get_data(url)

    root = html.fromstring(xml)
    latest_version = root.xpath('//div/h5/a[@href]')[0]
    text = latest_version.text.replace('Pokémon GO', '').replace(' ', '')
    return text
