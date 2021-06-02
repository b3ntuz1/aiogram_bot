import requests
from datetime import datetime
from lxml import html
from setup_db import KVStorage


def get_data(url):
    try:
        data = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return 0
    return data.content


def parse(data, tags):
    result = []
    data = html.fromstring(data)
    for node in data.xpath("//item"):
        result_dict = {}
        for i in node.getchildren():
            if(i.tag.lower() in tags):
                txt = i.text if i.text != None else i.tail
                result_dict[i.tag] = txt
        result.append(result_dict)
    return result


def post(data):
    result = data["title"]
    result += f"\n{data['pubdate']}"
    # result += f"   (timestamp is: {totimestamp(data['pubdate'])})"
    result += f"\n{data['link']}\n"
    return result


def totimestamp(date:str) -> int:
    """ Get string like 'Fri, 05 Feb 2021 22:52:00 -0800' and
    Return timestamp:int
    """
    months = {
        "Dec": "12", "Jan": "01", "Feb": "02",
        "Mar": "03", "Apr": "04", "May": "05",
        "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11"
    }
    date = date.split(" ")[1:]
    month = months[date[1].capitalize()]
    result = datetime.fromisoformat(f"{date[2]}-{month}-{date[0]}T{date[3]}").timestamp()

    # поправка часу на грінвіч
    if date[4] in "GMT":
        return int(result)

    if date[4][0] == '-':
        result += int(date[4][1:3]) * 3600 + int(date[4][3:] * 60)
    else:
        result -= int(date[4][1:3]) * 3600 + int(date[4][3:] * 60)

    return int(result)


def main():
    try:
        kvs = KVStorage.select().where(KVStorage.key=="rss").get()
    except KVStorage.DoesNotExist:
        kvs = KVStorage(key="rss", value="0")

    tags = ["title", "link", "pubdate"]

    rss_chanels = [
        "https://pokemongohub.net/feed/",
    ]
    
#     rss_chanels = [
#         "https://ru.ign.com/articles/rss",
#         "https://www.gamespot.com/feeds/news",
#         "https://hackernoon.com/feed",
#         "https://www.eurogamer.net/?format=rss",
#         ]

    result = ""
    now = datetime.utcnow()

    for url in rss_chanels:
        data = get_data(url)
        data = parse(data, tags)
        for d in data:
            if (int(kvs.value) <= totimestamp(d['pubdate'])):
                result += post(d) + '\n'
    
    # save check time to db
    kvs.value = int(now.timestamp())
    kvs.save()

    return result

if __name__ == "__main__":
    # save result ot txt file
    now = str(datetime.utcnow().isoformat()).replace(' ', '_')
    result = main()
    if (len(result) > 0):
        with open(f'{now}.txt', 'w') as fh:
            fh.write(result)
