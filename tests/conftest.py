import os
import time
import random
import string

import pytest

from python3_anticaptcha.core.enum import ProxyTypeEnm


@pytest.fixture(scope="function")
def delay_func():
    time.sleep(1)


@pytest.fixture(scope="class")
def delay_class():
    time.sleep(2)


@pytest.mark.usefixtures("delay_func")
@pytest.mark.usefixtures("delay_class")
class BaseTest:
    API_KEY = os.getenv("API_KEY", "ad9053f3182ca81755768608fa75")
    sleep_time = 5

    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    def get_proxy_args(self) -> dict:
        return {
            "proxyType": ProxyTypeEnm.http,
            "proxyAddress": "0.0.0.0",
            "proxyPort": 445,
            "proxyLogin": self.get_random_string(),
            "proxyPassword": self.get_random_string(),
        }

    @staticmethod
    def get_random_string(length: int = 10) -> str:
        """
        Method generate random string with set length

        Args:
            length: Len of generated string

        Returns:
            Random letter string
        """
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for _ in range(length))
        return result_str

    def read_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as file:
            return file.read()
