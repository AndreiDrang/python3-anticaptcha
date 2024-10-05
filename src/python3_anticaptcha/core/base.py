import os
import time
import uuid
import base64
import asyncio
import logging
from typing import Optional
from urllib import parse
from pathlib import Path

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from .enum import SaveFormatsEnm
from .config import RETRIES, ASYNC_RETRIES, BASE_REQUEST_URL, CREATE_TASK_POSTFIX
from .serializer import CreateTaskBaseSer, CreateTaskResponseSer, GetTaskResultRequestSer, GetTaskResultResponseSer
from .result_handler import get_sync_result, get_async_result

__all__ = ("BaseCaptcha",)


class BaseCaptcha:
    NO_CAPTCHA_ERR = "You did not send any file, local link or URL."
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(self, api_key: str, sleep_time: int = 15):
        self.__sleep_time = sleep_time

        # assign args to validator
        self.create_task_payload = CreateTaskBaseSer(clientKey=api_key)
        # `task` body for task creation payload
        self.task_params = {}
        # prepare `get task result` payload
        self._get_result_params = GetTaskResultRequestSer(clientKey=api_key)
        self.result = GetTaskResultResponseSer()

        # prepare session
        self._session = requests.Session()
        self._session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self._session.mount("https://", HTTPAdapter(max_retries=RETRIES))
        self._session.verify = False

    """
    Sync part
    """

    def _processing_captcha(self) -> dict:
        # added task params to payload
        self.create_task_payload.task.update(self.task_params)

        created_task = self._create_task()

        if created_task.errorId == 0:
            self._get_result_params.taskId = created_task.taskId
        else:
            return created_task.to_dict()

        time.sleep(self.__sleep_time)

        return get_sync_result(result_payload=self._get_result_params, sleep_time=self.__sleep_time)

    def _create_task(self, url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self._session.post(
                parse.urljoin(BASE_REQUEST_URL, url_postfix), json=self.create_task_payload.to_dict()
            )
            if resp.status_code == 200:
                return CreateTaskResponseSer(**resp.json())
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    @staticmethod
    def _send_post_request(
        payload: Optional[dict] = None,
        session: requests.Session = requests.Session(),
        url_postfix: str = CREATE_TASK_POSTFIX,
    ) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = session.post(parse.urljoin(BASE_REQUEST_URL, url_postfix), json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    def url_open(self, url: str, **kwargs):
        """
        Method open links
        """
        return self._session.get(url=url, **kwargs)

    @staticmethod
    def _local_file_captcha(captcha_file: str):
        """
        Method get local file, read it and prepare for sending to Captcha solving service
        """
        with open(captcha_file, "rb") as file:
            return file.read()

    def _file_const_saver(self, content: bytes, file_path: str, file_extension: str = "png"):
        """
        Method create and save file in folder
        """
        Path(file_path).mkdir(parents=True, exist_ok=True)

        # generate image name
        self._file_name = f"file-{uuid.uuid4()}.{file_extension}"

        # save image to folder
        with open(os.path.join(file_path, self._file_name), "wb") as out_image:
            out_image.write(content)

    def _body_file_processing(
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
                content = self.url_open(url=captcha_link, **kwargs).content
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

    """
    Async part
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

        return await get_async_result(result_payload=self._get_result_params.to_dict(), sleep_time=self.__sleep_time)

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

    # Context methods

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True
