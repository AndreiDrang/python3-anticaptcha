from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from tests.conftest import BaseTest
from python3_anticaptcha.core.base import BaseCaptcha
from python3_anticaptcha.core.enum import MyEnum, CaptchaTypeEnm
from python3_anticaptcha.core.config import RETRIES, ASYNC_RETRIES, BASE_REQUEST_URL, attempts_generator


class TestCore(BaseTest):
    """
    Success tests
    """

    def test_reties(self):
        assert isinstance(RETRIES, Retry)

    def test_async_reties(self):
        assert isinstance(ASYNC_RETRIES, AsyncRetrying)

    def test_create_base(self):
        BaseCaptcha(
            api_key=self.get_random_string(32),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=BASE_REQUEST_URL,
            sleep_time=self.sleep_time,
        )

    def test_aio_create_base(self):
        BaseCaptcha(
            api_key=self.get_random_string(32),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=BASE_REQUEST_URL,
            sleep_time=self.sleep_time,
        )

    def test_create_base_context(self):
        with BaseCaptcha(
            api_key=self.get_random_string(32),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=BASE_REQUEST_URL,
            sleep_time=self.sleep_time,
        ) as instance:
            pass

    async def test_aio_create_base_context(self):
        async with BaseCaptcha(
            api_key=self.get_random_string(32),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=BASE_REQUEST_URL,
            sleep_time=self.sleep_time,
        ) as instance:
            pass


class TestConfig(BaseTest):
    def test_attempts_generator(self):
        attempt = None
        attempts = attempts_generator(amount=5)
        for attempt in attempts:
            assert isinstance(attempt, int)
        assert attempt == 4


class TestEnum(BaseTest):
    def test_enum_list(self):
        assert isinstance(MyEnum.list(), list)

    def test_enum_list_values(self):
        assert isinstance(MyEnum.list_values(), list)

    def test_enum_list_names(self):
        assert isinstance(MyEnum.list_names(), list)
