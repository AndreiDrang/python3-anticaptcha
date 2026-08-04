"""Hermetic tests for all Control API endpoints.

Each test mocks only the HTTP transport and asserts the observable endpoint and
JSON payload. No account key or live service is required.
"""

import pytest

from python3_anticaptcha.control import Control
from python3_anticaptcha.core.const import BASE_REQUEST_URL
from python3_anticaptcha.core.enum import ControlPostfixEnm
from tests.conftest import BaseTest
from tests.core.conftest import resp


def endpoint(postfix) -> str:
    return BASE_REQUEST_URL.rstrip("/") + "/" + postfix


def sync_url(call) -> str:
    return call.kwargs.get("url", call.args[0])


def async_url(call) -> str:
    return call["kwargs"].get("url", call["args"][0])


class TestControl(BaseTest):
    def test_get_balance_exact_request(self, sio_http):
        sio_http.post.return_value = resp({"errorId": 0, "balance": 12.5})
        result = Control(api_key=self.API_KEY).get_balance()

        assert result == {"errorId": 0, "balance": 12.5}
        call = sio_http.post.call_args
        assert sync_url(call) == endpoint(ControlPostfixEnm.GET_BALANCE)
        assert call.kwargs["json"] == {"clientKey": self.API_KEY}

    async def test_aio_get_balance_exact_request(self, aio_http):
        aio_http.enqueue_post({"errorId": 0, "balance": 12.5})
        result = await Control(api_key=self.API_KEY).aio_get_balance()

        assert result == {"errorId": 0, "balance": 12.5}
        call = aio_http.post_calls[0]
        assert async_url(call) == endpoint(ControlPostfixEnm.GET_BALANCE)
        assert call["kwargs"]["json"] == {"clientKey": self.API_KEY}

    def test_get_queue_status_exact_request(self, sio_http):
        sio_http.post.return_value = resp({"waiting": 12, "load": 1.5, "bid": 0.001, "speed": 2, "total": 20})
        result = Control.get_queue_status(queue_id=7)

        assert result["waiting"] == 12
        call = sio_http.post.call_args
        assert sync_url(call) == endpoint(ControlPostfixEnm.GET_QUEUE_STATS)
        assert call.kwargs["json"] == {"queueId": 7}

    async def test_aio_get_queue_status_exact_request(self, aio_http):
        aio_http.enqueue_post({"waiting": 12, "load": 1.5, "bid": 0.001, "speed": 2, "total": 20})
        result = await Control.aio_get_queue_status(queue_id=7)

        assert result["total"] == 20
        call = aio_http.post_calls[0]
        assert async_url(call) == endpoint(ControlPostfixEnm.GET_QUEUE_STATS)
        assert call["kwargs"]["json"] == {"queueId": 7}

    def test_get_spending_stats_merges_clientkey_and_kwargs(self, sio_http):
        payload = {"errorId": 0, "data": [{"volume": 2, "money": 0.01}]}
        sio_http.post.return_value = resp(payload)
        result = Control(api_key=self.API_KEY).get_spending_stats(softId=867, queue="English ImageToText")

        assert result == payload
        call = sio_http.post.call_args
        assert sync_url(call) == endpoint(ControlPostfixEnm.GET_SPENDING_STATS)
        assert call.kwargs["json"] == {
            "clientKey": self.API_KEY,
            "softId": 867,
            "queue": "English ImageToText",
        }

    async def test_aio_get_spending_stats_merges_clientkey_and_kwargs(self, aio_http):
        payload = {"errorId": 0, "data": [{"volume": 2}]}
        aio_http.enqueue_post(payload)
        result = await Control(api_key=self.API_KEY).aio_get_spending_stats(softId=867)

        assert result == payload
        call = aio_http.post_calls[0]
        assert async_url(call) == endpoint(ControlPostfixEnm.GET_SPENDING_STATS)
        assert call["kwargs"]["json"] == {"clientKey": self.API_KEY, "softId": 867}

    @pytest.mark.parametrize("mode", [None, "views", "errors"])
    def test_get_app_stats_exact_payload(self, sio_http, mode):
        payload = {"errorId": 0, "chartData": []}
        sio_http.post.return_value = resp(payload)
        result = Control(api_key=self.API_KEY).get_app_stats(softId=867, mode=mode)

        assert result == payload
        call = sio_http.post.call_args
        assert sync_url(call) == endpoint(ControlPostfixEnm.GET_APP_STATS)
        assert call.kwargs["json"] == {"clientKey": self.API_KEY, "softId": 867, "mode": mode}

    async def test_aio_get_app_stats_exact_payload(self, aio_http):
        payload = {"errorId": 0, "chartData": []}
        aio_http.enqueue_post(payload)
        result = await Control(api_key=self.API_KEY).aio_get_app_stats(softId=867, mode="views")

        assert result == payload
        call = aio_http.post_calls[0]
        assert async_url(call) == endpoint(ControlPostfixEnm.GET_APP_STATS)
        assert call["kwargs"]["json"] == {"clientKey": self.API_KEY, "softId": 867, "mode": "views"}

    @pytest.mark.parametrize(
        "sync_name, async_name, postfix",
        [
            ("report_incorrect_image", "aio_report_incorrect_image", ControlPostfixEnm.REPORT_INCORRECT_IMAGE_CAPTCHA),
            (
                "report_incorrect_recaptcha",
                "aio_report_incorrect_recaptcha",
                ControlPostfixEnm.REPORT_INCORRECT_RECAPTCHA,
            ),
            ("report_correct_recaptcha", "aio_report_correct_recaptcha", ControlPostfixEnm.REPORT_CORRECT_RECAPTCHA),
            ("report_incorrect_hcaptcha", "aio_report_incorrect_hcaptcha", ControlPostfixEnm.REPORT_INCORRECT_HCAPTCHA),
        ],
    )
    def test_report_sync_endpoint_and_payload(self, sio_http, sync_name, async_name, postfix):
        payload = {"errorId": 0, "status": "success"}
        sio_http.post.return_value = resp(payload)
        result = getattr(Control(api_key=self.API_KEY), sync_name)(taskId=99)

        assert result == payload
        call = sio_http.post.call_args
        assert sync_url(call) == endpoint(postfix)
        assert call.kwargs["json"] == {"clientKey": self.API_KEY, "taskId": 99}

    @pytest.mark.parametrize(
        "async_name, postfix",
        [
            ("aio_report_incorrect_image", ControlPostfixEnm.REPORT_INCORRECT_IMAGE_CAPTCHA),
            ("aio_report_incorrect_recaptcha", ControlPostfixEnm.REPORT_INCORRECT_RECAPTCHA),
            ("aio_report_correct_recaptcha", ControlPostfixEnm.REPORT_CORRECT_RECAPTCHA),
            ("aio_report_incorrect_hcaptcha", ControlPostfixEnm.REPORT_INCORRECT_HCAPTCHA),
        ],
    )
    async def test_report_async_endpoint_and_payload(self, aio_http, async_name, postfix):
        payload = {"errorId": 0, "status": "success"}
        aio_http.enqueue_post(payload)
        result = await getattr(Control(api_key=self.API_KEY), async_name)(taskId=99)

        assert result == payload
        call = aio_http.post_calls[0]
        assert async_url(call) == endpoint(postfix)
        assert call["kwargs"]["json"] == {"clientKey": self.API_KEY, "taskId": 99}
