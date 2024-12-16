import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer
from python3_anticaptcha.core.context_instr import AIOContextManager, SIOContextManager


class TestReCaptchaV2(BaseTest):
    recaptcha_v2_proxyless_types = (
        CaptchaTypeEnm.RecaptchaV2TaskProxyless,
        CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
    )
    recaptcha_v2_proxy_types = (
        CaptchaTypeEnm.RecaptchaV2Task,
        CaptchaTypeEnm.RecaptchaV2EnterpriseTask,
    )
    recaptcha_v2_types = recaptcha_v2_proxy_types + recaptcha_v2_proxyless_types

    websiteURL = "https://rucaptcha.com/demo/recaptcha-v2"
    websiteKey = "6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u"
    websiteURLEnterprise = "https://rucaptcha.com/demo/recaptcha-v2-enterprise"
    websiteKeyEnterprise = "6Lf26sUnAAAAAIKLuWNYgRsFUfmI-3Lex3xT5N-s"

    def test_sio_success(self):
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_success(self):
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    def test_sio_enterprise_success(self):
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKeyEnterprise,
            websiteURL=self.websiteURLEnterprise,
            captcha_type=CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 0
        assert ser_result.taskId is not None
        assert ser_result.cost != 0.0

    async def test_aio_enterprise_success(self):
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKeyEnterprise,
            websiteURL=self.websiteURLEnterprise,
            captcha_type=CaptchaTypeEnm.RecaptchaV2EnterpriseTaskProxyless,
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

    def test_err_captcha_type(self):
        with pytest.raises(ValueError):
            ReCaptchaV2(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                captcha_type=self.get_random_string(length=10),
            )

    @pytest.mark.parametrize("recaptcha_type", recaptcha_v2_proxy_types)
    @pytest.mark.parametrize("proxyType", ProxyTypeEnm)
    def test_proxy_args(self, proxyType: ProxyTypeEnm, recaptcha_type):
        proxy_args = self.get_proxy_args()
        proxy_args.update({"proxyType": proxyType})
        instance = ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=recaptcha_type,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value

    @pytest.mark.parametrize("recaptcha_type", recaptcha_v2_types)
    def test_context(self, mocker, recaptcha_type):
        context_enter_spy = mocker.spy(SIOContextManager, "__enter__")
        context_exit_spy = mocker.spy(SIOContextManager, "__exit__")
        with ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=recaptcha_type,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    @pytest.mark.parametrize("recaptcha_type", recaptcha_v2_types)
    async def test_aio_context(self, mocker, recaptcha_type):
        context_enter_spy = mocker.spy(AIOContextManager, "__aenter__")
        context_exit_spy = mocker.spy(AIOContextManager, "__aexit__")
        async with ReCaptchaV2(
            api_key=self.API_KEY,
            websiteKey=self.websiteKey,
            websiteURL=self.websiteURL,
            captcha_type=recaptcha_type,
        ) as instance:
            assert context_enter_spy.call_count == 1
        assert context_exit_spy.call_count == 1

    @pytest.mark.parametrize("recaptcha_type", recaptcha_v2_types)
    def test_err_context(self, recaptcha_type):
        with pytest.raises(ValueError):
            with ReCaptchaV2(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                captcha_type=recaptcha_type,
            ) as instance:
                raise ValueError("Test error")

    @pytest.mark.parametrize("recaptcha_type", recaptcha_v2_types)
    async def test_err_aio_context(self, recaptcha_type):
        with pytest.raises(ValueError):
            async with ReCaptchaV2(
                api_key=self.API_KEY,
                websiteKey=self.websiteKey,
                websiteURL=self.websiteURL,
                captcha_type=recaptcha_type,
            ) as instance:
                raise ValueError("Test error")
