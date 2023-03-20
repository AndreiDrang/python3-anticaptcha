import time
import asyncio
import logging
from typing import Union, Optional
from urllib import parse

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ResponseStatusEnm
from python3_anticaptcha.core.config import (
    RETRIES,
    BASE_REQUEST_URL,
    GET_RESULT_POSTFIX,
    CREATE_TASK_POSTFIX,
    attempts_generator,
)
from python3_anticaptcha.core.serializer import (
    CreateTaskRequestSer,
    CreateTaskResponseSer,
    GetTaskResultRequestSer,
    GetTaskResultResponseSer,
)


class BaseCaptcha:
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        sleep_time: int = 15,
        **kwargs,
    ):
        # validate captcha_type parameter
        if captcha_type not in CaptchaTypeEnm.list_values():
            raise ValueError(f"Invalid `captcha_type` parameter set, available - {CaptchaTypeEnm.list_values()}")
        self.__sleep_time = sleep_time

        # assign args to validator
        self._params = CreateTaskRequestSer(clientKey=api_key, **locals())
        # `task` body for task creation payload
        self.task_params = {}
        # prepare `get task result` payload
        self._get_result_params = GetTaskResultRequestSer(clientKey=api_key)

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
        self._params.task = self.task_params

        created_task = self._create_task()

        if created_task.errorId == 0:
            self._get_result_params.taskId = created_task.taskId
            return self._get_result().dict()
        return created_task.dict()

    def _create_task(self, url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self._session.post(parse.urljoin(BASE_REQUEST_URL, url_postfix), json=self._params.dict())
            if resp.status_code == 200:
                return CreateTaskResponseSer(**resp.json())
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    def _get_result(self) -> GetTaskResultResponseSer:
        """
        Method send SYNC `getTaskResult` request to service and wait for result
        """
        # initial waiting
        time.sleep(self.__sleep_time)

        attempts = attempts_generator()
        for _ in attempts:
            try:
                task_result_response = self._session.post(
                    parse.urljoin(BASE_REQUEST_URL, GET_RESULT_POSTFIX), json=self._get_result_params.dict()
                )
                if task_result_response.status_code == 200:
                    task_result_data = GetTaskResultResponseSer(**task_result_response.json())

                    if task_result_data.errorId == 0:
                        if task_result_data.status == ResponseStatusEnm.processing:
                            time.sleep(self.__sleep_time)
                        else:
                            task_result_data.taskId = self._get_result_params.taskId
                            return task_result_data
                    else:
                        task_result_data.taskId = self._get_result_params.taskId
                        return task_result_data
                else:
                    raise ValueError(task_result_response.raise_for_status())
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

    """
    Async part
    """

    async def _aio_processing_captcha(self) -> dict:
        # added task params to payload
        self._params.task = self.task_params

        created_task = await self._aio_create_task()

        if created_task.errorId == 0:
            self._get_result_params.taskId = created_task.taskId
            result = await self._aio_get_result()
            return result.dict()
        return created_task.dict()

    async def _aio_create_task(self, url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(parse.urljoin(BASE_REQUEST_URL, url_postfix), json=self._params.dict()) as resp:
                    if resp.status == 200:
                        return CreateTaskResponseSer(**await resp.json())
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    async def _aio_get_result(self) -> GetTaskResultResponseSer:
        """
        Method send SYNC `getTaskResult` request to service and wait for result
        """
        # initial waiting
        await asyncio.sleep(self.__sleep_time)

        attempts = attempts_generator()
        async with aiohttp.ClientSession() as session:
            for _ in attempts:
                try:
                    async with session.post(
                        parse.urljoin(BASE_REQUEST_URL, GET_RESULT_POSTFIX),
                        json=self._get_result_params.dict(),
                    ) as task_result_response:
                        if task_result_response.status == 200:
                            task_result_data = GetTaskResultResponseSer(**await task_result_response.json())

                            if task_result_data.errorId == 0:
                                if task_result_data.status == ResponseStatusEnm.processing:
                                    time.sleep(self.__sleep_time)
                                else:
                                    task_result_data.taskId = self._get_result_params.taskId
                                    return task_result_data
                            else:
                                task_result_data.taskId = self._get_result_params.taskId
                                return task_result_data
                        else:
                            raise ValueError(task_result_response.raise_for_status())
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
