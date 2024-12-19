from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm

__all__ = ("GeeTest",)


class GeeTest(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        gt: str,
        version: int = 3,
        challenge: Optional[str] = None,
        geetestApiServerSubdomain: Optional[str] = None,
        initParameters: Optional[str] = None,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        sleep_time: int = 10,
    ):
        """
        The class is used to work with GeeTest.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of the webpage
            gt: The domain public key, rarely updated.
            version: Version number. Default version is 3. Supported versions: 3 and 4.
            challenge: Changing token key. Make sure you grab a fresh one for each captcha; otherwise,
                        you'll be charged for an error task. Required for version 3. Not required for version 4
            geetestApiServerSubdomain: Optional API subdomain. May be required for some implementations.
            initParameters: Additional initialization parameters for version 4
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
            >>> GeeTest(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="GeeTestTaskProxyless",
            ...         websiteURL="https://www.geetest.com/en/adaptive-captcha-demo",
            ...         gt="81388ea1fc187e0c335c0a8907ff2625",
            ...         challenge="12345678abc90123d45678ef90123a456b",
            ...         version=3,
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "challenge":"3c1c5153aa48011e92883aed820069f3hj",
                    "validate":"47ad5a0a6eb98a95b2bcd9e9eecc8272",
                    "seccode":"83fa4f2d23005fc91c3a015a1613f803|jordan"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> await GeeTest(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="GeeTestTaskProxyless",
            ...         websiteURL="https://www.geetest.com/en/adaptive-captcha-demo",
            ...         gt="81388ea1fc187e0c335c0a8907ff2625",
            ...         version=4,
            ...         initParameters="additional_init_params"
            ...        ).aio_captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "captcha_id": "fcd636b4514bf7ac4143922550b3008b",
                    "lot_number": "354ab6dd4e594fdc903074c4d8d37b24",
                    "pass_token": "b645946a654e60218c7922......8d660bbd1ed5",
                    "gen_time": "1649921519",
                    "captcha_output": "cFPIA.....rRoA=="
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> GeeTest(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="GeeTestTask",
            ...         websiteURL="https://www.geetest.com/en/adaptive-captcha-demo",
            ...         gt="81388ea1fc187e0c335c0a8907ff2625",
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
                    "challenge":"3c1c5153aa48011e92883aed820069f3hj",
                    "validate":"47ad5a0a6eb98a95b2bcd9e9eecc8272",
                    "seccode":"83fa4f2d23005fc91c3a015a1613f803|jordan"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

        Notes:
            https://anti-captcha.com/apidoc/task-types/GeeTestTask

            https://anti-captcha.com/apidoc/task-types/GeeTestTaskProxyless
        """
        super().__init__(api_key=api_key, sleep_time=sleep_time)

        # validation of the received parameters
        if captcha_type == CaptchaTypeEnm.GeeTestTask:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                gt=gt,
                challenge=challenge,
                geetestApiServerSubdomain=geetestApiServerSubdomain,
                version=version,
                initParameters=initParameters,
                proxyType=proxyType,
                proxyAddress=proxyAddress,
                proxyPort=proxyPort,
                proxyLogin=proxyLogin,
                proxyPassword=proxyPassword,
                userAgent=userAgent,
            )
        elif captcha_type == CaptchaTypeEnm.GeeTestTaskProxyless:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                gt=gt,
                challenge=challenge,
                geetestApiServerSubdomain=geetestApiServerSubdomain,
                version=version,
                initParameters=initParameters,
            )
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`, \
                available - {CaptchaTypeEnm.GeeTestTask.value,CaptchaTypeEnm.GeeTestTaskProxyless.value}"
            )
