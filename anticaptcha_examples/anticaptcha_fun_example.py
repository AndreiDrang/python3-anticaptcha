import asyncio

from python3_anticaptcha import FunCaptchaTask


ANTICAPTCHA_KEY = ""
WEB_URL = ""
SITE_KEY = ""
# Пример работы антикапчи с фанкапчёй и с использованием прокси при этом
result = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                       proxyType='http',
                                       proxyAddress="8.8.8.8",
                                       proxyPort=8080,
                                       proxyLogin="proxyLoginHere",
                                       proxyPassword="proxyPasswordHere")\
		.captcha_handler(websiteURL=WEB_URL,
                         websitePublicKey=SITE_KEY)

print(result)

# Асинхронный пример работы
async def run():
    try:
        # io.IOBase
        # Пример работы антикапчи с фанкапчёй и с использованием прокси при этом
        result = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                               proxyType='http',
                                               proxyAddress="8.8.8.8",
                                               proxyPort=8080,
                                               proxyLogin="proxyLoginHere",
                                               proxyPassword="proxyPasswordHere") \
            .captcha_handler(websiteURL=WEB_URL,
                             websitePublicKey=SITE_KEY)
        
        print(result)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()