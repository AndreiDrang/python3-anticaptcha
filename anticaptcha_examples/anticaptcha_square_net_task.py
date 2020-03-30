import asyncio

import requests

from python3_anticaptcha import SquareNetTextTask, CallbackClient

"""
Пример работы с данным типом капчи

SquareNetTextTask : выбрать нужный объект на картинке с сеткой изображений
________________________
SquareNetTextTask : select objects on image with an overlay grid
"""
# вводим ключ от сервиса
ANTICAPTCHA_KEY = ""

# Простой пример работы / Base example
result = SquareNetTextTask.SquareNetTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
    objectName="captcha numbers",
    rowsCount=2,
    columnsCount=3,
    image_link="https://raw.githubusercontent.com/AndreiDrang/python-rucaptcha/master/examples/088636.png",
)
print(result)

# Асинхронный метод работы / Asyncio exaple
async def run():

    result = await SquareNetTextTask.aioSquareNetTextTask(
        anticaptcha_key=ANTICAPTCHA_KEY
    ).captcha_handler(
        objectName="captcha numbers",
        rowsCount=2,
        columnsCount=3,
        image_link="https://raw.githubusercontent.com/AndreiDrang/python-rucaptcha/master/examples/088636.png",
    )
    print(result)


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
    "https://pythoncaptcha.cloud:8001/register_key",
    json={"key": QUEUE_KEY, "vhost": "anticaptcha_vhost"},
)
# если очередь успешно создана:
if answer == "OK":
    # создаём задание с callbackURL параметром
    result = SquareNetTextTask.SquareNetTextTask(
        anticaptcha_key=ANTICAPTCHA_KEY,
        callbackUrl=f"https://pythoncaptcha.cloud:8001/anticaptcha/fun_captcha/{QUEUE_KEY}",
    ).captcha_handler(
        objectName="captcha numbers",
        rowsCount=2,
        columnsCount=3,
        image_link="https://raw.githubusercontent.com/AndreiDrang/python-rucaptcha/master/examples/088636.png",
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
