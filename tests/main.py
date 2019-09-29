import os


class MainAntiCaptcha(object):
    WRONG_QUEUE_ID = WRONG_TASK_ID = -1

    def setup_class(self):
        self.anticaptcha_key_fail = os.getenv("anticaptcha_key")[:5]
        self.anticaptcha_key_true = os.getenv("anticaptcha_key")
        self.server_ip = "85.255.8.26"
        self.host = "https://pythoncaptcha.cloud"
        self.image_url = self.host + "/static/image/common_image_example/620626.png"
