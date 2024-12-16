from tests.conftest import BaseTest
from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm
from python3_anticaptcha.custom_task import CustomTask
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer


class TestCustomTask(BaseTest):
    websiteURL = "https://anti-captcha.com/tutorials/v2-textarea"
    templateName = "Anti-bot screen bypass"
    variables = {"css_selector": "some value"}

    def get_proxy_args(self) -> dict:
        proxy_args = super().get_proxy_args()
        proxy_args.update({"proxyType": ProxyTypeEnm.https})
        return proxy_args

    def test_sio_success(self):
        instance = CustomTask(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            templateName=self.templateName,
            variables=self.variables,
            captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless,
            **self.get_proxy_args(),
        )
        result = instance.captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId in (24,)

    async def test_aio_success(self):
        instance = CustomTask(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            templateName=self.templateName,
            variables=self.variables,
            captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless,
            **self.get_proxy_args(),
        )
        result = await instance.aio_captcha_handler()

        assert isinstance(result, dict)
        ser_result = GetTaskResultResponseSer(**result)
        assert ser_result.errorId in (24,)

    def test_proxy_args(self):
        proxy_args = self.get_proxy_args()

        instance = CustomTask(
            api_key=self.API_KEY,
            websiteURL=self.websiteURL,
            templateName=self.templateName,
            variables=self.variables,
            captcha_type=CaptchaTypeEnm.GeeTestTaskProxyless,
            **proxy_args,
        )
        for key, value in proxy_args.items():
            assert instance.task_params[key] == value
