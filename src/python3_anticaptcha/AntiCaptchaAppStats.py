import aiohttp
import requests

from python3_anticaptcha import get_app_stats_url


class AntiCaptchaAppStats:
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

    def get_stats(self, softId: int, mode: str = "errors"):
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        answer = requests.post(
            get_app_stats_url,
            json={"clientKey": self.ANTICAPTCHA_KEY, "softId": softId, "mode": mode},
            verify=False,
        )

        return answer.json()


class aioAntiCaptchaAppStats:
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

    async def get_stats(self, softId: int, mode: str = "errors"):
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                get_app_stats_url,
                json={"clientKey": self.ANTICAPTCHA_KEY, "softId": softId, "mode": mode},
            ) as resp:
                return await resp.json()
