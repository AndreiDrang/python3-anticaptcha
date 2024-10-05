import shutil
from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enum import CaptchaTypeEnm, SaveFormatsEnm

SAVE_FORMATS = ("const", "temp")


class ImageToTextCaptcha(BaseCaptcha):

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.ImageToTextTask,
        sleep_time: int = 5,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        img_path: str = "PythonAntiCaptchaImages",
    ):
        """
        The class is used to work with ImageToTextTask.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            sleep_time: The waiting time between requests to get the result of the Captcha
            save_format: Image save format - temporary or persistance
            img_clearing: True - delete file after solution, False - don't delete file after solution
            img_path: Folder to save captcha images

        Examples:
            >>> ImageToTextCaptcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="TurnstileTaskProxyless",
            ...         websiteURL="https://rucaptcha.com/demo/cloudflare-turnstile",
            ...         websiteKey="0x4AAAAAAAC3DHQFLr1GavRN"
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "token":"0.Qz0.....f1",
                  "userAgent":"Mozilla/.....36"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

        Notes:
            https://anti-captcha.com/apidoc/task-types/ImageToTextTask
        """

        super().__init__(api_key=api_key, sleep_time=sleep_time)

        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path

        self.task_params = dict(type=captcha_type)

    def captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **additional_params,
    ) -> dict:
        """
        Synchronous method for captcha solving

        Args:
            captcha_link: link to captcha image file
            captcha_file: path to local captcha image file
            captcha_base64: captcha image encoded in base64 format
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyLogin``, ``proxyPassword`` and etc. - more info in service docs

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """

        self.task_params.update({**additional_params})
        self._body_file_processing(
            save_format=self.save_format,
            file_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
        )
        if not self.result.errorId:
            return self._processing_captcha()
        return self.result.to_dict()

    def __del__(self):
        if self.save_format == SaveFormatsEnm.CONST.value and self.img_clearing:
            shutil.rmtree(self.img_path, ignore_errors=True)