import time
import asyncio

import aiohttp
import requests

from python3_anticaptcha import app_key, create_task_url, get_sync_result, get_async_result


class NoCaptchaTask:
    def __init__(self, anticaptcha_key: str, sleep_time: int = 10, callbackUrl: str = None, **kwargs):
        """
        Модуль отвечает за решение NoCaptcha.
        :param anticaptcha_key: ключ от АнтиКапчи
        :param sleep_time: Время ожидания решения
        :param callbackUrl: URL для решения капчи с ответом через callback
        :param kwargs: Параметры для подключения к прокси. Подробнее в официальной документации или примерe  - anticaptcha_examples/anticaptcha_nocaptcha_example.py
        """

        if sleep_time < 10:
            raise ValueError(f"Param `sleep_time` must be greater than 10. U set - {sleep_time}")
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {
            "clientKey": anticaptcha_key,
            "task": {"type": "NoCaptchaTask"},
            "softId": app_key,
        }

        # задаём callbackUrl если передан
        if callbackUrl:
            self.task_payload.update({"callbackUrl": callbackUrl})

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}
        # заполнить пайлоад остальными аргументами
        if kwargs:
            for key in kwargs:
                self.task_payload["task"].update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчей
    def captcha_handler(
        self, websiteURL: str, websiteKey: str, recaptchaDataSValue: str = "", **kwargs
    ) -> dict:
        """
        Метод получает ссылку на страницу, где расположена капча, и ключ капчи
        :param: websiteURL: Ссылка на страницу с капчёй
        :param: websiteKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи)
                :param recaptchaDataSValue: Некоторые реализации виджета рекапчи могут содержать
                                    дополнительный параметр "data-s" в div'е рекапчи,
                                    который является одноразовым токеном и
                                    должен собираться каждый раз при решении рекапчи.
        :param kwargs: Дополнительные параметры для `requests.post(....)`.
        return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "recaptchaDataSValue": recaptchaDataSValue,
            }
        )
        # отправляем реквест, в ответ получаем JSON содержащий номер решаемой капчи
        captcha_id = requests.post(create_task_url, json=self.task_payload, verify=False, **kwargs).json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id["errorId"] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id
        # если передан параметр `callbackUrl` - не ждём решения капчи а возвращаем незаполненный ответ
        if self.task_payload.get("callbackUrl"):
            return self.result_payload

        else:
            # Ждем решения капчи
            time.sleep(self.sleep_time)
            return get_sync_result(result_payload=self.result_payload, sleep_time=self.sleep_time)


class aioNoCaptchaTask:
    def __init__(self, anticaptcha_key: str, sleep_time: str = 10, callbackUrl: str = None, **kwargs):
        """
        Модуль отвечает за решение NoCaptcha.
        :param anticaptcha_key: ключ от АнтиКапчи
                :param sleep_time: Время ожидания решения
        :param callbackUrl: URL для решения капчи с ответом через callback
        :param kwargs: Параметры для подключения к прокси. Подробнее в официальной документации или примерe  - anticaptcha_examples/anticaptcha_nocaptcha_example.py
        """

        if sleep_time < 10:
            raise ValueError(f"Param `sleep_time` must be greater than 10. U set - {sleep_time}")
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {
            "clientKey": anticaptcha_key,
            "task": {"type": "NoCaptchaTask"},
            "softId": app_key,
        }

        # задаём callbackUrl если передан
        if callbackUrl:
            self.task_payload.update({"callbackUrl": callbackUrl})

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}
        # заполнить пайлоад остальными аргументами
        if kwargs:
            for key in kwargs:
                self.task_payload["task"].update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчей
    async def captcha_handler(self, websiteURL: str, websiteKey: str, recaptchaDataSValue: str = "") -> dict:
        """
        Метод получает ссылку на страницу, где расположена капча, и ключ капчи
        :param: websiteURL: Ссылка на страницу с капчёй.
        :param: websiteKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи).
                :param recaptchaDataSValue: Некоторые реализации виджета рекапчи могут содержать
                                    дополнительный параметр "data-s" в div'е рекапчи,
                                    который является одноразовым токеном и
                                    должен собираться каждый раз при решении рекапчи.
        return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "recaptchaDataSValue": recaptchaDataSValue,
            }
        )
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

        # если передан параметр `callbackUrl` - не ждём решения капчи а возвращаем незаполненный ответ
        if self.task_payload.get("callbackUrl"):
            return self.result_payload

        else:
            # Ждем решения капчи
            await asyncio.sleep(self.sleep_time)
            return await get_async_result(result_payload=self.result_payload, sleep_time=self.sleep_time)
