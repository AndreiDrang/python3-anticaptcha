import os
import uuid
from pathlib import Path

from .serializer import CreateTaskBaseSer, GetTaskResultRequestSer, GetTaskResultResponseSer
from .context_instr import AIOContextManager, SIOContextManager

__all__ = ("CaptchaParams", "CaptchaHandler")


class CaptchaParams(SIOContextManager, AIOContextManager):
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        sleep_time: The waiting time between requests to get the result of the Captcha
    """

    def __init__(self, api_key: str, sleep_time: int = 15, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_time = sleep_time

        # assign args to validator
        self.create_task_payload = CreateTaskBaseSer(clientKey=api_key)
        # `task` body for task creation payload
        self.task_params = {}
        # prepare `get task result` payload
        self.get_result_params = GetTaskResultRequestSer(clientKey=api_key)


class CaptchaHandler:
    NO_CAPTCHA_ERR = "You did not send any file, local link or URL."
    result = GetTaskResultResponseSer()
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

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
        self.file_name = f"file-{uuid.uuid4()}.{file_extension}"

        # save image to folder
        with open(os.path.join(file_path, self.file_name), "wb") as out_image:
            out_image.write(content)
