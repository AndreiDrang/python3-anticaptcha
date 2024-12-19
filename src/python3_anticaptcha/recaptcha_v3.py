from typing import Optional

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("ReCaptchaV3",)


class ReCaptchaV3(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        websiteURL: str,
        websiteKey: str,
        minScore: float,
        pageAction: Optional[str] = None,
        isEnterprise: bool = False,
        apiDomain: Optional[str] = None,
        captcha_type: CaptchaTypeEnm = CaptchaTypeEnm.RecaptchaV3TaskProxyless,
        sleep_time: int = 10,
    ):
        """
        The class is used to work with ReCaptchaV3 and RecaptchaV3Enterprise.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of the webpage
            websiteKey: Recaptcha website key.
            minScore: Filters workers with a particular score.
                        It can have one of the following values: 0.3, 0.7, 0.9
            pageAction: Recaptcha's "action" value
                        Website owners use this parameter to define what users are doing on the page.
            isEnterprise: Set this flag to "true" if you need this V3 solved with Enterprise API.
                            Default value is "false" and the reCaptcha is solved with non-enterprise API.
            apiDomain: Use this parameter to send the domain name from which the reCaptcha script should be served.
                        Can have only one of two values: "www.google.com" or "www.recaptcha.net".
                        Do not use this parameter unless you understand what you are doing.
            sleep_time: The waiting time between requests to get the result of the Captcha

        Examples:
            >>> ReCaptchaV3(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            ...         websiteURL="https://www.recaptcha.com/en/adaptive-captcha-demo",
            ...         websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            ...         minScore=0.3,
            ...         pageAction="login",
            ...         isEnterprise=False,
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

            >>> await ReCaptchaV3(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            ...         websiteURL="https://www.recaptcha.com/en/adaptive-captcha-demo",
            ...         websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            ...         minScore=0.3,
            ...         pageAction="login",
            ...         isEnterprise=True,
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

            >>> ReCaptchaV3(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            ...         websiteURL="https://www.recaptcha.com/en/adaptive-captcha-demo",
            ...         websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            ...         minScore=0.3,
            ...         pageAction="login",
            ...         isEnterprise=True,
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
            https://anti-captcha.com/apidoc/task-types/RecaptchaV3TaskProxyless

            https://anti-captcha.com/apidoc/task-types/RecaptchaV3Enterprise
        """
        super().__init__(api_key=api_key, sleep_time=sleep_time)
        self.task_params = dict(
            type=captcha_type,
            websiteURL=websiteURL,
            websiteKey=websiteKey,
            minScore=minScore,
            pageAction=pageAction,
            isEnterprise=isEnterprise,
            apiDomain=apiDomain,
        )
