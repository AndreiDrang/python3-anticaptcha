from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm

__all__ = ("Altcha",)


class Altcha(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        challengeURL: Optional[str] = None,
        challengeJSON: Optional[str] = None,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        sleep_time: Optional[int] = 10,
    ):
        """
        The class is used to work with Altcha.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of the webpage
            challengeURL: Full URL to the challenge page (use either challengeURL or challengeJSON)
            challengeJSON: JSON-encoded challenge data string (use either challengeURL or challengeJSON)
            proxyType: Type of the proxy
            proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                            host names instead of IPs,
                            transparent proxies (where client IP is visible),
                            proxies from local networks (192.., 10.., 127...)
            proxyPort: Proxy port.
            proxyLogin: Proxy login.
            proxyPassword: Proxy password.
            userAgent: Browser UserAgent.
            sleep_time: The waiting time between requests to get the result of the Captcha

        Examples:
            >>> Altcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="AltchaTaskProxyless",
            ...         websiteURL="https://example.com/",
            ...         challengeURL="/api/challenge"
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

            >>> await Altcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="AltchaTaskProxyless",
            ...         websiteURL="https://example.com/",
            ...         challengeJSON='{"algorithm":"SHA-256","challenge":"..."}'
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

            >>> Altcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="AltchaTask",
            ...         websiteURL="https://example.com/",
            ...         challengeURL="/api/challenge",
            ...         proxyType="http",
            ...         proxyAddress="1.2.3.4",
            ...         proxyPort=8080
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
            https://anti-captcha.com/apidoc/task-types/AltchaTask

            https://anti-captcha.com/apidoc/task-types/AltchaTaskProxyless
        """

        super().__init__(api_key=api_key, sleep_time=sleep_time)

        # validation of the received parameters
        if captcha_type == CaptchaTypeEnm.AltchaTask:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                challengeURL=challengeURL,
                challengeJSON=challengeJSON,
                proxyType=proxyType,
                proxyAddress=proxyAddress,
                proxyPort=proxyPort,
                proxyLogin=proxyLogin,
                proxyPassword=proxyPassword,
                userAgent=userAgent,
            )
        elif captcha_type == CaptchaTypeEnm.AltchaTaskProxyless:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                challengeURL=challengeURL,
                challengeJSON=challengeJSON,
            )
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`, \
                available - {CaptchaTypeEnm.AltchaTaskProxyless.value, CaptchaTypeEnm.AltchaTask.value}"
            )
