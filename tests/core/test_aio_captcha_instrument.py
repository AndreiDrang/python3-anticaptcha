"""Async counterpart to ``test_sio_captcha_instrument``.

The same create-task/get-result state machine and payload contract are exercised
through a fake ``aiohttp.ClientSession``. ``asyncio_mode=auto`` means these tests
intentionally have no ``@pytest.mark.asyncio`` decorator.
"""

import base64

import pytest

from python3_anticaptcha.core.aio_captcha_instrument import AIOCaptchaInstrument
from python3_anticaptcha.core.base import CaptchaParams
from python3_anticaptcha.core.const import APP_KEY, BASE_REQUEST_URL, CREATE_TASK_POSTFIX, GET_RESULT_POSTFIX
from python3_anticaptcha.core.enum import SaveFormatsEnm
from tests.core.conftest import CREATE_TASK_OK, RESULT_ERROR, RESULT_PROCESSING, RESULT_READY

CREATE_URL = BASE_REQUEST_URL.rstrip("/") + CREATE_TASK_POSTFIX
RESULT_URL = BASE_REQUEST_URL.rstrip("/") + GET_RESULT_POSTFIX


def make_params(**task_params) -> CaptchaParams:
    p = CaptchaParams(api_key="KEY", sleep_time=0)
    p.task_params.update(task_params)
    return p


def call_url_and_json(call):
    kwargs = call["kwargs"]
    url = kwargs.get("url", call["args"][0] if call["args"] else None)
    return url, kwargs.get("json")


class TestAsyncProcessingStateMachine:
    async def test_ready_returns_after_single_result_call(self, aio_http):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)

        result = await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["status"] == "ready"
        assert result["taskId"] == 4242
        assert result["solution"]["gRecaptchaResponse"] == "FAKE_SOLUTION_TOKEN"
        assert len(aio_http.post_calls) == 2

    async def test_polls_while_processing_then_returns_ready(self, aio_http):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_PROCESSING)
        aio_http.enqueue_post(RESULT_READY)

        result = await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["status"] == "ready"
        assert len(aio_http.post_calls) == 3

    async def test_create_task_error_short_circuits(self, aio_http):
        aio_http.enqueue_post({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})

        result = await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["errorId"] == 1
        assert len(aio_http.post_calls) == 1

    async def test_result_error_returns_with_taskid(self, aio_http):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_ERROR)

        result = await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["errorId"] == RESULT_ERROR["errorId"]
        assert result["taskId"] == 4242
        assert len(aio_http.post_calls) == 2


class TestAsyncRequestPayloadContract:
    async def test_create_task_endpoint_and_payload(self, aio_http):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)

        await AIOCaptchaInstrument(
            make_params(type="RecaptchaV2TaskProxyless", websiteURL="https://x", websiteKey="K")
        ).processing_captcha()

        create_url, body = call_url_and_json(aio_http.post_calls[0])
        assert create_url == CREATE_URL
        assert body["clientKey"] == "KEY"
        assert body["softId"] == APP_KEY
        assert body["task"] == {"type": "RecaptchaV2TaskProxyless", "websiteURL": "https://x", "websiteKey": "K"}

    async def test_result_endpoint_and_taskid_payload(self, aio_http):
        aio_http.enqueue_post({"errorId": 0, "taskId": 777})
        aio_http.enqueue_post(RESULT_READY)

        await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        result_url, body = call_url_and_json(aio_http.post_calls[1])
        assert result_url == RESULT_URL
        assert body["clientKey"] == "KEY"
        assert body["taskId"] == 777


class TestAsyncCreateTaskHttpError:
    async def test_non_200_status_raises_value_error(self, aio_http):
        aio_http.enqueue_post({}, status=500, reason="server failed")

        with pytest.raises(ValueError, match="server failed"):
            await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()


class TestAsyncProcessingImageCaptcha:
    async def test_file_is_base64_encoded_into_body(self, aio_http, tmp_path):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)
        img = tmp_path / "cap.png"
        img.write_bytes(b"PNGDATA")

        await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link=None,
            captcha_file=str(img),
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        _, body = call_url_and_json(aio_http.post_calls[0])
        assert body["task"]["body"] == base64.b64encode(b"PNGDATA").decode("utf-8")

    async def test_base64_is_encoded_into_body(self, aio_http, tmp_path):
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)

        await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link=None,
            captcha_file=None,
            captcha_base64=b"RAW",
            img_path=str(tmp_path),
        )

        _, body = call_url_and_json(aio_http.post_calls[0])
        assert body["task"]["body"] == base64.b64encode(b"RAW").decode("utf-8")

    async def test_link_content_is_encoded_into_body(self, aio_http, tmp_path):
        aio_http.enqueue_get(content=b"FROMURL")
        aio_http.enqueue_post(CREATE_TASK_OK)
        aio_http.enqueue_post(RESULT_READY)

        await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link="https://img.example.com/x.png",
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        _, body = call_url_and_json(aio_http.post_calls[0])
        assert body["task"]["body"] == base64.b64encode(b"FROMURL").decode("utf-8")

    async def test_no_input_returns_error_12_without_network(self, aio_http, tmp_path):
        result = await AIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link=None,
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        assert result["errorId"] == 12
        assert result["errorCode"] == AIOCaptchaInstrument.NO_CAPTCHA_ERR
        assert aio_http.post_calls == []

    async def test_url_read_failure_returns_error_12(self, mocker, aio_http, tmp_path):
        instrument = AIOCaptchaInstrument(make_params(type="ImageToTextTask"))
        mocker.patch.object(instrument, "_url_read", side_effect=ValueError("network down"))

        result = await instrument.processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link="https://img.example.com/x.png",
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        assert result["errorId"] == 12
        assert "network down" in result["errorDescription"]

    async def test_const_format_with_clearing_removes_saved_file(self, mocker, tmp_path):
        instrument = AIOCaptchaInstrument(make_params(type="ImageToTextTask"))
        mocker.patch.object(instrument, "_url_read", return_value=b"IMG")
        mocker.patch.object(instrument, "processing_captcha", return_value={"errorId": 0})

        await instrument.processing_image_captcha(
            save_format=SaveFormatsEnm.CONST.value,
            img_clearing=True,
            captcha_link="https://img.example.com/x.png",
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path / "out"),
        )

        assert list((tmp_path / "out").glob("*")) == []


class TestAsyncSendPostRequest:
    async def test_returns_json(self, aio_http):
        aio_http.enqueue_post({"errorId": 0, "balance": 12.5})

        result = await AIOCaptchaInstrument.send_post_request(payload={"clientKey": "K"}, url_postfix="/getBalance")

        assert result == {"errorId": 0, "balance": 12.5}

    async def test_non_200_raises_value_error(self, aio_http):
        aio_http.enqueue_post({}, status=429, reason="too many")

        with pytest.raises(ValueError, match="too many"):
            await AIOCaptchaInstrument.send_post_request(payload={"clientKey": "K"})
