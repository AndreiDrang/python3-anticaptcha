import inspect

import pytest
import requests_mock

from python3_anticaptcha import ImageToTextTask, config

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
            "sleep_time",
            "save_format",
            "language",
            "callbackUrl",
        ]
        default_handler_params = [
            "self",
            "captcha_link",
            "captcha_file",
            "captcha_base64",
        ]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(
            ImageToTextTask.aioImageToTextTask.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            ImageToTextTask.aioImageToTextTask.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(ImageToTextTask.ImageToTextTask.__init__)
        handler_params = inspect.getfullargspec(
            ImageToTextTask.ImageToTextTask.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_create_task_payload(self):
        customcaptcha = ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(customcaptcha, ImageToTextTask.ImageToTextTask)

        with requests_mock.Mocker() as req_mock:
            req_mock.register_uri("GET", self.image_url, json=self.VALID_RESPONSE_JSON)
            req_mock.register_uri(
                "POST", config.create_task_url, json=self.ERROR_RESPONSE_JSON
            )
            customcaptcha.captcha_handler(captcha_link=self.image_url)

        history = req_mock.request_history

        assert len(history) == 2

        request_payload = history[1].json()

        # check all dict keys
        assert ["clientKey", "task", "languagePool", "softId"] == list(
            request_payload.keys()
        )
        assert request_payload["softId"] == config.app_key
        assert ["type", "body"] == list(request_payload["task"].keys())
        assert request_payload["task"]["type"] == "ImageToTextTask"

    def test_get_result_payload(self):
        customcaptcha = ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(customcaptcha, ImageToTextTask.ImageToTextTask)

        with requests_mock.Mocker() as req_mock:
            req_mock.register_uri("GET", self.image_url, json=self.VALID_RESPONSE_JSON)
            req_mock.register_uri(
                "POST", config.create_task_url, json=self.VALID_RESPONSE_JSON
            )
            req_mock.register_uri(
                "POST", config.get_result_url, json=self.VALID_RESPONSE_RESULT_JSON
            )
            customcaptcha.captcha_handler(captcha_link=self.image_url)

        history = req_mock.request_history

        assert len(history) == 3

        request_payload = history[2].json()

        # check all dict keys
        assert ["clientKey", "taskId"] == list(request_payload.keys())
        assert request_payload["taskId"] == self.VALID_RESPONSE_JSON["taskId"]

    """
    Response checking
    """

    def test_response_imagecaptcha(self):
        imagecaptcha = ImageToTextTask.ImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(imagecaptcha, ImageToTextTask.ImageToTextTask)

        response = imagecaptcha.captcha_handler(captcha_link=self.image_url)
        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    @pytest.mark.asyncio
    async def test_response_aioimagecaptcha(self):
        imagecaptcha = ImageToTextTask.aioImageToTextTask(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(imagecaptcha, ImageToTextTask.aioImageToTextTask)

        response = await imagecaptcha.captcha_handler(captcha_link=self.image_url)

        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

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
            assert await ImageToTextTask.ImageToTextTask(
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
