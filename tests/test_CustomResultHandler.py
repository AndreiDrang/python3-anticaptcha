import inspect

import pytest

from python3_anticaptcha import CustomResultHandler

from tests.main import MainAntiCaptcha


class TestAntiCaptcha(MainAntiCaptcha):
    """
    Params check
    """

    def test_result_handler_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time"]
        default_handler_params = ["self", "task_id"]
        # get customcaptcha init and task_handler params
        aioinit_params = inspect.getfullargspec(
            CustomResultHandler.aioCustomResultHandler.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            CustomResultHandler.aioCustomResultHandler.task_handler
        )

        # get customcaptcha init and task_handler params
        init_params = inspect.getfullargspec(CustomResultHandler.CustomResultHandler.__init__)
        handler_params = inspect.getfullargspec(
            CustomResultHandler.CustomResultHandler.task_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    """
    Response checking
    """

    def test_response_result_handler(self):
        # prepare client
        custom_result = CustomResultHandler.CustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # check response type
        assert isinstance(custom_result, CustomResultHandler.CustomResultHandler)

        response = custom_result.task_handler(task_id=self.WRONG_TASK_ID)
        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription", "taskId"] == list(response.keys())

    @pytest.mark.asyncio
    async def test_response_aioresult_handler(self):
        # prepare client
        custom_result = CustomResultHandler.aioCustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # check response type
        assert isinstance(custom_result, CustomResultHandler.aioCustomResultHandler)

        response = await custom_result.task_handler(task_id=self.WRONG_TASK_ID)
        # check response type
        assert isinstance(response, dict)
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription", "taskId"] == list(response.keys())

    """
    Fail tests
    """

    def test_fail_result_handler(self):
        # prepare client
        custom_result = CustomResultHandler.CustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = custom_result.task_handler(task_id=self.WRONG_TASK_ID)
        # check error code
        assert 1 == response["errorId"]

    def test_fail_result_handler_context(self):
        # prepare client
        with CustomResultHandler.CustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as custom_result:

            response = custom_result.task_handler(task_id=self.WRONG_TASK_ID)
            # check error code
            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioresult_handler(self):
        # prepare client
        custom_result = CustomResultHandler.aioCustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = await custom_result.task_handler(task_id=self.WRONG_TASK_ID)
        # check error code
        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioresult_handler_context(self):
        # prepare client
        with CustomResultHandler.aioCustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as custom_result:

            response = await custom_result.task_handler(task_id=self.WRONG_TASK_ID)
            # check error code
            assert 1 == response["errorId"]

    """
    True tests
    """

    def test_true_result_handler(self):
        # prepare client
        custom_result = CustomResultHandler.CustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = custom_result.task_handler(task_id=self.WRONG_TASK_ID)
        # check error code
        assert 16 == response["errorId"]

    def test_true_result_handler_context(self):
        # prepare client
        with CustomResultHandler.CustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_true
        ) as custom_result:

            response = custom_result.task_handler(task_id=self.WRONG_TASK_ID)
            # check error code
            assert 16 == response["errorId"]

    @pytest.mark.asyncio
    async def test_true_aioresult_handler(self):
        # prepare client
        custom_result = CustomResultHandler.aioCustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = await custom_result.task_handler(task_id=self.WRONG_TASK_ID)
        # check error code
        assert 16 == response["errorId"]

    @pytest.mark.asyncio
    async def test_true_aioresult_handler_context(self):
        # prepare client
        with CustomResultHandler.aioCustomResultHandler(
            anticaptcha_key=self.anticaptcha_key_true
        ) as custom_result:

            response = await custom_result.task_handler(task_id=self.WRONG_TASK_ID)
            # check error code
            assert 16 == response["errorId"]
