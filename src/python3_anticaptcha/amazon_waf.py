from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm

__all__ = ("AmazonWAF",)


class AmazonWAF(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        iv: str,
        context: str,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        sleep_time: Optional[int] = 10,
    ):
        """
        The class is used to work with FunCaptcha.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of a target web page. Can be located anywhere on the web site, even in a member area
            websiteKey: Value of key from window.gokuProps object in WAF page source code
            iv: Value of iv from window.gokuProps object in WAF page source code
            context: Value of context from window.gokuProps object in WAF page source code

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
            >>> AmazonWAF(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="AmazonTaskProxyless",
            ...         websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
            ...         websiteKey="AQIDAgghr5y45ywZwdADFLWk7XOA==",
            ...         iv="CgAAXFFFFSAAABVk",
            ...         context="qoJYgnKscdqwdqwdqwaormh/dYYK+Y=",
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "token":"0.Qz0.....f1"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> await AmazonWAF(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="AmazonTaskProxyless",
            ...         websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
            ...         websiteKey="AQIDAgghr5y45ywZwdADFLWk7XOA==",
            ...         iv="CgAAXFFFFSAAABVk",
            ...         context="qoJYgnKscdqwdqwdqwaormh/dYYK+Y=",
            ...        ).aio_captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "token":"0.Qz0.....f1"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> AmazonWAF(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type="AmazonTaskProxyless",
            ...         websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
            ...         websiteKey="AQIDAgghr5y45ywZwdADFLWk7XOA==",
            ...         iv="CgAAXFFFFSAAABVk",
            ...         context="qoJYgnKscdqwdqwdqwaormh/dYYK+Y=",
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
                  "token":"0.Qz0.....f1"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

        Notes:
            https://anti-captcha.com/apidoc/task-types/AmazonTask

            https://anti-captcha.com/apidoc/task-types/AmazonTaskProxyless
        """
        super().__init__(api_key=api_key, sleep_time=sleep_time)

        # validation of the received parameters
        if captcha_type == CaptchaTypeEnm.AmazonTask:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                websitePublicKey=websiteKey,
                iv=iv,
                context=context,
                proxyType=proxyType,
                proxyAddress=proxyAddress,
                proxyPort=proxyPort,
                proxyLogin=proxyLogin,
                proxyPassword=proxyPassword,
                userAgent=userAgent,
            )
        elif captcha_type == CaptchaTypeEnm.AmazonTaskProxyless:
            self.task_params = dict(
                type=captcha_type,
                websiteURL=websiteURL,
                websitePublicKey=websiteKey,
                iv=iv,
                context=context,
            )
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`, \
                available - {CaptchaTypeEnm.FunCaptchaTaskProxyless.value,CaptchaTypeEnm.FunCaptchaTask.value}"
            )
