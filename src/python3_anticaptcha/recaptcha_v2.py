from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm

__all__ = ("ReCaptchaV2",)


class ReCaptchaV2(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        recaptchaDataSValue: Optional[str] = None,
        isInvisible: bool = False,
        enterprisePayload: Optional[dict] = None,
        apiDomain: Optional[str] = None,
        proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
        sleep_time: int = 10,
    ):
        """
        The class is used to work with ReCaptchaV2 and RecaptchaV2Enterprise.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of the webpage
            websiteKey: Recaptcha website key.
            recaptchaDataSValue: Value of 'data-s' parameter.
                                    Applies only to reCaptchas on Google web sites.
            isInvisible: Specify whether or not reCaptcha is invisible.
                            This will render an appropriate widget for our workers.
            enterprisePayload: Additional parameters which should be passed to
                                "grecaptcha.enterprise.render" method along with sitekey.
            apiDomain: Use this parameter to send the domain name from which the reCaptcha script should be served.
                        Can have only one of two values: "www.google.com" or "www.recaptcha.net".
                        Do not use this parameter unless you understand what you are doing.
            proxyType: Type of the proxy
            proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                            host names instead of IPs,
                            transparent proxies (where client IP is visible),
                            proxies from local networks (192.., 10.., 127...)
            proxyPort: Proxy port.
            proxyLogin: Proxy login.
            proxyPassword: Proxy password.
            userAgent: Browser UserAgent.
            cookies: Additional cookies that we should use in Google domains.
            sleep_time: The waiting time between requests to get the result of the Captcha

        Examples:
            >>> ReCaptchaV2(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
            ...         websiteURL="https://www.recaptcha.com/en/adaptive-captcha-demo",
            ...         websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            ...         recaptchaDataSValue="12345678abc90123d45678ef90123a456b",
            ...         isInvisible=False,
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "gRecaptchaResponse":"3AHJ_VuvYIB.......6a3"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> await ReCaptchaV2(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type=CaptchaTypeEnm.RecaptchaV2Task,
            ...         websiteURL="https://www.recaptcha.com/en/adaptive-captcha-demo",
            ...         websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            ...         recaptchaDataSValue="12345678abc90123d45678ef90123a456b",
            ...         isInvisible=False,
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9988,
            ...         proxyLogin="proxy_login",
            ...         proxyPassword="proxy_password",
            ...         userAgent="some_real_user_agent",
            ...         cookies="some-cookies-data",
            ...        ).aio_captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "gRecaptchaResponse":"3AHJ_VuvYIB.......6a3"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> ReCaptchaV2(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type=CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
            ...         websiteURL="https://www.recaptcha.com/en/adaptive-captcha-demo",
            ...         websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            ...         enterprisePayload={
            ...                     "s": "SOME_ADDITIONAL_TOKEN"
            ...         },
            ...         apiDomain="www.google.com",
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                    "gRecaptchaResponse":"3AHJ_VuvYIB.......6a3"
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

        Notes:
            https://anti-captcha.com/apidoc/task-types/RecaptchaV2TaskProxyless

            https://anti-captcha.com/apidoc/task-types/RecaptchaV2Task

            https://anti-captcha.com/apidoc/task-types/RecaptchaV2EnterpriseTaskProxyless

            https://anti-captcha.com/apidoc/task-types/RecaptchaV2EnterpriseTask
        """
        super().__init__(api_key=api_key, sleep_time=sleep_time)
        self.task_params = dict(
            type=captcha_type,
            websiteURL=websiteURL,
            websiteKey=websiteKey,
        )
        if captcha_type in (
            CaptchaTypeEnm.RecaptchaV2TaskProxyless,
            CaptchaTypeEnm.RecaptchaV2Task,
        ):
            self.task_params.update(
                dict(
                    recaptchaDataSValue=recaptchaDataSValue,
                    isInvisible=isInvisible,
                )
            )
            if captcha_type == CaptchaTypeEnm.RecaptchaV2Task:
                self.task_params.update(
                    dict(
                        proxyType=proxyType,
                        proxyAddress=proxyAddress,
                        proxyPort=proxyPort,
                        proxyLogin=proxyLogin,
                        proxyPassword=proxyPassword,
                        userAgent=userAgent,
                        cookies=cookies,
                    )
                )
        elif captcha_type in (
            CaptchaTypeEnm.RecaptchaV2EnterpriseTask,
            CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
        ):
            self.task_params.update(
                dict(
                    enterprisePayload=enterprisePayload,
                    apiDomain=apiDomain,
                )
            )
            if captcha_type == CaptchaTypeEnm.RecaptchaV2EnterpriseTask:
                self.task_params.update(
                    dict(
                        proxyType=proxyType,
                        proxyAddress=proxyAddress,
                        proxyPort=proxyPort,
                        proxyLogin=proxyLogin,
                        proxyPassword=proxyPassword,
                        userAgent=userAgent,
                        cookies=cookies,
                    )
                )
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`, \
                available - {CaptchaTypeEnm.RecaptchaV2Task.value,
                CaptchaTypeEnm.RecaptchaV2TaskProxyless.value,
                CaptchaTypeEnm.RecaptchaV2EnterpriseTask.value,
                CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless.value}"
            )
