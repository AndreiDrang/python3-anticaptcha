import inspect

import pytest

from python3_anticaptcha import AntiCaptchaControl

from tests.main import MainAntiCaptcha


class TestAntiCaptcha(MainAntiCaptcha):
    WRONG_SAVE_FORMAT = "qwerty"
    """
    Params check
    """

    def test_customcatpcha_params(self):
        default_init_params = [
            "self",
            "anticaptcha_key",
        ]
        default_get_balance_params = [
            "self",
        ]
        default_app_stats_params = [
            "self",
            "softId",
            "mode",
        ]
        default_complaint_params = [
            "self",
            "reported_id",
            "captcha_type"
        ]
        default_queue_status_params = [
            "self",
            "queue_id"
        ]
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
    async def test_response_aioimagecaptcha(self):
        imagecaptcha = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(imagecaptcha, AntiCaptchaControl.aioAntiCaptchaControl)

    """
    Fail tests
    """

    def test_fail_imagecaptcha_value(self):
        with pytest.raises(ValueError):
            assert ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.anticaptcha_key_fail,
                save_format=self.WRONG_SAVE_FORMAT,
            )

    def test_fail_imagecaptcha_const(self):
        imagecaptcha = ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[0],
        )

        response = imagecaptcha.captcha_handler(captcha_link=self.image_url)

        assert 1 == response["errorId"]

    def test_fail_imagecaptcha_const_context(self):
        with ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[0],
        ) as imagecaptcha:

            response = imagecaptcha.captcha_handler(captcha_link=self.image_url)

            assert 1 == response["errorId"]

    def test_fail_imagecaptcha_temp(self):
        imagecaptcha = ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[1],
        )

        response = imagecaptcha.captcha_handler(captcha_link=self.image_url)

        assert 1 == response["errorId"]

    def test_fail_imagecaptcha_temp_context(self):
        with ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[1],
        ) as imagecaptcha:

            response = imagecaptcha.captcha_handler(captcha_link=self.image_url)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioimagecaptcha_value(self):
        with pytest.raises(ValueError):
            assert ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.anticaptcha_key_fail,
                save_format=self.WRONG_SAVE_FORMAT,
            )

    @pytest.mark.asyncio
    async def test_fail_aioimagecaptcha_temp(self):
        imagecaptcha = ImageToTextTask.aioImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[1],
        )
        response = await imagecaptcha.captcha_handler(captcha_link=self.image_url)
        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioimagecaptcha_temp_context(self):
        with ImageToTextTask.aioImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[1],
        ) as imagecaptcha:
            response = await imagecaptcha.captcha_handler(captcha_link=self.image_url)
            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioimagecaptcha_const(self):
        imagecaptcha = ImageToTextTask.aioImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[0],
        )
        response = await imagecaptcha.captcha_handler(captcha_link=self.image_url)
        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioimagecaptcha_const_context(self):
        with ImageToTextTask.aioImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            save_format=ImageToTextTask.SAVE_FORMATS[0],
        ) as imagecaptcha:
            response = await imagecaptcha.captcha_handler(captcha_link=self.image_url)
            assert 1 == response["errorId"]

    """
    True tests
    """
