import requests

from .config import create_tast_url, get_result_url, app_key
#TODO from .errors import AntiCaptchaError


class NoCaptchaTask:
    """
    TODO
    """
    def __init__(self, anticaptcha_key, sleep_time=5, website_url, website_key, **kwargs):
        """
        TODO
        :params
        return:
        """
        self.ANTIKAPTCHA_KEY = anticaptcha_key
        self.sleep_time = sleep_time
        #TODO заполнить пайлоад для решения рекапчи
        self.task_payload = {}

    if kwargs:
        for key in kwargs:
            self.task_payload['task'].update(kwars) # is it error?


    def captcha_handler(self):
        #TODO