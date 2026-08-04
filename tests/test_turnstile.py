"""Tests for Turnstile proxyless/proxy task payloads."""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.turnstile import Turnstile
from tests.conftest import BaseTest


class TestTurnstile(BaseTest):
    BASE = {"websiteURL": "https://example.test", "websiteKey": "SITEKEY"}

    @pytest.mark.parametrize("captcha_type", [CaptchaTypeEnm.TurnstileTaskProxyless, CaptchaTypeEnm.TurnstileTask])
    def test_accepts_supported_types(self, captcha_type):
        instance = Turnstile(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websiteURL"] == self.BASE["websiteURL"]

    def test_optional_challenge_fields_are_preserved(self):
        instance = Turnstile(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
            action="login",
            turnstileCData="CDATA",
            **self.BASE,
        )
        assert instance.task_params["action"] == "login"
        assert instance.task_params["turnstileCData"] == "CDATA"

    def test_proxy_task_has_exact_proxy_values(self):
        proxy = {"proxyType": ProxyTypeEnm.http, "proxyAddress": "1.2.3.4", "proxyPort": 8080}
        instance = Turnstile(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.TurnstileTask, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_proxyless_does_not_include_proxy_keys(self):
        instance = Turnstile(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless, **self.BASE)
        assert "proxyType" not in instance.task_params

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            Turnstile(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    def test_sync_handler_sends_type(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        Turnstile(
            api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless, **self.BASE
        ).captcha_handler()
        assert sio_http.post.call_args.kwargs["json"]["task"]["type"] == CaptchaTypeEnm.TurnstileTaskProxyless
