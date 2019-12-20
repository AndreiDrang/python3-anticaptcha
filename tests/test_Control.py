import inspect
import random

import pytest
import requests_mock

from python3_anticaptcha import AntiCaptchaControl, config

from tests.main import MainAntiCaptcha


class TestControl(MainAntiCaptcha):
    WRONG_MODE = WRONG_CAPTCHA_TYPE = "qwerty"
    WRONG_SOFT_ID = "-1" + config.app_key
    REPORT_ID = WRONG_QUEUE_ID = -1
    QUEUE_STATUS_KEYS = ("waiting", "load", "bid", "speed", "total")
    """
    Params check
    """

    def test_params(self):
        default_init_params = ["self", "anticaptcha_key"]
        default_get_balance_params = ["self"]
        default_app_stats_params = ["self", "softId", "mode"]
        default_complaint_params = ["self", "reported_id", "captcha_type"]
        default_queue_status_params = ["queue_id"]
        # get aiocaptchacontrol init and other params
        aio_init_params = inspect.getfullargspec(AntiCaptchaControl.aioAntiCaptchaControl.__init__)
        aio_balance_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_balance
        )
        aio_app_stats_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_app_stats
        )
        aio_complaint_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.complaint_on_result
        )
        aio_queue_status_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_queue_status
        )

        # get captchacontrol init and other params
        init_params = inspect.getfullargspec(AntiCaptchaControl.AntiCaptchaControl.__init__)
        balance_params = inspect.getfullargspec(AntiCaptchaControl.AntiCaptchaControl.get_balance)
        app_stats_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_app_stats
        )
        complaint_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.complaint_on_result
        )
        queue_status_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_queue_status
        )
        # check aio module params
        assert default_init_params == aio_init_params[0]
        assert default_get_balance_params == aio_balance_params[0]
        assert default_app_stats_params == aio_app_stats_params[0]
        assert default_complaint_params == aio_complaint_params[0]
        assert default_queue_status_params == aio_queue_status_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_get_balance_params == balance_params[0]
        assert default_app_stats_params == app_stats_params[0]
        assert default_complaint_params == complaint_params[0]
        assert default_queue_status_params == queue_status_params[0]

    def test_balance_payload(self):
        control = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key=self.anticaptcha_key_true)
        # check response type
        assert isinstance(control, AntiCaptchaControl.AntiCaptchaControl)

        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.get_balance_url, json=self.ERROR_RESPONSE_JSON)
            control.get_balance()

        history = req_mock.request_history

        assert len(history) == 1

        request_payload = history[0].json()

        # check all dict keys
        assert ["clientKey",] == list(request_payload.keys())
        assert request_payload["clientKey"] == self.anticaptcha_key_true

    def test_stats_payload(self):
        control = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key=self.anticaptcha_key_true)
        # check response type
        assert isinstance(control, AntiCaptchaControl.AntiCaptchaControl)
        mode = random.choice(AntiCaptchaControl.mods)

        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.get_app_stats_url, json=self.ERROR_RESPONSE_JSON)
            control.get_app_stats(softId=config.app_key, mode=mode)

        history = req_mock.request_history

        assert len(history) == 1

        request_payload = history[0].json()

        # check all dict keys
        assert ["clientKey", "softId", "mode"] == list(request_payload.keys())
        assert request_payload["clientKey"] == self.anticaptcha_key_true
        assert request_payload["softId"] == config.app_key
        assert request_payload["mode"] == mode

    def test_complaint_image_payload(self):
        control = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key=self.anticaptcha_key_true)
        # check response type
        assert isinstance(control, AntiCaptchaControl.AntiCaptchaControl)
        task_id = 123456

        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.incorrect_imagecaptcha_url, json=self.ERROR_RESPONSE_JSON)
            control.complaint_on_result(reported_id = task_id, captcha_type = AntiCaptchaControl.complaint_types[0])

        history = req_mock.request_history

        assert len(history) == 1

        request_payload = history[0].json()

        # check all dict keys
        assert ["clientKey", "taskId"] == list(request_payload.keys())
        assert request_payload["clientKey"] == self.anticaptcha_key_true
        assert request_payload["taskId"] == task_id

    def test_complaint_re_payload(self):
        control = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key=self.anticaptcha_key_true)
        # check response type
        assert isinstance(control, AntiCaptchaControl.AntiCaptchaControl)
        task_id = 123456
        print(config.incorrect_recaptcha_url)
        print(AntiCaptchaControl.complaint_types[1])
        with requests_mock.Mocker() as req_mock:
            req_mock.post(config.incorrect_recaptcha_url, json=self.ERROR_RESPONSE_JSON)
            control.complaint_on_result(reported_id = task_id, captcha_type = AntiCaptchaControl.complaint_types[1])

        history = req_mock.request_history

        assert len(history) == 1

        request_payload = history[0].json()

        # check all dict keys
        assert ["clientKey", "taskId"] == list(request_payload.keys())
        assert request_payload["clientKey"] == self.anticaptcha_key_true
        assert request_payload["taskId"] == task_id

    """
    Response checking
    """

    def test_response_control(self):
        control_captcha = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(control_captcha, AntiCaptchaControl.AntiCaptchaControl)

    @pytest.mark.asyncio
    async def test_response_aiocontrol(self):
        control_captcha = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert isinstance(control_captcha, AntiCaptchaControl.aioAntiCaptchaControl)

    """
    Fail tests
    """

    def test_fail_balance(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = captcha_control.get_balance()

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_balance_context(self):
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    def test_fail_key_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_app_stats_context(self):
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = captcha_control.get_app_stats(softId=config.app_key)

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    def test_fail_id_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_mode_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        with pytest.raises(ValueError):
            assert captcha_control.get_app_stats(softId=config.app_key, mode=self.WRONG_MODE)

    def test_fail_key_complaint(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = captcha_control.complaint_on_result(
            reported_id=self.REPORT_ID, captcha_type=AntiCaptchaControl.complaint_types[0]
        )

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    def test_fail_id_complaint(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = captcha_control.complaint_on_result(
            reported_id=self.REPORT_ID, captcha_type=AntiCaptchaControl.complaint_types[0]
        )

        assert isinstance(response, dict)

        assert 16 == response["errorId"]

    def test_fail_type_complaint(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        with pytest.raises(ValueError):
            assert captcha_control.complaint_on_result(
                reported_id=self.REPORT_ID, captcha_type=self.WRONG_CAPTCHA_TYPE
            )

    def test_fail_id_queue_status(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl

        with pytest.raises(ValueError):
            assert captcha_control.get_queue_status(queue_id=self.WRONG_QUEUE_ID)

    @pytest.mark.asyncio
    async def test_fail_aiobalance(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = await captcha_control.get_balance()

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiobalance_context(self):
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = await captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioapp_stats_context(self):
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = await captcha_control.get_app_stats(softId=config.app_key)

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiokey_app_stats(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = await captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioid_app_stats(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = await captcha_control.get_app_stats(softId=self.WRONG_SOFT_ID)

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiomode_app_stats(self):
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as captcha_control:

            response = await captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiokey_complaint(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        response = await captcha_control.complaint_on_result(
            reported_id=self.REPORT_ID, captcha_type=AntiCaptchaControl.complaint_types[0]
        )

        assert isinstance(response, dict)

        assert 1 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aioid_complaint(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = await captcha_control.complaint_on_result(
            reported_id=self.REPORT_ID, captcha_type=AntiCaptchaControl.complaint_types[0]
        )

        assert isinstance(response, dict)

        assert 16 == response["errorId"]

    @pytest.mark.asyncio
    async def test_fail_aiotype_complaint(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )

        with pytest.raises(ValueError):
            assert await captcha_control.complaint_on_result(
                reported_id=self.REPORT_ID, captcha_type=self.WRONG_CAPTCHA_TYPE
            )

    @pytest.mark.asyncio
    async def test_fail_aioid_queue_status(self):
        captcha_control = AntiCaptchaControl.aioAntiCaptchaControl

        with pytest.raises(ValueError):
            assert await captcha_control.get_queue_status(queue_id=self.WRONG_QUEUE_ID)

    """
    True tests
    """

    def test_true_mode_app_stats(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        for mode in AntiCaptchaControl.mods:
            response = captcha_control.get_app_stats(softId=config.app_key, mode=mode)

            assert isinstance(response, dict)

            assert 0 == response["errorId"]

    def test_true_mode_app_stats_context(self):
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        ) as captcha_control:

            for mode in AntiCaptchaControl.mods:
                response = captcha_control.get_app_stats(softId=config.app_key, mode=mode)

                assert isinstance(response, dict)

                assert 0 == response["errorId"]

    def test_true_balance(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )

        response = captcha_control.get_balance()

        assert isinstance(response, dict)

        assert 0 == response["errorId"]

    def test_true_balance_context(self):
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        ) as captcha_control:

            response = captcha_control.get_balance()

            assert isinstance(response, dict)

            assert 0 == response["errorId"]

    def test_true_queue_status(self):
        captcha_control = AntiCaptchaControl.AntiCaptchaControl
        for queue_id in AntiCaptchaControl.queue_ids:
            response = captcha_control.get_queue_status(queue_id=queue_id)

            assert isinstance(response, dict)

            assert self.QUEUE_STATUS_KEYS == tuple(response.keys())
