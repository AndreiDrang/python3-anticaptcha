import os
import uuid
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter

from .const import RETRIES
from .serializer import CreateTaskBaseSer, GetTaskResultRequestSer, GetTaskResultResponseSer

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
