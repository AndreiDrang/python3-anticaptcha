"""Tests for Altcha URL/JSON and proxy task payloads."""

import pytest

from python3_anticaptcha.altcha import Altcha
from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from tests.conftest import BaseTest


class TestAltcha(BaseTest):
    BASE = {"websiteURL": "https://example.test"}

    @pytest.mark.parametrize("captcha_type", [CaptchaTypeEnm.AltchaTaskProxyless, CaptchaTypeEnm.AltchaTask])
    def test_accepts_supported_types(self, captcha_type):
        instance = Altcha(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websiteURL"] == self.BASE["websiteURL"]

    def test_proxyless_preserves_either_challenge_input(self):
        instance = Altcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
            challengeURL="/challenge",
            challengeJSON='{"algorithm":"SHA-256"}',
            **self.BASE,
        )
        assert instance.task_params["challengeURL"] == "/challenge"
        assert instance.task_params["challengeJSON"] == '{"algorithm":"SHA-256"}'
        assert "proxyType" not in instance.task_params

    def test_proxy_task_has_exact_proxy_values(self):
        proxy = {"proxyType": ProxyTypeEnm.http, "proxyAddress": "1.2.3.4", "proxyPort": 8080}
        instance = Altcha(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.AltchaTask, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            Altcha(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    def test_handler_sends_type(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        Altcha(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.AltchaTaskProxyless, **self.BASE).captcha_handler()
        assert sio_http.post.call_args.kwargs["json"]["task"]["type"] == CaptchaTypeEnm.AltchaTaskProxyless
