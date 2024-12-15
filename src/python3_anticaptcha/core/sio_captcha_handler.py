import time
import base64
import logging
from typing import Optional
from urllib import parse
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter

from .base import CaptchaParams, CaptchaHandler
from .enum import SaveFormatsEnm, ResponseStatusEnm
from .const import RETRIES, BASE_REQUEST_URL, GET_RESULT_POSTFIX, CREATE_TASK_POSTFIX
from .utils import attempts_generator
from .serializer import CreateTaskResponseSer, GetTaskResultResponseSer

__all__ = ("SIOCaptchaHandler",)


class SIOCaptchaHandler(CaptchaHandler):
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        sleep_time: The waiting time between requests to get the result of the Captcha
    """

    def __init__(self, captcha_params: CaptchaParams):
        super().__init__()
        self.captcha_params = captcha_params
        # prepare session
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))
        self.session.verify = False

    def processing_captcha(self) -> dict:
        # added task params to payload
        self.captcha_params.create_task_payload.task.update(self.captcha_params.task_params)

        created_task = self._create_task()

        if created_task.errorId == 0:
            self.captcha_params.get_result_params.taskId = created_task.taskId
        else:
            return created_task.to_dict()

        time.sleep(self.captcha_params.sleep_time)

        return self._get_result()

    def body_file_processing(
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
                content = self._url_read(url=captcha_link, **kwargs).content
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

    def _create_task(self, url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self.session.post(
                parse.urljoin(BASE_REQUEST_URL, url_postfix), json=self.captcha_params.create_task_payload.to_dict()
            )
            if resp.status_code == 200:
                return CreateTaskResponseSer(**resp.json())
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    @staticmethod
    def send_post_request(
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

    def _url_read(self, url: str, **kwargs):
        """
        Method open links
        """
        return self.session.get(url=url, **kwargs)

    def _get_result(self, url_response: str = GET_RESULT_POSTFIX) -> dict:
        attempts = attempts_generator()
        for _ in attempts:
            captcha_response = GetTaskResultResponseSer(
                **self.session.post(
                    url=urljoin(BASE_REQUEST_URL, url_response), json=self.captcha_params.get_result_params.to_dict()
                ).json(),
                taskId=self.captcha_params.get_result_params.taskId,
            )

            if captcha_response.errorId == 0:
                if captcha_response.status == ResponseStatusEnm.processing:
                    time.sleep(self.captcha_params.sleep_time)
                else:
                    self.session.close()
            else:
                self.session.close()
        return captcha_response.to_dict()
