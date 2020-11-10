import time
import asyncio

import aiohttp
import requests

from python3_anticaptcha import app_key, create_task_url, get_sync_result, get_async_result

MIN_SCORES = (0.3, 0.7, 0.9)


class ReCaptchaV3TaskProxyless:
    def __init__(self, anticaptcha_key: str, sleep_time: int = 5, callbackUrl: str = None, **kwargs):
        """
        Модуль отвечает за решение ReCaptcha v3 без прокси
        :param anticaptcha_key: Ключ антикапчи
        :param sleep_time: Время ожидания решения капчи
        :param callbackUrl: URL для решения капчи с ответом через callback
        :param kwargs: Другие необязательные параметры из документации
        """
        if sleep_time < 5:
            raise ValueError(f"Param `sleep_time` must be less than 5. U send - {sleep_time}")
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {
            "clientKey": anticaptcha_key,
            "task": {"type": "RecaptchaV3TaskProxyless"},
            "softId": app_key,
        }
        # задаём callbackUrl если передан
        if callbackUrl:
            self.task_payload.update({"callbackUrl": callbackUrl})

        # Пайлоад для получения результата
        self.result_payload = {"clientKey": anticaptcha_key}

        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.task_payload["task"].update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчёй
    def captcha_handler(
        self, websiteURL: str, websiteKey: str, minScore: float, pageAction: str = None, **kwargs
    ) -> dict:
        """
        Метод решения ReCaptcha V3
        :param websiteURL: Ссылка на страницу с капчёй
        :param websiteKey: Ключ-индентификатор рекапчи на целевой странице. Берется из HTML этой страницы.
        :param minScore: Определяет фильтр, по которому отбирается работник с нужным минимальным score.
        :param pageAction: Значение параметра action, которое передается виджетом рекапчи в гугл,
                    и которое потом видит владелец сайта при проверке токена.
        :param kwargs: Дополнительные параметры для `requests.post(....)`, который отправляет даныйе на решение.
        :return: Возвращает ответ сервера в виде JSON-строки
        """
        if minScore not in MIN_SCORES:
            raise ValueError(f"Wrong `minScore` param - {minScore}, available params - {MIN_SCORES};")
        # вставляем в пайлоад адрес страницы и ключ-индентификатор рекапчи
        self.task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "minScore": minScore,
                "pageAction": pageAction,
            }
        )
        # Отправляем на антикапчу пайлоад
        # в результате получаем JSON ответ содержащий номер решаемой капчи
        captcha_id = requests.post(create_task_url, json=self.task_payload, verify=False, **kwargs).json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id["errorId"] == 0:
            captcha_id = captcha_id["taskId"]
            self.result_payload.update({"taskId": captcha_id})
        else:
            return captcha_id

            # если передан параметр `callbackUrl` - не ждём решения капчи а возвращаем незаполненный ответ
        if self.task_payload.get("callbackUrl"):
            return self.result_payload

        else:
            # Ожидаем решения капчи
            time.sleep(self.sleep_time)
            return get_sync_result(result_payload=self.result_payload, sleep_time=self.sleep_time)


class aioReCaptchaV3TaskProxyless:
    def __init__(self, anticaptcha_key: str, sleep_time: int = 5, callbackUrl: str = None, **kwargs):
        """
        Модуль отвечает за решение ReCaptcha V3 без прокси
        :param anticaptcha_key: Ключ антикапчи
        :param sleep_time: Время ожидания решения капчи
        :param callbackUrl: URL для решения капчи с ответом через callback
        :param kwargs: Другие необязательные параметры из документации
        """
        if sleep_time < 5:
            raise ValueError(f"Param `sleep_time` must be less than 5. U send - {sleep_time}")
        self.sleep_time = sleep_time

        # Пайлоад для создания задачи
        self.task_payload = {
            "clientKey": anticaptcha_key,
            "task": {"type": "RecaptchaV3TaskProxyless"},
            "softId": app_key,
        }

        # задаём callbackUrl если передан
        if callbackUrl:
            self.task_payload.update({"callbackUrl": callbackUrl})

        # Пайлоад для получения результата
        self.result_payload = {"clientKey": anticaptcha_key}

        # Если переданы ещё параметры - вносим их в payload
        if kwargs:
            for key in kwargs:
                self.task_payload["task"].update({key: kwargs[key]})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    # Работа с капчёй
    async def captcha_handler(
        self, websiteURL: str, websiteKey: str, minScore: float, pageAction: str = None
    ) -> dict:
        """
        Метод решения ReCaptcha V3
        :param websiteURL: Ссылка на страницу с капчёй
        :param websiteKey: Ключ-индентификатор рекапчи на целевой странице. Берется из HTML этой страницы.
        :param minScore: Определяет фильтр, по которому отбирается работник с нужным минимальным score.
        :param pageAction: Значение параметра action, которое передается виджетом рекапчи в гугл,
                    и которое потом видит владелец сайта при проверке токена.
        :return: Возвращает ответ сервера в виде JSON-строки
        """
        if minScore not in MIN_SCORES:
            raise ValueError(f"Wrong `minScore` param - {minScore}, available params - {MIN_SCORES};")
        # вставляем в пайлоад адрес страницы и ключ-индентификатор рекапчи
        self.task_payload["task"].update(
            {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "minScore": minScore,
                "pageAction": pageAction,
            }
        )
        # Отправляем на антикапчу пайлоад
        # в результате получаем JSON ответ содержащий номер решаемой капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(create_task_url, json=self.task_payload) as resp:
                captcha_id = await resp.json()

        # Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
        if captcha_id["errorId"] == 0:
            captcha_id = captcha_id["taskId"]
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
