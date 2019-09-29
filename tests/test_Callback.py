import requests

from tests.main import MainAntiCaptcha


class TestAntiCaptcha(MainAntiCaptcha):
    def test_callback_server(self):
        # test server alive
        response = requests.get(f"http://{self.server_ip}:8001/ping")
        assert response.status_code == 200
        # try register new queue
        response = requests.post(
            f"http://{self.server_ip}:8001/register_key",
            json={"key": "fwefefefopewofkewopfkop", "vhost": "anticaptcha_vhost"},
        )
        assert response.status_code == 200
