import requests
import aiohttp

from python3_anticaptcha import (
    get_balance_url,
    get_app_stats_url,
    incorrect_imagecaptcha_url,
    incorrect_recaptcha_url,
    get_queue_status_url,
)

# available app stats mods
mods = ("errors", "views", "downloads", "users", "money")
# available complaint captcha types
complaint_types = ("image", "recaptcha")
# availalbe queue ID's
queue_ids = (1, 2, 5, 6, 7, 10)


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

    def get_balance(self) -> dict:
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        answer = requests.post(
            get_balance_url, json={"clientKey": self.ANTICAPTCHA_KEY}
        )

        return answer.json()

    def get_app_stats(self, softId: int, mode: str = "errors") -> dict:
        """
        Получение статистики приложения
        :return: Возвращает актуальный баланс
        """
        if mode not in mods:
            raise ValueError(
                f"\nWrong `mode` parameter. Valid params: {mods}."
                f"\n\tYour param - `{mode}`"
            )
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "softId": softId, "mode": mode}
        answer = requests.post(get_app_stats_url, json=payload)

        if answer.text:
            return answer.json()
        else:
            return {"errorId": 1}

    def complaint_on_result(
        self, reported_id: int, captcha_type: str = "image"
    ) -> dict:
        f"""
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :param captcha_type: Тип капчи на который идёт жалоба. Возможные варианты:
                            {complaint_types}
        :return: Возвращает True/False, в зависимости от результата
        """
        if captcha_type not in complaint_types:
            raise ValueError(
                f"\nWrong `captcha_type` parameter. Valid params: {complaint_types}."
                f"\n\tYour param - `{captcha_type}`"
            )
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "taskId": reported_id}
        # complaint on image captcha
        if captcha_type == "image":
            answer = requests.post(incorrect_imagecaptcha_url, json=payload)
        # complaint on re-captcha
        elif captcha_type == "recaptcha":
            answer = requests.post(incorrect_recaptcha_url, json=payload)
        return answer.json()

    @staticmethod
    def get_queue_status(queue_id: int) -> dict:
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

        if queue_id not in queue_ids:
            raise ValueError(
                f"\nWrong `mode` parameter. Valid params: {queue_ids}."
                f"\n\tYour param - `{queue_id}`"
            )
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

    async def get_balance(self) -> dict:
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                get_balance_url, json={"clientKey": self.ANTICAPTCHA_KEY}
            ) as resp:
                return await resp.json()

    async def get_app_stats(self, softId: int, mode: str = "errors") -> dict:
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        if mode not in mods:
            raise ValueError(
                f"\nWrong `mode` parameter. Valid params: {mods}."
                f"\n\tYour param - `{mode}`"
            )
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "softId": softId, "mode": mode}
        async with aiohttp.ClientSession() as session:
            async with session.post(get_app_stats_url, json=payload) as resp:
                if await resp.text():
                    return await resp.json()
                else:
                    return {"errorId": 1}

    async def complaint_on_result(
        self, reported_id: int, captcha_type: str = "image"
    ) -> dict:
        f"""
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :param captcha_type: Тип капчи на который идёт жалоба. Возможные варианты:
                            {complaint_types}
        :return: Возвращает True/False, в зависимости от результата
        """
        if captcha_type not in complaint_types:
            raise ValueError(
                f"\nWrong `captcha_type` parameter. Valid params: {complaint_types}."
                f"\n\tYour param - `{captcha_type}`"
            )
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "taskId": reported_id}
        # complaint on image captcha
        if captcha_type == "image":
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    incorrect_imagecaptcha_url, json=payload
                ) as resp:
                    return await resp.json()
        # complaint on re-captcha
        elif captcha_type == "recaptcha":
            async with aiohttp.ClientSession() as session:
                async with session.post(incorrect_recaptcha_url, json=payload) as resp:
                    return await resp.json()

    @staticmethod
    async def get_queue_status(queue_id: int) -> dict:
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
        if queue_id not in queue_ids:
            raise ValueError(
                f"\nWrong `mode` parameter. Valid params: {queue_ids}."
                f"\n\tYour param - `{queue_id}`"
            )
        payload = {"queueId": queue_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(get_queue_status_url, json=payload) as resp:
                return await resp.json()
