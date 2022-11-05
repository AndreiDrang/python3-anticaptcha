# python3-anticaptcha

![AntiCaptcha](files/AntiCaptcha.png)

[![PyPI version](https://badge.fury.io/py/python3-anticaptcha.svg)](https://badge.fury.io/py/python3-anticaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python3-anticaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python3-anticaptcha)
[![Downloads](https://pepy.tech/badge/python3-anticaptcha/month)](https://pepy.tech/project/python3-anticaptcha)

[![Code Climate](https://codeclimate.com/github/AndreiDrang/python3-anticaptcha/badges/gpa.svg)](https://codeclimate.com/github/AndreiDrang/python3-anticaptcha)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2daabf7ff7974f01b9348fe64483c7af)](https://app.codacy.com/app/drang.andray/python3-anticaptcha?utm_source=github.com&utm_medium=referral&utm_content=AndreiDrang/python3-anticaptcha&utm_campaign=Badge_Grade_Settings)


Python3 library for [Anti-Captcha](https://anti-captcha.com/mainpage) service.

Tested on UNIX based OS.

The library is intended for software developers and is used to work with the [Anti-Captcha](https://anti-captcha.com/mainpage) service API.

***
Application in [AppCenter](https://anti-captcha.com/clients/tools/appcenter/app/867).

If you have any questions, please send a message to the [Telegram](https://t.me/pythoncaptcha) chat room.

Or email python-captcha@pm.me
***

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
Присутствуют [примеры работы с библиотекой](./anticaptcha_examples).

Full examples you can find [here](./anticaptcha_examples).

***
### At the moment the following methods are implemented:
### На данный момент реализованы следующие методы:

##### 0.[Manual result handler.](./anticaptcha_examples/custom_result_handler_example.py)

 
```python
from python3_anticaptcha import CustomResultHandler
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = "your_key"
# Task ID to get result
TASK_ID = 123456
# This module is used to obtain the result of solving the task in "manual" mode
custom_result = CustomResultHandler.CustomResultHandler(
    anticaptcha_key=ANTICAPTCHA_KEY
)

user_answer = custom_result.task_handler(task_id=TASK_ID)
print(user_answer)
```

##### 1. [Image to text captcha.](./anticaptcha_examples/anticaptcah_image_to_text_example.py)

 
```python
from python3_anticaptcha import ImageToTextTask
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# Link to captcha image.
image_link = "https://pythoncaptcha.tech/static/image/common_image_example/800070.png"
# Get string for solve captcha, and some other info.
user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).\
                captcha_handler(captcha_link=image_link)

print(user_answer)
```

##### 2. [ReCaptcha v2.](./anticaptcha_examples/anticaptcha_nocaptcha_example.py)


##### 3. [ReCaptcha v2 Proxyless. ](./anticaptcha_examples/anticaptcha_nocaptcha_example.py) + [Selenium example](./anticaptcha_examples/selenium_recaptcha_v2.py)

```python
from python3_anticaptcha import NoCaptchaTaskProxyless
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# G-ReCaptcha ключ сайта. Website google key.
SITE_KEY = '6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'
# Page url.
PAGE_URL = 'https://www.google.com/recaptcha/intro/android.html'
# Get string for solve captcha, and other info.
user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
                .captcha_handler(websiteURL=PAGE_URL,
                                 websiteKey=SITE_KEY)

print(user_answer)
```

##### 4. [ReCaptcha v3 Proxyless. ](./anticaptcha_examples/anticaptcha_nocaptcha_example.py)

```python
from python3_anticaptcha import ReCaptchaV3TaskProxyless
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# G-ReCaptcha - website google key.
SITE_KEY = '6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'
# Page url.
PAGE_URL = 'https://some_link'
# The filter by which the employee with the required minimum score is selected.
# possible options - 0.3, 0.5, 0.7
MIN_SCORE=0.3
# The value of the `action` parameter, which is passed by the recaptcha widget to google.
PAGE_ACTION='login'
# Get string for solve captcha, and other info.
user_answer = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
                .captcha_handler(websiteURL=PAGE_URL,
                                 websiteKey=SITE_KEY,
                                 minScore=MIN_SCORE,
                                 pageAction=PAGE_ACTION
                                )

print(user_answer)
```

##### 5. [Fun Captcha.](./anticaptcha_examples/anticaptcha_fun_example.py)

##### 6. [Fun Captcha Proxyless.](./anticaptcha_examples/anticaptcha_fun_example.py)

```python
from python3_anticaptcha import FunCaptchaTask
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# G-ReCaptcha site key
SITE_KEY = ''
# Link to the page with captcha
PAGE_URL = ''
# Get full data for solve captcha.
user_answer = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                            proxyType="http",
                                            proxyAddress="8.8.8.8",
                                            proxyPort=8080)\
                .captcha_handler(websiteURL=PAGE_URL,
                                 websitePublicKey=SITE_KEY)

print(user_answer)
```

##### 7. [Account management module.](./anticaptcha_examples/anticaptcha_control_example.py)

```python
from python3_anticaptcha import AntiCaptchaControl
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
# Balance info
result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).get_balance()
# Submitting a complaint about incorrectly resolved captcha images
result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).complaint_on_result(
    reported_id=543212, captcha_type="image"
)
# Submitting a complaint about incorrectly resolved ReCaptcha
result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).complaint_on_result(
    reported_id=5432134, captcha_type="recaptcha"
)
# Giving information about loading the queue, depending on the queue ID
result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).get_queue_status(queue_id=1)
```

##### 8. [Custom Captcha.](./anticaptcha_examples/anticaptcha_customcaptcha_example.py)

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

##### 9. [Gee Test.](./anticaptcha_examples/gee_example.py)

##### 10. [Gee Test Proxyless.](./anticaptcha_examples/gee_example.py)

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

##### 11. [HCaptcha.](./anticaptcha_examples/anticaptcha_hcaptcha_example.py)

##### 12. [HCaptcha Proxyless.](./anticaptcha_examples/anticaptcha_hcaptcha_example.py)

```python
from python3_anticaptcha import HCaptchaTaskProxyless
# Enter the key to the AntiCaptcha service from your account. Anticaptcha service key.
ANTICAPTCHA_KEY = ""
WEB_URL = "https://dashboard.hcaptcha.com/signup"
SITE_KEY = "00000000-0000-0000-0000-000000000000"

result = HCaptchaTaskProxyless.HCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY).\
            captcha_handler(websiteURL=WEB_URL, websiteKey=SITE_KEY)

print(result)
```
***
Кроме того, для тестирования различных типов капчи предоставляется [специальный сайт](https://pythoncaptcha.tech/), на котором собраны все имеющиеся типы капчи, с удобной системой тестирования ваших скриптов.

Some examples you can test with our [web-site](https://pythoncaptcha.tech/).

***
#### For tests:
1. Clone repository
2. ```bash
    export anticaptcha_key=SERVICE_KEY
    make test
    ```
