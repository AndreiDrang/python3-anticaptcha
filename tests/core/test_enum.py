"""Tests for ``core.enum`` — the enum is the source of truth for accepted
captcha types (per AGENTS.md), so its helper API and membership are a contract.
"""

import pytest

from python3_anticaptcha.core.enum import (
    CaptchaTypeEnm,
    ControlPostfixEnm,
    EndpointPostfixEnm,
    ProxyTypeEnm,
    ResponseStatusEnm,
    SaveFormatsEnm,
)


class TestMyEnumHelpers:
    def test_list_returns_enum_members(self):
        members = ProxyTypeEnm.list()
        assert isinstance(members, list)
        assert all(isinstance(m, ProxyTypeEnm) for m in members)

    def test_list_values_are_strings(self):
        values = ProxyTypeEnm.list_values()
        assert isinstance(values, list)
        assert all(isinstance(v, str) for v in values)

    def test_list_names_are_strings(self):
        names = ProxyTypeEnm.list_names()
        assert isinstance(names, list)
        assert all(isinstance(n, str) for n in names)

    def test_list_values_and_names_have_same_length(self):
        assert len(ProxyTypeEnm.list_values()) == len(ProxyTypeEnm.list_names()) == len(ProxyTypeEnm.list())


class TestProxyTypeEnm:
    @pytest.mark.parametrize("value", ["http", "https", "socks4", "socks5"])
    def test_supported_proxy_types(self, value):
        assert value in ProxyTypeEnm.list_values()

    def test_enum_members_are_usable_as_strings(self):
        # (str, MyEnum) subclass — members compare equal to their values
        assert ProxyTypeEnm.http == "http"


class TestResponseStatusEnm:
    @pytest.mark.parametrize("value", ["processing", "ready", "error"])
    def test_all_statuses_present(self, value):
        assert value in ResponseStatusEnm.list_values()


class TestSaveFormatsEnm:
    def test_values(self):
        assert set(SaveFormatsEnm.list_values()) == {"temp", "const"}


class TestCaptchaTypeEnm:
    EXPECTED_TYPES = {
        "Control",
        "ImageToTextTask",
        "ImageToCoordinatesTask",
        "RecaptchaV2Task",
        "RecaptchaV2TaskProxyless",
        "RecaptchaV3TaskProxyless",
        "RecaptchaV2EnterpriseTask",
        "RecaptchaV2EnterpriseTaskProxyless",
        "FunCaptchaTask",
        "FunCaptchaTaskProxyless",
        "GeeTestTask",
        "GeeTestTaskProxyless",
        "HCaptchaTask",
        "HCaptchaTaskProxyless",
        "TurnstileTask",
        "TurnstileTaskProxyless",
        "FriendlyCaptchaTask",
        "FriendlyCaptchaTaskProxyless",
        "ProsopoTask",
        "ProsopoTaskProxyless",
        "AmazonTask",
        "AmazonTaskProxyless",
        "AltchaTask",
        "AltchaTaskProxyless",
        "AntiGateTask",
    }

    def test_all_expected_types_present(self):
        assert set(CaptchaTypeEnm.list_values()) == self.EXPECTED_TYPES

    def test_no_duplicate_values(self):
        values = CaptchaTypeEnm.list_values()
        assert len(values) == len(set(values))


class TestEndpointAndControlPostfix:
    def test_endpoint_postfix_values(self):
        assert EndpointPostfixEnm.CREATE_TASK == "createTask"
        assert EndpointPostfixEnm.GET_TASK_RESULT == "getTaskResult"

    def test_control_postfix_values_match_api_doc(self):
        # These map directly to the live API method names — pin them exactly.
        assert ControlPostfixEnm.GET_BALANCE == "getBalance"
        assert ControlPostfixEnm.GET_QUEUE_STATS == "getQueueStats"
        assert ControlPostfixEnm.GET_APP_STATS == "getAppStats"
        assert ControlPostfixEnm.GET_SPENDING_STATS == "getSpendingStats"
        assert ControlPostfixEnm.REPORT_INCORRECT_IMAGE_CAPTCHA == "reportIncorrectImageCaptcha"
        assert ControlPostfixEnm.REPORT_INCORRECT_RECAPTCHA == "reportIncorrectRecaptcha"
        assert ControlPostfixEnm.REPORT_CORRECT_RECAPTCHA == "reportCorrectRecaptcha"
        assert ControlPostfixEnm.REPORT_INCORRECT_HCAPTCHA == "reportIncorrectHcaptcha"
