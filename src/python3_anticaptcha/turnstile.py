from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm
from .core.aio_captcha_handler import AIOCaptchaHandler
from .core.sio_captcha_handler import SIOCaptchaHandler


class Turnstile(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        action: Optional[str] = None,
        turnstileCData: Optional[str] = None,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        sleep_time: Optional[int] = 10,
    ):
        """
        The class is used to work with Turnstile.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of the webpage
            websiteKey: Turnstile sitekey
            proxyType: Type of the proxy
            proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                            host names instead of IPs,
                            transparent proxies (where client IP is visible),
                            proxies from local networks (192.., 10.., 127...)
            proxyPort: Proxy port.
            proxyLogin: Proxy login.
            proxyPassword: Proxy password.
            sleep_time: The waiting time between requests to get the result of the Captcha

        Examples:
            >>> Turnstile(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="TurnstileTaskProxyless",
            ...         websiteURL="https://demo.turnstile.workers.dev/",
            ...         websiteKey="1x00000000000000000000AA"
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

            >>> await Turnstile(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="TurnstileTaskProxyless",
            ...         websiteURL="https://demo.turnstile.workers.dev/",
            ...         websiteKey="1x00000000000000000000AA"
            ...        ).aio_captcha_handler()
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

            >>> Turnstile(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="TurnstileTask",
            ...         websiteURL="https://demo.turnstile.workers.dev/",
            ...         websiteKey="1x00000000000000000000AA",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9988,
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

            >>> Turnstile(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="TurnstileTask",
            ...         websiteURL="https://demo.turnstile.workers.dev/",
            ...         websiteKey="1x00000000000000000000AA",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9988
            ...        ).captcha_handler(proxyLogin="some_login",
            ...                         proxyPassword="some_strong_password")
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
            https://anti-captcha.com/apidoc/task-types/TurnstileTask

            https://anti-captcha.com/apidoc/task-types/TurnstileTaskProxyless
        """

        super().__init__(api_key=api_key, sleep_time=sleep_time)

        # validation of the received parameters
        if captcha_type == CaptchaTypeEnm.TurnstileTask:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                websiteKey=websiteKey,
                action=action,
                turnstileCData=turnstileCData,
                proxyType=proxyType,
                proxyAddress=proxyAddress,
                proxyPort=proxyPort,
                proxyLogin=proxyLogin,
                proxyPassword=proxyPassword,
            )
        elif captcha_type == CaptchaTypeEnm.TurnstileTaskProxyless:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                websiteKey=websiteKey,
                action=action,
                turnstileCData=turnstileCData,
            )
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`, \
                available - {CaptchaTypeEnm.TurnstileTaskProxyless.value,CaptchaTypeEnm.TurnstileTask.value}"
            )

    def captcha_handler(self, **additional_params) -> dict:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyLogin``, ``proxyPassword`` and etc. - more info in service docs

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """

        self.task_params.update({**additional_params})
        self._captcha_handling_instrument = SIOCaptchaHandler(captcha_params=self)
        return self._captcha_handling_instrument.processing_captcha()

    async def aio_captcha_handler(self, **additional_params) -> dict:
        """
        Asynchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyLogin``, ``proxyPassword`` and etc. - more info in service docs

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """

        self.task_params.update({**additional_params})
        self._captcha_handling_instrument = AIOCaptchaHandler(captcha_params=self)
        return await self._captcha_handling_instrument.processing_captcha()
