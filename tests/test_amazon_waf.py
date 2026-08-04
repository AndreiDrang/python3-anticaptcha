"""Tests for Amazon WAF proxyless/proxy payload selection."""

import pytest

from python3_anticaptcha.amazon_waf import AmazonWAF
from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from tests.conftest import BaseTest


class TestAmazonWAF(BaseTest):
    BASE = {"websiteURL": "https://example.test", "websiteKey": "KEY", "iv": "IV", "context": "CTX"}

    @pytest.mark.parametrize("captcha_type", [CaptchaTypeEnm.AmazonTaskProxyless, CaptchaTypeEnm.AmazonTask])
    def test_accepts_supported_types_and_maps_website_key(self, captcha_type):
        instance = AmazonWAF(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websitePublicKey"] == "KEY"
        assert instance.task_params["iv"] == "IV"
        assert instance.task_params["context"] == "CTX"

    def test_proxy_task_preserves_proxy_and_user_agent(self):
        proxy = {
            "proxyType": ProxyTypeEnm.http,
            "proxyAddress": "1.2.3.4",
            "proxyPort": 8080,
            "proxyLogin": "u",
            "proxyPassword": "p",
            "userAgent": "agent",
        }
        instance = AmazonWAF(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.AmazonTask, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_proxyless_omits_proxy_fields(self):
        instance = AmazonWAF(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.AmazonTaskProxyless, **self.BASE)
        assert "proxyType" not in instance.task_params

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            AmazonWAF(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    async def test_async_handler_sends_selected_type(self, aio_http):
        aio_http.enqueue_post({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        await AmazonWAF(
            api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.AmazonTaskProxyless, **self.BASE
        ).aio_captcha_handler()
        assert aio_http.post_calls[0]["kwargs"]["json"]["task"]["type"] == CaptchaTypeEnm.AmazonTaskProxyless
