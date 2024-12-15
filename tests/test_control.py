from tests.conftest import BaseTest
from python3_anticaptcha.control import Control
from python3_anticaptcha.core.serializer import BaseAPIResponseSer


class TestControl(BaseTest):
    def test_get_balance(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.get_balance()

        assert isinstance(result, dict)
        assert result["balance"] != 0.0
        assert result["errorId"] == 0

    async def test_aio_get_balance(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_get_balance()

        assert isinstance(result, dict)
        assert result["balance"] != 0.0
        assert result["errorId"] == 0

    def test_get_queue_status(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.get_queue_status(queue_id=1)

        assert isinstance(result, dict)
        assert result["bid"] != 0.0
        assert result["load"] != 0.0
        assert result["speed"] != 0.0
        assert result["total"] != 0.0
        assert result["waiting"] != 0.0

    async def test_aio_get_queue_status(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_get_queue_status(queue_id=1)

        assert isinstance(result, dict)
        assert result["bid"] != 0.0
        assert result["load"] != 0.0
        assert result["speed"] != 0.0
        assert result["total"] != 0.0
        assert result["waiting"] != 0.0

    def test_get_spending_stats(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.get_spending_stats(softId=867, queue="English ImageToText")

        assert isinstance(result, dict)
        assert result["data"] != []

    async def test_aio_get_spending_stats(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_get_spending_stats(softId=867, queue="English ImageToText")

        assert isinstance(result, dict)
        assert result["data"] != []

    def test_get_app_stats(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.get_app_stats(softId=867)

        assert isinstance(result, dict)
        assert result["chartData"] != []
        assert result["chartData"][0]["data"] != []

    async def test_aio_get_app_stats(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_get_app_stats(softId=867)

        assert isinstance(result, dict)
        assert result["chartData"] != []
        assert result["chartData"][0]["data"] != []

    def test_report_incorrect_image(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.report_incorrect_image(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    async def test_aio_report_incorrect_image(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_report_incorrect_image(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    def test_report_incorrect_recaptcha(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.report_incorrect_recaptcha(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    async def test_aio_report_incorrect_recaptcha(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_report_incorrect_recaptcha(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    def test_report_correct_recaptcha(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.report_correct_recaptcha(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    async def test_aio_report_correct_recaptcha(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_report_correct_recaptcha(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    def test_report_incorrect_hcaptcha(self):
        instance = Control(api_key=self.API_KEY)
        result = instance.report_incorrect_hcaptcha(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)

    async def test_aio_report_incorrect_hcaptcha(self):
        instance = Control(api_key=self.API_KEY)
        result = await instance.aio_report_incorrect_hcaptcha(taskId=867)

        assert isinstance(result, dict)
        assert BaseAPIResponseSer(**result)
