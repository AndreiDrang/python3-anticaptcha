import base64
from unittest.mock import MagicMock

import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import SaveFormatsEnm, ResponseStatusEnm
from python3_anticaptcha.image_to_text import ImageToText
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer
from python3_anticaptcha.core.aio_captcha_handler import AIOCaptchaHandler
from python3_anticaptcha.core.sio_captcha_handler import SIOCaptchaHandler


class TestImageToText(BaseTest):
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

    def test_sio_success_file(self):
        instance = ImageToText(api_key=self.API_KEY)
        result = instance.captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_success_file(self):
        instance = ImageToText(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    @pytest.mark.parametrize("img_clearing", (True, False))
    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    def test_captcha_link(self, mocker, save_format, img_clearing):
        captured_instances = []
        mocker.patch(
            "python3_anticaptcha.image_captcha.SIOCaptchaHandler",
            side_effect=lambda *args, **kwargs: captured_instances.append(SIOCaptchaHandler(*args, **kwargs))
            or captured_instances[-1],
        )
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_handler.SIOCaptchaHandler.processing_captcha"
        )
        mocked_method.return_value = "tested"

        instance = ImageToText(api_key=self.API_KEY, save_format=save_format, img_clearing=img_clearing)
        result = instance.captcha_handler(captcha_link=self.captcha_url)

        assert mocked_method.call_count == 1
        assert result == mocked_method.return_value
        instance_b = captured_instances[0]
        real_data = instance_b.captcha_params
        assert isinstance(real_data.create_task_payload.task["body"], str)

    @pytest.mark.parametrize("img_clearing", (True, False))
    @pytest.mark.parametrize("save_format", SaveFormatsEnm.list_values())
    async def test_aio_captcha_link(self, mocker, save_format, img_clearing):
        captured_instances = []
        mocker.patch(
            "python3_anticaptcha.image_captcha.AIOCaptchaHandler",
            side_effect=lambda *args, **kwargs: captured_instances.append(AIOCaptchaHandler(*args, **kwargs))
            or captured_instances[-1],
        )
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_handler.AIOCaptchaHandler.processing_captcha"
        )
        mocked_method.return_value = "tested"

        instance = ImageToText(api_key=self.API_KEY, save_format=save_format, img_clearing=img_clearing)
        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

        assert mocked_method.call_count == 1
        assert result == mocked_method.return_value
        instance_b = captured_instances[0]
        real_data = instance_b.captcha_params
        assert isinstance(real_data.create_task_payload.task["body"], str)

    def test_err_captcha_link(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_handler.SIOCaptchaHandler._url_read"
        )
        mocked_method.side_effect = ValueError("Test error")

        instance = ImageToText(api_key=self.API_KEY)
        result = instance.captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0

    async def test_aio_err_captcha_link(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_handler.AIOCaptchaHandler._url_read"
        )
        mocked_method.side_effect = ValueError("Test error")

        instance = ImageToText(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0

    def test_captcha_base64(self, mocker):
        captcha_params_spy = mocker.spy(SIOCaptchaHandler, "body_file_processing")
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_handler.SIOCaptchaHandler.processing_captcha"
        )
        mocked_method.return_value = "tested"

        file_data = self.read_file(file_path=self.captcha_file)

        instance = ImageToText(api_key=self.API_KEY)
        result = instance.captcha_handler(captcha_base64=file_data)

        assert captcha_params_spy.call_args.kwargs["captcha_base64"] == file_data
        assert instance._captcha_handling_instrument.captcha_params.create_task_payload.task[
            "body"
        ] == base64.b64encode(file_data).decode("utf-8")
        assert result == mocked_method.return_value

    async def test_aio_captcha_base64(self, mocker):
        captcha_params_spy = mocker.spy(AIOCaptchaHandler, "body_file_processing")
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_handler.AIOCaptchaHandler.processing_captcha"
        )
        mocked_method.return_value = "tested"

        file_data = self.read_file(file_path=self.captcha_file)

        instance = ImageToText(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(captcha_base64=file_data)

        assert captcha_params_spy.call_args.kwargs["captcha_base64"] == file_data
        assert instance._captcha_handling_instrument.captcha_params.create_task_payload.task[
            "body"
        ] == base64.b64encode(file_data).decode("utf-8")
        assert result == mocked_method.return_value

    def test_methods_exists(self):
        assert "captcha_handler" in ImageToText.__dict__.keys()
        assert "aio_captcha_handler" in ImageToText.__dict__.keys()
        instance = ImageToText(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_args(self):
        instance = ImageToText(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_del(self, mocker):
        mocked_method: MagicMock = mocker.patch("shutil.rmtree")
        ImageToText(api_key=self.API_KEY, save_format=SaveFormatsEnm.CONST, img_clearing=True)
        assert mocked_method.call_count == 1

    def test_kwargs(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_handler.SIOCaptchaHandler.body_file_processing"
        )

        instance = ImageToText(api_key=self.API_KEY)
        instance.captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    async def test_aio_kwargs(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_handler.AIOCaptchaHandler.body_file_processing"
        )

        instance = ImageToText(api_key=self.API_KEY)
        await instance.aio_captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    def test_err_body_file_processing(self, mocker):
        instance = ImageToText(api_key=self.API_KEY)
        result = instance.captcha_handler(**self.kwargs_params)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.status == ResponseStatusEnm.error
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0

    async def test_aio_err_body_file_processing(self, mocker):
        instance = ImageToText(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(**self.kwargs_params)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.status == ResponseStatusEnm.error
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0
