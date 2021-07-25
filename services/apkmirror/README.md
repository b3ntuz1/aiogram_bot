# Парсер apkmirror

Парсить web-сторінку з apkmirror та знаходить apk файли.
Щоб почати роботу потрібно створити обʼєкт типу ApkMirror, а параметром передати
частину URL після apk/ і до останнього слеша, наприклад,
якщо маємо "www.apkmirror.com/apk/niantic-inc/pokemon-go/", то передати треба
"niantic-inc/pokemon-go". Без слешів на початку та вкінці.

Приклад викорстання. Щоб отримати номер останьої версії Pokemon GO:

```
from services.apkmirror import ApkMirror

apk = ApkMirror("niantic-inc/pokemon-go")
apk.parse()
print(f"Latest version is: {apk.version()}")
```


## API

**parse() -> bool** -- запустити першою. парсить сторінку та створює атрибут класу tree

**link() -> str** -- посилання на сторінку де можна завантажити apk

**version() -> str** -- остання версія apk. Потребує атрибут tree.

**whats_new() -> str** -- текст опис із секції What's New на сторінці проекту. Потребує атрибут tree.

**description() -> str** -- текст опис apk із сторінки проекту. Потребує атрибут tree.
