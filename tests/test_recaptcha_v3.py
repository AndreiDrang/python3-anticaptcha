"""Tests for ReCaptchaV3 task assembly and sync/async delegation."""

import pytest

from python3_anticaptcha.core.enum import CaptchaTypeEnm
from python3_anticaptcha.recaptcha_v3 import ReCaptchaV3
from tests.conftest import BaseTest


class TestReCaptchaV3(BaseTest):
    def make(self, captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless, **kwargs):
        return ReCaptchaV3(
            api_key=self.API_KEY,
            websiteURL="https://example.test",
            websiteKey="SITEKEY",
            minScore=0.7,
            captcha_type=captcha_type,
            **kwargs,
        )

    @pytest.mark.parametrize(
        "captcha_type",
        [CaptchaTypeEnm.RecaptchaV3TaskProxyless, "RecaptchaV3EnterpriseTaskProxyless"],
    )
    def test_preserves_type_and_v3_fields(self, captcha_type):
        instance = self.make(captcha_type, pageAction="login", isEnterprise=True, apiDomain="www.google.com")
        assert instance.task_params == {
            "type": captcha_type,
            "websiteURL": "https://example.test",
            "websiteKey": "SITEKEY",
            "minScore": 0.7,
            "pageAction": "login",
            "isEnterprise": True,
            "apiDomain": "www.google.com",
        }

    def test_default_optional_fields_are_explicit(self):
        instance = self.make()
        assert instance.task_params["pageAction"] is None
        assert instance.task_params["isEnterprise"] is False
        assert instance.task_params["apiDomain"] is None

    def test_sync_handler_returns_create_error(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        result = self.make().captcha_handler()
        assert result["errorId"] == 1
        assert sio_http.post.call_count == 1

    async def test_async_handler_returns_create_error(self, aio_http):
        aio_http.enqueue_post({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        result = await self.make().aio_captcha_handler()
        assert result["errorId"] == 1
        assert len(aio_http.post_calls) == 1
