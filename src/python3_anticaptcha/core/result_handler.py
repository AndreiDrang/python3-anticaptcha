import time
import asyncio
from urllib.parse import urljoin

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from .enum import ResponseStatusEnm
from .config import RETRIES, BASE_REQUEST_URL, GET_RESULT_POSTFIX, attempts_generator
from .serializer import GetTaskResultRequestSer, GetTaskResultResponseSer


def get_sync_result(
    result_payload: GetTaskResultRequestSer, sleep_time: int, url_response: str = GET_RESULT_POSTFIX
) -> dict:
    # create a session
    session = requests.Session()
    # set the number of attempts to connect to the server in case of error
    session.mount("http://", HTTPAdapter(max_retries=RETRIES))
    session.mount("https://", HTTPAdapter(max_retries=RETRIES))
    session.verify = False

    attempts = attempts_generator()
    for _ in attempts:
        captcha_response = GetTaskResultResponseSer(
            **session.post(url=urljoin(BASE_REQUEST_URL, url_response), json=result_payload.to_dict()).json(),
            taskId=result_payload.taskId,
        )

        if captcha_response.errorId == 0:
            if captcha_response.status == ResponseStatusEnm.processing:
                time.sleep(sleep_time)
            else:
                session.close()
        else:
            session.close()
    return captcha_response.to_dict()


async def get_async_result(result_payload: dict, sleep_time: int, url_response: str = GET_RESULT_POSTFIX) -> dict:
    attempts = attempts_generator()
    # Send request for status of captcha solution.
    async with aiohttp.ClientSession() as session:
        for _ in attempts:
            async with session.post(url=urljoin(BASE_REQUEST_URL, url_response), json=result_payload) as resp:
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
