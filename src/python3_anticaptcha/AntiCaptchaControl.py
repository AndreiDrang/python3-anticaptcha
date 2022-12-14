import aiohttp
import requests

# Адрес для получения баланса
get_balance_url = "https://api.anti-captcha.com/getBalance"
# Адрес для отправки жалобы на неверное решение капчи-изображения
incorrect_imagecaptcha_url = "https://api.anti-captcha.com/reportIncorrectImageCaptcha"
# Адрес для отправки жалобы на неверное решение ReCaptcha
incorrect_recaptcha_url = "https://api.anti-captcha.com/reportIncorrectRecaptcha"
# Адрес для получения информации о очереди
get_queue_status_url = "https://api.anti-captcha.com/getQueueStats"
# С помощью этого метода можно получить статистику трат за последние 24 часа.
get_spend_stats_url = "https://api.anti-captcha.com/getSpendingStats"
# Адрес для получения информации о приложении
get_app_stats_url = "https://api.anti-captcha.com/getAppStats"
# С помощью этого метода можно получить статистику трат за последние 24 часа.
send_funds_url = "https://api.anti-captcha.com/sendFunds"

# available app stats mods
mods = ("errors", "views", "downloads", "users", "money")
# available complaint captcha types
complaint_types = ("image", "recaptcha")
# availalbe queue ID's
queue_ids = (1, 2, 5, 6, 7, 10, 11, 12, 13, 18, 19, 20, 21, 22)

queues_names = (
    "English ImageToText",
    "Russian ImageToText",
    "Recaptcha Proxy-on",
    "Recaptcha Proxyless",
    "FunCaptcha",
    "Funcaptcha Proxyless",
    "Square Net Task",
    "GeeTest Proxy-on",
    "GeeTest Proxyless",
)


class AntiCaptchaControl:
    def __init__(self, anticaptcha_key: str):
        """
        Синхронный метод работы с балансом и жалобами
        :param anticaptcha_key: Ключ антикапчи
        """
        self.ANTICAPTCHA_KEY = anticaptcha_key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    def get_balance(self) -> dict:
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        answer = requests.post(get_balance_url, json={"clientKey": self.ANTICAPTCHA_KEY}, verify=False)

        return answer.json()

    def send_funds(self, accountLogin: str = None, accountEmail: str = None, amount: float = None) -> dict:
        """
        Отправить средства другому пользователю
        В вашем аккаунте должна быть включена опция отправки средств через API.
        Включается через службу поддержки, нужно указать причину зачем вам это требуется.

        :param accountLogin: Логин целевого аккаунта
        :param accountEmail: Адрес почты целевого аккаунта
        :param amount: Сумма
        """
        payload = {
            "clientKey": self.ANTICAPTCHA_KEY,
            "accountLogin": accountLogin,
            "accountEmail": accountEmail,
            "amount": amount,
        }
        # get response
        answer = requests.post(send_funds_url, json=payload, verify=False)
        return answer.json()

    def get_spend_stats(
        self, date: int = None, queue: str = None, softId: int = None, ip: str = None
    ) -> dict:
        f"""
        С помощью этого метода можно получить статистику трат за последние 24 часа.
        :param date: Unix timestamp начала периода 24-х часового отчета
        :param queue: Имя очереди, может быть найдено в статистике Антикапчи.
                        Если не указано, то возвращается суммированная статистика по всем очередям.
        :param softId: ID приложения из Developers Center
        :param ip: IP с которого шли запросы к API
        :return: Возвращает словарь с данными трат
        """
        if queue and queue not in queues_names:
            raise ValueError(
                f"\nWrong `queue` parameter. Valid params: {queues_names}." f"\n\tYour param - `{queue}`"
            )
        payload = {
            "clientKey": self.ANTICAPTCHA_KEY,
            "date": date,
            "queue": queue,
            "softId": softId,
            "ip": ip,
        }
        # get response
        answer = requests.post(get_spend_stats_url, json=payload, verify=False)
        return answer.json()

    def get_app_stats(self, softId: int, mode: str = "errors") -> dict:
        """
        Получение статистики приложения
        :return: Возвращает актуальный баланс
        """
        if mode not in mods:
            raise ValueError(f"\nWrong `mode` parameter. Valid params: {mods}." f"\n\tYour param - `{mode}`")
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "softId": softId, "mode": mode}
        answer = requests.post(get_app_stats_url, json=payload, verify=False)

        if answer.text:
            return answer.json()
        else:
            return {"errorId": 1}

    def complaint_on_result(self, reported_id: int, captcha_type: str = "image") -> dict:
        f"""
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :param captcha_type: Тип капчи на который идёт жалоба. Возможные варианты:
                            {complaint_types}
        :return: Возвращает True/False, в зависимости от результата
        """
        if captcha_type not in complaint_types:
            raise ValueError(
                f"\nWrong `captcha_type` parameter. Valid params: {complaint_types}."
                f"\n\tYour param - `{captcha_type}`"
            )
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "taskId": reported_id}
        # complaint on image captcha
        if captcha_type == "image":
            answer = requests.post(incorrect_imagecaptcha_url, json=payload, verify=False)
        # complaint on re-captcha
        elif captcha_type == "recaptcha":
            answer = requests.post(incorrect_recaptcha_url, json=payload, verify=False)
        return answer.json()

    @staticmethod
    def get_queue_status(queue_id: int) -> dict:
        """
        Получение информации о загрузке очереди, в зависимости от ID очереди.

        Метод позволяет определить, насколько в данный момент целесообразно загружать новое задание в очередь.
        Данные в выдаче кешируются на 10 секунд.

        Список ID очередей:
            1   - стандартная ImageToText, язык английский
            2   - стандартная ImageToText, язык русский
            5   - Recaptcha NoCaptcha
            6   - Recaptcha Proxyless
            7   - Funcaptcha
            10  - Funcaptcha Proxyless
            11  - Square Net Task
            12  - GeeTest Proxy-On
            13  - GeeTest Proxyless
            18  - Recaptcha V3 s0.3
            19  - Recaptcha V3 s0.7
            20  - Recaptcha V3 s0.9

        Пример выдачи ответа:
            {
                "waiting":242,
                "load":60.33,
                "bid":"0.0008600982",
                "speed":10.77,
                "total": 610
            }
        :param queue_id: Номер очереди
        :return: JSON-объект
        """

        if queue_id not in queue_ids:
            raise ValueError(
                f"\nWrong `mode` parameter. Valid params: {queue_ids}." f"\n\tYour param - `{queue_id}`"
            )
        payload = {"queueId": queue_id}

        answer = requests.post(get_queue_status_url, json=payload, verify=False)

        return answer.json()


class aioAntiCaptchaControl:
    def __init__(self, anticaptcha_key: str):
        """
        Асинхронный метод работы с балансом и жалобами
        :param anticaptcha_key: Ключ антикапчи
        """
        self.ANTICAPTCHA_KEY = anticaptcha_key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def get_balance(self) -> dict:
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(get_balance_url, json={"clientKey": self.ANTICAPTCHA_KEY}) as resp:
                if await resp.text():
                    return await resp.json()
                else:
                    return {"errorId": 1}

    async def send_funds(
        self, accountLogin: str = None, accountEmail: str = None, amount: float = None
    ) -> dict:
        """
        Отправить средства другому пользователю
        В вашем аккаунте должна быть включена опция отправки средств через API.
        Включается через службу поддержки, нужно указать причину зачем вам это требуется.

        :param accountLogin: Логин целевого аккаунта
        :param accountEmail: Адрес почты целевого аккаунта
        :param amount: Сумма
        """
        payload = {
            "clientKey": self.ANTICAPTCHA_KEY,
            "accountLogin": accountLogin,
            "accountEmail": accountEmail,
            "amount": amount,
        }
        # get response
        async with aiohttp.ClientSession() as session:
            async with session.post(send_funds_url, json=payload) as resp:
                if await resp.text():
                    return await resp.json()
                else:
                    return {"errorId": 1}

    async def get_spend_stats(
        self, date: int = None, queue: str = None, softId: int = None, ip: str = None
    ) -> dict:
        f"""
        С помощью этого метода можно получить статистику трат за последние 24 часа.
        :param date: Unix timestamp начала периода 24-х часового отчета
        :param queue: Имя очереди, может быть найдено в статистике Антикапчи.
                        Если не указано, то возвращается суммированная статистика по всем очередям.
        :param softId: ID приложения из Developers Center
        :param ip: IP с которого шли запросы к API
        :return: Возвращает словарь с данными трат
        """
        if queue and queue not in queues_names:
            raise ValueError(
                f"\nWrong `queue` parameter. Valid params: {queues_names}." f"\n\tYour param - `{queue}`"
            )
        payload = {
            "clientKey": self.ANTICAPTCHA_KEY,
            "date": date,
            "queue": queue,
            "softId": softId,
            "ip": ip,
        }
        # get response
        async with aiohttp.ClientSession() as session:
            async with session.post(get_spend_stats_url, json=payload) as resp:
                if await resp.text():
                    return await resp.json()
                else:
                    return {"errorId": 1}

    async def get_app_stats(self, softId: int, mode: str = "errors") -> dict:
        """
        Получение баланса аккаунта
        :return: Возвращает актуальный баланс
        """
        if mode not in mods:
            raise ValueError(f"\nWrong `mode` parameter. Valid params: {mods}." f"\n\tYour param - `{mode}`")
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "softId": softId, "mode": mode}
        async with aiohttp.ClientSession() as session:
            async with session.post(get_app_stats_url, json=payload) as resp:
                if await resp.text():
                    return await resp.json()
                else:
                    return {"errorId": 1}

    async def complaint_on_result(self, reported_id: int, captcha_type: str = "image") -> dict:
        f"""
        Позволяет отправить жалобу на неправильно решённую капчу.
        :param reported_id: Отправляете ID капчи на которую нужно пожаловаться
        :param captcha_type: Тип капчи на который идёт жалоба. Возможные варианты:
                            {complaint_types}
        :return: Возвращает True/False, в зависимости от результата
        """
        if captcha_type not in complaint_types:
            raise ValueError(
                f"\nWrong `captcha_type` parameter. Valid params: {complaint_types}."
                f"\n\tYour param - `{captcha_type}`"
            )
        payload = {"clientKey": self.ANTICAPTCHA_KEY, "taskId": reported_id}
        # complaint on image captcha
        if captcha_type == "image":
            async with aiohttp.ClientSession() as session:
                async with session.post(incorrect_imagecaptcha_url, json=payload) as resp:
                    if await resp.text():
                        return await resp.json()
                    else:
                        return {"errorId": 1}
        # complaint on re-captcha
        elif captcha_type == "recaptcha":
            async with aiohttp.ClientSession() as session:
                async with session.post(incorrect_recaptcha_url, json=payload) as resp:
                    if await resp.text():
                        return await resp.json()
                    else:
                        return {"errorId": 1}

    @staticmethod
    async def get_queue_status(queue_id: int) -> dict:
        """
        Получение информации о загрузке очереди, в зависимости от ID очереди.

        Метод позволяет определить, насколько в данный момент целесообразно загружать новое задание в очередь.
        Данные в выдаче кешируются на 10 секунд.

        Список ID очередей:
            1   - стандартная ImageToText, язык английский
            2   - стандартная ImageToText, язык русский
            5   - Recaptcha NoCaptcha
            6   - Recaptcha Proxyless
            7   - Funcaptcha
            10  - Funcaptcha Proxyless

        Пример выдачи ответа:
            {
                "waiting":242,
                "load":60.33,
                "bid":"0.0008600982",
                "speed":10.77,
                "total": 610
            }
        :param queue_id: Номер очереди
        :return: JSON-объект
        """
        if queue_id not in queue_ids:
            raise ValueError(
                f"\nWrong `mode` parameter. Valid params: {queue_ids}." f"\n\tYour param - `{queue_id}`"
            )
        payload = {"queueId": queue_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(get_queue_status_url, json=payload) as resp:
                if await resp.text():
                    return await resp.json()
                else:
                    return {"errorId": 1}
