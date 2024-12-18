from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm, SaveFormatsEnm
from .core.aio_captcha_instrument import AIOCaptchaInstrument
from .core.sio_captcha_instrument import SIOCaptchaInstrument

__all__ = ("ImageToCoordinates",)


class ImageToCoordinates(CaptchaParams):

    def __init__(
        self,
        api_key: str,
        comment: Optional[str] = None,
        mode: str = "points",
        websiteURL: Optional[str] = None,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.ImageToCoordinatesTask,
        sleep_time: int = 5,
        save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        img_path: str = "PythonAntiCaptchaImages",
    ):
        """
        The class is used to work with ImageToTextTask.

        Args:
            api_key: Capsolver API key
            comment: Comments for the task in English characters only.
                        Example: "Select objects in specified order" or "select all cars".
            mode: Task mode, can be "points" or "rectangles". The default is "points".
            websiteURL: Optional parameter to distinguish source of image captchas in spending statistics.
            captcha_type: Captcha type
            sleep_time: The waiting time between requests to get the result of the Captcha
            save_format: Image save format - temporary or persistance
            img_clearing: True - delete file after solution, False - don't delete file after solution
            img_path: Folder to save captcha images

        Examples:
            >>> ImageToCoordinates(api_key="99d7d111a0111dc11184111c8bb111da",
            ...                     save_format=SaveFormatsEnm.CONST,
            ...                     comment="select all cars",
            ...                     mode="rectangles",
            ...                     websiteURL="https://some-website.xyz/"
            ...        ).captcha_handler(captcha_file='files/captcha-image.jpg')
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "coordinates":[
                        [17,48,54,83],
                        [76,93,140,164]
                    ]
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> ImageToCoordinates(api_key="99d7d111a0111dc11184111c8bb111da",
            ...                     save_format=SaveFormatsEnm.CONST,
            ...                     comment="select 3 cats",
            ...                     mode="points",
            ...                     websiteURL="https://some-website.xyz/"
            ...        ).captcha_handler(captcha_link='https://........../captcha-image.jpg')
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "coordinates":[
                        [17,48,54,83],
                        [76,93,140,164]
                    ]
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> await ImageToCoordinates(api_key="99d7d111a0111dc11184111c8bb111da",
            ...                     save_format=SaveFormatsEnm.TEMP,
            ...                     comment="select 3 cats",
            ...                     mode="points",
            ...                     websiteURL="https://some-website.xyz/"
            ...        ).aio_captcha_handler(captcha_link='https://........../captcha-image.jpg')
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "coordinates":[
                        [17,48,54,83],
                        [76,93,140,164]
                    ]
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }


        Notes:
            https://anti-captcha.com/apidoc/task-types/ImageToCoordinatesTask
        """

        super().__init__(api_key=api_key, sleep_time=sleep_time)

        self.save_format = save_format
        self.img_clearing = img_clearing
        self.img_path = img_path

        self.task_params = dict(
            type=captcha_type,
            comment=comment,
            mode=mode,
            websiteURL=websiteURL,
        )

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

        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.processing_image_captcha(
            save_format=self.save_format,
            img_clearing=self.img_clearing,
            img_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
        )

    async def aio_captcha_handler(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **additional_params,
    ) -> dict:
        """
        Asynchronous method for captcha solving

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

        self._captcha_handling_instrument = AIOCaptchaInstrument(captcha_params=self)
        return await self._captcha_handling_instrument.processing_image_captcha(
            save_format=self.save_format,
            img_clearing=self.img_clearing,
            img_path=self.img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
        )
