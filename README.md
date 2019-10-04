# python3-anticaptcha

[![PyPI version](https://badge.fury.io/py/python3-anticaptcha.svg)](https://badge.fury.io/py/python3-anticaptcha)
[![Build Status](https://semaphoreci.com/api/v1/andreidrang/python3-anticaptcha/branches/master/shields_badge.svg)](https://semaphoreci.com/andreidrang/python3-anticaptcha)
[![Code Climate](https://codeclimate.com/github/AndreiDrang/python3-anticaptcha/badges/gpa.svg)](https://codeclimate.com/github/AndreiDrang/python3-anticaptcha)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2daabf7ff7974f01b9348fe64483c7af)](https://app.codacy.com/app/drang.andray/python3-anticaptcha?utm_source=github.com&utm_medium=referral&utm_content=AndreiDrang/python3-anticaptcha&utm_campaign=Badge_Grade_Settings)
![Callback_Server_Status Run](https://img.shields.io/badge/Callback_Server_Status-Run-blue.svg)

Python 3.6 library for Anti-Captcha service.

[Application in AppCenter](https://anti-captcha.com/clients/tools/appcenter/app/867).

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

With any questions, please contact us in [Telegram](https://t.me/joinchat/CD2EtQ5Pm0dmoSQQMTkVlw).
***
Присутствуют [примеры работы с библиотекой](https://github.com/AndreiDrang/python3-anticaptcha/tree/master/anticaptcha_examples).

Full examples you can find [here](https://github.com/AndreiDrang/python3-anticaptcha/tree/master/anticaptcha_examples).

***
### At the moment the following methods are implemented:
### На данный момент реализованы следующие методы:

0.[Manual result handler.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/custom_result_handler_example.py)

 
```python
from python3_anticaptcha import CustomResultHandler
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# Task ID to get result
TASK_ID = 123456
# This module is used to obtain the result of solving the task in "manual" mode
custom_result = CustomResultHandler.CustomResultHandler(
    anticaptcha_key=ANTICAPTCHA_KEY
)

user_answer = custom_result.task_handler(task_id=TASK_ID)
print(user_answer)
```
1.[Image to text captcha.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcah_image_to_text_example.py)

 
```python
from python3_anticaptcha import ImageToTextTask
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# Ссылка на изображения для расшифровки. Link to captcha image.
image_link = "http://85.255.8.26/static/image/common_image_example/800070.png"
# Возвращается строка-расшифровка капчи. Get string for solve captcha, and some other info.
user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).\
                captcha_handler(captcha_link=image_link)

print(user_answer)
```

2.[ReCaptcha v2.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_nocaptcha_example.py)


3.[ReCaptcha v2 Proxyless. ](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_nocaptcha_example.py) + [Selenium example](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/selenium_recaptcha_v2.py)

```python
from python3_anticaptcha import NoCaptchaTaskProxyless
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта. Website google key.
SITE_KEY = '6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'
# Ссылка на страницу с капчёй. Page url.
PAGE_URL = 'https://www.google.com/recaptcha/intro/android.html'
# Возвращается строка-расшифровка капчи. Get string for solve captcha, and other info.
user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
                .captcha_handler(websiteURL=PAGE_URL,
                                 websiteKey=SITE_KEY)

print(user_answer)
```

3.[ReCaptcha v3 Proxyless. ](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_nocaptcha_example.py)

```python
from python3_anticaptcha import ReCaptchaV3TaskProxyless
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта. Website google key.
SITE_KEY = '6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'
# Ссылка на страницу с капчёй. Page url.
PAGE_URL = 'https://some_link'
# Фильтр, по которому отбирается работник с нужным минимальным score.
# возможные варианты - 0.3, 0.5, 0.7
MIN_SCORE=0.3
# Значение параметра action, которое передается виджетом рекапчи в гугл.
PAGE_ACTION='login'
# Возвращается строка-расшифровка капчи. Get string for solve captcha, and other info.
user_answer = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
                .captcha_handler(websiteURL=PAGE_URL,
                                 websiteKey=SITE_KEY
                                 minScore=MIN_SCORE,
                                 pageAction=PAGE_ACTION
                                )

print(user_answer)
```

4.[Fun Captcha.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_fun_example.py)

5.[Fun Captcha Proxyless.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_fun_example.py)

```python
from python3_anticaptcha import FunCaptchaTask
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта
SITE_KEY = ''
# Ссылка на страницу с капчёй
PAGE_URL = ''
# Возвращается строка с ключём для отправки на проверку. Get full data for solve captcha.
user_answer = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                            proxyType="http",
                                            proxyAddress="8.8.8.8",
                                            proxyPort=8080)\
                .captcha_handler(websiteURL=PAGE_URL,
                                 websitePublicKey=SITE_KEY)

print(user_answer)
```

6.[Account management module.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_control_example.py)

```python
from python3_anticaptcha import AntiCaptchaControl
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# Возвращается строка c балансом. Balance info.
user_answer = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).get_balance()

print(user_answer)
```

7.[Custom Captcha.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_control_example.py)

```python
from python3_anticaptcha import CustomCaptchaTask
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# ссылка на изображение
imageUrl = "https://files.anti-captcha.com/26/41f/c23/7c50ff19.jpg"
# минимальный пример использования модуля
my_custom_task = CustomCaptchaTask.CustomCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY).\
                    captcha_handler(imageUrl=imageUrl)
print(my_custom_task)
```

8.[Gee Test.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_control_example.py)

9.[Gee Test Proxyless.](https://github.com/AndreiDrang/python3-anticaptcha/blob/master/anticaptcha_examples/anticaptcha_control_example.py)

```python
from python3_anticaptcha import GeeTestTaskProxyless
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# обязательные параметры
websiteURL = "http:\/\/mywebsite.com\/geetest\/test.php"
gt = "874703612e5cac182812a00e273aad0d"
challenge = "a559b82bca2c500101a1c8a4f4204742"
# пример работы с GeeTestTask без прокси
result = GeeTestTaskProxyless.GeeTestTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY,
                                                   websiteURL=websiteURL,
                                                   gt=gt).\
            captcha_handler(challenge=challenge)

print(result)
```
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](https://pythoncaptcha.cloud/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.

Some examples you can test with our [web-site](https://pythoncaptcha.cloud/).

***
For tests:
1. Clon repo;
2. ```bash
    export anticaptcha_key=SERVICE_KEY
    pip install pytest pytest-asyncio
    pytest tests
    ```
