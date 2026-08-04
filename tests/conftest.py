"""Shared test fixtures and helpers for the python3-anticaptcha test suite.

The previous version of this file added ``delay_func``/``delay_class`` fixtures that
called ``time.sleep`` on every test. They added ~3 seconds of pure latency per test
with zero behavioral value, so they were removed during the test-suite rewrite.

The HTTP boundary itself (``requests`` / ``aiohttp``) is mocked in
``tests/core/conftest.py`` so the default suite never touches the network.
"""

import random
import string

import pytest

from python3_anticaptcha.core.enum import ProxyTypeEnm

# Re-export the transport fixtures for module-level tests. The implementation
# lives in tests/core/conftest.py beside the instrument tests, but pytest only
# discovers child conftest fixtures below that directory by default.
from tests.core.conftest import aio_http, sio_http  # noqa: F401

# An obviously-fake 32-char key. Never a real credential — used only so the
# ``clientKey`` field has a stable, recognizable value in request assertions.
API_KEY = "0" * 32


@pytest.fixture(scope="function")
def api_key() -> str:
    """A deterministic, obviously-fake API key for request-payload assertions."""
    return API_KEY


class BaseTest:
    """Base mixin providing small construction helpers.

    Test classes inherit this for historical compatibility. It intentionally
    contains no network, no sleeps, and no fixtures.
    """

    API_KEY = API_KEY
    sleep_time = 5

    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    def get_proxy_args(self) -> dict:
        """Minimal valid proxy block used by proxy-accepting captcha types."""
        return {
            "proxyType": ProxyTypeEnm.http,
            "proxyAddress": "0.0.0.0",
            "proxyPort": 445,
            "proxyLogin": self.get_random_string(),
            "proxyPassword": self.get_random_string(),
        }

    @staticmethod
    def get_random_string(length: int = 10) -> str:
        """Generate a deterministic-length lowercase random string."""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))

    def read_file(self, file_path: str) -> bytes:
        """Read a fixture file as raw bytes (used for image-captcha tests)."""
        with open(file_path, "rb") as file:
            return file.read()
