# python3-anticaptcha

Python 3 library for AntiCaptcha.

Tested on UNIX based OS.

Библиотека предназначена для разрабаотчиков ПО и служит для облегчения работы с API сервиса AntiCaptcha.

## How to install? Как установить?

### pip

```bash
pip install python3-anticaptcha
```


### Source
```bash
git clone https://github.com/AndreiDrang/python3-anticaptcha.git
cd python3-anticaptcha
python setup.py install
```
***
По всем вопросам можете писать в [Telegram](https://t.me/joinchat/CD2EtQ5Pm0dmoSQQMTkVlw) чат.
***
### На данный момент реализованы следующие методы:

1.[Решение капчи-изображения.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcah_image_to_text_example.py)

Краткий пример:
```python
from python3_anticaptcha import ImageToTextTask
# Введите ключ от сервиса AntiCaptcha, из своего аккаунта
ANTICAPTCHA_KEY = ""
# Ссылка на изображения для расшифровки
image_link = "http://85.255.8.26/static/image/common_image_example/800070.png"
# Возвращается строка-расшифровка капчи
user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).captcha_handler(captcha_link=image_link)

print(user_answer)
```

2.[Решение новой ReCaptcha v2 с прокси.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_nocaptcha_example.py)


3.[Решение новой ReCaptcha v2 без прокси.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_nocaptcha_example.py)

Краткий пример:
```python
from python3_anticaptcha import NoCaptchaTaskProxyless
# Введите ключ от сервиса AntiCaptcha, из своего аккаунта
ANTICAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = '6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'
# Ссылка на страницу с капчёй
PAGE_URL = 'https://www.google.com/recaptcha/intro/android.html'
# Возвращается строка-расшифровка капчи
user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
                                                            .captcha_handler(websiteURL=PAGE_URL,
                                                                             websiteKey=SITE_KEY)

print(user_answer)
```

4.[Решение FunCaptchaTask.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_fun_example.py)

Краткий пример:
```python
from python3_anticaptcha import FunCaptchaTask
# Введите ключ от сервиса AntiCaptcha, из своего аккаунта
ANTICAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ''
# Ссылка на страницу с капчёй
PAGE_URL = ''
# Возвращается строка с ключём для отправки на проверку
user_answer = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                            proxyType="http",
                                            proxyAddress="8.8.8.8",
                                            proxyPort=8080)\
                                            .captcha_handler(websiteURL=PAGE_URL,
                                                             websitePublicKey=SITE_KEY)

print(user_answer)
```

5.[Модуль для получения инофрмации о балансе аккаунта и отправке жалоб.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_control_example.py)

Краткий пример:
```python
from python3_anticaptcha import AntiCaptchaControl
# Введите ключ от сервиса AntiCaptcha, из своего аккаунта
ANTICAPTCHA_KEY = ""
# Возвращается строка c балансом
user_answer = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).get_balance()

print(user_answer)
```
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](http://85.255.8.26/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.

Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python-rucaptcha/tree/master/CaptchaTester), которые демонстрируются на примере данного сайта