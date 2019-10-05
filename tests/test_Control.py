import inspect

import pytest

from python3_anticaptcha import AntiCaptchaControl, config

from tests.main import MainAntiCaptcha


class TestAntiCaptcha(MainAntiCaptcha):
    WRONG_MODE = "qwerty"
    WRONG_SOFT_ID = config.app_key + "0"
    """
    Params check
    """

    def test_customcatpcha_params(self):
        default_init_params = ["self", "anticaptcha_key"]
        default_get_balance_params = ["self"]
        default_app_stats_params = ["self", "softId", "mode"]
        default_complaint_params = ["self", "reported_id", "captcha_type"]
        default_queue_status_params = ["queue_id"]
        # get aiocaptchacontrol init and other params
        aio_init_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.__init__
        )
        aio_balance_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_balance
        )
        aio_app_stats_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_app_stats
        )
        aio_complaint_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.complaint_on_result
        )
        aio_queue_status_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_queue_status
        )

        # get captchacontrol init and other params
        init_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.__init__
        )
        balance_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_balance
        )
        app_stats_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_app_stats
        )
        complaint_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.complaint_on_result
        )
        queue_status_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_queue_status
        )
        # check aio module params
        assert default_init_params == aio_init_params[0]
        assert default_get_balance_params == aio_balance_params[0]
        assert default_app_stats_params == aio_app_stats_params[0]
        assert default_complaint_params == aio_complaint_params[0]
        assert default_queue_status_params == aio_queue_status_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_get_balance_params == balance_params[0]
        assert default_app_stats_params == app_stats_params[0]
        assert default_complaint_params == complaint_params[0]
        assert default_queue_status_params == queue_status_params[0]

    """
    Response checking
    """

    def test_response_control(self):
        control_captcha = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(control_captcha, AntiCaptchaControl.AntiCaptchaControl)

    @pytest.mark.asyncio
    async def test_response_aiocontrol(self):
        control_captcha = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(control_captcha, AntiCaptchaControl.aioAntiCaptchaControl)

    """
    Fail tests
    """

    def test_fail_balance(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = captcha_control.get_balance()

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_balance_context(self):
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    def test_fail_key_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_app_stats_context(self):
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = captcha_control.get_app_stats(softId=config.app_key)

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    def test_fail_id_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_mode_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        with pytest.raises(ValueError):
            captcha_control.get_app_stats(softId=config.app_key, mode=self.WRONG_MODE)

    @pytest.mark.asyncio
    async def test_fail_aiobalance(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = await captcha_control.get_balance()

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiobalance_context(self):
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = await captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioapp_stats_context(self):
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = await captcha_control.get_app_stats(softId=config.app_key)

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiokey_app_stats(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = await captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioid_app_stats(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = await captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiomode_app_stats(self):
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = await captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    """
    True tests
    """

    def test_true_mode_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        for mode in AntiCaptchaControl.mods:
            response = captcha_control.get_app_stats(softId=config.app_key, mode=mode)

            assert isinstance(response, dict)
