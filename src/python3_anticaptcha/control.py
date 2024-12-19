from typing import Optional

from .core.base import CaptchaParams
from .core.enum import ControlPostfixEnm
from .core.aio_captcha_instrument import AIOCaptchaInstrument
from .core.sio_captcha_instrument import SIOCaptchaInstrument

__all__ = ("Control",)


class Control(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Turnstile.

        Args:
            api_key: Capsolver API key
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
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_balance()
            {
               "errorId": 0,
               "balance": 14.12396
            }

            >>> Control.get_queue_status(queue_id=1)
            {
               "waiting": 234,
               "load": 46.58,
               "bid": 0.000576,
               "speed": 8.43,
               "total": 438
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_spending_stats(softId=867)
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_app_stats(softId=867, mode='views')
            {
               "errorId":0,
               "chartData":[
                  {
                    ......
                  }
               ],
               "fromDate":"17 Feb 23:48",
               "toDate":"19 Mar 23:48"
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_incorrect_image(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_incorrect_recaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_correct_recaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_incorrect_hcaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }

        Notes:
            https://anti-captcha.com/apidoc/methods/getBalance

            https://anti-captcha.com/apidoc/methods/getQueueStats

            https://anti-captcha.com/apidoc/methods/getSpendingStats

            https://anti-captcha.com/apidoc/methods/getAppStats

            https://anti-captcha.com/apidoc/methods/reportIncorrectHcaptcha

            https://anti-captcha.com/apidoc/methods/reportCorrectRecaptcha

            https://anti-captcha.com/apidoc/methods/reportIncorrectRecaptcha

            https://anti-captcha.com/apidoc/methods/reportIncorrectImageCaptcha
        """
        super().__init__(api_key=api_key, *args, **kwargs)

    def get_balance(self) -> dict:
        """
        Retrieve an account balance with its account key.

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_balance()
            {
               "errorId": 0,
               "balance": 14.12396
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getBalance
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.GET_BALANCE,
            payload={"clientKey": self.create_task_payload.clientKey},
        )

    async def aio_get_balance(self) -> dict:
        """
        Async retrieve an account balance with its account key.

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_get_balance()
            {
               "errorId": 0,
               "balance": 14.12396
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getBalance
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.GET_BALANCE, payload={"clientKey": self.create_task_payload.clientKey}
        )

    @staticmethod
    def get_queue_status(queue_id: int) -> dict:
        """
        This method makes it possible to define a suitable time for uploading a new task

        Args:
            queue_id: Identifier of a queue

        Examples:
            >>> Control.get_queue_status(queue_id=1)
            {
               "waiting": 234,
               "load": 46.58,
               "bid": 0.000576,
               "speed": 8.43,
               "total": 438
            }

            >>> Control.get_queue_status(queue_id=20)
            {
               "waiting": 90,
               "load": 38.36,
               "bid": 0.002,
               "speed": 7.38,
               "total": 146
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getQueueStats
        """
        return SIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.GET_QUEUE_STATS, payload={"queueId": queue_id}
        )

    @staticmethod
    async def aio_get_queue_status(queue_id: int) -> dict:
        """
        Async method makes it possible to define a suitable time for uploading a new task

        Args:
            queue_id: Identifier of a queue

        Examples:
            >>> await Control.aio_get_queue_status(queue_id=1)
            {
               "waiting": 234,
               "load": 46.58,
               "bid": 0.000576,
               "speed": 8.43,
               "total": 438
            }

            >>> await Control.aio_get_queue_status(queue_id=20)
            {
               "waiting": 90,
               "load": 38.36,
               "bid": 0.002,
               "speed": 7.38,
               "total": 146
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getQueueStats
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.GET_QUEUE_STATS, payload={"queueId": queue_id}
        )

    def get_spending_stats(self, **kwargs) -> dict:
        """
        This method grabs account spendings and task volume statistics for a 24 hour period.

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_spending_stats(softId=867)
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_spending_stats(softId=867,
            ...                                                                         queue="English ImageToText")
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_spending_stats(queue="English ImageToText")
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getSpendingStats
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.GET_SPENDING_STATS,
            payload={"clientKey": self.create_task_payload.clientKey, **kwargs},
        )

    async def aio_get_spending_stats(self, **kwargs) -> dict:
        """
        Async method grabs account spendings and task volume statistics for a 24 hour period.

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_get_spending_stats(softId=867)
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_get_spending_stats(softId=867,
            ...                                                                             queue="English ImageToText")
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_get_spending_stats(queue="English ImageToText")
            {
               "errorId":0,
               "data":[
                  {
                     "dateFrom":1679183850,
                     "dateTill":1679187449,
                     "volume":0,
                     "money":0
                  }
               ]
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getSpendingStats
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.GET_SPENDING_STATS,
            payload={"clientKey": self.create_task_payload.clientKey, **kwargs},
        )

    def get_app_stats(self, softId: int, mode: Optional[str] = None) -> dict:
        """
        This method retrieves daily statistics for your application, which you register in Developer Center.
            Statistics are available only to the application owner. Improper access returns `ERROR_ACCESS_DENIED`.

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_app_stats(softId=867, mode='views')
            {
               "errorId":0,
               "chartData":[
                  {
                    ......
                  }
               ],
               "fromDate":"17 Feb 23:48",
               "toDate":"19 Mar 23:48"
            }

            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").get_app_stats(softId=867, mode='errors')
            {
               "errorId":0,
               "chartData":[
                  {
                    ......
                  }
               ],
               "fromDate":"17 Feb 23:48",
               "toDate":"19 Mar 23:48"
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getAppStats
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.GET_APP_STATS,
            payload={"clientKey": self.create_task_payload.clientKey, "softId": softId, "mode": mode},
        )

    async def aio_get_app_stats(self, softId: int, mode: Optional[str] = None) -> dict:
        """
        Async method retrieves daily statistics for your application, which you register in Developer Center.
            Statistics are available only to the application owner. Improper access returns `ERROR_ACCESS_DENIED`.

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_get_app_stats(softId=867, mode='views')
            {
               "errorId":0,
               "chartData":[
                  {
                    ......
                  }
               ],
               "fromDate":"17 Feb 23:48",
               "toDate":"19 Mar 23:48"
            }

            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_get_app_stats(softId=867, mode='errors')
            {
               "errorId":0,
               "chartData":[
                  {
                    ......
                  }
               ],
               "fromDate":"17 Feb 23:48",
               "toDate":"19 Mar 23:48"
            }

        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/getAppStats
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.GET_APP_STATS,
            payload={"clientKey": self.create_task_payload.clientKey, "softId": softId, "mode": mode},
        )

    def report_incorrect_image(self, taskId: int) -> dict:
        """
        Complaints are accepted for image captchas only.

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_incorrect_image(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportIncorrectImageCaptcha
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.REPORT_INCORRECT_IMAGE_CAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    async def aio_report_incorrect_image(self, taskId: int) -> dict:
        """
        Async complaints are accepted for image captchas only.

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_report_incorrect_image(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportIncorrectImageCaptcha
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.REPORT_INCORRECT_IMAGE_CAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    def report_incorrect_recaptcha(self, taskId: int) -> dict:
        """
        Complaints are accepted for V2 and V3 Recaptchas only, including Enterprise Recaptcha.

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_incorrect_recaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportIncorrectRecaptcha
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.REPORT_INCORRECT_RECAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    async def aio_report_incorrect_recaptcha(self, taskId: int) -> dict:
        """
        Async complaints are accepted for V2 and V3 Recaptchas only, including Enterprise Recaptcha.

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_report_incorrect_recaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportIncorrectRecaptcha
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.REPORT_INCORRECT_RECAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    def report_correct_recaptcha(self, taskId: int) -> dict:
        """
        Reporting correctly solved ReCaptcha

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_correct_recaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportCorrectRecaptcha
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.REPORT_CORRECT_RECAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    async def aio_report_correct_recaptcha(self, taskId: int) -> dict:
        """
        Async reporting correctly solved ReCaptcha

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_report_correct_recaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportCorrectRecaptcha
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.REPORT_CORRECT_RECAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    def report_incorrect_hcaptcha(self, taskId: int) -> dict:
        """
        Use this method to send us information about tokens which did not pass on target service

        Examples:
            >>> Control(api_key="99d7d111a0111dc11184111c8bb111da").report_incorrect_hcaptcha(taskId=425436541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportIncorrectHcaptcha
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=ControlPostfixEnm.REPORT_INCORRECT_HCAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )

    async def aio_report_incorrect_hcaptcha(self, taskId: int) -> dict:
        """
        Async method to send us information about tokens which did not pass on target service

        Examples:
            >>> await Control(api_key="99d7d111a0111dc11184111c8bb111da").aio_report_incorrect_hcaptcha(taskId=4256541)
            {
                "errorId":0,
                "status":"success"
            }


        Returns:
            Dict with full server response

        Notes:
            https://anti-captcha.com/apidoc/methods/reportIncorrectHcaptcha
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=ControlPostfixEnm.REPORT_INCORRECT_HCAPTCHA,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": taskId},
        )
