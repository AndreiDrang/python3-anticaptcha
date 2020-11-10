import time
import asyncio

import aiohttp
import requests

from python3_anticaptcha import app_key, create_task_url, get_sync_result, get_async_result


class GeeTestTaskProxyless:
    def __init__(
        self,
        anticaptcha_key: str,
        websiteURL: str,
        gt: str,
        sleep_time: int = 10,
        callbackUrl: str = None,
    ):
        """
        Модуль отвечает за решение GeeTestTaskProxyless
        :param anticaptcha_key: Ключ от АнтиКапчи
        :param websiteURL: Адрес страницы на которой решается капча
        :param gt: Ключ-индентификатор капчи на целевой странице
        :param sleep_time: Время ожидания решения
        :param callbackUrl: URL для решения капчи с ответом через callback
        """
        if sleep_time < 10:
            raise ValueError(f"Param `sleep_time` must be greater than 10. U set - {sleep_time}")
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {
            "clientKey": anticaptcha_key,
            "task": {"type": "GeeTestTaskProxyless", "websiteURL": websiteURL, "gt": gt},
            "softId": app_key,
        }
        # задаём callbackUrl если передан
        if callbackUrl:
            self.task_payload.update({"callbackUrl": callbackUrl})

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчёй
    def captcha_handler(self, challenge: str, **kwargs) -> dict:
        """
                Метод получает ссылку изображение для задания
                :param challenge: Переменный токен который необходимо обновлять каждый раз перед созданием задачи
        :param kwargs: Дополнительные параметры для `requests.post(....)`.
                :return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload["task"].update({"challenge": challenge})
        # Отправляем на антикапча параметры фанкапич,
        # в результате получаем JSON ответ содержащий номер решаемой капчи
        captcha_id = requests.post(create_task_url, json=self.task_payload, verify=False, **kwargs).json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id["errorId"] == 0:
            captcha_id = captcha_id["taskId"]
            # обновляем пайлоад на получение решения капчи
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id
            # если передан параметр `callbackUrl` - не ждём решения капчи а возвращаем незаполненный ответ
        if self.task_payload.get("callbackUrl"):
            return self.result_payload

        else:
            # Ждем решения капчи
            time.sleep(self.sleep_time)
            return get_sync_result(result_payload=self.result_payload, sleep_time=self.sleep_time)


class aioGeeTestTaskProxyless:
    def __init__(
        self,
        anticaptcha_key: str,
        websiteURL: str,
        gt: str,
        sleep_time: int = 10,
        callbackUrl: str = None,
    ):
        """
                Модуль отвечает за решение GeeTestTaskProxyless
                :param anticaptcha_key: Ключ от АнтиКапчи
                :param websiteURL: Адрес страницы на которой решается капча
        :param gt: Ключ-индентификатор капчи на целевой странице
                :param sleep_time: Время ожидания решения
        :param callbackUrl: URL для решения капчи с ответом через callback
        """
        if sleep_time < 10:
            raise ValueError(f"Param `sleep_time` must be greater than 10. U set - {sleep_time}")
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {
            "clientKey": anticaptcha_key,
            "task": {"type": "GeeTestTaskProxyless", "websiteURL": websiteURL, "gt": gt},
            "softId": app_key,
        }
        # задаём callbackUrl если передан
        if callbackUrl:
            self.task_payload.update({"callbackUrl": callbackUrl})

        # пайлоад для получения ответа сервиса
        self.result_payload = {"clientKey": anticaptcha_key}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчёй
    async def captcha_handler(self, challenge: str) -> dict:
        """
        Метод получает ссылку изображение для задания
        :param challenge: Переменный токен который необходимо обновлять каждый раз перед созданием задачи
        :return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
        """
        self.task_payload["task"].update({"challenge": challenge})
        # Отправляем на антикапча параметры фанкапич,
        # в результате получаем JSON ответ содержащий номер решаемой капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(create_task_url, json=self.task_payload) as resp:
                captcha_id = await resp.json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id["errorId"] == 0:
            captcha_id = captcha_id["taskId"]
            # обновляем пайлоад на получение решения капчи
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

            # если передан параметр `callbackUrl` - не ждём решения капчи а возвращаем незаполненный ответ
        if self.task_payload.get("callbackUrl"):
            return self.result_payload

        else:
            # Ждем решения капчи
            await asyncio.sleep(self.sleep_time)
            return await get_async_result(result_payload=self.result_payload, sleep_time=self.sleep_time)
