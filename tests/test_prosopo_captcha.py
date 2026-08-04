"""Tests for Prosopo (new coverage for the previously untested module)."""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.prosopo_captcha import Prosopo
from tests.conftest import BaseTest


class TestProsopo(BaseTest):
    BASE = {"websiteURL": "https://example.test", "websiteKey": "SITEKEY"}

    @pytest.mark.parametrize("captcha_type", [CaptchaTypeEnm.ProsopoTaskProxyless, CaptchaTypeEnm.ProsopoTask])
    def test_accepts_supported_types(self, captcha_type):
        instance = Prosopo(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websiteKey"] == "SITEKEY"

    def test_proxyless_has_exact_base_shape(self):
        instance = Prosopo(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.ProsopoTaskProxyless, **self.BASE)
        assert set(instance.task_params) == {"type", "websiteURL", "websiteKey"}

    def test_proxy_task_preserves_exact_proxy_values(self):
        proxy = {"proxyType": ProxyTypeEnm.https, "proxyAddress": "1.2.3.4", "proxyPort": 443}
        instance = Prosopo(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.ProsopoTask, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            Prosopo(api_key=self.API_KEY, captcha_type="bad", **self.BASE)

    def test_sync_handler_sends_selected_type(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        Prosopo(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.ProsopoTaskProxyless, **self.BASE).captcha_handler()
        assert sio_http.post.call_args.kwargs["json"]["task"]["type"] == CaptchaTypeEnm.ProsopoTaskProxyless
