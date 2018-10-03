import time
import requests
import asyncio
import aiohttp

from .config import create_task_url, app_key, user_agent_data
from .get_answer import get_sync_result, get_async_result


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

        if sleep_time < 5:
            raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {"clientKey": anticaptcha_key,
                             "task":
                                 {
                                     "type": "NoCaptchaTask",
                                     "userAgent": user_agent_data,
                                     "proxyType": proxyType,
                                     "proxyAddress": proxyAddress,
                                     "proxyPort": proxyPort,
                                 },
                             "softId": app_key
                             }

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}
        # заполнить пайлоад остальными аргументами
        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update({key: kwargs[key]})

    # Работа с капчей
    def captcha_handler(self, websiteURL, websiteKey, **kwargs):
        """
        Метод получает ссылку на страницу, где расположена капча, и ключ капчи
        :param: websiteURL: Ссылка на страницу с капчёй
        :param: websiteKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи)
        return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload['task'].update({"websiteURL": websiteURL,
                                          "websiteKey": websiteKey})
        # отправляем реквест, в ответ получаем JSON содержащий номер решаемой капчи
        captcha_id = requests.post(create_task_url, json=self.task_payload, **kwargs).json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id['errorId'] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

        # Ждем решения капчи
        time.sleep(self.sleep_time)
        return get_sync_result(result_payload = self.result_payload, sleep_time = self.sleep_time)


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
                                     "type": "NoCaptchaTask",
                                     "userAgent": user_agent_data,
                                     "proxyType": proxyType,
                                     "proxyAddress": proxyAddress,
                                     "proxyPort": proxyPort,
                                 },
                             "softId": app_key
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
        return await get_async_result(result_payload = self.result_payload, sleep_time = self.sleep_time)
