import os
import time
import random
import string

import pytest


@pytest.fixture(scope="function")
def delay():
    time.sleep(1)


@pytest.mark.usefixtures("delay")
class BaseTest:
    API_KEY = os.getenv("API_KEY", "ad9053f3182ca81755768608fa75")
    sleep_time = 5

    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    @staticmethod
    def get_random_string(length: int) -> str:
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
