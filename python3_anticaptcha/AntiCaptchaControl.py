import requests
import aiohttp

from python3_anticaptcha import (
    get_balance_url,
    incorrect_captcha_url,
    get_queue_status_url,
)


class AntiCaptchaControl:
    def __init__(self, anticaptcha_key: str):
        """
        Синхронный метод работы с балансом и жалобами
        :param anticaptcha_key: Ключ антикапчи
        """
        self.ANTICAPTCHA_KEY = anticaptcha_key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    def get_balance(self):
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        answer = requests.post(
            get_balance_url, json={"clientKey": self.ANTICAPTCHA_KEY}
        )

        return answer.json()

    def complaint_on_result(self, reported_id: int):
        """
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :return: Возвращает True/False, в зависимости от результата
        """
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "taskId": reported_id}

        answer = requests.post(incorrect_captcha_url, json=payload)

        return answer.json()

    def get_queue_status(self, queue_id: int):
        """
        Получение информации о загрузке очереди, в зависимости от ID очереди.

        Метод позволяет определить, насколько в данный момент целесообразно загружать новое задание в очередь.
        Данные в выдаче кешируются на 10 секунд.

        Список ID очередей:
            1   - стандартная ImageToText, язык английский
            2   - стандартная ImageToText, язык русский
            5   - Recaptcha NoCaptcha
            6   - Recaptcha Proxyless
            7   - Funcaptcha
            10  - Funcaptcha Proxyless

        Пример выдачи ответа:
            {
                "waiting":242,
                "load":60.33,
                "bid":"0.0008600982",
                "speed":10.77,
                "total": 610
            }
        :param queue_id: Номер очереди
        :return: JSON-объект
        """
        payload = {"queueId": queue_id}

        answer = requests.post(get_queue_status_url, json=payload)

        return answer.json()


class aioAntiCaptchaControl:
    def __init__(self, anticaptcha_key: str):
        """
        Асинхронный метод работы с балансом и жалобами
        :param anticaptcha_key: Ключ антикапчи
        """
        self.ANTICAPTCHA_KEY = anticaptcha_key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def get_balance(self):
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                get_balance_url, json={"clientKey": self.ANTICAPTCHA_KEY}
            ) as resp:
                return await resp.json()

    async def complaint_on_result(self, reported_id: int):
        """
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :return: Возвращает True/False, в зависимости от результата
        """
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "taskId": reported_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(incorrect_captcha_url, json=payload) as resp:
                return await resp.json()

    async def get_queue_status(self, queue_id: int):
        """
        Получение информации о загрузке очереди, в зависимости от ID очереди.

        Метод позволяет определить, насколько в данный момент целесообразно загружать новое задание в очередь.
        Данные в выдаче кешируются на 10 секунд.

        Список ID очередей:
            1   - стандартная ImageToText, язык английский
            2   - стандартная ImageToText, язык русский
            5   - Recaptcha NoCaptcha
            6   - Recaptcha Proxyless
            7   - Funcaptcha
            10  - Funcaptcha Proxyless

        Пример выдачи ответа:
            {
                "waiting":242,
                "load":60.33,
                "bid":"0.0008600982",
                "speed":10.77,
                "total": 610
            }
        :param queue_id: Номер очереди
        :return: JSON-объект
        """
        payload = {"queueId": queue_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(get_queue_status_url, json=payload) as resp:
                return await resp.json()
