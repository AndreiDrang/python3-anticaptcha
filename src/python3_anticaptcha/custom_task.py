from typing import Optional

from .core.base import CaptchaParams
from .core.enum import ProxyTypeEnm, CaptchaTypeEnm

__all__ = ("CustomTask",)


class CustomTask(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        websiteURL: str,
        templateName: str,
        variables: dict,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: str,
        proxyPassword: str,
        domainsOfInterest: list = [],
        proxyType: ProxyTypeEnm = ProxyTypeEnm.https,
        captcha_type: CaptchaTypeEnm = CaptchaTypeEnm.AntiGateTask,
        sleep_time: Optional[int] = 10,
    ):
        """
        The class is used to work with CustomTask - AntiGateTask.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type
            websiteURL: Address of a target web page where our worker will navigate.
            templateName: Name of a scenario template from our database.
                            You can use an existing template or create your own.
                            You can search for an existing template below this table.
            variables: An object containing the template's variables and their values.
            domainsOfInterest: List of domain names where we should collect cookies and
                                    localStorage data.
                            This list can also be defined statically when editing а template.
            proxyType: Type of the proxy, must be https
            proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                            host names instead of IPs,
                            transparent proxies (where client IP is visible),
                            proxies from local networks (192.., 10.., 127...)
            proxyPort: Proxy port.
            proxyLogin: Proxy login.
            proxyPassword: Proxy password.
            sleep_time: The waiting time between requests to get the result of the Captcha

        Examples:
            >>> CustomTask(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         websiteURL="https://anti-captcha.com/tutorials/v2-textarea",
            ...         templateName="Anti-bot screen bypass",
            ...         variables={
            ...             "css_selector":"some value"
            ...         },
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9988,
            ...         proxyLogin="proxy_login",
            ...         proxyPassword="proxy_password",
            ...        ).captcha_handler()
            {
               "errorId": 0,
               "errorCode": None,
               "errorDescription": None,
               "status":"ready",
               "solution":{
                  "...."
               },
               "cost": 0.002,
               "ip": "46.53.249.230",
               "createTime": 1679004358,
               "endTime": 1679004368,
               "solveCount": 0,
               "taskId": 396687629
            }

            >>> await CustomTask(api_key="99d7d111a0111dc11184111c8bb111da",
            ...         websiteURL="https://anti-captcha.com/tutorials/v2-textarea",
            ...         templateName="Anti-bot screen bypass",
            ...         variables={
            ...             "css_selector":"some value"
            ...         },
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9988,
            ...         proxyLogin="proxy_login",
            ...         proxyPassword="proxy_password",
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

        Notes:
            https://anti-captcha.com/apidoc/task-types/AntiGateTask
        """
        super().__init__(api_key=api_key, sleep_time=sleep_time)

        self.task_params = dict(
            type=captcha_type,
            websiteURL=websiteURL,
            templateName=templateName,
            variables=variables,
            domainsOfInterest=domainsOfInterest,
            proxyType=proxyType,
            proxyAddress=proxyAddress,
            proxyPort=proxyPort,
            proxyLogin=proxyLogin,
            proxyPassword=proxyPassword,
        )
