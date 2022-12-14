import time
import asyncio

from python3_anticaptcha import get_sync_result, get_async_result


class CustomResultHandler:
    def __init__(self, anticaptcha_key: str, sleep_time: int = 5, **kwargs):
        """
        The module is responsible for obtaining a captcha solution by task ID
        :param anticaptcha_key: Key to AntiCaptcha
        :param sleep_time: Solution timeout
        """
        if sleep_time < 5:
            raise ValueError(f"Param `sleep_time` must be greater than 5. U set - {sleep_time}")
        self.sleep_time = sleep_time
        # payload for receiving service response
        self.result_payload = {"clientKey": anticaptcha_key}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    def task_handler(self, task_id: int) -> dict:
        """
        Method get task ID and try get captcha solution from server
        :param task_id: Captcha task ID
        """
        # update payload to get a captcha solution
        self.result_payload.update({"taskId": task_id})

        # wait captcha solution result
        time.sleep(self.sleep_time)
        return get_sync_result(result_payload=self.result_payload, sleep_time=self.sleep_time)


class aioCustomResultHandler:
    def __init__(self, anticaptcha_key: str, sleep_time: int = 5, **kwargs):
        """
        The async module is responsible for obtaining a captcha solution by task ID
        :param anticaptcha_key: Key to AntiCaptcha
        :param sleep_time: Solution timeout
        """
        if sleep_time < 5:
            raise ValueError(f"Param `sleep_time` must be greater than 5. U set - {sleep_time}")
        self.sleep_time = sleep_time
        # payload for receiving service response
        self.result_payload = {"clientKey": anticaptcha_key}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def task_handler(self, task_id: int) -> dict:
        """
        Method get task ID and try get captcha solution from server
        :param task_id: Captcha task ID
        """
        # update payload to get a captcha solution
        self.result_payload.update({"taskId": task_id})

        # wait captcha solution result
        await asyncio.sleep(self.sleep_time)
        return await get_async_result(result_payload=self.result_payload, sleep_time=self.sleep_time)
