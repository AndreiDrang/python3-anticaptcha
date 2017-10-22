import requests

from .config import create_task_url, get_result_url, app_key
#TODO from .errors import AntiCaptchaError


class NoCaptchaTask:
    """
    TODO
    """
    # Добавить прокси адрес
    def __init__(self, anticaptcha_key, website_url, website_key, proxy_type="http", sleep_time=5, **kwargs):
        """
        TODO
        :params
        return:
        """
        self.ANTIKAPTCHA_KEY = anticaptcha_key
        self.sleep_time = sleep_time
        self.website_url = website_url
        self.website_key = website_key
        self.proxy_type = proxy_type
        #TODO заполнить пайлоад для решения рекапчи
        self.task_payload = {"clientKey": self.ANTIKAPTCHA_KEY,
                             "task":
                             {
                                "type": "NoCaptchaTask",
                                "website_url": self.website_url,
                                "website_key": self.website_key,
                                "proxy_type": self.proxy_type,
                                "proxy_adress": "",
                                "proxy_login": "",
                                "proxy_password": ""
                             }}

        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update(kwargs) # is it error?


    def captcha_handler(self):
        #TODO
        pass