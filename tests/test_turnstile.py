import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.turnstile import Turnstile
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer
from python3_anticaptcha.core.context_instr import AIOContextManager, SIOContextManager


class TestTurnstile(BaseTest):
    websiteURL = "https://demo.turnstile.workers.dev/"
    websiteKey = "1x00000000000000000000AA"

    def test_sio_success(self):
        instance = Turnstile(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_success(self):
        instance = Turnstile(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    def test_err_captcha_type(self):
        with pytest.raises(ValueError):
            Turnstile(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                captcha_type=self.get_random_string(length=10),
            )

    @pytest.mark.parametrize("proxyType", ProxyTypeEnm)
    def test_proxy_args(self, proxyType: ProxyTypeEnm):
        proxy_args = self.get_proxy_args()
        proxy_args.update({"proxyType": proxyType})
        instance = Turnstile(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.TurnstileTask,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value

    def test_context(self, mocker):
        context_enter_spy = mocker.spy(SIOContextManager, "__enter__")
        context_exit_spy = mocker.spy(SIOContextManager, "__exit__")
        with Turnstile(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    async def test_aio_context(self, mocker):
        context_enter_spy = mocker.spy(AIOContextManager, "__aenter__")
        context_exit_spy = mocker.spy(AIOContextManager, "__aexit__")
        async with Turnstile(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    def test_err_context(self):
        with pytest.raises(ValueError):
            with Turnstile(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
            ) as instance:
                raise ValueError("Test error")

    async def test_err_aio_context(self):
        with pytest.raises(ValueError):
            async with Turnstile(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                captcha_type=CaptchaTypeEnm.TurnstileTaskProxyless,
            ) as instance:
                raise ValueError("Test error")
