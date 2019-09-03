import os
import random
import inspect
import asyncio

import pytest
import requests

from python3_anticaptcha import (
    NoCaptchaTaskProxyless,
    AntiCaptchaControl,
    CustomCaptchaTask,
    ReCaptchaV3TaskProxyless,
)

# 1. `export anticaptcha_key=274832f8168a36019895a1e1174777c0`


class TestAntiCaptcha(object):
    WRONG_QUEUE_ID = WRONG_TASK_ID = -1

    def setup_class(self):
        self.anticaptcha_key_fail = os.getenv("anticaptcha_key")[:5]
        self.anticaptcha_key_true = os.getenv("anticaptcha_key")
        self.server_ip = "85.255.8.26"        

    # CallBack
    def test_callback_server(self):
        # test server alive
        response = requests.get(f"http://{self.server_ip}:8001/ping")
        assert response.status_code == 200
        # try register new queue
        response = requests.post(
            f"http://{self.server_ip}:8001/register_key",
            json={"key": "fwefefefopewofkewopfkop", "vhost": "anticaptcha_vhost"},
        )
        assert response.status_code == 200

    def test_customcatpcha_params(self):
        default_init_params = [
            "self",
            "anticaptcha_key",
            "sleep_time",
            "assignment",
            "forms",
            "callbackUrl",
        ]
        default_handler_params = ["self", "imageUrl"]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(
            CustomCaptchaTask.aioCustomCaptchaTask.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            CustomCaptchaTask.aioCustomCaptchaTask.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(
            CustomCaptchaTask.CustomCaptchaTask.__init__
        )
        handler_params = inspect.getfullargspec(
            CustomCaptchaTask.CustomCaptchaTask.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_fail_customcaptcha(self):
        customcaptcha = CustomCaptchaTask.CustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            sleep_time=10,
            assignment="Smth interesting",
        )
        # check response type
        assert type(customcaptcha) is CustomCaptchaTask.CustomCaptchaTask

        response = customcaptcha.captcha_handler(
            imageUrl=self.server_ip + "/static/image/common_image_example/088636.png"
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    @asyncio.coroutine
    def test_fail_aiocustomcaptcha(self):
        customcaptcha = CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=self.anticaptcha_key_fail,
            sleep_time=10,
            assignment="Smth interesting",
        )
        # check response type
        assert type(customcaptcha) is CustomCaptchaTask.aioCustomCaptchaTask

        response = yield customcaptcha.captcha_handler(
            imageUrl=self.server_ip + "/static/image/common_image_example/088636.png"
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    def test_nocaptcha_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time", "callbackUrl"]
        default_handler_params = ["self", "websiteURL", "websiteKey"]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.NoCaptchaTaskProxyless.__init__
        )
        handler_params = inspect.getfullargspec(
            NoCaptchaTaskProxyless.NoCaptchaTaskProxyless.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_fail_nocaptcha_proxyless(self):
        nocaptcha = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

        response = nocaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    def test_fail_nocaptcha_proxyless_context(self):
        with NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as nocaptcha:

            # check response type
            assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

            response = nocaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    @asyncio.coroutine
    def test_fail_aionocaptcha_proxyless(self):
        nocaptcha = NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

        response = yield nocaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    @asyncio.coroutine
    def test_fail_aionocaptcha_proxyless_context(self):
        with NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as nocaptcha:
            # check response type
            assert type(nocaptcha) is NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

            response = yield nocaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    def test_recaptcha_v3_params(self):
        default_init_params = ["self", "anticaptcha_key", "sleep_time", "callbackUrl"]
        default_handler_params = [
            "self",
            "websiteURL",
            "websiteKey",
            "minScore",
            "pageAction",
        ]
        # get customcaptcha init and captcha_handler params
        aioinit_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless.__init__
        )
        aiohandler_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless.captcha_handler
        )

        # get customcaptcha init and captcha_handler params
        init_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless.__init__
        )
        handler_params = inspect.getfullargspec(
            ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless.captcha_handler
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_handler_params == aiohandler_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_handler_params == handler_params[0]

    def test_fail_recaptcha_v3_proxyless(self):
        recaptcha = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(recaptcha) is ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless

        response = recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=0.3,
            pageAction="login_test",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.1,
                pageAction="login_test",
            )

    def test_true_recaptcha_v3_proxyless(self):
        recaptcha = ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # check response type
        assert type(recaptcha) is ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless

        response = recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=0.3,
            pageAction="login_test",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription", "taskId"] == list(response.keys())
        # check error code
        # TODO change to `0`
        assert response["errorId"] == 31

    def test_fail_recaptcha_v3_proxyless_context(self):
        with ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:

            # check response type
            assert type(recaptcha) is ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless

            response = recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.3,
                pageAction="login_test",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with ReCaptchaV3TaskProxyless.ReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            with pytest.raises(ValueError):
                assert recaptcha.captcha_handler(
                    websiteURL="https://www.google.com/recaptcha/api2/demo",
                    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                    minScore=0.1,
                    pageAction="login_test",
                )

    @asyncio.coroutine
    def test_fail_aiorecaptcha_v3_proxyless(self):
        recaptcha = ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(recaptcha) is ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless

        response = yield recaptcha.captcha_handler(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            minScore=0.3,
            pageAction="login_test",
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.1,
                pageAction="login_test",
            )

    @asyncio.coroutine
    def test_fail_aiorecaptcha_v3_proxyless_context(self):
        with ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            # check response type
            assert (
                type(recaptcha) is ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless
            )

            response = yield recaptcha.captcha_handler(
                websiteURL="https://www.google.com/recaptcha/api2/demo",
                websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                minScore=0.3,
                pageAction="login_test",
            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with ReCaptchaV3TaskProxyless.aioReCaptchaV3TaskProxyless(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as recaptcha:
            with pytest.raises(ValueError):
                assert recaptcha.captcha_handler(
                    websiteURL="https://www.google.com/recaptcha/api2/demo",
                    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
                    minScore=0.1,
                    pageAction="login_test",
                )

    """
    Control
    """

    def test_control_type(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # check response type
        assert type(result) is AntiCaptchaControl.AntiCaptchaControl

    def test_control_params(self):
        default_init_params = ["self", "anticaptcha_key"]
        default_balance_params = ["self"]
        default_complaint_params = ["self", "reported_id", "captcha_type"]
        default_queue_status_params = ["self", "queue_id"]
        # get customcaptcha init and other params
        aioinit_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.__init__
        )
        aiobalance_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_balance
        )
        aiocomplaint_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.complaint_on_result
        )
        aioqueue_status_params = inspect.getfullargspec(
            AntiCaptchaControl.aioAntiCaptchaControl.get_queue_status
        )

        # get customcaptcha init and other params
        init_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.__init__
        )
        balance_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_balance
        )
        complaint_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.complaint_on_result
        )
        queue_status_params = inspect.getfullargspec(
            AntiCaptchaControl.AntiCaptchaControl.get_queue_status
        )
        # check aio module params
        assert default_init_params == aioinit_params[0]
        assert default_balance_params == aiobalance_params[0]
        assert default_complaint_params == aiocomplaint_params[0]
        assert default_queue_status_params == aioqueue_status_params[0]
        # check sync module params
        assert default_init_params == init_params[0]
        assert default_balance_params == balance_params[0]
        assert default_complaint_params == complaint_params[0]
        assert default_queue_status_params == queue_status_params[0]

    # AntiCaptcha Control
    def test_fail_queue_status(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        q_id = self.WRONG_QUEUE_ID

        with pytest.raises(ValueError):
            # get queue status
            assert result.get_queue_status(queue_id=q_id)
        
    # AntiCaptcha Control
    def test_true_queue_status(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        q_id = random.choice(AntiCaptchaControl.queue_ids)
        for q_id in AntiCaptchaControl.queue_ids:
            # get queue status
            response = result.get_queue_status(queue_id=q_id)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ['waiting', 'load', 'bid', 'speed', 'total'] == list(response.keys())

    # AntiCaptcha Control
    def test_fail_balance(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # get balance
        response = result.get_balance()
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

    # AntiCaptcha Control
    def test_fail_app_stats(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # get balance
        response = result.get_app_stats(softId=867)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert result.get_app_stats(softId=867, mode="filure")

    # AntiCaptcha Control
    def test_fail_complaint_on_result(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # complaint on result
        response = result.complaint_on_result(reported_id=self.WRONG_TASK_ID)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert result.complaint_on_result(
                reported_id=self.WRONG_TASK_ID, captcha_type="not_image"
            )

    # AntiCaptcha Control
    def test_true_balance(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # get balance
        response = result.get_balance()
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "balance"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

    # AntiCaptcha Control
    def test_true_complaint_on_result(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # complaint on result
        response = result.complaint_on_result(reported_id=self.WRONG_TASK_ID, captcha_type="image")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 16

        # complaint on result
        response = result.complaint_on_result(reported_id=self.WRONG_TASK_ID, captcha_type="recaptcha")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 16

    def test_fail_control_context(self):
        # prepare client
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as result:
            # get balance
            response = result.get_balance()
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

            # complaint on result
            response = result.complaint_on_result(reported_id=self.WRONG_TASK_ID)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
            # check error code
            assert response["errorId"] == 1

    # AntiCaptcha Control
    def test_true_app_stats(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # get balance
        response = result.get_app_stats(softId=867)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = result.get_app_stats(softId=867, mode="errors")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = result.get_app_stats(softId=867, mode="views")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = result.get_app_stats(softId=867, mode="downloads")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = result.get_app_stats(softId=867, mode="users")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = result.get_app_stats(softId=867, mode="money")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

    def test_true_control_context(self):
        # prepare client
        with AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        ) as result:
            # get balance
            response = result.get_balance()
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "balance"] == list(response.keys())
            # check error code
            assert response["errorId"] == 0

            # complaint on result
            response = result.complaint_on_result(reported_id=self.WRONG_TASK_ID)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
            # check error code
            assert response["errorId"] == 16

    # AntiCaptcha Control
    @asyncio.coroutine
    def test_fail_aioqueue_status(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        q_id = self.WRONG_QUEUE_ID

        with pytest.raises(ValueError):
            # get queue status
            assert result.get_queue_status(queue_id=q_id)
        
    # AntiCaptcha Control
    @asyncio.coroutine
    def test_true_aioqueue_status(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        q_id = random.choice(AntiCaptchaControl.queue_ids)
        for q_id in AntiCaptchaControl.queue_ids:
            # get queue status
            response = yield result.get_queue_status(queue_id=q_id)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ['waiting', 'load', 'bid', 'speed', 'total'] == list(response.keys())

    @asyncio.coroutine
    def test_fail_aiobalance(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # get balance
        response = yield result.get_balance()
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

    @asyncio.coroutine
    def test_fail_aiocomplaint_on_result(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # complaint on result
        response = yield result.complaint_on_result(reported_id=self.WRONG_TASK_ID)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert result.complaint_on_result(
                reported_id=self.WRONG_TASK_ID, captcha_type="not_image"
            )

    @asyncio.coroutine
    def test_fail_aioapp_stats(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        )
        # complaint on result
        response = yield result.get_app_stats(softId=867)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 1

        with pytest.raises(ValueError):
            assert result.get_app_stats(softId=867, mode="filure")

    @asyncio.coroutine
    def test_true_aioapp_stats(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # complaint on result
        response = yield result.get_app_stats(softId=867)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = yield result.get_app_stats(softId=867, mode="errors")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = yield result.get_app_stats(softId=867, mode="views")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = yield result.get_app_stats(softId=867, mode="downloads")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = yield result.get_app_stats(softId=867, mode="users")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

        # get balance
        response = yield result.get_app_stats(softId=867, mode="money")
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "chartData", "fromDate", "toDate"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

    @asyncio.coroutine
    def test_true_aiobalance(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # get balance
        response = yield result.get_balance()
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "balance"] == list(response.keys())
        # check error code
        assert response["errorId"] == 0

    @asyncio.coroutine
    def test_true_aiocontrol(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        )
        # complaint on result
        response = yield result.complaint_on_result(
            reported_id=self.WRONG_TASK_ID, captcha_type="image"
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 16
        # complaint on result
        response = yield result.complaint_on_result(
            reported_id=self.WRONG_TASK_ID, captcha_type="recaptcha"
        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
        # check error code
        assert response["errorId"] == 16

    @asyncio.coroutine
    def test_fail_aiocontrol_context(self):
        # prepare client
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_fail
        ) as result:
            # get balance
            response = yield result.get_balance()
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())

            # complaint on result
            response = yield result.complaint_on_result(reported_id=self.WRONG_TASK_ID)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
            # check error code
            assert response["errorId"] == 1

    @asyncio.coroutine
    def test_true_aiocontrol_context(self):
        # prepare client
        with AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=self.anticaptcha_key_true
        ) as result:
            # get balance
            response = yield result.get_balance()
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "balance"] == list(response.keys())
            # check error code
            assert response["errorId"] == 0

            # complaint on result
            response = yield result.complaint_on_result(reported_id=self.WRONG_TASK_ID)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ["errorId", "errorCode", "errorDescription"] == list(response.keys())
            # check error code
            assert response["errorId"] == 16
