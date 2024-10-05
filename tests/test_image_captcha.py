from unittest.mock import AsyncMock, MagicMock

from tests.conftest import BaseTest
from python3_anticaptcha.image_captcha import ImageToTextCaptcha
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer


class TestImageCaptcha(BaseTest):
    captcha_file = "files/captcha-image.jpg"
    captcha_url = (
        "https://raw.githubusercontent.com/AndreiDrang/python3-anticaptcha/refs/heads/main/files/captcha-image.jpg"
    )

    kwargs_params = {
        "phrase": False,
        "case": False,
        "numeric": 0,
        "math": False,
        "minLength": 0,
        "maxLength": 0,
        "languagePool": "en",
    }

    def test_methods_exists(self):
        assert "captcha_handler" in ImageToTextCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ImageToTextCaptcha.__dict__.keys()
        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_args(self):
        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_kwargs(self, mocker):
        mocked_method: MagicMock = mocker.patch("python3_anticaptcha.core.base.BaseCaptcha._body_file_processing")

        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        instance.captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    async def test_aio_kwargs(self, mocker):
        mocked_method: AsyncMock = mocker.patch("python3_anticaptcha.core.base.BaseCaptcha._aio_body_file_processing")

        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        await instance.aio_captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    def test_result_with_errorId(self, mocker):
        mocked_method: MagicMock = mocker.patch("python3_anticaptcha.core.base.BaseCaptcha._body_file_processing")

        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        instance.result.errorId = 1
        result = instance.captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1
        assert isinstance(result, dict)
        assert result == GetTaskResultResponseSer(**result).to_dict()

    async def test_aio_result_with_errorId(self, mocker):
        mocked_method: AsyncMock = mocker.patch("python3_anticaptcha.core.base.BaseCaptcha._aio_body_file_processing")

        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        instance.result.errorId = 1
        result = await instance.aio_captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1
        assert isinstance(result, dict)
        assert result == GetTaskResultResponseSer(**result).to_dict()
