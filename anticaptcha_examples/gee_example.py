import asyncio

from python3_anticaptcha import GeeTestTask, GeeTestTaskProxyless


# пример решения GeeTestTask - скользящая капча от geetest.com

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

# пример работы с GeeTestTask c прокси
result = GeeTestTask.GeeTestTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                 websiteURL=websiteURL,
                                 gt=gt,
                                 proxyType="http",
                                 proxyAddress = "8.8.8.8",
                                 proxyPort = 8080,
                                 proxyLogin = "proxyLoginHere",
                                 proxyPassword = "proxyPasswordHere",
                                 userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
                                 cookies = "test=value").\
            captcha_handler(challenge=challenge)

print(result)


# Асинхронный пример работы
async def run():
    try:
        # пример работы с GeeTestTask c прокси
        result = GeeTestTask.aioGeeTestTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                            websiteURL=websiteURL,
                                            gt=gt,
                                            proxyType="http",
                                            proxyAddress = "8.8.8.8",
                                            proxyPort = 8080,
                                            proxyLogin = "proxyLoginHere",
                                            proxyPassword = "proxyPasswordHere",
                                            userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
                                            cookies = "test=value").\
                    captcha_handler(challenge=challenge)
        
        print(result)
        # пример работы с GeeTestTask без прокси
        result = GeeTestTaskProxyless.aioGeeTestTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY,
                                                              websiteURL=websiteURL,
                                                              gt=gt).\
                    captcha_handler(challenge=challenge)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
