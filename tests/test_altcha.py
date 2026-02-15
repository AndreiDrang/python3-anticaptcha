import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.altcha import Altcha
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer
from python3_anticaptcha.core.context_instr import AIOContextManager, SIOContextManager


class TestAltcha(BaseTest):
    websiteURL = "https://example.com/"
    challengeURL = "/api/challenge"

    def test_sio_success(self):
        instance = Altcha(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            challengeURL=self.challengeURL,
            captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_success(self):
        instance = Altcha(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            challengeURL=self.challengeURL,
            captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    def test_err_captcha_type(self):
        with pytest.raises(ValueError):
            Altcha(
                api_key=self.API_KEY,
                websiteURL=self.websiteURL,
                challengeURL=self.challengeURL,
                captcha_type=self.get_random_string(length=10),
            )

    @pytest.mark.parametrize("proxyType", ProxyTypeEnm)
    def test_proxy_args(self, proxyType: ProxyTypeEnm):
        proxy_args = self.get_proxy_args()
        proxy_args.update({"proxyType": proxyType})
        instance = Altcha(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            challengeURL=self.challengeURL,
            captcha_type=CaptchaTypeEnm.AltchaTask,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value

    def test_context(self, mocker):
        context_enter_spy = mocker.spy(SIOContextManager, "__enter__")
        context_exit_spy = mocker.spy(SIOContextManager, "__exit__")
        with Altcha(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            challengeURL=self.challengeURL,
            captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    async def test_aio_context(self, mocker):
        context_enter_spy = mocker.spy(AIOContextManager, "__aenter__")
        context_exit_spy = mocker.spy(AIOContextManager, "__aexit__")
        async with Altcha(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            challengeURL=self.challengeURL,
            captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    def test_err_context(self):
        with pytest.raises(ValueError):
            with Altcha(
                api_key=self.API_KEY,
                websiteURL=self.websiteURL,
                challengeURL=self.challengeURL,
                captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
            ) as instance:
                raise ValueError("Test error")

    async def test_err_aio_context(self):
        with pytest.raises(ValueError):
            async with Altcha(
                api_key=self.API_KEY,
                websiteURL=self.websiteURL,
                challengeURL=self.challengeURL,
                captcha_type=CaptchaTypeEnm.AltchaTaskProxyless,
            ) as instance:
                raise ValueError("Test error")
