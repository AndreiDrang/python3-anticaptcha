import os

# 1. `export anticaptcha_key=274832f8168a36019895a1e1174777c0`


class MainAntiCaptcha(object):
    WRONG_QUEUE_ID = WRONG_TASK_ID = -1

    def setup_class(self):
        self.anticaptcha_key_fail = os.getenv("anticaptcha_key")[:5]
        self.anticaptcha_key_true = os.getenv("anticaptcha_key")
        self.server_ip = "85.255.8.26"
        self.host = "https://pythoncaptcha.tech"
        self.image_url = self.host + "/static/image/common_image_example/620626.png"

        self.ERROR_RESPONSE_JSON = {
            "errorId": 1,
            "errorCode": 123,
            "errorDescription": "String with data",
        }
        self.VALID_RESPONSE_JSON = {
            "errorId": 0,
            "errorCode": 0,
            "taskId": 456,
            "errorDescription": "String with data",
        }
        self.VALID_RESPONSE_RESULT_JSON = {"errorId": 0, "status": "ready"}
