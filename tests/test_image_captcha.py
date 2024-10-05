from tests.conftest import BaseTest
from python3_anticaptcha.image_captcha import ImageToTextCaptcha


class TestImageCaptcha(BaseTest):
    captcha_file = "files/captcha-image.jpg"
    captcha_url = (
        "https://raw.githubusercontent.com/AndreiDrang/python3-anticaptcha/refs/heads/main/files/captcha-image.jpg"
    )

    kwargs_params = {
        "phrase": False,
        "case": False,
        "numeric": 0,
        "math": False,
        "minLength": 0,
        "maxLength": 0,
        "languagePool": "en",
    }

    def test_methods_exists(self):
        assert "captcha_handler" in ImageToTextCaptcha.__dict__.keys()
        assert "aio_captcha_handler" in ImageToTextCaptcha.__dict__.keys()
        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY

    def test_args(self):
        instance = ImageToTextCaptcha(api_key=self.API_KEY)
        assert instance.create_task_payload.clientKey == self.API_KEY
