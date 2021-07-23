# парсер apkmirror

Парсить web-сторінку з apkmirror та знаходить apk файли.
Щоб почати роботу потрібно створити обʼєкт типу ApkMirror, а параметром передати
рядок "назва_компанії/назва_програми". Наприклад, щоб отримати номер останьої
версії Pokemon GO:

```
from services.apkmirror import ApkMirror

apk = ApkMirror("niantic-inc/pokemon-go")
apk.parse()
print(f"Latest version is: {apk.version()}")
```


## API

** parse() -> bool ** -- запустити першою

** link() -> str ** -- посилання на сторінку де можна завантажити apk

** version() -> str ** -- остання версія apk

** whats_new() -> str ** -- текст опис із секції What's New на сторінці проекту

** description() -> str ** -- текст опис apk із сторінки проекту
