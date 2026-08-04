"""Tests for ``core.context_instr`` — the sync/async context-manager mixins that
``CaptchaParams`` inherits.

Previous tests only asserted that a ``ValueError`` raised inside the block
propagated — which is trivially true and does not exercise ``__exit__`` at all.
These tests assert the actual contract: the return value of the dunders and
that a clean exit does NOT suppress anything.
"""

import pytest

from python3_anticaptcha.core.context_instr import AIOContextManager, SIOContextManager


class TestSIOContextManager:
    def test_enter_returns_self(self):
        cm = SIOContextManager()
        with cm as bound:
            assert bound is cm

    def test_clean_exit_returns_true(self):
        cm = SIOContextManager()
        # __exit__ called with all-None args on a clean exit
        assert cm.__exit__(None, None, None) is True

    def test_exception_exit_returns_false_so_it_propagates(self):
        cm = SIOContextManager()
        # returning a false value => exception is NOT suppressed
        assert cm.__exit__(ValueError, ValueError("x"), None) is False

    def test_raised_exception_propagates(self):
        cm = SIOContextManager()
        with pytest.raises(ValueError, match="boom"):
            with cm:
                raise ValueError("boom")


class TestAIOContextManager:
    async def test_aenter_returns_self(self):
        cm = AIOContextManager()
        async with cm as bound:
            assert bound is cm

    async def test_clean_aexit_returns_true(self):
        cm = AIOContextManager()
        assert await cm.__aexit__(None, None, None) is True

    async def test_exception_aexit_returns_false(self):
        cm = AIOContextManager()
        assert await cm.__aexit__(ValueError, ValueError("x"), None) is False

    async def test_raised_exception_propagates(self):
        cm = AIOContextManager()
        with pytest.raises(ValueError, match="boom"):
            async with cm:
                raise ValueError("boom")
