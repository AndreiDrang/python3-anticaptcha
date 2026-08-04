import os
import shutil
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

    @staticmethod
    def _file_const_saver(content: bytes, file_path: str, file_extension: str = "png") -> str:
        """
        Method create and save file in folder
        """
        Path(file_path).mkdir(parents=True, exist_ok=True)

        # generate image name
        file_name = f"file-{uuid.uuid4()}.{file_extension}"

        full_file_path = os.path.join(file_path, file_name)

        # save image to folder
        with open(full_file_path, "wb") as out_image:
            out_image.write(content)
        return full_file_path

    @staticmethod
    def _file_clean(full_file_path: str):
        # The path handed in may be either a single saved image file (the
        # common img_clearing case) or a directory tree; handle both so that
        # clearing actually removes the artifact from disk.
        if os.path.isdir(full_file_path):
            shutil.rmtree(full_file_path, ignore_errors=True)
        else:
            try:
                os.remove(full_file_path)
            except OSError:
                pass


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
