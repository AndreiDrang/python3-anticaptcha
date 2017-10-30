import requests
import time
import aiohttp
import asyncio
import tempfile
import hashlib
import os
import base64

from .config import create_task_url, get_result_url, app_key


class ImageToTextTask:
    '''
    Данный метод подходит для решения капчи-изображение.
    Подробней информацию смотрите в методе 'captcha_handler' и '__init__'
    '''

    def __init__(self, anticaptcha_key, sleep_time=5, save_format = 'temp', language = 'en',**kwargs):
        '''
        Инициализация нужных переменных, создание папки для изображений и кэша
        После завершения работы - удаляются временные фалйы и папки
        :param anticaptcha_key:  АПИ ключ капчи из кабинета пользователя
        :param sleep_time: Вермя ожидания решения капчи
        :param save_format: Формат в котором будет сохраняться изображение, либо как временный файл - 'temp',
                            либо как обычное изображение в папку созданную библиотекой - 'const'.
        :param language: Язык капчи
        :param **kwargs: За подробной информацией обратитесь к документации на сайте anticaptcha.
        '''
        self.sleep_time = sleep_time
        self.save_format = save_format

        # Пайлоад для создания задачи
        self.task_payload = {"clientKey": anticaptcha_key,
                             "task":
                                 {
                                       "type": "ImageToTextTask",
                                 },
                             "languagePool": language
                             }

        # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
        # если всё ок - идём дальше
        self.result_payload = {"clientKey": anticaptcha_key}
        
        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update({key: kwargs[key]})

    def image_temp_saver(self, content):
        '''
        Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
        :return: Возвращает ID капчи
        '''
        with tempfile.NamedTemporaryFile(suffix='.png') as captcha_image:
            captcha_image.write(content)
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            self.task_payload['task'].update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи и получая ответ - извлекаем номер
            captcha_id = (requests.post(create_task_url, json = self.task_payload).json())
        return captcha_id

    def image_const_saver(self, content):
        '''
        Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
        :return: Возвращает ID капчи
        '''
        img_path = 'PythonAntiCaptchaImages'

        if not os.path.exists(img_path):
            os.mkdir(img_path)

        # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
        image_hash = hashlib.sha224(content).hexdigest()

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'wb') as out_image:
            out_image.write(content)

        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'rb') as captcha_image:
            # Добавляем в пайлоад картинку и отправляем
            self.task_payload['task'].update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            # Отправляем на антикапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ содержащий номер решаемой капчи
            captcha_id = requests.post(create_task_url, json = self.task_payload).json()

        # удаляем файл капчи
        os.remove(os.path.join(img_path, "im-{0}.png".format(image_hash)))

        return captcha_id

    # Работа с капчёй
    def captcha_handler(self, captcha_link):
        '''
        Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
        RuCaptcha, дожидается решения капчи и вовзращает вам результат
        :param captcha_link: Ссылка на изображение
        :return: Возвращает весь ответ сервера JSON-строкой.
        '''

        content = requests.get(captcha_link).content

        # согласно значения переданного параметра выбираем функцию для сохранения изображения
        if self.save_format == 'const':
            captcha_id = self.image_const_saver(content)
        elif self.save_format == 'temp':
            captcha_id = self.image_temp_saver(content)
        else:
            return """Wrong 'save_format' parameter. Valid formats: 'const' or 'temp'.\n 
                    Неправильный 'save_format' параметр. Возможные форматы: 'const' или 'temp'."""

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id['errorId'] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

        # Ожидаем решения капчи
        time.sleep(self.sleep_time)
        while True:
            # отправляем запрос на результат решения капчи, если не решена ожидаем
            captcha_response = requests.post(get_result_url, json = self.result_payload)

            # Если ошибки нет - проверяем статус капчи
            if captcha_response.json()['errorId'] == 0:
                # Если капча ещё не готова- ожидаем
                if captcha_response.json()["status"] == "processing":
                    time.sleep(self.sleep_time)
                # если уже решена - возвращаем ответ сервера
                else:
                    return captcha_response.json()
            # Иначе возвращаем ответ сервера
            else:
                return captcha_response.json()



class aioImageToTextTask:
    '''
	Данный метод подходит для всинхронного решения капчи-изображение.
	Подробней информацию смотрите в методе 'captcha_handler' и '__init__'
	'''
    
    def __init__(self, anticaptcha_key, sleep_time=5, save_format='temp', language='en', **kwargs):
        '''
		Инициализация нужных переменных, создание папки для изображений и кэша
		После завершения работы - удаляются временные фалйы и папки
		:param anticaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param sleep_time: Вермя ожидания решения капчи
		:param save_format: Формат в котором будет сохраняться изображение, либо как временный файл - 'temp',
							либо как обычное изображение в папку созданную библиотекой - 'const'.
		:param language: Язык капчи
		:param **kwargs: За подробной информацией обратитесь к документации на сайте anticaptcha.
		'''
        self.sleep_time = sleep_time
        self.save_format = save_format
        
        # Пайлоад для создания задачи
        self.task_payload = {"clientKey": anticaptcha_key,
                             "task":
                                 {
                                     "type": "ImageToTextTask",
                                 },
                             "languagePool": language
                             }
        
        # отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
        # если всё ок - идём дальше
        self.result_payload = {"clientKey": anticaptcha_key}
        
        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update({key: kwargs[key]})
    
    async def image_temp_saver(self, captcha_link):
        '''
		Метод сохраняет файл изображения как временный и отправляет его сразу на сервер для расшифровки.
		:return: Возвращает ID капчи
		'''
        # Скачиваем капчу
        async with aiohttp.ClientSession() as session:
            async with session.get(captcha_link) as resp:
                content = await resp.content.readany()
        
        with tempfile.NamedTemporaryFile(suffix='.png') as captcha_image:
            captcha_image.write(content)
            # Создаём пайлоад, вводим ключ от сайта, выбираем метод ПОСТ и ждём ответа в JSON-формате
            self.task_payload['task'].update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            # Отправляем на рукапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ с номером решаемой капчи
            async with aiohttp.ClientSession() as session:
                async with session.post(create_task_url, json=self.task_payload) as resp:
                    return await resp.json()
    
    async def image_const_saver(self, captcha_link):
        '''
		Метод создаёт папку и сохраняет в неё изображение, затем передаёт его на расшифровку и удалет файл.
		:return: Возвращает ID капчи
		'''
        img_path = 'PythonAntiCaptchaImages'
        
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        
        # Скачиваем капчу
        async with aiohttp.ClientSession() as session:
            async with session.get(captcha_link) as resp:
                content = await resp.content.readany()
        
        # Высчитываем хэш изображения, для того что бы сохранить его под уникальным именем
        image_hash = hashlib.sha224(content).hexdigest()
        
        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'wb') as out_image:
            out_image.write(content)
        
        with open(os.path.join(img_path, 'im-{0}.png'.format(image_hash)), 'rb') as captcha_image:
            # Добавляем в пайлоад картинку и отправляем
            self.task_payload['task'].update({"body": base64.b64encode(captcha_image.read()).decode('utf-8')})
            # Отправляем на антикапча изображение капчи и другие парметры,
            # в результате получаем JSON ответ содержащий номер решаемой капчи
            
            async with aiohttp.ClientSession() as session:
                async with session.post(create_task_url, json=self.task_payload) as resp:
                    captcha_id = await resp.json()
        
        # удаляем файл капчи
        os.remove(os.path.join(img_path, "im-{0}.png".format(image_hash)))
        return captcha_id
    
    # Работа с капчёй
    async def captcha_handler(self, captcha_link):
        '''
		Метод получает от вас ссылку на изображение, скачивает его, отправляет изображение на сервер
		RuCaptcha, дожидается решения капчи и вовзращает вам результат
		:param captcha_link: Ссылка на изображение
		:return: Возвращает весь ответ сервера JSON-строкой.
		'''
        
        # согласно значения переданного параметра выбираем функцию для сохранения изображения
        if self.save_format == 'const':
            captcha_id = await self.image_const_saver(captcha_link)
        elif self.save_format == 'temp':
            captcha_id = await self.image_temp_saver(captcha_link)
        else:
            return """Wrong 'save_format' parameter. Valid formats: 'const' or 'temp'.\n
                    Неправильный 'save_format' параметр. Возможные форматы: 'const' или 'temp'."""
        
        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id['errorId'] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id
        
        # Ожидаем решения капчи
        await asyncio.sleep(self.sleep_time)
        # отправляем запрос на результат решения капчи, если не решена ожидаем
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(get_result_url, json=self.result_payload) as resp:
                    json_result = await resp.json()
                    
                    # Если ошибки нет - проверяем статус капчи
                    if json_result['errorId'] == 0:
                        # Если капча ещё не готова- ожидаем
                        if json_result["status"] == "processing":
                            await asyncio.sleep(self.sleep_time)
                        # если уже решена - возвращаем ответ сервера
                        else:
                            return json_result
                    # Иначе возвращаем ответ сервера
                    else:
                        return json_result

