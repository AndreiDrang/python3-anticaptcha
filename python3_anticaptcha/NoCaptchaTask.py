import requests
from .config import create_task_url, get_result_url, app_key, user_agent_data
#TODO from .errors import AntiCaptchaError


class NoCaptchaTask:
    """
    TODO
    """
    # Добавить прокси адрес
    def __init__(self, anticaptcha_key, website_url, website_key, proxy_type="http", proxy_adress="?", 
                 proxy_prot=None, proxy_password=None sleep_time=5, user_agent=user_agent_data, **kwargs):
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
                                    "proxy_adress": None,
                                    "proxy_login": None,
                                    "proxy_password": None
                                 }
                             }

    if kwargs:
        for key in kwargs:
            self.task_payload['task'].update({key: kwargs[key]})


    def captcha_handler(self):
        # отправляем реквест
        captcha_id = requests.post(create_task_url, json=self.task_payload).json()

        if captcha_id['errorId'] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

        time.sleep(self.sleep_time)
        while True:
            pass