"""Tests for the AntiGate/CustomTask payload."""

from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm
from python3_anticaptcha.custom_task import CustomTask
from tests.conftest import BaseTest


class TestCustomTask(BaseTest):
    def make(self, **kwargs):
        return CustomTask(
            api_key=self.API_KEY,
            websiteURL="https://example.test",
            templateName="Template",
            variables={"selector": "#challenge"},
            proxyAddress="1.2.3.4",
            proxyPort=8080,
            proxyLogin="user",
            proxyPassword="pass",
            **kwargs,
        )

    def test_default_payload_contains_exact_custom_fields(self):
        instance = self.make()
        assert instance.task_params == {
            "type": CaptchaTypeEnm.AntiGateTask,
            "websiteURL": "https://example.test",
            "templateName": "Template",
            "variables": {"selector": "#challenge"},
            "domainsOfInterest": [],
            "proxyType": ProxyTypeEnm.https,
            "proxyAddress": "1.2.3.4",
            "proxyPort": 8080,
            "proxyLogin": "user",
            "proxyPassword": "pass",
        }

    def test_preserves_domains_and_proxy_type(self):
        instance = self.make(domainsOfInterest=["example.test"], proxyType=ProxyTypeEnm.http)
        assert instance.task_params["domainsOfInterest"] == ["example.test"]
        assert instance.task_params["proxyType"] == ProxyTypeEnm.http

    def test_handler_sends_antigate_type(self, sio_http):
        sio_http.post_sequence({"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST"})
        self.make().captcha_handler()
        assert sio_http.post.call_args.kwargs["json"]["task"]["type"] == CaptchaTypeEnm.AntiGateTask
