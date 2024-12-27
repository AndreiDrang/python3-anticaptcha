from .serializer import CreateTaskBaseSer, GetTaskResultRequestSer
from .context_instr import AIOContextManager, SIOContextManager
from .captcha_instrument import CaptchaInstrument
from .aio_captcha_instrument import AIOCaptchaInstrument
from .sio_captcha_instrument import SIOCaptchaInstrument

__all__ = ("CaptchaParams",)


class CaptchaParams(SIOContextManager, AIOContextManager):
    """
    Basic Captcha params class

    Args:
        api_key: Capsolver API key
        sleep_time: The waiting time between requests to get the result of the Captcha
    """

    def __init__(self, api_key: str, sleep_time: int = 15, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_time = sleep_time

        # assign args to validator
        self.create_task_payload = CreateTaskBaseSer(clientKey=api_key)
        # `task` body for task creation payload
        self.task_params = {}
        # prepare `get task result` payload
        self.get_result_params = GetTaskResultRequestSer(clientKey=api_key)

        self._captcha_handling_instrument = CaptchaInstrument()

    def set_callback_url(self, callbackUrl: str) -> None:
        """
        Method for `callbackUrl` param set.

        Args:
            callbackUrl: Optional web address where we can send the results of captcha task processing.
                            Contents are sent by AJAX POST request and are identical
                                to the contents of getTaskResult method.

        Notes:
            https://anti-captcha.com/apidoc/methods/createTask
        """
        self.create_task_payload.callbackUrl = callbackUrl

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
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
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
        self._captcha_handling_instrument = AIOCaptchaInstrument(captcha_params=self)
        return await self._captcha_handling_instrument.processing_captcha()
