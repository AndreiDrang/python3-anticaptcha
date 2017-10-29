import requests
import time

from .config import create_task_url, get_result_url, app_key, user_agent_data


class NoCaptchaTask:

    def __init__(self, anticaptcha_key, proxyAddress, proxyPort, sleep_time=5, proxyType = 'http', **kwargs):
        """
        :params
        return:
        """
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {"clientKey": anticaptcha_key,
                             "task":
                                 {
                                     "type": "FunCaptchaTask",
                                     "userAgent": user_agent_data,
                                     "proxyType": proxyType,
                                     "proxyAddress": proxyAddress,
                                     "proxyPort": proxyPort,
                                 },
                             }

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}
        
        if kwargs:
            for key in kwargs:
                self.task_payload['task'].update({key: kwargs[key]})


    def captcha_handler(self, websiteURL, websiteKey):
        self.task_payload['task'].update({"websiteURL": websiteURL,
                                          "websiteKey": websiteKey})
        # отправляем реквест
        captcha_id = requests.post(create_task_url, json=self.task_payload).json()

        if captcha_id['errorId'] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

        # Ждем решения капчи
        time.sleep(self.sleep_time)
        while True:
            captcha_response = requests.post(get_result_url, json=self.result_payload)

            if captcha_response.json()["errorId"] == 0:
                if captcha_response.json()["status"] == "processing":
                    time.sleep(self.sleep_time)
                else:
                    return captcha_response.json()
            else:
                return captcha_response.json()