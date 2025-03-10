from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm

__all__ = ("FriendlyCaptcha",)


class FriendlyCaptcha(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        websiteURL: str,
        websiteKey: str,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.FriendlyCaptchaTaskProxyless,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        sleep_time: Optional[int] = 10,
    ):
        """
        The class is used to work with FriendlyCaptcha.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of the webpage
            websiteKey: Friendly Captcha sitekey
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
            >>> FriendlyCaptcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="FriendlyCaptchaTaskProxyless",
            ...         websiteURL="https://demo.arkoselabs.com",
            ...         websiteKey="FCMDESUD3M34857N"
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "token":"0.Qz0.....f1",
                  "userAgent":"Mozilla/5.0 (Wind.....",
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> await FriendlyCaptcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="FriendlyCaptchaTaskProxyless",
            ...         websiteURL="https://demo.arkoselabs.com",
            ...         websitePublicKey="DF9C4D87-CB7B-4062-9FEB-BADB6ADA61E6"
            ...        ).aio_captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "token":"0.Qz0.....f1",
                  "userAgent":"Mozilla/5.0 (Wind.....",
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> FriendlyCaptcha(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="FriendlyCaptchaTask",
            ...         websiteURL="https://demo.arkoselabs.com",
            ...         websitePublicKey="DF9C4D87-CB7B-4062-9FEB-BADB6ADA61E6",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9988,
            ...         proxyLogin="proxy_login",
            ...         proxyPassword="proxy_password",
            ...         userAgent="some_real_user_agent",
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "token":"0.Qz0.....f1",
                  "userAgent":"Mozilla/5.0 (Wind.....",
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

        Notes
            https://anti-captcha.com/apidoc/task-types/FriendlyCaptchaTask

            https://anti-captcha.com/apidoc/task-types/FriendlyCaptchaTaskProxyless
        """
        super().__init__(api_key=api_key, sleep_time=sleep_time)

        # validation of the received parameters
        if captcha_type == CaptchaTypeEnm.FriendlyCaptchaTask:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                websiteKey=websiteKey,
                proxyType=proxyType,
                proxyAddress=proxyAddress,
                proxyPort=proxyPort,
                proxyLogin=proxyLogin,
                proxyPassword=proxyPassword,
                userAgent=userAgent,
            )
        elif captcha_type == CaptchaTypeEnm.FriendlyCaptchaTaskProxyless:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                websiteKey=websiteKey,
            )
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`, \
                available - {CaptchaTypeEnm.FriendlyCaptchaTaskProxyless.value,CaptchaTypeEnm.FriendlyCaptchaTask.value}"
            )
