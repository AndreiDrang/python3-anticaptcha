from typing import Generator

import urllib3
from tenacity import AsyncRetrying, wait_fixed, stop_after_attempt
from requests.adapters import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RETRIES = Retry(total=5, backoff_factor=0.9, status_forcelist=[500, 502, 503, 504])
ASYNC_RETRIES = AsyncRetrying(wait=wait_fixed(5), stop=stop_after_attempt(5), reraise=True)

BASE_REQUEST_URL = "https://api.anti-captcha.com/"
CREATE_TASK_POSTFIX = "/createTask"
GET_RESULT_POSTFIX = "/getTaskResult"
APP_KEY = "867"


# Connection retry generator
def attempts_generator(amount: int = 30) -> Generator:
    """
    Function generates a generator of length equal to `amount`

    Args:
        amount: number of attempts generated

    Yields:
        int: The next number in the range of 1 to ``amount`` - 1.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in attempts_generator(5)])
        [1, 2, 3, 4]

    Returns:
        Attempt number
    """
    yield from range(1, amount)
