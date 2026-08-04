"""Tests for ``core.const`` — connection/global constants that every instrument
depends on. Pinning them guards against silent behavior changes.
"""

from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from python3_anticaptcha.core import const


def test_base_request_url():
    assert const.BASE_REQUEST_URL == "https://api.anti-captcha.com/"


def test_endpoint_postfixes():
    assert const.CREATE_TASK_POSTFIX == "/createTask"
    assert const.GET_RESULT_POSTFIX == "/getTaskResult"


def test_app_key():
    # softId is the Literal default of CreateTaskBaseSer; changing it would
    # alter the affiliate/softId attribution of every request.
    assert const.APP_KEY == "867"


def test_sync_retries_config():
    assert isinstance(const.RETRIES, Retry)
    assert const.RETRIES.total == 5
    assert const.RETRIES.backoff_factor == 0.9
    # transient server errors are retried
    assert set(const.RETRIES.status_forcelist) == {500, 502, 503, 504}


def test_async_retries_config():
    assert isinstance(const.ASYNC_RETRIES, AsyncRetrying)
    # reraise=True means the last error surfaces instead of RetryError
    assert const.ASYNC_RETRIES.reraise is True
