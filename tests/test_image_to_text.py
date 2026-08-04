"""Tests for ImageToText configuration and image-handler behavior."""

import base64

from python3_anticaptcha.core.enum import CaptchaTypeEnm, SaveFormatsEnm
from python3_anticaptcha.image_to_text import ImageToText
from tests.conftest import BaseTest
from tests.core.conftest import CREATE_TASK_OK, RESULT_READY


class TestImageToText(BaseTest):
    def test_defaults_configure_image_task(self):
        instance = ImageToText(api_key=self.API_KEY)
        assert instance.task_params == {"type": CaptchaTypeEnm.ImageToTextTask}
        assert instance.save_format == SaveFormatsEnm.TEMP
        assert instance.img_clearing is True

    def test_constructor_preserves_file_options(self):
        instance = ImageToText(
            api_key=self.API_KEY,
            captcha_type="ImageToTextTask",
            save_format=SaveFormatsEnm.CONST,
            img_clearing=False,
            img_path="/tmp/captchas",
            sleep_time=2,
        )
        assert instance.task_params["type"] == "ImageToTextTask"
        assert instance.save_format == SaveFormatsEnm.CONST
        assert instance.img_clearing is False
        assert instance.img_path == "/tmp/captchas"
        assert instance.sleep_time == 2

    def test_sync_handler_encodes_base64_and_parses_response(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        result = ImageToText(api_key=self.API_KEY).captcha_handler(captcha_base64=b"RAW")

        assert result["status"] == "ready"
        assert result["taskId"] == 4242
        body = sio_http.post.call_args_list[0].kwargs["json"]
        assert body["task"]["type"] == CaptchaTypeEnm.ImageToTextTask
        assert body["task"]["body"] == base64.b64encode(b"RAW").decode("utf-8")

    async def test_async_handler_encodes_base64_and_parses_response(self, aio_http):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)
        result = await ImageToText(api_key=self.API_KEY).aio_captcha_handler(captcha_base64=b"RAW")

        assert result["status"] == "ready"
        assert result["taskId"] == 4242
        body = aio_http.post_calls[0]["kwargs"]["json"]
        assert body["task"]["body"] == base64.b64encode(b"RAW").decode("utf-8")

    def test_extra_task_options_are_forwarded_exactly(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        instance = ImageToText(api_key=self.API_KEY)
        instance.captcha_handler(captcha_base64=b"RAW", phrase=True, numeric=1, languagePool="en")
        task = sio_http.post.call_args.kwargs["json"]["task"]
        assert task["phrase"] is True
        assert task["numeric"] == 1
        assert task["languagePool"] == "en"
