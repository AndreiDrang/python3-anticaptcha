"""Tests for FunCaptcha proxyless/proxy task payload selection."""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.fun_captcha import FunCaptcha
from tests.conftest import BaseTest


class TestFunCaptcha(BaseTest):
    BASE = {"websiteURL": "https://example.test", "websitePublicKey": "PUBLIC"}

    @pytest.mark.parametrize("captcha_type", [CaptchaTypeEnm.FunCaptchaTaskProxyless, CaptchaTypeEnm.FunCaptchaTask])
    def test_accepts_supported_types(self, captcha_type):
        instance = FunCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websiteURL"] == self.BASE["websiteURL"]
        assert instance.task_params["websitePublicKey"] == self.BASE["websitePublicKey"]

    def test_proxyless_excludes_proxy_fields(self):
        instance = FunCaptcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.FunCaptchaTaskProxyless,
            funcaptchaApiJSSubdomain="sub",
            data="DATA",
            **self.BASE,
        )
        assert instance.task_params["funcaptchaApiJSSubdomain"] == "sub"
        assert instance.task_params["data"] == "DATA"
        assert "proxyType" not in instance.task_params

    def test_proxy_task_preserves_exact_proxy_values(self):
        proxy = {
            "proxyType": ProxyTypeEnm.http,
            "proxyAddress": "1.2.3.4",
            "proxyPort": 8080,
            "proxyLogin": "u",
            "proxyPassword": "p",
            "userAgent": "agent",
        }
        instance = FunCaptcha(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.FunCaptchaTask, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            FunCaptcha(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    def test_handler_sends_selected_type(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        FunCaptcha(
            api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.FunCaptchaTaskProxyless, **self.BASE
        ).captcha_handler()
        assert sio_http.post.call_args.kwargs["json"]["task"]["type"] == CaptchaTypeEnm.FunCaptchaTaskProxyless
