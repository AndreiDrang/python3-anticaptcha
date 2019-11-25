import os
import random
import inspect
import asyncio

import pytest

from python3_anticaptcha import (
    NoCaptchaTaskProxyless,
    ReCaptchaV3TaskProxyless,
)

# 1. `export anticaptcha_key=274832f8168a36019895a1e1174777c0`


class TestAntiCaptcha(object):
    WRONG_QUEUE_ID = WRONG_TASK_ID = -1

    def setup_class(self):
        self.anticaptcha_key_fail = os.getenv("anticaptcha_key")[:5]
        self.anticaptcha_key_true = os.getenv("anticaptcha_key")
        self.server_ip = "85.255.8.26"

    def test_nocaptcha_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time", "callbackUrl"]
        default_handler_params = ["self", "websiteURL", "websiteKey"]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.NoCaptchaTaskProxyless.__init__
        )
        handler_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.NoCaptchaTaskProxyless.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_fail_nocaptcha_proxyless(self):
        nocaptcha = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

        response = nocaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    def test_fail_nocaptcha_proxyless_context(self):
        with NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as nocaptcha:

            # check response type
            assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

            response = nocaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    @asyncio.coroutine
    def test_fail_aionocaptcha_proxyless(self):
        nocaptcha = NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

        response = yield nocaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    @asyncio.coroutine
    def test_fail_aionocaptcha_proxyless_context(self):
        with NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as nocaptcha:
            # check response type
            assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

            response = yield nocaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    def test_recaptcha_v3_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time", "callbackUrl"]
        default_handler_params = [
            "self",
            "websiteURL",
            "websiteKey",
            "minScore",
            "pageAction",
        ]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless.__init__
        )
        handler_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_true_recaptcha_v3_proxyless(self):
        recaptcha = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # check response type
        assert type(recaptcha) is ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless

        response = recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=0.3,
            pageAction="login_test",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription", "taskId"] == list(
            response.keys()
        )
        # check error code
        # TODO change to `0`
        assert response["errorId"] == 31

    def test_fail_recaptcha_v3_proxyless_context(self):
        with ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:

            # check response type
            assert type(recaptcha) is ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless

            response = recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.3,
                pageAction="login_test",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            with pytest.raises(ValueError):
                assert recaptcha.captcha_handler(
                    websiteURL="https://www.google.com/recaptcha/api2/demo",
                    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                    minScore=0.1,
                    pageAction="login_test",
                )

    @asyncio.coroutine
    def test_fail_aiorecaptcha_v3_proxyless(self):
        recaptcha = ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(recaptcha) is ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless

        response = yield recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=0.3,
            pageAction="login_test",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.1,
                pageAction="login_test",
            )

    @asyncio.coroutine
    def test_fail_aiorecaptcha_v3_proxyless_context(self):
        with ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            # check response type
            assert (
                type(recaptcha) is ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless
            )

            response = yield recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.3,
                pageAction="login_test",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            with pytest.raises(ValueError):
                assert recaptcha.captcha_handler(
                    websiteURL="https://www.google.com/recaptcha/api2/demo",
                    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                    minScore=0.1,
                    pageAction="login_test",
                )

    