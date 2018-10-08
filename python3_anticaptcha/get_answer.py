import requests
import aiohttp
import asyncio
import time

from requests.adapters import HTTPAdapter

from .config import get_result_url


def get_sync_result(result_payload: dict, sleep_time: int):
    # создаём сессию
    session = requests.Session()
    # выставляем кол-во попыток подключения к серверу при ошибке
    session.mount('http://', HTTPAdapter(max_retries = 5))
    session.mount('https://', HTTPAdapter(max_retries = 5))

    while True:
        captcha_response = session.post(get_result_url, json=result_payload)

        if captcha_response.json()["errorId"] == 0:
            if captcha_response.json()["status"] == "processing":
                time.sleep(sleep_time)
            else:
                return captcha_response.json()
        else:
            return captcha_response.json()


async def get_async_result(result_payload: dict, sleep_time: int):
    # Отправляем запрос на статус решения капчи.
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.post(get_result_url, json=result_payload) as resp:
                json_result = await resp.json()
                # Если нет ошибки - проверяем статус капчи
                if json_result["errorId"] == 0:
                    # Если еще не решена, ожидаем
                    if json_result["status"] == "processing":
                        await asyncio.sleep(sleep_time)
                    # Иначе возвращаем ответ
                    else:
                        return json_result
                else:
                    return json_result
