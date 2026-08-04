"""Tests for GeeTest v3/v4 task payload assembly."""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.gee_test import GeeTest
from tests.conftest import BaseTest


class TestGeeTest(BaseTest):
    BASE = {"websiteURL": "https://example.test", "gt": "GT"}

    @pytest.mark.parametrize("captcha_type", [CaptchaTypeEnm.GeeTestTaskProxyless, CaptchaTypeEnm.GeeTestTask])
    def test_accepts_supported_types(self, captcha_type):
        instance = GeeTest(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["version"] == 3

    def test_preserves_v3_and_v4_options(self):
        instance = GeeTest(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless,
            challenge="CHALLENGE",
            version=4,
            initParameters="INIT",
            geetestApiServerSubdomain="api",
            **self.BASE,
        )
        assert instance.task_params["challenge"] == "CHALLENGE"
        assert instance.task_params["version"] == 4
        assert instance.task_params["initParameters"] == "INIT"
        assert instance.task_params["geetestApiServerSubdomain"] == "api"

    def test_proxy_fields_only_on_proxy_task(self):
        proxy = {"proxyType": ProxyTypeEnm.https, "proxyAddress": "1.2.3.4", "proxyPort": 443}
        instance = GeeTest(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.GeeTestTask, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            GeeTest(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    async def test_async_handler_sends_type(self, aio_http):
        aio_http.enqueue_post({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        await GeeTest(
            api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless, **self.BASE
        ).aio_captcha_handler()
        assert aio_http.post_calls[0]["kwargs"]["json"]["task"]["type"] == CaptchaTypeEnm.GeeTestTaskProxyless
