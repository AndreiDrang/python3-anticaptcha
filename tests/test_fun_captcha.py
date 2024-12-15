import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.fun_captcha import FunCaptcha
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer


class TestFunCaptcha(BaseTest):
    websiteURL = "https://demo.arkoselabs.com/?key=DF9C4D87-CB7B-4062-9FEB-BADB6ADA61E6"
    websitePublicKey = "DF9C4D87-CB7B-4062-9FEB-BADB6ADA61E6"

    def get_proxy_args(self) -> dict:
        proxy_args = super().get_proxy_args()
        proxy_args.update({"userAgent": self.get_random_string()})
        return proxy_args

    def test_sio_success(self):
        instance = FunCaptcha(
            api_key=self.API_KEY,
            websitePublicKey=self.websitePublicKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.FunCaptchaTaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 24
        assert "This domain name is banned from solving" in ser_result.errorDescription

    async def test_aio_success(self):
        instance = FunCaptcha(
            api_key=self.API_KEY,
            websitePublicKey=self.websitePublicKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.FunCaptchaTaskProxyless,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 24
        assert "This domain name is banned from solving" in ser_result.errorDescription

    @pytest.mark.parametrize("proxyType", ProxyTypeEnm)
    def test_proxy_args(self, proxyType: ProxyTypeEnm):
        proxy_args = self.get_proxy_args()
        proxy_args.update({"proxyType": proxyType})

        instance = FunCaptcha(
            api_key=self.API_KEY,
            websitePublicKey=self.websitePublicKey,
            websiteURL=self.websiteURL,
            captcha_type=CaptchaTypeEnm.FunCaptchaTask,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value

    def test_err_captcha_type(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                api_key=self.API_KEY,
                websitePublicKey=self.websitePublicKey,
                websiteURL=self.websiteURL,
                captcha_type=self.get_random_string(length=10),
            )
