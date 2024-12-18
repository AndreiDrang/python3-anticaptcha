import base64
from unittest.mock import MagicMock

import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import SaveFormatsEnm, ResponseStatusEnm
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer
from python3_anticaptcha.image_to_coordinates import ImageToCoordinates
from python3_anticaptcha.core.captcha_instrument import FileInstrument
from python3_anticaptcha.core.aio_captcha_instrument import AIOCaptchaInstrument
from python3_anticaptcha.core.sio_captcha_instrument import SIOCaptchaInstrument


class TestImageToCoordinates(BaseTest):
    captcha_file = "files/captcha-image-coordinates.jpg"
    captcha_url = "https://raw.githubusercontent.com/AndreiDrang/python3-anticaptcha/refs/heads/main/files/captcha-image-coordinates.jpg"

    kwargs_params = {
        "comment": "select all cats",
        "mode": "points",
        "websiteURL": captcha_url,
    }

    def test_sio_success_file(self):
        instance = ImageToCoordinates(api_key=self.API_KEY, **self.kwargs_params)
        result = instance.captcha_handler(captcha_file=self.captcha_file)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_success_file(self):
        instance = ImageToCoordinates(api_key=self.API_KEY, **self.kwargs_params)
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
            "python3_anticaptcha.image_to_coordinates.SIOCaptchaInstrument",
            side_effect=lambda *args, **kwargs: captured_instances.append(SIOCaptchaInstrument(*args, **kwargs))
            or captured_instances[-1],
        )
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_instrument.SIOCaptchaInstrument.processing_captcha"
        )
        mocked_method.return_value = "tested"

        instance = ImageToCoordinates(api_key=self.API_KEY, save_format=save_format, img_clearing=img_clearing)
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
            "python3_anticaptcha.image_to_coordinates.AIOCaptchaInstrument",
            side_effect=lambda *args, **kwargs: captured_instances.append(AIOCaptchaInstrument(*args, **kwargs))
            or captured_instances[-1],
        )
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_instrument.AIOCaptchaInstrument.processing_captcha"
        )
        mocked_method.return_value = "tested"

        instance = ImageToCoordinates(api_key=self.API_KEY, save_format=save_format, img_clearing=img_clearing)
        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

        assert mocked_method.call_count == 1
        assert result == mocked_method.return_value
        instance_b = captured_instances[0]
        real_data = instance_b.captcha_params
        assert isinstance(real_data.create_task_payload.task["body"], str)

    def test_err_captcha_link(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_instrument.SIOCaptchaInstrument._url_read"
        )
        mocked_method.side_effect = ValueError("Test error")

        instance = ImageToCoordinates(api_key=self.API_KEY)
        result = instance.captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0

    async def test_aio_err_captcha_link(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_instrument.AIOCaptchaInstrument._url_read"
        )
        mocked_method.side_effect = ValueError("Test error")

        instance = ImageToCoordinates(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0

    def test_captcha_base64(self, mocker):
        captcha_params_spy = mocker.spy(SIOCaptchaInstrument, "processing_image_captcha")
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_instrument.SIOCaptchaInstrument.processing_captcha"
        )
        mocked_method.return_value = "tested"

        file_data = self.read_file(file_path=self.captcha_file)

        instance = ImageToCoordinates(api_key=self.API_KEY)
        result = instance.captcha_handler(captcha_base64=file_data)

        assert captcha_params_spy.call_args.kwargs["captcha_base64"] == file_data
        assert instance._captcha_handling_instrument.captcha_params.create_task_payload.task[
            "body"
        ] == base64.b64encode(file_data).decode("utf-8")
        assert result == mocked_method.return_value

    async def test_aio_captcha_base64(self, mocker):
        captcha_params_spy = mocker.spy(AIOCaptchaInstrument, "processing_image_captcha")
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_instrument.AIOCaptchaInstrument.processing_captcha"
        )
        mocked_method.return_value = "tested"

        file_data = self.read_file(file_path=self.captcha_file)

        instance = ImageToCoordinates(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(captcha_base64=file_data)

        assert captcha_params_spy.call_args.kwargs["captcha_base64"] == file_data
        assert instance._captcha_handling_instrument.captcha_params.create_task_payload.task[
            "body"
        ] == base64.b64encode(file_data).decode("utf-8")
        assert result == mocked_method.return_value

    def test_methods_exists(self):
        assert "captcha_handler" in ImageToCoordinates.__dict__.keys()
        assert "aio_captcha_handler" in ImageToCoordinates.__dict__.keys()
        instance = ImageToCoordinates(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_args(self):
        instance = ImageToCoordinates(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_del(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_instrument.SIOCaptchaInstrument.processing_captcha"
        )
        mocked_method.return_value = "tested"
        del_method = mocker.spy(FileInstrument, "_file_clean")

        instance = ImageToCoordinates(api_key=self.API_KEY, save_format=SaveFormatsEnm.CONST, img_clearing=True)
        result = instance.captcha_handler(captcha_link=self.captcha_url)

        assert mocked_method.call_count == 1
        assert result == mocked_method.return_value
        assert del_method.call_count == 1

    async def test_aio_del(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_instrument.AIOCaptchaInstrument.processing_captcha"
        )
        mocked_method.return_value = "tested"
        del_method = mocker.spy(FileInstrument, "_file_clean")

        instance = ImageToCoordinates(api_key=self.API_KEY, save_format=SaveFormatsEnm.CONST, img_clearing=True)
        result = await instance.aio_captcha_handler(captcha_link=self.captcha_url)

        assert mocked_method.call_count == 1
        assert result == mocked_method.return_value
        assert del_method.call_count == 1

    def test_init_kwargs(self):
        instance = ImageToCoordinates(api_key=self.API_KEY, **self.kwargs_params)

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    def test_kwargs(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.sio_captcha_instrument.SIOCaptchaInstrument.processing_image_captcha"
        )

        instance = ImageToCoordinates(api_key=self.API_KEY)
        instance.captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    async def test_aio_kwargs(self, mocker):
        mocked_method: MagicMock = mocker.patch(
            "python3_anticaptcha.core.aio_captcha_instrument.AIOCaptchaInstrument.processing_image_captcha"
        )

        instance = ImageToCoordinates(api_key=self.API_KEY)
        await instance.aio_captcha_handler(**self.kwargs_params)

        assert mocked_method.call_count == 1

        assert set(self.kwargs_params.keys()).issubset(set(instance.task_params.keys()))
        assert set(self.kwargs_params.values()).issubset(set(instance.task_params.values()))

    def test_err_body_file_processing(self, mocker):
        instance = ImageToCoordinates(api_key=self.API_KEY)
        result = instance.captcha_handler(**self.kwargs_params)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.status == ResponseStatusEnm.error
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0

    async def test_aio_err_body_file_processing(self, mocker):
        instance = ImageToCoordinates(api_key=self.API_KEY)
        result = await instance.aio_captcha_handler(**self.kwargs_params)

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.status == ResponseStatusEnm.error
        assert ser_result.errorId == 12
        assert ser_result.taskId is None
        assert ser_result.cost == 0.0
