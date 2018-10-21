# Адрес для создания задачи
create_task_url = "https://api.anti-captcha.com/createTask"
# Адрес для получения ответа
get_result_url = "https://api.anti-captcha.com/getTaskResult"
# Адрес для получения баланса
get_balance_url = "https://api.anti-captcha.com/getBalance"
# Адрес для отправки жалобы на неверное решение капчи
incorrect_captcha_url = "https://api.anti-captcha.com/reportIncorrectImageCaptcha"
# Адрес для получения информации об очереди
get_queue_status_url = "https://api.anti-captcha.com/getQueueStats"
# ключ приложения
app_key = "867"
# random user agent data
# получаем рандомный userAgent
# TODO протестировать `fake_useragent` на исправление старых беспричинных падений и обновить получение данных
from fake_useragent import UserAgent
try:
	user_agent_data = UserAgent().random
except:
	user_agent_data = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)'
