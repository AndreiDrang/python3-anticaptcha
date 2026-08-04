"""Tests for ``core.base.CaptchaParams`` — the shared parent of every handler.

``CaptchaParams`` has two responsibilities: (1) hold the request payloads and
``sleep_time``; (2) delegate ``captcha_handler``/``aio_captcha_handler`` to a
sync/async instrument, merging in extra params. Delegation is the contract
here, so spying on the instrument is legitimate (unlike in the instrument tests,
where the instrument itself is the unit under test).
"""

from python3_anticaptcha.core.base import CaptchaParams
from python3_anticaptcha.core.serializer import CreateTaskBaseSer, GetTaskResultRequestSer


class TestConstruction:
    def test_sets_clientkey_on_both_payloads(self):
        inst = CaptchaParams(api_key="MY_KEY")
        assert inst.create_task_payload.clientKey == "MY_KEY"
        assert inst.get_result_params.clientKey == "MY_KEY"

    def test_default_sleep_time_is_15(self):
        # base default differs from the per-type default (10) — pin it
        assert CaptchaParams(api_key="k").sleep_time == 15

    def test_explicit_sleep_time(self):
        assert CaptchaParams(api_key="k", sleep_time=3).sleep_time == 3

    def test_starts_with_empty_task_params(self):
        assert CaptchaParams(api_key="k").task_params == {}

    def test_create_task_payload_shape(self):
        inst = CaptchaParams(api_key="k")
        assert isinstance(inst.create_task_payload, CreateTaskBaseSer)
        assert inst.create_task_payload.task == {}

    def test_get_result_params_shape(self):
        inst = CaptchaParams(api_key="k")
        assert isinstance(inst.get_result_params, GetTaskResultRequestSer)
        assert inst.get_result_params.taskId is None


class TestSetCallbackUrl:
    def test_writes_callback_url(self):
        inst = CaptchaParams(api_key="k")
        inst.set_callback_url(callbackUrl="https://example.com/cb")
        assert inst.create_task_payload.callbackUrl == "https://example.com/cb"

    def test_overwrites_previous_value(self):
        inst = CaptchaParams(api_key="k")
        inst.set_callback_url(callbackUrl="a")
        inst.set_callback_url(callbackUrl="b")
        assert inst.create_task_payload.callbackUrl == "b"


class TestSyncHandlerDelegation:
    def test_merges_additional_params_into_task_params(self, mocker):
        spy = mocker.patch("python3_anticaptcha.core.base.SIOCaptchaInstrument")
        spy.return_value.processing_captcha.return_value = {"errorId": 0}
        inst = CaptchaParams(api_key="k")

        inst.captcha_handler(proxyLogin="user", proxyPassword="pw")

        assert inst.task_params["proxyLogin"] == "user"
        assert inst.task_params["proxyPassword"] == "pw"

    def test_constructs_sio_instrument_with_self(self, mocker):
        spy = mocker.patch("python3_anticaptcha.core.base.SIOCaptchaInstrument")
        spy.return_value.processing_captcha.return_value = {"ok": True}
        inst = CaptchaParams(api_key="k")

        result = inst.captcha_handler()

        spy.assert_called_once_with(captcha_params=inst)
        assert result == {"ok": True}

    def test_returns_processing_captcha_result(self, mocker):
        spy = mocker.patch("python3_anticaptcha.core.base.SIOCaptchaInstrument")
        spy.return_value.processing_captcha.return_value = {"errorId": 0, "taskId": 7}
        inst = CaptchaParams(api_key="k")

        assert inst.captcha_handler() == {"errorId": 0, "taskId": 7}


class TestAsyncHandlerDelegation:
    async def test_merges_additional_params_and_delegates(self, mocker):
        spy = mocker.patch("python3_anticaptcha.core.base.AIOCaptchaInstrument")
        spy.return_value.processing_captcha = mocker.AsyncMock(return_value={"errorId": 0})
        inst = CaptchaParams(api_key="k")

        await inst.aio_captcha_handler(websiteURL="https://x")

        assert inst.task_params["websiteURL"] == "https://x"
        spy.assert_called_once_with(captcha_params=inst)

    async def test_returns_processing_captcha_result(self, mocker):
        spy = mocker.patch("python3_anticaptcha.core.base.AIOCaptchaInstrument")
        spy.return_value.processing_captcha = mocker.AsyncMock(return_value={"errorId": 0, "taskId": 9})
        inst = CaptchaParams(api_key="k")

        result = await inst.aio_captcha_handler()
        assert result == {"errorId": 0, "taskId": 9}


class TestContextManager:
    def test_sync_context_returns_self(self):
        with CaptchaParams(api_key="k") as inst:
            assert isinstance(inst, CaptchaParams)

    async def test_async_context_returns_self(self):
        async with CaptchaParams(api_key="k") as inst:
            assert isinstance(inst, CaptchaParams)
