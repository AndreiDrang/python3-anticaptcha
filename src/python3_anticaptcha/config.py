from typing import Generator

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Connection retry generator
def attempts_generator(amount: int = 5) -> Generator:
    """
    Function generates a generator of length equal to `amount`

    Args:
        amount: number of attempts generated

    Returns:
        Attempt number
    """
    for i in range(1, amount):
        yield i
