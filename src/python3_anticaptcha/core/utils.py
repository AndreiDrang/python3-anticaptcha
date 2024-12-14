from typing import Generator


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
