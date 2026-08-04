"""Tests for ``core.utils.attempts_generator`` — the retry-count source for the
get-result polling loop.

The default ``amount=30`` is the untested invariant noted in the audit (a
duplicate with a different default lives in ``config.py``). The instruments
import the ``core/utils`` copy, so that is the one that matters.
"""

import pytest

from python3_anticaptcha.core.utils import attempts_generator


def test_default_amount_is_30():
    # default yields 1..29 (range(1, 30)), i.e. 29 attempts
    attempts = list(attempts_generator())
    assert attempts == list(range(1, 30))
    assert attempts[-1] == 29


@pytest.mark.parametrize("amount, expected", [(2, [1]), (3, [1, 2]), (5, [1, 2, 3, 4])])
def test_explicit_amount(amount, expected):
    assert list(attempts_generator(amount=amount)) == expected


def test_amount_one_yields_empty():
    # boundary: range(1, 1) is empty — no polling attempts at all
    assert list(attempts_generator(amount=1)) == []


def test_yields_ints():
    assert all(isinstance(a, int) for a in attempts_generator(amount=5))


def test_is_a_generator_not_a_list():
    gen = attempts_generator(amount=3)
    assert iter(gen) is gen  # generator object
    assert next(gen) == 1
