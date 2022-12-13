import pytest
from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from src.tests.conftest import BaseTest
from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import CaptchaTypeEnm
from python3_captchaai.core.config import RETRIES, REQUEST_URL, ASYNC_RETRIES, attempts_generator


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
            api_key=self.get_random_string(36),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=REQUEST_URL,
            sleep_time=self.sleep_time,
        )

    def test_aio_create_base(self):
        BaseCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=REQUEST_URL,
            sleep_time=self.sleep_time,
        )

    def test_create_base_context(self):
        with BaseCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=REQUEST_URL,
            sleep_time=self.sleep_time,
        ) as instance:
            pass

    async def test_aio_create_base_context(self):
        async with BaseCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=CaptchaTypeEnm.Control,
            request_url=REQUEST_URL,
            sleep_time=self.sleep_time,
        ) as instance:
            pass

    """
    Failed
    """

    def test_no_key_err(self):
        with pytest.raises(TypeError):
            BaseCaptcha(captcha_type=CaptchaTypeEnm.Control, request_url=REQUEST_URL, sleep_time=self.sleep_time)

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            BaseCaptcha(api_key=self.get_random_string(36), request_url=REQUEST_URL, sleep_time=self.sleep_time)

    def test_no_request_url(self):
        with pytest.raises(TypeError):
            BaseCaptcha(
                api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.Control, sleep_time=self.sleep_time
            )

    def test_no_sleep_time(self):
        with pytest.raises(TypeError):
            BaseCaptcha(
                api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.Control, request_url=REQUEST_URL
            )

    def test_no_key_err_context(self):
        with pytest.raises(TypeError):
            with BaseCaptcha(
                captcha_type=CaptchaTypeEnm.Control, request_url=REQUEST_URL, sleep_time=self.sleep_time
            ) as instance:
                pass

    def test_no_captcha_type_context(self):
        with pytest.raises(TypeError):
            with BaseCaptcha(
                api_key=self.get_random_string(36), request_url=REQUEST_URL, sleep_time=self.sleep_time
            ) as instance:
                pass

    def test_no_request_url_context(self):
        with pytest.raises(TypeError):
            with BaseCaptcha(
                api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.Control, sleep_time=self.sleep_time
            ) as instance:
                pass

    def test_no_sleep_time_context(self):
        with pytest.raises(TypeError):
            with BaseCaptcha(
                api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.Control, request_url=REQUEST_URL
            ) as instance:
                pass

    async def test_aio_no_key_err_context(self):
        with pytest.raises(TypeError):
            async with BaseCaptcha(
                captcha_type=CaptchaTypeEnm.Control, request_url=REQUEST_URL, sleep_time=self.sleep_time
            ) as instance:
                pass

    async def test_aio_no_captcha_type_context(self):
        with pytest.raises(TypeError):
            async with BaseCaptcha(
                api_key=self.get_random_string(36), request_url=REQUEST_URL, sleep_time=self.sleep_time
            ) as instance:
                pass

    async def test_aio_no_request_url_context(self):
        with pytest.raises(TypeError):
            async with BaseCaptcha(
                api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.Control, sleep_time=self.sleep_time
            ) as instance:
                pass

    async def test_aio_no_sleep_time_context(self):
        with pytest.raises(TypeError):
            async with BaseCaptcha(
                api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.Control, request_url=REQUEST_URL
            ) as instance:
                pass

    def test_create_base_err_context(self):
        with pytest.raises(Exception):
            with BaseCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                request_url=REQUEST_URL,
                sleep_time=self.sleep_time,
            ) as instance:
                raise Exception()

    async def test_aio_create_base_err_context(self):
        with pytest.raises(Exception):
            async with BaseCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                request_url=REQUEST_URL,
                sleep_time=self.sleep_time,
            ) as instance:
                raise Exception()

    @pytest.mark.parametrize("api_len", [35, 37])
    def test_wrong_key_err(self, api_len: int):
        with pytest.raises(ValueError):
            BaseCaptcha(
                api_key=self.get_random_string(api_len),
                captcha_type=CaptchaTypeEnm.Control,
                request_url=REQUEST_URL,
                sleep_time=self.sleep_time,
            )

    @pytest.mark.parametrize("sleep_time", range(-2, 5))
    def test_wrong_sleep_time(self, sleep_time: int):
        with pytest.raises(ValueError):
            BaseCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                request_url=REQUEST_URL,
                sleep_time=sleep_time,
            )

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            BaseCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.get_random_string(10),
                request_url=REQUEST_URL,
                sleep_time=self.sleep_time,
            )


class TestEnum(BaseTest):
    def test_enum_list(self):
        assert isinstance(CaptchaTypeEnm.list(), list)

    def test_enum_list_values(self):
        assert isinstance(CaptchaTypeEnm.list_values(), list)

    def test_enum_list_names(self):
        assert isinstance(CaptchaTypeEnm.list_names(), list)

    def test_enum_name(self):
        assert isinstance(CaptchaTypeEnm.Control.name, str)
        assert CaptchaTypeEnm.Control.name == "Control"

    def test_enum_value(self):
        assert isinstance(CaptchaTypeEnm.Control.value, str)
        assert CaptchaTypeEnm.Control.value == "Control"


class TestConfig(BaseTest):
    def test_attempts_generator(self):
        attempt = None
        attempts = attempts_generator(amount=5)
        for attempt in attempts:
            assert isinstance(attempt, int)
        assert attempt == 4
