import os
import uuid
from pathlib import Path

from .serializer import GetTaskResultResponseSer

__all__ = ("CaptchaInstrument",)


class FileInstrument:
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


class CaptchaInstrument(FileInstrument):
    NO_CAPTCHA_ERR = "You did not send any file, local link or URL."
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(self):
        self.result = GetTaskResultResponseSer()
