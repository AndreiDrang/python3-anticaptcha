"""Tests for FriendlyCaptcha (new coverage for the previously untested module)."""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.friendly_captcha import FriendlyCaptcha
from tests.conftest import BaseTest


class TestFriendlyCaptcha(BaseTest):
    BASE = {"websiteURL": "https://example.test", "websiteKey": "SITEKEY"}

    @pytest.mark.parametrize(
        "captcha_type", [CaptchaTypeEnm.FriendlyCaptchaTaskProxyless, CaptchaTypeEnm.FriendlyCaptchaTask]
    )
    def test_accepts_supported_types(self, captcha_type):
        instance = FriendlyCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websiteKey"] == "SITEKEY"

    def test_proxyless_has_no_proxy_keys(self):
        instance = FriendlyCaptcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.FriendlyCaptchaTaskProxyless,
            **self.BASE,
        )
        assert set(instance.task_params) == {"type", "websiteURL", "websiteKey"}

    def test_proxy_task_preserves_exact_proxy_values(self):
        proxy = {
            "proxyType": ProxyTypeEnm.http,
            "proxyAddress": "1.2.3.4",
            "proxyPort": 8080,
            "proxyLogin": "u",
            "proxyPassword": "p",
            "userAgent": "agent",
        }
        instance = FriendlyCaptcha(
            api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.FriendlyCaptchaTask, **self.BASE, **proxy
        )
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            FriendlyCaptcha(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    async def test_async_handler_sends_selected_type(self, aio_http):
        aio_http.enqueue_post({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        await FriendlyCaptcha(
            api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.FriendlyCaptchaTaskProxyless, **self.BASE
        ).aio_captcha_handler()
        assert aio_http.post_calls[0]["kwargs"]["json"]["task"]["type"] == CaptchaTypeEnm.FriendlyCaptchaTaskProxyless
