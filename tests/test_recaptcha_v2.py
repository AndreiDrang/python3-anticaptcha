"""Behavioral tests for ``ReCaptchaV2`` payload assembly.

No test calls the live service. The class's business contract is the exact task
shape selected by the four accepted captcha types; transport state-machine tests
live in ``tests/core/test_*captcha_instrument.py``.
"""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2
from tests.conftest import BaseTest


class TestReCaptchaV2(BaseTest):
    BASE = {"websiteURL": "https://example.test", "websiteKey": "SITEKEY"}

    @pytest.mark.parametrize(
        "captcha_type",
        [
            CaptchaTypeEnm.RecaptchaV2TaskProxyless,
            CaptchaTypeEnm.RecaptchaV2Task,
            CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
            CaptchaTypeEnm.RecaptchaV2EnterpriseTask,
        ],
    )
    def test_accepts_every_supported_type(self, captcha_type):
        instance = ReCaptchaV2(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE)
        assert instance.task_params["type"] == captcha_type
        assert instance.task_params["websiteURL"] == self.BASE["websiteURL"]
        assert instance.task_params["websiteKey"] == self.BASE["websiteKey"]

    @pytest.mark.parametrize(
        "captcha_type",
        [CaptchaTypeEnm.RecaptchaV2TaskProxyless, CaptchaTypeEnm.RecaptchaV2Task],
    )
    def test_non_enterprise_fields_are_present(self, captcha_type):
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            captcha_type=captcha_type,
            recaptchaDataSValue="DATA-S",
            isInvisible=True,
            **self.BASE,
        )
        assert instance.task_params["recaptchaDataSValue"] == "DATA-S"
        assert instance.task_params["isInvisible"] is True

    @pytest.mark.parametrize(
        "captcha_type",
        [CaptchaTypeEnm.RecaptchaV2Task, CaptchaTypeEnm.RecaptchaV2EnterpriseTask],
    )
    def test_proxy_type_contains_exact_proxy_fields(self, captcha_type):
        proxy = {
            "proxyType": ProxyTypeEnm.http,
            "proxyAddress": "1.2.3.4",
            "proxyPort": 8080,
            "proxyLogin": "user",
            "proxyPassword": "pass",
            "userAgent": "agent",
            "cookies": "a=b",
        }
        instance = ReCaptchaV2(api_key=self.API_KEY, captcha_type=captcha_type, **self.BASE, **proxy)
        for key, value in proxy.items():
            assert instance.task_params[key] == value

    def test_enterprise_fields_are_not_replaced_by_proxy_fields(self):
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
            enterprisePayload={"s": "TOKEN"},
            apiDomain="www.google.com",
            **self.BASE,
        )
        assert instance.task_params["enterprisePayload"] == {"s": "TOKEN"}
        assert instance.task_params["apiDomain"] == "www.google.com"
        assert "proxyType" not in instance.task_params

    def test_rejects_unsupported_type(self):
        with pytest.raises(ValueError, match="Invalid `captcha_type`"):
            ReCaptchaV2(api_key=self.API_KEY, captcha_type="Unsupported", **self.BASE)

    def test_handler_uses_configured_client_key_and_type(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        result = ReCaptchaV2(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
            **self.BASE,
        ).captcha_handler()

        assert result["errorId"] == 1
        body = sio_http.post.call_args.kwargs["json"]
        assert body["clientKey"] == self.API_KEY
        assert body["task"]["type"] == CaptchaTypeEnm.RecaptchaV2TaskProxyless
