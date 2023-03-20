from typing import Union, Optional

from .core.base import BaseCaptcha
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm
from .core.serializer import TurnstileOptionsSer, TurnstileProxylessOptionsSer


class Turnstile(BaseCaptcha):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        sleep_time: Optional[int] = 10,
        **kwargs,
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
            sleep_time: The waiting time between requests to get the result of the Captcha
            kwargs: Additional not required params for main request body.
                    Like `callbackUrl`/`languagePool` and etc.
                    More info - https://anti-captcha.com/apidoc/methods/createTask

        Examples:
            >>> Turnstile(api_key="99d7d111a0111dc11184111c8bb111da",
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

            >>> await Turnstile(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="TurnstileTaskProxyless",
            ...         websiteURL="https://rucaptcha.com/demo/cloudflare-turnstile",
            ...         websiteKey="0x4AAAAAAAC3DHQFLr1GavRN"
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
            ...         captcha_type="TurnstileTaskProxyless",
            ...         websiteURL="https://rucaptcha.com/demo/cloudflare-turnstile",
            ...         websiteKey="0x4AAAAAAAC3DHQFLr1GavRN",
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
            ...         captcha_type="TurnstileTaskProxyless",
            ...         websiteURL="https://rucaptcha.com/demo/cloudflare-turnstile",
            ...         websiteKey="0x4AAAAAAAC3DHQFLr1GavRN",
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

        super().__init__(api_key=api_key, captcha_type=captcha_type, sleep_time=sleep_time, **kwargs)

        # validation of the received parameters
        if captcha_type == CaptchaTypeEnm.TurnstileTask:
            self.task_params = TurnstileOptionsSer(type=captcha_type, **locals()).dict()
        elif captcha_type == CaptchaTypeEnm.TurnstileTaskProxyless:
            self.task_params = TurnstileProxylessOptionsSer(type=captcha_type, **locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {CaptchaTypeEnm.TurnstileTask.value, CaptchaTypeEnm.TurnstileTaskProxyless.value}"""
            )

    def captcha_handler(self, **additional_params) -> dict:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyLogin``, ``proxyPassword`` and etc. - more info in service docs

        Returns:
            Full service response

        Notes:
            Check class docstirng for more info
        """

        self.task_params.update({**additional_params})
        return self._processing_captcha()

    async def aio_captcha_handler(self, **additional_params) -> dict:
        """
        Asynchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyLogin``, ``proxyPassword`` and etc. - more info in service docs

        Returns:
            Full service response

        Notes:
            Check class docstirng for more info
        """

        self.task_params.update({**additional_params})
        return await self._aio_processing_captcha()
