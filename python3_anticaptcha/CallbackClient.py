import json
import time

import requests
import pika

from python3_anticaptcha import (
    HOST,
    PORT,
    RTMQ_USERNAME,
    RTMQ_PASSWORD,
    RTMQ_HOST,
    RTMQ_PORT,
    RTMQ_VHOST,
)


class CallbackClient:
    """
    Класс отвечает за получение информации о решении капчи с call-back сервера
    """

    def __init__(self, task_id: int, queue_name: str = None, call_type: str = "cache"):
        """
        :param task_id: ID полученное при создании задания в сервисе AntiCaptcha
        :param queue_name: Название очереди выбранное и переданное последним параметров в URL для `pingback`.
                           Если передан параметр `call_type=queue` то поле это обязательное.
        :param call_type: Ресурс к которому будут отправлятся запросы: `cache` или `queue`
        """
        # заполняем данные IP/PORT
        self.host = HOST
        self.port = PORT

        # ID задания
        self.task_id = int(task_id)
        # тип запросов к серверу
        self.call_type = call_type
        if self.call_type in ("cache", "queue"):
            if self.call_type == "queue":
                if queue_name:
                    self.queue_name = queue_name

                    # заполянем данные для подключения к очереди
                    self.rtmq_username = RTMQ_USERNAME
                    self.rtmq_password = RTMQ_PASSWORD
                    self.rtmq_host = RTMQ_HOST
                    self.rtmq_port = RTMQ_PORT
                    self.rtmq_vhost = RTMQ_VHOST
                else:
                    raise ValueError(
                        "\nВыбран тип получения решения `call_type=queue`, но не передан параметр названия очереди - `queue_name`. "
                        f"\n\tПередайте параметр `queue_name` или измените `call_type=queue` на `call_type=cache`"
                        "\nYou select `call_type=queue` but don`t set `queue_name` param."
                        f"\n\tSet `queue_name` param or change `call_type=queue` to `call_type=cache`"
                    )

        else:
            raise ValueError(
                "\nПередан неверный формат для запросов к callback серверу. "
                f"\n\tВозможные варинты: `cache` или `queue`. Вы передали - `{self.call_type}`"
                "\nWrong `call_type` parameter. Valid params: `cache` or `queue`."
                f"\n\tYour param - `{self.call_type}`"
            )

    def __handle_queue_message(self, requests_timeout: int):
        """
        Метод отвечает за подключение к RabbitMQ очереди и ожидания сообщения с нужным `task_id`
        :param requests_timeout: Время между запросами к серверу.
        """
        # кол-во попыток на получение результата
        attempts = 20

        # подключаемся к RabbitMQ и устанавливаем осединение + канал
        parameters = pika.URLParameters(
            f"amqp://{self.rtmq_username}:{self.rtmq_password}@{self.rtmq_host}:{self.rtmq_port}/{self.rtmq_vhost}"
        )
        connection = pika.BlockingConnection(parameters=parameters)
        channel = connection.channel()

        while attempts > 0:
            # получение сообщения из очереди
            method_frame, _, body = channel.basic_get(self.queue_name)
            if body:
                # декодируем сообщение из bytes в JSON
                json_body = json.loads(body.decode())

                # если ID задания сообщения из очереди совпадает с ID требуемого задания - возвращаем его.
                # если ID не совпадают - ожидаем дальше
                if int(json_body.get("taskId")) == self.task_id:
                    channel.basic_ack(method_frame.delivery_tag)
                    connection.close()
                    return json_body
            # ставим небольшую задержку что бы не спамить сервер rabbitmq
            time.sleep(requests_timeout)
            # уменьшаем счётчик попыток
            attempts -= 1

        return False

    def __handle_cache_message(self, requests_timeout: int):
        """
        Метод отвечает за подключение к серверу, передачу `task_id` и получение резульатата решения капчи из кеша
        :param requests_timeout: Время между запросами к серверу.
        """
        # кол-во попыток на получение результата
        attempts = 20

        # создание сессии
        session = requests.Session()

        while attempts > 0:
            with session.get(
                f"http://{self.host}:{self.port}/anticaptcha/cache/{self.task_id}"
            ) as resp:
                json_body = resp.json()

            # если получен результат решения капчи, а не информация об отсутсвии решения
            if json_body.get("status") != "processing":
                return json_body
            else:
                # ставим небольшую задержку что бы не спамить сервер rabbitmq
                time.sleep(requests_timeout)
                # уменьшаем счётчик попыток
                attempts -= 1

        return False

    def captcha_handler(
        self, requests_timeout: int = 1, auth_params: dict = None
    ) -> dict:
        """
        Метод отвечает за получение результата решения капчи с callback сервера
        :param requests_timeout: Время между запросами к серверу.
        :param auth_params: передаются параметры в формате JSON для подключения к удалённому серверу:
                       {
                           'host': '85.255.8.26',
                           'port': '8001',
                           'rtmq_username': 'hardworker_1',
                           'rtmq_password': 'password',
                           'rtmq_host': '85.255.8.26',
                           'rtmq_port': '5672',
                           'rtmq_vhost': 'anticaptcha_vhost',
                       }
        :return: JSON с решением капчи. Формат - {'id':<task_id>, 'code':<solve>}
        """
        # если переданы кастомные параметры для подключения к серверу или очереди RabbitMQ
        if auth_params:
            # кастомные параметры для подключения к серверу
            self.host = auth_params["host"] if auth_params.get("host") else self.host
            self.port = auth_params["port"] if auth_params.get("port") else self.port

            # кастомные параметры для подключения к очереди
            if self.call_type == "queue":
                self.rtmq_username = (
                    auth_params["rtmq_username"]
                    if auth_params.get("rtmq_username")
                    else self.rtmq_username
                )
                self.rtmq_password = (
                    auth_params["rtmq_password"]
                    if auth_params.get("rtmq_password")
                    else self.rtmq_password
                )
                self.rtmq_host = (
                    auth_params["rtmq_host"]
                    if auth_params.get("rtmq_host")
                    else self.rtmq_host
                )
                self.rtmq_port = (
                    auth_params["rtmq_port"]
                    if auth_params.get("rtmq_port")
                    else self.rtmq_port
                )
                self.rtmq_vhost = (
                    auth_params["rtmq_vhost"]
                    if auth_params.get("rtmq_vhost")
                    else self.rtmq_vhost
                )

        # получение данных из кеша
        if self.call_type == "cache":
            result = self.__handle_cache_message(requests_timeout=requests_timeout)

        # получение данных из очереди
        else:
            result = self.__handle_queue_message(requests_timeout=requests_timeout)

        # если результат не был получен
        if not result:
            result = {
                "taskId": self.task_id,
                "message": {"taskId": self.task_id, "status": "processing"},
            }

        return result
