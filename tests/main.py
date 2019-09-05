import os


class MainAntiCaptcha(object):
    WRONG_QUEUE_ID = WRONG_TASK_ID = -1

    def setup_class(self):
        self.anticaptcha_key_fail = os.getenv("anticaptcha_key")[:5]
        self.anticaptcha_key_true = os.getenv("anticaptcha_key")
        self.server_ip = "85.255.8.26"
        self.image_url = "https://raw.githubusercontent.com/AndreiDrang/python3-anticaptcha/master/anticaptcha_examples/088636.png"
