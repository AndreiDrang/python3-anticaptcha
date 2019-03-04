import asyncio

import requests

import python3_anticaptcha
from python3_anticaptcha import NoCaptchaTaskProxyless, AntiCaptchaControl

class TestAntiCaptcha(object):
    def setup_class(self):
        #def __init__(self):
        self.anticaptcha_key = "ae23fffcfaa29b170e3843e3a486ef19"
        self.server_ip = '85.255.8.26'

    # CallBack
    def test_callback_server(self):
        # test server alive
        response = requests.get(f'http://{self.server_ip}:8001/ping')
        assert response.status_code == 200
        # try register new queue
        response = requests.post(f'http://{self.server_ip}:8001/register_key', 
                                 json={'key':'fwefefefopewofkewopfkop', 
                                       'vhost':'anticaptcha_vhost'}
                                )
        assert response.status_code == 200

    def test_nocaptcha_proxyless(self):
        nocaptcha = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = self.anticaptcha_key)
        # check response type
        assert type(nocaptcha) is python3_anticaptcha.NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

        response = nocaptcha.captcha_handler(
                        websiteURL='https://www.google.com/recaptcha/api2/demo',
                        websiteKey='6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
                    )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    def test_nocaptcha_proxyless_context(self):
        with NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = self.anticaptcha_key) as nocaptcha:
               
            # check response type
            assert type(nocaptcha) is python3_anticaptcha.NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

            response = nocaptcha.captcha_handler(
                            websiteURL='https://www.google.com/recaptcha/api2/demo',
                            websiteKey='6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
                        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    @asyncio.coroutine
    def test_aionocaptcha_proxyless(self):
        nocaptcha = NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(anticaptcha_key=self.anticaptcha_key)
        # check response type
        assert type(nocaptcha) is python3_anticaptcha.NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

        response = yield nocaptcha.captcha_handler(
                            websiteURL='https://www.google.com/recaptcha/api2/demo',
                            websiteKey='6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
                        )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    @asyncio.coroutine
    def test_aionocaptcha_proxyless_context(self):
        with NoCaptchaTaskProxyless.aioNoCaptchaTaskProxyless(anticaptcha_key=self.anticaptcha_key) as nocaptcha:
            # check response type
            assert type(nocaptcha) is python3_anticaptcha.NoCaptchaTaskProxyless.NoCaptchaTaskProxyless

            response = yield nocaptcha.captcha_handler(
                                websiteURL='https://www.google.com/recaptcha/api2/demo',
                                websiteKey='6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
                            )
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    # AntiCaptcha Control
    def test_control(self):
        # prepare client
        result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = self.anticaptcha_key)
        # check response type
        assert type(result) is python3_anticaptcha.AntiCaptchaControl.AntiCaptchaControl
        
        # get balance
        response = result.get_balance()
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

        # complaint on result
        response = result.complaint_on_result(reported_id=432423342)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    def test_control_context(self):
        # prepare client
        with AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = self.anticaptcha_key) as result:
            # check response type
            assert type(result) is python3_anticaptcha.AntiCaptchaControl.AntiCaptchaControl
        
            # get balance
            response = result.get_balance()
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

            # complaint on result
            response = result.complaint_on_result(reported_id=432423342)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    @asyncio.coroutine
    def test_aiocontrol(self):
        # prepare client
        result = AntiCaptchaControl.aioAntiCaptchaControl(anticaptcha_key = self.anticaptcha_key)
        # check response type
        assert type(result) is python3_anticaptcha.AntiCaptchaControl.AntiCaptchaControl
        
        # get balance
        response = yield result.get_balance()
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

        # complaint on result
        response = yield result.complaint_on_result(reported_id=432423342)
        # check response type
        assert type(response) is dict
        # check all dict keys
        assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

    @asyncio.coroutine
    def test_aiocontrol_context(self):
        # prepare client
        with AntiCaptchaControl.aioAntiCaptchaControl(anticaptcha_key = self.anticaptcha_key) as result:
            # check response type
            assert type(result) is python3_anticaptcha.AntiCaptchaControl.AntiCaptchaControl
        
            # get balance
            response = yield result.get_balance()
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())

            # complaint on result
            response = yield result.complaint_on_result(reported_id=432423342)
            # check response type
            assert type(response) is dict
            # check all dict keys
            assert ['errorId', 'errorCode', 'errorDescription'] == list(response.keys())
