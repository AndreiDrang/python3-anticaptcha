import base64
import asyncio
import logging
from typing import Optional
from urllib import parse
from urllib.parse import urljoin

import aiohttp

from .base import CaptchaParams, CaptchaHandler
from .enum import SaveFormatsEnm
from .const import ASYNC_RETRIES, BASE_REQUEST_URL, GET_RESULT_POSTFIX, CREATE_TASK_POSTFIX
from .utils import attempts_generator
from .serializer import CreateTaskResponseSer

__all__ = ("AIOCaptchaHandler",)


class AIOCaptchaHandler(CaptchaHandler):
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        sleep_time: The waiting time between requests to get the result of the Captcha
    """

    def __init__(self, captcha_params: CaptchaParams):
        super().__init__()
        self.captcha_params = captcha_params

    async def processing_captcha(self) -> dict:
        # added task params to payload
        self.captcha_params.create_task_payload.task.update(self.captcha_params.task_params)

        created_task = await self._create_task()

        if created_task.errorId == 0:
            self.captcha_params.get_result_params.taskId = created_task.taskId
        else:
            return created_task.to_dict()

        await asyncio.sleep(self.captcha_params.sleep_time)

        return await self._get_result()

    async def body_file_processing(
        self,
        save_format: SaveFormatsEnm,
        file_path: str,
        file_extension: str = "png",
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ):
        # if a local file link is passed
        if captcha_file:
            self.captcha_params.create_task_payload.task.update(
                {"body": base64.b64encode(self._local_file_captcha(captcha_file=captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.captcha_params.create_task_payload.task.update(
                {"body": base64.b64encode(captcha_base64).decode("utf-8")}
            )
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self._url_read(url=captcha_link, **kwargs)
                # according to the value of the passed parameter, select the function to save the image
                if save_format == SaveFormatsEnm.CONST.value:
                    self._file_const_saver(content, file_path, file_extension=file_extension)
                self.captcha_params.create_task_payload.task.update({"body": base64.b64encode(content).decode("utf-8")})
            except Exception as error:
                self.result.errorId = 12
                self.result.errorCode = self.NO_CAPTCHA_ERR
                self.result.errorDescription = str(error)

        else:
            self.result.errorId = 12
            self.result.errorCode = self.NO_CAPTCHA_ERR

    async def _url_read(self, url: str, **kwargs) -> bytes:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()

    async def _create_task(self, url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(BASE_REQUEST_URL, url_postfix), json=self.captcha_params.create_task_payload.to_dict()
                ) as resp:
                    if resp.status == 200:
                        return CreateTaskResponseSer(**await resp.json())
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    @staticmethod
    async def send_post_request(payload: Optional[dict] = None, url_postfix: str = CREATE_TASK_POSTFIX) -> dict:
        """
        Function send ASYNC request to service and wait for result
        """

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(parse.urljoin(BASE_REQUEST_URL, url_postfix), json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    async def _get_result(self, url_response: str = GET_RESULT_POSTFIX) -> dict:
        attempts = attempts_generator()
        # Send request for status of captcha solution.
        async with aiohttp.ClientSession() as session:
            for _ in attempts:
                async with session.post(
                    url=urljoin(BASE_REQUEST_URL, url_response), json=self.captcha_params.get_result_params.to_dict()
                ) as resp:
                    json_result = await resp.json()
                    # if there is no error, check CAPTCHA status
                    if json_result["errorId"] == 0:
                        # If not yet resolved, wait
                        if json_result["status"] == "processing":
                            await asyncio.sleep(self.captcha_params.sleep_time)
                        # otherwise return response
                        else:
                            json_result.update({"taskId": self.captcha_params.get_result_params.taskId})
                            return json_result
                    else:
                        json_result.update({"taskId": self.captcha_params.get_result_params.taskId})
                        return json_result
