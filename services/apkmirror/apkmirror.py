from urllib.request import urlopen, Request, HTTPError
from lxml import html


class ApkMirror:
    def __init__(self, project):
        self.url = "https://www.apkmirror.com"
        self.project = project
        self.tree = None

    def parse(self) -> bool:
        """ Парсить сторінку яку було передано під час створення обʼєкту. Повертає
        True в разі успішної роботи або False якщо щось пішло не так. Встановлює атрибут
        класу 'tree' з DOM деревом сторінки. """
        data = self._download(self.project)
        if data is None:
            return False
        self.tree = html.fromstring(data.read())
        return True

    def app_title(self) -> str:
        app_title = self.tree.cssselect('.app-title')[0].text
        return app_title

    def link(self) -> str:
        """ Поверне URL сторінки з якої можна буде завантажити апк """
        appname = self.project.split('/')[1]
        return f"{self.url}/apk/{self.project}/{appname}-{self.version().replace('.', '-')}-release"

    def version(self) -> str:
        """ Остання версія проекту """
        element = self.tree.cssselect('.infoslide-value')[0].text
        return element.replace(' ', '')

    def whats_new(self) -> str:
        """ Що нового в апдейті. Цей метод викликати тільки після self.parse() """
        return str(self.tree.cssselect('.notes')[2].text_content())

    def description(self) -> str:
        """ Опис проекту. Цей метод викликати тільки після self.parse() """
        return str(self.tree.cssselect('.notes')[1].text_content())

    def _download(self, path):
        """ Службовий метод для завантаження даних із apkmirror """
        url = self.url + '/apk/' + path
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
        }
        req = Request(url, headers=headers)
        # відловити помилки підключення до хосту вразі невдачі
        # інакше отримати Response
        try:
            data = urlopen(req)
            return data
        except HTTPError as e:
            print(f"Cant connect to {self.url}. Reason: {e.reason}\nCode: {e.code}")
            return None
