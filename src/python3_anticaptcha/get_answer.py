import time
import asyncio

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from python3_anticaptcha.config import get_result_url, attempts_generator


def get_sync_result(result_payload: dict, sleep_time: int, **kwargs) -> dict:
    # create a session
    session = requests.Session()
    # set the number of attempts to connect to the server in case of error
    session.mount("http://", HTTPAdapter(max_retries=5))
    session.mount("https://", HTTPAdapter(max_retries=5))
    session.verify = False

    attempts = attempts_generator()
    for _ in attempts:
        captcha_response = session.post(get_result_url, json=result_payload, **kwargs).json()

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
    attempts = attempts_generator()
    # Send request for status of captcha solution.
    async with aiohttp.ClientSession() as session:
        for _ in attempts:
            async with session.post(get_result_url, json=result_payload) as resp:
                json_result = await resp.json()
                # if there is no error, check CAPTCHA status
                if json_result["errorId"] == 0:
                    # If not yet resolved, wait
                    if json_result["status"] == "processing":
                        await asyncio.sleep(sleep_time)
                    # otherwise return response
                    else:
                        json_result.update({"taskId": result_payload["taskId"]})
                        return json_result
                else:
                    json_result.update({"taskId": result_payload["taskId"]})
                    return json_result
