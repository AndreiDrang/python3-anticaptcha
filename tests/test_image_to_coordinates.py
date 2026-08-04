"""Tests for ImageToCoordinates task fields and image-handler behavior."""

import base64

from python3_anticaptcha.core.enum import CaptchaTypeEnm, SaveFormatsEnm
from python3_anticaptcha.image_to_coordinates import ImageToCoordinates
from tests.conftest import BaseTest
from tests.core.conftest import CREATE_TASK_OK, RESULT_READY


class TestImageToCoordinates(BaseTest):
    def test_defaults_are_exact(self):
        instance = ImageToCoordinates(api_key=self.API_KEY)
        assert instance.task_params == {
            "type": CaptchaTypeEnm.ImageToCoordinatesTask,
            "comment": None,
            "mode": "points",
            "websiteURL": None,
        }
        assert instance.save_format == SaveFormatsEnm.TEMP
        assert instance.img_clearing is True

    def test_constructor_preserves_coordinate_options(self):
        instance = ImageToCoordinates(
            api_key=self.API_KEY,
            comment="select cars",
            mode="rectangles",
            websiteURL="https://example.test",
            save_format=SaveFormatsEnm.CONST,
            img_clearing=False,
        )
        assert instance.task_params == {
            "type": CaptchaTypeEnm.ImageToCoordinatesTask,
            "comment": "select cars",
            "mode": "rectangles",
            "websiteURL": "https://example.test",
        }
        assert instance.save_format == SaveFormatsEnm.CONST
        assert instance.img_clearing is False

    def test_sync_handler_sends_coordinate_fields_and_body(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        result = ImageToCoordinates(
            api_key=self.API_KEY, comment="select cars", mode="rectangles", websiteURL="https://example.test"
        ).captcha_handler(captcha_base64=b"RAW")

        assert result["status"] == "ready"
        task = sio_http.post.call_args_list[0].kwargs["json"]["task"]
        assert task["comment"] == "select cars"
        assert task["mode"] == "rectangles"
        assert task["websiteURL"] == "https://example.test"
        assert task["body"] == base64.b64encode(b"RAW").decode("utf-8")

    async def test_async_handler_returns_ready_result(self, aio_http):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)
        result = await ImageToCoordinates(api_key=self.API_KEY).aio_captcha_handler(captcha_base64=b"RAW")
        assert result["status"] == "ready"
        assert result["taskId"] == 4242

    def test_extra_options_are_forwarded_exactly(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        instance = ImageToCoordinates(api_key=self.API_KEY)
        instance.captcha_handler(captcha_base64=b"RAW", comment="override", mode="points")
        task = sio_http.post.call_args.kwargs["json"]["task"]
        assert task["comment"] == "override"
        assert task["mode"] == "points"
