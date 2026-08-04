"""Tests for ``core.sio_captcha_instrument.SIOCaptchaInstrument``.

This is the sync create-task/get-result state machine plus image-file handling.
Everything runs through the real boundary: only ``requests.Session`` (and
``time.sleep``) is mocked. The create-task/get-result contract — endpoint URL,
JSON payload, and response parsing — is asserted exactly.
"""

import base64

import pytest
import requests

from python3_anticaptcha.core.base import CaptchaParams
from python3_anticaptcha.core.const import APP_KEY, BASE_REQUEST_URL, CREATE_TASK_POSTFIX, GET_RESULT_POSTFIX
from python3_anticaptcha.core.enum import SaveFormatsEnm
from python3_anticaptcha.core.sio_captcha_instrument import SIOCaptchaInstrument
from tests.core.conftest import (
    CREATE_TASK_OK,
    RESULT_ERROR,
    RESULT_PROCESSING,
    RESULT_READY,
    resp,
)

CREATE_URL = BASE_REQUEST_URL.rstrip("/") + CREATE_TASK_POSTFIX
RESULT_URL = BASE_REQUEST_URL.rstrip("/") + GET_RESULT_POSTFIX


def make_params(**task_params) -> CaptchaParams:
    p = CaptchaParams(api_key="KEY", sleep_time=0)
    p.task_params.update(task_params)
    return p


def post_kwargs(call):
    """Return (url, json) from a session.post call regardless of call style."""
    kwargs = call.kwargs
    if "url" in kwargs:
        return kwargs["url"], kwargs.get("json")
    return call.args[0], kwargs.get("json")


class TestProcessingCaptchaStateMachine:
    def test_ready_returns_after_single_result_call(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        result = SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["status"] == "ready"
        assert result["taskId"] == 4242
        assert result["errorId"] == 0
        assert result["solution"]["gRecaptchaResponse"] == "FAKE_SOLUTION_TOKEN"
        # FIXED behavior: exactly one create + one result call (was 30 before fix)
        assert sio_http.post.call_count == 2

    def test_polls_while_processing_then_returns_ready(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_PROCESSING, RESULT_READY)
        result = SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["status"] == "ready"
        assert sio_http.post.call_count == 3  # create + processing + ready

    def test_create_task_error_short_circuits_no_result_call(self, sio_http):
        create_err = {"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"}
        sio_http.post_sequence(create_err)
        result = SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DOES_NOT_EXIST"
        # critically: getTaskResult must NOT be called when creation fails
        assert sio_http.post.call_count == 1

    def test_result_error_returns_immediately(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_ERROR)
        result = SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        assert result["errorId"] == RESULT_ERROR["errorId"]
        assert result["taskId"] == 4242
        assert sio_http.post.call_count == 2

    def test_taskid_is_propagated_from_create_to_result_request(self, sio_http):
        sio_http.post_sequence({"errorId": 0, "taskId": 777}, RESULT_READY)
        SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        _, result_payload = post_kwargs(sio_http.post.call_args_list[1])
        assert result_payload["taskId"] == 777


class TestRequestPayloadContract:
    def test_create_task_hits_exact_endpoint(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        SIOCaptchaInstrument(make_params(type="ImageToTextTask", websiteURL="https://x")).processing_captcha()

        url, _ = post_kwargs(sio_http.post.call_args_list[0])
        assert url == CREATE_URL

    def test_create_task_payload_contains_clientkey_softid_and_task(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        SIOCaptchaInstrument(
            make_params(type="RecaptchaV2TaskProxyless", websiteURL="https://x", websiteKey="K")
        ).processing_captcha()

        _, body = post_kwargs(sio_http.post.call_args_list[0])
        assert body["clientKey"] == "KEY"
        assert body["softId"] == APP_KEY
        assert body["callbackUrl"] == ""
        assert body["task"]["type"] == "RecaptchaV2TaskProxyless"
        assert body["task"]["websiteURL"] == "https://x"
        assert body["task"]["websiteKey"] == "K"

    def test_get_result_hits_exact_endpoint_with_clientkey(self, sio_http):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()

        url, body = post_kwargs(sio_http.post.call_args_list[1])
        assert url == RESULT_URL
        assert body["clientKey"] == "KEY"


class TestCreateTaskHttpError:
    def test_non_200_status_raises_value_error(self, sio_http):
        sio_http.post.return_value = resp({}, status_code=500)
        with pytest.raises(ValueError):
            SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_captcha()


class TestProcessingImageCaptcha:
    def test_captcha_file_is_base64_encoded_into_body(self, sio_http, tmp_path):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        img = tmp_path / "cap.png"
        img.write_bytes(b"PNGDATA")

        SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link=None,
            captcha_file=str(img),
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        _, body = post_kwargs(sio_http.post.call_args_list[0])
        assert body["task"]["body"] == base64.b64encode(b"PNGDATA").decode("utf-8")

    def test_captcha_base64_is_encoded_into_body(self, sio_http, tmp_path):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link=None,
            captcha_file=None,
            captcha_base64=b"RAW",
            img_path=str(tmp_path),
        )

        _, body = post_kwargs(sio_http.post.call_args_list[0])
        assert body["task"]["body"] == base64.b64encode(b"RAW").decode("utf-8")

    def test_captcha_link_body_from_url_content(self, sio_http, tmp_path):
        sio_http.post_sequence(CREATE_TASK_OK, RESULT_READY)
        sio_http.get.return_value = resp({}, content=b"FROMURL")

        SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link="https://img.example.com/x.png",
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        _, body = post_kwargs(sio_http.post.call_args_list[0])
        assert body["task"]["body"] == base64.b64encode(b"FROMURL").decode("utf-8")

    def test_no_input_returns_error_12_without_network(self, sio_http, tmp_path):
        result = SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link=None,
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        assert result["errorId"] == 12
        assert result["errorCode"] == SIOCaptchaInstrument.NO_CAPTCHA_ERR
        # no input => processing_captcha must never run
        assert sio_http.post.call_count == 0
        assert sio_http.get.call_count == 0

    def test_url_read_failure_returns_error_12(self, sio_http, tmp_path):
        sio_http.get.side_effect = ValueError("network down")

        result = SIOCaptchaInstrument(make_params(type="ImageToTextTask")).processing_image_captcha(
            save_format=SaveFormatsEnm.TEMP.value,
            img_clearing=False,
            captcha_link="https://img.example.com/x.png",
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path),
        )

        assert result["errorId"] == 12
        assert "network down" in result["errorDescription"]


class TestSaveFormatConstLifecycle:
    def test_const_format_with_clearing_removes_saved_file(self, mocker, tmp_path):
        # _url_read returns content; CONST path saves a file then cleans it.
        instrument = SIOCaptchaInstrument(make_params(type="ImageToTextTask"))
        mocker.patch.object(instrument, "_url_read", return_value=resp({}, content=b"IMG"))
        # avoid the network: processing_captcha is not this unit's concern here
        mocker.patch.object(instrument, "processing_captcha", return_value={"errorId": 0})

        instrument.processing_image_captcha(
            save_format=SaveFormatsEnm.CONST.value,
            img_clearing=True,
            captcha_link="https://img.example.com/x.png",
            captcha_file=None,
            captcha_base64=None,
            img_path=str(tmp_path / "out"),
        )

        # FIXED behavior: the saved file must actually be gone after clearing
        assert list((tmp_path / "out").glob("*")) == []


class TestSendPostRequest:
    def test_returns_parsed_json_on_200(self, sio_http):
        sio_http.post.return_value = resp({"errorId": 0, "balance": 12.5})
        result = SIOCaptchaInstrument.send_post_request(
            payload={"clientKey": "K"}, session=requests.Session(), url_postfix="/getBalance"
        )
        assert result == {"errorId": 0, "balance": 12.5}

    def test_non_200_raises_value_error(self, sio_http):
        sio_http.post.return_value = resp({}, status_code=429)
        with pytest.raises(ValueError):
            SIOCaptchaInstrument.send_post_request(payload={"clientKey": "K"}, session=requests.Session())
