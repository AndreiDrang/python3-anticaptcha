import asyncio

from python3_anticaptcha import ImageToTextTask

ANTICAPTCHA_KEY = ""
"""
Данная библиотека реализует два различных метода для сохранения изображений(для последующей их передачи сервису):
1. В качестве временного файла, параметр задаётся по умолчанию, но для того что бы его объявить явно нужно передать
save_format = 'temp' .
2. В качестве обычного файла, для этого нужно передать:
save_format = 'const' . !!!Используйте данный параметр при работе через Windows. USE IT ON WINDOWS!!!
"""
# Пример который показывает работу антикапчи при решении капчи-изображением и сохранением её в качестве обычного файла в
# папку.
# Example for working with captcha-image link, and save it like a usual file in system.

result = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY, save_format='const') \
    .captcha_handler(captcha_link='http://85.255.8.26/static/image/common_image_example/800070.png')
print(result)

# Пример который показывает работу антикапчи при решении капчи-изображением и сохранением её в качестве ВРЕМЕННОГО файла
# Протестировано на Линуксах. Не используйте данный вариант на Windows! Возможно починим, но потом.
# Example for working with captcha-image like a temporary file. Tested on UNIX-based systems. Don`t use it on Windows!
result = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY) \
    .captcha_handler(captcha_link='http://85.255.8.26/static/image/common_image_example/800070.png')
print(result)


# Пример асинхронного запуска решения капчи
# AsyncIO example. Work with constant-saved file.
async def run():
    try:
        resolve = await ImageToTextTask.aioImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY, save_format='const') \
            .captcha_handler(captcha_link='http://85.255.8.26/static/image/common_image_example/800070.png')

        print(resolve)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

"""
Пример работы со скачанными файлами изображений капчи.
Example for working with downloaded file.
"""
# Синхронный
# папка в которой находится изображение, один из вариантов написания
# The path to the file must be transferred in this format to the method
captcha_file = r'D:\Python\933588.png'
# так же есть возможность передать так:
# or in this format:
# captcha_file = 'D:\/Python\/933588.png'

result = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY).captcha_handler(captcha_file=captcha_file)
print(result)


# Асинхронный пример
# AsyncIO example.

async def run():
    try:
        resolve = await ImageToTextTask.aioImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY)\
	        .captcha_handler(captcha_file=captcha_file)

        print(resolve)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
