import asyncio
import requests

from python3_anticaptcha import NoCaptchaTaskProxyless, NoCaptchaTask, CallbackClient

ANTICAPTCHA_KEY = "ae23fffcfaa29b170e3843e3a486ef19"

# Пример показывает работу антикапчи с "невидимой" рекапчёй от гугла, точно так же работает обычная рекапча от гугла.
# Это метод для работы без прокси
result = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
    anticaptcha_key=ANTICAPTCHA_KEY
).captcha_handler(
    websiteURL="https://www.google.com/recaptcha/api2/demo",
    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
)
print(result)

# contextmanager
with NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY) as nocaptcha:
    response = nocaptcha.captcha_handler(
        websiteURL="https://www.google.com/recaptcha/api2/demo",
        websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    )
print(response)


# Пример работы антикапчи с гугловской невидимой рекапчёй и обычной рекапчёй с использованием ПРОКСИ
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

# Асинхронный пример
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

"""
Callback example
"""
QUEUE_KEY = "wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ_anticaptcha_queue"

"""
Перед тем как начать пользоваться сервисом нужно создать для своей задачи отдельную очередь
Очередь можно создать один раз и пользоваться постоянно

Для создания очереди нужно передать два параметра:
1. key - название очереди, чем оно сложнее тем лучше
2. vhost - название виртуального хоста(в данном случаи - `anticaptcha_vhost`)
"""

answer = requests.post(
    "http://85.255.8.26:8001/register_key", json={"key": QUEUE_KEY, "vhost": "anticaptcha_vhost"}
)
# если очередь успешно создана:
if answer == "OK":
    # создаём задание с callbackURL параметром
    result = NoCaptchaTask.NoCaptchaTask(
        anticaptcha_key=ANTICAPTCHA_KEY,
        proxyType="http",
        proxyAddress="8.8.8.8",
        proxyPort=8080,
        proxyLogin="proxyLoginHere",
        proxyPassword="proxyPasswordHere",
        callbackUrl=f"http://85.255.8.26:8001/anticaptcha/nocaptcha/{QUEUE_KEY}",
    ).captcha_handler(
        websiteURL="https://www.google.com/recaptcha/api2/demo",
        websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    )

    print(result)

    # получение результата из кеша
    print(CallbackClient.CallbackClient(task_id=result["taskId"]).captcha_handler())
    # получение результата из RabbitMQ очереди
    print(
        CallbackClient.CallbackClient(
            task_id=result["taskId"], queue_name=QUEUE_KEY, call_type="queue"
        ).captcha_handler()
    )
