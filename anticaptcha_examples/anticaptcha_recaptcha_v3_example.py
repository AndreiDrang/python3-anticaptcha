import asyncio

from python3_anticaptcha import ReCaptchaV3TaskProxyless

ANTICAPTCHA_KEY = "ae23fffcfaa29b170e3843e3a486ef19"

"""
WARNING:

`minScore` param can be only in [0.3, 0.5, 0.7]
"""

# Пример показывает работу антикапчи с ReCaptcha v3.
# Это метод для работы без прокси
result = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
    websiteURL="https://some_page_link",
    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    minScore=0.3,
    pageAction="login",
)
print(result)

# contextmanager
with ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY) as recaptcha:
    response = recaptcha.captcha_handler(
        websiteURL="https://some_page_link",
        websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        minScore=0.3,
        pageAction="login",
    )
print(response)

# Асинхронный пример
async def run():
    try:
        result = await ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=ANTICAPTCHA_KEY
        ).captcha_handler(
            websiteURL="https://some_page_link",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=0.3,
            pageAction="login",
        )
        print(result)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
