import requests
import aiohttp

from .config import get_balance_url, incorrect_captcha_url


class AntiCaptchaControl:
    def __init__(self, anticaptcha_key):
        """
        Синхронный метод работы с балансом и жалобами
        :param anticaptcha_key: Ключ антикапчи
        """
        self.ANTICAPTCHA_KEY = anticaptcha_key

    def get_balance(self):
        '''
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        '''
        answer = requests.post(get_balance_url, json = {'clientKey': self.ANTICAPTCHA_KEY})

        return answer.json()

    def complaint_on_result(self, reported_id):
        '''
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :return: Возвращает True/False, в зависимости от результата
        '''
        payload = {'clientKey': self.ANTICAPTCHA_KEY,
                   'taskId': reported_id,
                   }

        answer = requests.post(incorrect_captcha_url, json = payload)

        return answer.json()


class aioAntiCaptchaControl:
    def __init__(self, anticaptcha_key):
        """
        Асинхронный метод работы с балансом и жалобами
        :param anticaptcha_key: Ключ антикапчи
        """
        self.ANTICAPTCHA_KEY = anticaptcha_key

    async def get_balance(self):
        '''
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        '''
        async with aiohttp.ClientSession() as session:
            async with session.post(get_balance_url, json={'clientKey': self.ANTICAPTCHA_KEY}) as resp:
                return await resp.json()

    async def complaint_on_result(self, reported_id):
        '''
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :return: Возвращает True/False, в зависимости от результата
        '''
        payload = {'clientKey': self.ANTICAPTCHA_KEY,
                   'taskId': reported_id,
                   }
        async with aiohttp.ClientSession() as session:
            async with session.post(incorrect_captcha_url, json=payload) as resp:
                return await resp.json()