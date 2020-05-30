import inspect

import pytest
import requests_mock

from tests.main import MainAntiCaptcha
from python3_anticaptcha import NoCaptchaTask, config


class TestNoCaptcha(MainAntiCaptcha):
    WEBSITE_URL = "https://www.google.com/recaptcha/api2/demo"
    WEBSITE_KEY = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"

    """
    Params check
    """

    def test_nocaptcha_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time", "callbackUrl"]
        default_handler_params = ["self", "websiteURL", "websiteKey", 'recaptchaDataSValue']
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(NoCaptchaTask.aioNoCaptchaTask.__init__)
        aiohandler_params = inspect.getfullargspec(NoCaptchaTask.aioNoCaptchaTask.captcha_handler)

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(NoCaptchaTask.NoCaptchaTask.__init__)
        handler_params = inspect.getfullargspec(NoCaptchaTask.NoCaptchaTask.captcha_handler)
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    """
    Request payload test MOCK
    """

    def test_create_task_payload(self):
        no_captcha = NoCaptchaTask.NoCaptchaTask(anticaptcha_key=self.anticaptcha_key_fail)
        # check response type
        assert isinstance(no_captcha, NoCaptchaTask.NoCaptchaTask)

        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.create_task_url, json=self.ERROR_RESPONSE_JSON)
            no_captcha.captcha_handler(websiteURL=self.WEBSITE_URL, websiteKey=self.WEBSITE_KEY)

        history = req_mock.request_history

        assert len(history) == 1

        request_payload = history[0].json()

        # check all dict keys
        assert ["clientKey", "task", "softId"] == list(request_payload.keys())
        assert request_payload["softId"] == config.app_key
        assert ["type", "websiteURL", "websiteKey", 'recaptchaDataSValue'] == list(request_payload["task"].keys())
        assert request_payload["task"]["type"] == "NoCaptchaTask"
