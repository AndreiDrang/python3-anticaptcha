import inspect

import pytest

from tests.main import MainAntiCaptcha
from python3_anticaptcha import ReCaptchaV3TaskProxyless


class TestAntiCaptcha(MainAntiCaptcha):
    WRONG_MIN_SCORE = 0.1
    """
    Params check
    """

    def test_recaptcha3_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time", "callbackUrl"]
        default_handler_params = ["self", "websiteURL", "websiteKey", "minScore", "pageAction"]
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

    """
    Response checking
    """

    def test_response_recaptcha3(self):
        recaptcha = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(recaptcha, ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless)

        response = recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=ReCaptchaV3TaskProxyless.MIN_SCORES[0],
            pageAction="login_test",
        )
        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    @pytest.mark.asyncio
    async def test_response_aiorecaptcha3(self):
        recaptcha = ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(recaptcha, ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless)

        response = await recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=ReCaptchaV3TaskProxyless.MIN_SCORES[0],
            pageAction="login_test",
        )
        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    """
    Fail tests
    """

    def test_fail_recaptcha3_value(self):
        recaptcha = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        with pytest.raises(ValueError):
            assert recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.1,
                pageAction="login_test",
            )

    def test_fail_recaptcha3_value_context(self):
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

    @pytest.mark.asyncio
    async def test_fail_aiorecaptcha3_value(self):
        recaptcha = ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        with pytest.raises(ValueError):
            assert await recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.1,
                pageAction="login_test",
            )

    @pytest.mark.asyncio
    async def test_fail_aiorecaptcha3_value_context(self):
        with ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            with pytest.raises(ValueError):
                assert await recaptcha.captcha_handler(
                    websiteURL="https://www.google.com/recaptcha/api2/demo",
                    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                    minScore=0.1,
                    pageAction="login_test",
                )

    """
    True tests
    """
