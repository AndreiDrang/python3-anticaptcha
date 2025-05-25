import pytest

from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.amazon_waf import AmazonWAF
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer


class TestAmazonWAF(BaseTest):
    websiteURL = "https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest"
    websiteKey = "AQIDAgghr5y45ywZwdADFLWk7XOA=="
    iv = "CgAAXFFFFSAAABVk"
    _context = "qoJYgnKscdqwdqwdqwaormh/dYYK+Y="

    def get_proxy_args(self) -> dict:
        proxy_args = super().get_proxy_args()
        proxy_args.update({"userAgent": self.get_random_string()})
        return proxy_args

    def test_sio_success(self):
        instance = AmazonWAF(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            iv=self.iv,
            context=self._context,
            captcha_type=CaptchaTypeEnm.AmazonTaskProxyless,
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 24

    async def test_aio_success(self):
        instance = AmazonWAF(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            iv=self.iv,
            context=self._context,
            captcha_type=CaptchaTypeEnm.AmazonTaskProxyless,
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId == 24

    @pytest.mark.parametrize("proxyType", ProxyTypeEnm)
    def test_proxy_args(self, proxyType: ProxyTypeEnm):
        proxy_args = self.get_proxy_args()
        proxy_args.update({"proxyType": proxyType})

        instance = AmazonWAF(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            websiteKey=self.websiteKey,
            iv=self.iv,
            context=self._context,
            captcha_type=CaptchaTypeEnm.AmazonTask,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value

    def test_err_captcha_type(self):
        with pytest.raises(ValueError):
            AmazonWAF(
                api_key=self.API_KEY,
                websiteURL=self.websiteURL,
                websiteKey=self.websiteKey,
                iv=self.iv,
                context=self._context,
                captcha_type=self.get_random_string(length=10),
            )
