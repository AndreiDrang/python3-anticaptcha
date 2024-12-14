import base64
import asyncio
import logging
from typing import Optional
from urllib import parse
from urllib.parse import urljoin

import aiohttp

from .enum import SaveFormatsEnm
from .const import ASYNC_RETRIES, BASE_REQUEST_URL, GET_RESULT_POSTFIX, CREATE_TASK_POSTFIX, attempts_generator
from .serializer import CreateTaskResponseSer

__all__ = ("AIOCaptchaHandler",)

from .base import BaseCaptcha


class AIOCaptchaHandler(BaseCaptcha):
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    async def aio_url_read(self, url: str, **kwargs) -> bytes:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()

    async def _aio_processing_captcha(self) -> dict:
        # added task params to payload
        self.create_task_payload.task.update(self.task_params)

        created_task = await self._aio_create_task()

        if created_task.errorId == 0:
            self._get_result_params.taskId = created_task.taskId
        else:
            return created_task.to_dict()

        await asyncio.sleep(self.__sleep_time)

        return await self.get_async_result()

    async def _aio_create_task(self, url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(BASE_REQUEST_URL, url_postfix), json=self.create_task_payload.to_dict()
                ) as resp:
                    if resp.status == 200:
                        return CreateTaskResponseSer(**await resp.json())
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    @staticmethod
    async def _aio_send_post_request(payload: Optional[dict] = None, url_postfix: str = CREATE_TASK_POSTFIX) -> dict:
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

    async def _aio_body_file_processing(
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
            self.create_task_payload.task.update(
                {"body": base64.b64encode(self._local_file_captcha(captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.create_task_payload.task.update({"body": base64.b64encode(captcha_base64).decode("utf-8")})
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self.aio_url_read(url=captcha_link, **kwargs)
                # according to the value of the passed parameter, select the function to save the image
                if save_format == SaveFormatsEnm.CONST.value:
                    self._file_const_saver(content, file_path, file_extension=file_extension)
                self.create_task_payload.task.update({"body": base64.b64encode(content).decode("utf-8")})
            except Exception as error:
                self.result.errorId = 12
                self.result.errorCode = self.NO_CAPTCHA_ERR
                self.result.errorDescription = str(error)

        else:
            self.result.errorId = 12
            self.result.errorCode = self.NO_CAPTCHA_ERR

    async def get_async_result(self, url_response: str = GET_RESULT_POSTFIX) -> dict:
        attempts = attempts_generator()
        # Send request for status of captcha solution.
        async with aiohttp.ClientSession() as session:
            for _ in attempts:
                async with session.post(
                    url=urljoin(BASE_REQUEST_URL, url_response), json=self._get_result_params.to_dict()
                ) as resp:
                    json_result = await resp.json()
                    # if there is no error, check CAPTCHA status
                    if json_result["errorId"] == 0:
                        # If not yet resolved, wait
                        if json_result["status"] == "processing":
                            await asyncio.sleep(self.__sleep_time)
                        # otherwise return response
                        else:
                            json_result.update({"taskId": self._get_result_params.taskId})
                            return json_result
                    else:
                        json_result.update({"taskId": self._get_result_params.taskId})
                        return json_result

    # Context methods
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True
