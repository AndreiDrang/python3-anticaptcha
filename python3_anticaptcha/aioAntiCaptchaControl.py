import aiohttp
import asyncio

from .config import get_balance_url, incorrect_captcha_url


class AntiCaptchaControl:
    def __init__(self, anticaptcha_key):
        self.ANTICAPTCHA_KEY = anticaptcha_key

    def get_balance(self):
        '''
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        '''
        loop = asyncio.get_event_loop()
        server_answer = loop.run_until_complete(self.aio_get_balance())
        loop.close()
        
        return server_answer
        
    async def aio_get_balance(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(get_balance_url, json={'clientKey': self.ANTICAPTCHA_KEY}) as resp:
                return await resp.json()

    def complaint_on_result(self, reported_id):
        '''
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :return: Возвращает True/False, в зависимости от результата
        '''
        loop = asyncio.get_event_loop()
        server_answer = loop.run_until_complete(self.aio_complaint_on_result(reported_id))
        loop.close()
        
        if server_answer['errorId'] == 0:
            return True
        else:
            return False

        
    async def aio_complaint_on_result(self, reported_id):
        payload = {'clientKey': self.ANTICAPTCHA_KEY,
                   'taskId': reported_id,
                   }
        async with aiohttp.ClientSession() as session:
            async with session.post(incorrect_captcha_url, json=payload) as resp:
                return await resp.json()
