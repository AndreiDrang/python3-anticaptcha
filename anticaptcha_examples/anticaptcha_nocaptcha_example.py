import asyncio
import requests

from python3_anticaptcha import NoCaptchaTaskProxyless, NoCaptchaTask

ANTICAPTCHA_KEY = "ae23fffcfaa29b170e3843e3a486ef19"


"""
Синхронный пример без прокси
Sync example without proxy
"""
result = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
    websiteURL="https://www.google.com/recaptcha/api2/demo",
    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
)
print(result)

"""
Синхронный пример с контекстным менеджером и без прокси
Sync example with contextmanager and without proxy
"""
with NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY) as nocaptcha:
    response = nocaptcha.captcha_handler(
        websiteURL="https://www.google.com/recaptcha/api2/demo",
        websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    )
print(response)

"""
Синхронный пример с прокси
Sync example with proxy
"""
result = NoCaptchaTask.NoCaptchaTask(
    anticaptcha_key=ANTICAPTCHA_KEY,
    proxyType="http",
    proxyAddress="8.8.8.8",
    proxyPort=8080,
    proxyLogin="proxyLoginHere",
    proxyPassword="proxyPasswordHere",
).captcha_handler(
    websiteURL="https://www.google.com/recaptcha/api2/demo",
    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
)

print(result)

"""
Асинхронный пример без прокси
Async example without proxy
"""


async def run():
    try:
        result = await NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(
            anticaptcha_key=ANTICAPTCHA_KEY
        ).captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        )
        print(result)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
