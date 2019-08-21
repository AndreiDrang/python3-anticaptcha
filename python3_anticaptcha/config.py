# Адрес для создания задачи
create_task_url = "https://api.anti-captcha.com/createTask"
# Адрес для получения ответа
get_result_url = "https://api.anti-captcha.com/getTaskResult"
# Адрес для получения баланса
get_balance_url = "https://api.anti-captcha.com/getBalance"
# Адрес для отправки жалобы на неверное решение капчи-изображения
incorrect_imagecaptcha_url = "https://api.anti-captcha.com/reportIncorrectImageCaptcha"
# Адрес для отправки жалобы на неверное решение ReCaptcha
incorrect_recaptcha_url = "https://api.anti-captcha.com/reportIncorrectRecaptcha "
# Адрес для получения информации о очереди
get_queue_status_url = "https://api.anti-captcha.com/getQueueStats"
# Адрес для получения информации о приложении
get_app_stats_url = "https://api.anti-captcha.com/getAppStats"
# ключ приложения
app_key = "867"

"""
Параметры для callback
"""
# IP для работы callback`a
HOST = "85.255.8.26"
# PORT для работы callback`a
PORT = 8001
# данные для подключения к RabbitMQ на callback сервере
RTMQ_USERNAME = "hardworker_1"
RTMQ_PASSWORD = "password"
RTMQ_HOST = "85.255.8.26"
RTMQ_PORT = 5672
RTMQ_VHOST = "anticaptcha_vhost"
