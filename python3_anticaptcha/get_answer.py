import time
import asyncio

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from python3_anticaptcha import get_result_url


def get_sync_result(result_payload: dict, sleep_time: int) -> dict:
    # создаём сессию
    session = requests.Session()
    # выставляем кол-во попыток подключения к серверу при ошибке
    session.mount("http://", HTTPAdapter(max_retries=5))
    session.mount("https://", HTTPAdapter(max_retries=5))
    session.verify = False

    while True:
        captcha_response = session.post(get_result_url, json=result_payload).json()

        if captcha_response["errorId"] == 0:
            if captcha_response["status"] == "processing":
                time.sleep(sleep_time)
            else:
                captcha_response.update({"taskId": result_payload["taskId"]})
                session.close()
                return captcha_response
        else:
            captcha_response.update({"taskId": result_payload["taskId"]})
            session.close()
            return captcha_response


async def get_async_result(result_payload: dict, sleep_time: int) -> dict:
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
                        json_result.update({"taskId": result_payload["taskId"]})
                        return json_result
                else:
                    json_result.update({"taskId": result_payload["taskId"]})
                    return json_result
