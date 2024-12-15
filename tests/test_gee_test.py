import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.gee_test import GeeTest
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer


class GeeTestBase(BaseTest):
    websiteURL = "https://www.geetest.com/en/adaptive-captcha-demo"
    gt = "81388ea1fc187e0c335c0a8907ff2625"
    challenge = "12345678abc90123d45678ef90123a456b"
    version = 0

    def get_proxy_args(self) -> dict:
        proxy_args = super().get_proxy_args()
        proxy_args.update({"userAgent": self.get_random_string()})
        return proxy_args

    def test_sio_success(self):
        instance = GeeTest(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            gt=self.gt,
            challenge=self.challenge,
            version=self.version,
            captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId in (34, 12)

    async def test_aio_success(self):
        instance = GeeTest(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            gt=self.gt,
            challenge=self.challenge,
            version=self.version,
            captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId in (34, 12)

    @pytest.mark.parametrize("proxyType", ProxyTypeEnm)
    def test_proxy_args(self, proxyType: ProxyTypeEnm):
        proxy_args = self.get_proxy_args()
        proxy_args.update({"proxyType": proxyType})

        instance = GeeTest(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            gt=self.gt,
            challenge=self.challenge,
            version=self.version,
            captcha_type=CaptchaTypeEnm.GeeTestTask,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value

    def test_err_captcha_type(self):
        with pytest.raises(ValueError):
            GeeTest(
                api_key=self.API_KEY,
                websiteURL=self.websiteURL,
                gt=self.gt,
                challenge=self.challenge,
                version=self.version,
                captcha_type=self.get_random_string(length=10),
            )


class TestGeeTestV3(GeeTestBase):
    version = 3


class TestGeeTestV4(GeeTestBase):
    version = 4
