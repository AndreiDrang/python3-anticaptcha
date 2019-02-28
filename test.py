import requests

import python3_anticaptcha
from python3_anticaptcha import NoCaptchaTaskProxyless

class TestAntiCaptcha(object):
    def setup_class(self):
        #def __init__(self):
        self.anticaptcha_key = "ae23fffcfaa29b170e3843e3a486ef19"
        self.server_ip = '85.255.8.26'

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

    def test_nocaptcha(self):
        nocaptcha = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
                        anticaptcha_key = self.anticaptcha_key, 
                        callbackUrl=f'http://{self.server_ip}:8001/anticaptcha/nocaptcha/fwefefefopewofkewopfkop'
                    )
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
