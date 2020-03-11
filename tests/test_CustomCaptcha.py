import inspect

import pytest
import requests_mock

from tests.main import MainAntiCaptcha
from python3_anticaptcha import CustomCaptchaTask, config


class TestCustom(MainAntiCaptcha):
    CUSTOM_TASK = "2+2=?"

    """
    Params check
    """

    def test_customcatpcha_params(self):
        default_init_params = [
            "self",
            "anticaptcha_key",
            "sleep_time",
            "assignment",
            "forms",
            "callbackUrl",
        ]
        default_handler_params = ["self", "imageUrl"]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(CustomCaptchaTask.aioCustomCaptchaTask.__init__)
        aiohandler_params = inspect.getfullargspec(
            CustomCaptchaTask.aioCustomCaptchaTask.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(CustomCaptchaTask.CustomCaptchaTask.__init__)
        handler_params = inspect.getfullargspec(
            CustomCaptchaTask.CustomCaptchaTask.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_create_task_payload(self):
        customcaptcha = CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        )
        # check response type
        assert isinstance(customcaptcha, CustomCaptchaTask.CustomCaptchaTask)

        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.create_task_url, json=self.ERROR_RESPONSE_JSON)
            customcaptcha.captcha_handler(imageUrl=self.image_url)

        history = req_mock.request_history

        assert len(history) == 1

        request_payload = history[0].json()

        # check all dict keys
        assert ["clientKey", "task", "softId"] == list(request_payload.keys())
        assert request_payload["softId"] == config.app_key
        assert ["type", "assignment", "imageUrl"] == list(request_payload["task"].keys())
        assert request_payload["task"]["type"] == "CustomCaptchaTask"

    def test_get_result_payload(self):
        customcaptcha = CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        )
        # check response type
        assert isinstance(customcaptcha, CustomCaptchaTask.CustomCaptchaTask)

        with requests_mock.Mocker() as req_mock:
            req_mock.register_uri("POST", config.create_task_url, json=self.VALID_RESPONSE_JSON)
            req_mock.register_uri(
                "POST", config.get_result_url, json=self.VALID_RESPONSE_RESULT_JSON
            )
            customcaptcha.captcha_handler(imageUrl=self.image_url)

        history = req_mock.request_history

        assert len(history) == 2

        request_payload = history[1].json()

        # check all dict keys
        assert ["clientKey", "taskId"] == list(request_payload.keys())
        assert request_payload["taskId"] == self.VALID_RESPONSE_JSON["taskId"]

    """
    Response checking
    """

    def test_response_customcaptcha(self):
        customcaptcha = CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        )
        # check response type
        assert isinstance(customcaptcha, CustomCaptchaTask.CustomCaptchaTask)

        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.create_task_url, json=self.ERROR_RESPONSE_JSON)
            response = customcaptcha.captcha_handler(imageUrl=self.image_url)

        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    @pytest.mark.asyncio
    async def test_response_aiocustomcaptcha(self):
        customcaptcha = CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        )
        # check response type
        assert isinstance(customcaptcha, CustomCaptchaTask.aioCustomCaptchaTask)

        response = await customcaptcha.captcha_handler(imageUrl=self.image_url)
        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    """
    Fail tests
    """

    def test_fail_customcaptcha(self):
        customcaptcha = CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        )

        response = customcaptcha.captcha_handler(imageUrl=self.image_url)

        assert 1 == response["errorId"]

    def test_fail_customcaptcha_context(self):
        with CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        ) as customcaptcha:

            response = customcaptcha.captcha_handler(imageUrl=self.image_url)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiocustomcaptcha(self):
        customcaptcha = CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        )
        response = await customcaptcha.captcha_handler(imageUrl=self.image_url)
        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiocustomcaptcha_context(self):
        with CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail, assignment=self.CUSTOM_TASK
        ) as customcaptcha:
            response = await customcaptcha.captcha_handler(imageUrl=self.image_url)
            assert 1 == response["errorId"]

    """
    True tests
    """

    def test_true_customcaptcha(self):
        customcaptcha = CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_true, assignment=self.CUSTOM_TASK
        )

        response = customcaptcha.captcha_handler(imageUrl=self.image_url)

        assert 0 == response["errorId"]

    def test_true_customcaptcha_context(self):
        with CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_true, assignment=self.CUSTOM_TASK
        ) as customcaptcha:

            response = customcaptcha.captcha_handler(imageUrl=self.image_url)

            assert 0 == response["errorId"]

    @pytest.mark.asyncio
    async def test_true_aiocustomcaptcha(self):
        customcaptcha = CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_true, assignment=self.CUSTOM_TASK
        )
        response = await customcaptcha.captcha_handler(imageUrl=self.image_url)
        assert 0 == response["errorId"]

    @pytest.mark.asyncio
    async def test_true_aiocustomcaptcha_context(self):
        with CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_true, assignment=self.CUSTOM_TASK
        ) as customcaptcha:
            response = await customcaptcha.captcha_handler(imageUrl=self.image_url)
            assert 0 == response["errorId"]
