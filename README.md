# python-rucaptcha

[![Code Climate](https://codeclimate.com/github/AndreiDrang/python-rucaptcha/badges/gpa.svg)](https://codeclimate.com/github/AndreiDrang/python-rucaptcha)
[![PyPI version](https://badge.fury.io/py/python-rucaptcha.svg)](https://badge.fury.io/py/python-rucaptcha)

Python 3 library for RuCaptcha.

Библиотека предназначена для разрабаотчиков ПО и служит для облегчения работы с API сервиса RuCaptcha.

## How to install? Как установить?

### pip

```bash
pip install python-rucaptcha
```


### Source
```bash
git clone https://github.com/AndreiDrang/python-rucaptcha.git
cd python-rucaptcha
python setup.py install
```
***
По всем вопросам можете писать в [Telegram](https://t.me/joinchat/CD2EtQ5Pm0dmoSQQMTkVlw) чат.
***
### На данный момент реализованы следующие методы:

1.[Решение капчи-изображения(большие и маленькие).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ImageCaptcha.py)

Краткий пример:
```python
from python_rucaptcha import ImageCaptcha
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# Ссылка на изображения для расшифровки
captcha_link = ""
# Возвращается строка-расшифровка капчи
user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_link=captcha_link)
```

2.[Решение KeyCaptcha(пазл).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/KeyCaptcha.py) ***НЕ ПОДДЕРЖИВАЕТСЯ СЕРВИСОМ RuCaptcha***

3.[Решение аудиокапчи. Используется для SolveMedia капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/MediaCaptcha.py)

4.[Решение старой ReCaptcha v1.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV1.py)

5.[Решение новой ReCaptcha v2.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/ReCaptchaV2.py)

Краткий пример:
```python
from python_rucaptcha import ReCaptchaV2
# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ""
# Ссылка на страницу с капчёй
PAGE_URL = ""
# Возвращается строка-расшифровка капчи
answer = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(site_key=SITE_KEY, page_url=PAGE_URL)
```

6.[Решение RotateCaptcha(повернуть изображение).](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RotateCaptcha.py)

7.[Решение текстовой капчи.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/TextCaptcha.py)

8.[Модуль для получения инофрмации о балансе аккаунта и отправке жалоб.](https://github.com/AndreiDrang/python-rucaptcha/blob/master/python_rucaptcha/RuCaptchaControl.py)
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](http://85.255.8.26/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-rucaptcha/tree/master/CaptchaTester), которые демонстрируются на примере данного сайта
