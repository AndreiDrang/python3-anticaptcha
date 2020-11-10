import asyncio
import base64
import requests

from python3_anticaptcha import ImageToTextTask, CallbackClient
from python3_anticaptcha import errors

ANTICAPTCHA_KEY = ""
"""
Данная библиотека реализует два различных метода для сохранения изображений(для последующей их передачи сервису):
1. В качестве временного файла, параметр задаётся по умолчанию: 
save_format = 'temp' .
2. В качестве обычного файла, для этого нужно передать:
save_format = 'const' . 
========================================================================================================================
This library implements two different methods for saving images (for their subsequent transfer to the service):
1. As a temporary file, the parameter is set by default: 
save_format = 'temp'.
2. As a normal file, you need to pass this:
save_format = 'const' .
"""
# Пример который показывает работу антикапчи при решении капчи-изображением и сохранением её в качестве обычного файла в
# папку.
# Example for working with captcha-image link, and save it like a usual file in system.

result = ImageToTextTask.ImageToTextTask(
    anticaptcha_key=ANTICAPTCHA_KEY, save_format="const"
).captcha_handler(captcha_link="https://pythoncaptcha.tech/static/image/common_image_example/800070.png")
print(result)

# Пример который показывает работу антикапчи при решении капчи-изображением и сохранением её в качестве ВРЕМЕННОГО файла
# Протестировано на Линуксах. Не используйте данный вариант на Windows! Возможно починим, но потом.
# Example for working with captcha-image like a temporary file. Tested on UNIX-based systems. Don`t use it on Windows!
result = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
    captcha_link="https://pythoncaptcha.tech/static/image/common_image_example/800070.png"
)
print(result)

"""
========================================================================================================================
Base64 files
Пример работы с декодированием в base64 файла-капчи "налету"
An example of working with decoding in base64 captcha-file after download. On-the-fly-encoding
"""
base_64_link = base64.b64encode(
    requests.get("https://pythoncaptcha.tech/static/image/common_image_example/862963.png").content
).decode("utf-8")

user_answer_base64 = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
    captcha_base64=base_64_link
)

"""
Пример работы со скачанными файлами изображений капчи.
Example for working with downloaded file.
"""
# Синхронный
# папка в которой находится изображение, один из вариантов написания
# The path to the file must be transferred in this format to the method
captcha_file = "088636.png"
# так же есть возможность передать так:
# or in this format:
# captcha_file = 'D:\/Python\/933588.png'
# captcha_file = r'D:\Python\933588.png'

result = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
    captcha_file=captcha_file
)
print(result)
"""
Пример для работы с локальными файлами
"""
# папка в которой находится изображение, один из вариантов написания

# так же есть возможность передать так:
# captcha_file = r'D:\Python\933588.png'
# captcha_file = 'D:\/Python\/933588.png'
try:
    user_answer_local = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
        captcha_file=captcha_file
    )
    if user_answer_local["errorId"] == 0:
        # решение капчи
        print(user_answer_local["solution"]["text"])
    elif user_answer_local["errorId"] == 1:
        # Тело ошибки, если есть
        print(user_answer_local["errorBody"])

# отлов ошибки при проблемах чтения файла-изображения
except errors.ReadError as err:
    print(err)

"""
========================================================================================================================
Asynchronous examples
Пример асинхронного запуска решения капчи
# AsyncIO example. Work with constant-saved file.
"""


async def run():
    try:
        resolve = await ImageToTextTask.aioImageToTextTask(
            anticaptcha_key=ANTICAPTCHA_KEY, save_format="const"
        ).captcha_handler(
            captcha_link="https://pythoncaptcha.tech/static/image/common_image_example/800070.png"
        )

        print(resolve)

        resolve = await ImageToTextTask.aioImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
            captcha_file=captcha_file
        )

        print(resolve)

        resolve = await ImageToTextTask.aioImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(
            captcha_base64=base_64_link
        )

        print(resolve)

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
    "https://pythoncaptcha.tech:8001/register_key",
    json={"key": QUEUE_KEY, "vhost": "anticaptcha_vhost"},
)
# если очередь успешно создана:
if answer == "OK":

    # создаём задание с callbackURL параметром
    result = ImageToTextTask.ImageToTextTask(
        anticaptcha_key=ANTICAPTCHA_KEY,
        callbackUrl=f"https://pythoncaptcha.tech:8001/anticaptcha/image_to_text/{QUEUE_KEY}",
    ).captcha_handler(captcha_link="https://pythoncaptcha.tech/static/image/common_image_example/800070.png")
    print(result)

    # получение результата из кеша
    print(CallbackClient.CallbackClient(task_id=result["taskId"]).captcha_handler())
    # получение результата из RabbitMQ очереди
    print(
        CallbackClient.CallbackClient(
            task_id=result["taskId"], queue_name=QUEUE_KEY, call_type="queue"
        ).captcha_handler()
    )
