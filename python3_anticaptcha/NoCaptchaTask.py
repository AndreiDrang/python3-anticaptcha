import requests
import time
import asyncio
import aiohttp

from .config import create_task_url, get_result_url, app_key, user_agent_data


class NoCaptchaTask:

    def __init__(self, anticaptcha_key, proxyAddress, proxyPort, sleep_time=5, proxyType = 'http', **kwargs):
        """
        Модуль отвечает за решение NoCaptcha.
        userAgent рандомно берётся из актульного списка браузеров-параметров
        :param anticaptcha_key: ключ от АнтиКапчи
        :param proxyAdress: Адрес прокси-сервера
        :param proxyPort: Порт сервера
        :param proxyType: Тип прокси http/socks5/socks4
        :param sleeptime: Время ожидания решения
        :param kwargs: Необязательные параметры, можно переопределить userAgent
        """
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {"clientKey": anticaptcha_key,
                             "task":
                                 {
                                     "type": "FunCaptchaTask",
                                     "userAgent": user_agent_data,
                                     "proxyType": proxyType,
                                     "proxyAddress": proxyAddress,
                                     "proxyPort": proxyPort,
                                 },
                             }

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}
        # заполнить пайлоад остальными аргументами
        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update({key: kwargs[key]})

    # Работа с капчей
    def captcha_handler(self, websiteURL, websiteKey):
        """
        Метод получает ссылку на страницу, где расположена капча, и ключ капчи
        :param: websiteURL: Ссылка на страницу с капчёй
        :param: websiteKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи)
        return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload['task'].update({"websiteURL": websiteURL,
                                          "websiteKey": websiteKey})
        # отправляем реквест, в ответ получаем JSON содержащий номер решаемой капчи
        captcha_id = requests.post(create_task_url, json=self.task_payload).json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id['errorId'] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

        # Ждем решения капчи
        time.sleep(self.sleep_time)
        while True:
            captcha_response = requests.post(get_result_url, json=self.result_payload)

            if captcha_response.json()["errorId"] == 0:
                if captcha_response.json()["status"] == "processing":
                    time.sleep(self.sleep_time)
                else:
                    return captcha_response.json()
            else:
                return captcha_response.json()



class aioNoCaptchaTask:

    def __init__(self, anticaptcha_key, proxyAddress, proxyPort, sleep_time=5, proxyType = 'http', **kwargs):
        """
        Модуль отвечает за решение NoCaptcha.
        userAgent рандомно берётся из актульного списка браузеров-параметров
        :param anticaptcha_key: ключ от АнтиКапчи
        :param proxyAdress: Адрес прокси-сервера
        :param proxyPort: Порт сервера
        :param proxyType: Тип прокси http/socks5/socks4
        :param sleeptime: Время ожидания решения
        :param kwargs: Необязательные параметры, можно переопределить userAgent
        """
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {"clientKey": anticaptcha_key,
                             "task":
                                 {
                                     "type": "FunCaptchaTask",
                                     "userAgent": user_agent_data,
                                     "proxyType": proxyType,
                                     "proxyAddress": proxyAddress,
                                     "proxyPort": proxyPort,
                                 },
                             }

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}
        # заполнить пайлоад остальными аргументами
        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update({key: kwargs[key]})

    # Работа с капчей
    async def captcha_handler(self, websiteURL, websiteKey):
        """
        Метод получает ссылку на страницу, где расположена капча, и ключ капчи
        :param: websiteURL: Ссылка на страницу с капчёй
        :param: websiteKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи)
        return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload["task"].update({"websiteURL": websiteURL,
                                          "websiteKey": websiteKey})
        # отправляем реквест, в ответ получаем JSON содержащий номер решаемой капчи
        captcha_id = requests.post(create_task_url, json=self.task_payload).json()
        async with aiohttp.ClientSession() as session:
            async with session.post(create_task_url, json=self.task_payload) as resp:
                captcha_id = await resp.json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id["errorId"] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

        # Ждем решения капчи
        await asyncio.sleep(self.sleep_time)
        # Отправляем запрос на статус решения капчи.
        async with aiohttp.ClientSession as session:
            while True:
                async with session.post(get_result_url, json=self.result_payload) as resp:
                    json_result = await resp.json()
                    # Если нет ошибки - проверяем статус капчи
                    if json_result["errorId"] == 0:
                        # Если еще не решена, ожидаем
                        if json_result["status"] == "processing":
                            await asyncio.sleep(self.sleep_time)
                        # Иначе возвращаем ответ
                        else:
                            return json_result
                    else:
                        return json_result
