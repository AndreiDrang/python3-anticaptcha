import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import CaptchaTypeEnm
from python3_anticaptcha.recaptcha_v3 import ReCaptchaV3
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer
from python3_anticaptcha.core.context_instr import AIOContextManager, SIOContextManager


class TestReCaptchaV3(BaseTest):
    pageAction = "demo_action"
    minScore = 0.3
    websiteURL = "https://rucaptcha.com/demo/recaptcha-v3"
    websiteKey = "6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu"
    websiteURLEnterprise = "https://rucaptcha.com/demo/recaptcha-v3-enterprise"
    websiteKeyEnterprise = "6Lel38UnAAAAAMRwKj9qLH2Ws4Tf2uTDQCyfgR6b"

    def test_sio_success(self):
        instance = ReCaptchaV3(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            pageAction=self.pageAction,
            minScore=self.minScore,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_success(self):
        instance = ReCaptchaV3(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            pageAction=self.pageAction,
            minScore=self.minScore,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    def test_sio_enterprise_success(self):
        instance = ReCaptchaV3(
            api_key=self.API_KEY,
            websiteKey=self.websiteKeyEnterprise,
            websiteURL=self.websiteURLEnterprise,
            captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            isEnterprise=True,
            pageAction=self.pageAction,
            minScore=self.minScore,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_enterprise_success(self):
        instance = ReCaptchaV3(
            api_key=self.API_KEY,
            websiteKey=self.websiteKeyEnterprise,
            websiteURL=self.websiteURLEnterprise,
            captcha_type=CaptchaTypeEnm.RecaptchaV3TaskProxyless,
            isEnterprise=True,
            pageAction=self.pageAction,
            minScore=self.minScore,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    def get_proxy_args(self) -> dict:
        proxy_args = super().get_proxy_args()
        proxy_args.update({"userAgent": self.get_random_string(), "cookies": self.get_random_string()})
        return proxy_args

    def test_context(self, mocker):
        context_enter_spy = mocker.spy(SIOContextManager, "__enter__")
        context_exit_spy = mocker.spy(SIOContextManager, "__exit__")
        with ReCaptchaV3(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            pageAction=self.pageAction,
            minScore=self.minScore,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    async def test_aio_context(self, mocker):
        context_enter_spy = mocker.spy(AIOContextManager, "__aenter__")
        context_exit_spy = mocker.spy(AIOContextManager, "__aexit__")
        async with ReCaptchaV3(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            pageAction=self.pageAction,
            minScore=self.minScore,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    def test_err_context(self):
        with pytest.raises(ValueError):
            with ReCaptchaV3(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                pageAction=self.pageAction,
                minScore=self.minScore,
            ) as instance:
                raise ValueError("Test error")

    async def test_err_aio_context(self):
        with pytest.raises(ValueError):
            async with ReCaptchaV3(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                pageAction=self.pageAction,
                minScore=self.minScore,
            ) as instance:
                raise ValueError("Test error")
