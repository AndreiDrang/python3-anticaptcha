import requests
import time

from .config import create_task_url, get_result_url, app_key
# from .errors import RuCaptchaError
#TODO Добавить документацию


class NoCaptchaTaskProxyless:
	def __init__(self, anticaptcha_key, sleep_time=5, **kwargs):
		
		self.ANTICAPTCHA_KEY = anticaptcha_key
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": self.ANTICAPTCHA_KEY,
		                     "task":
			                     {
				                     "type": "NoCaptchaTaskProxyless",
			                     },
		                     }
		
		# отправляем запрос на результат решения капчи, если ещё капча не решена - ожидаем 5 сек
		# если всё ок - идём дальше
		self.result_payload = {"clientKey": self.ANTICAPTCHA_KEY}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
	
	# Работа с капчёй
	def captcha_handler(self, websiteURL, websiteKey):
		
		# вставляем в пайлоад адрес страницы и ключ-индентификатор рекапчи
		self.task_payload['task'].update({"websiteURL": websiteURL,
		                                  "websiteKey": websiteKey})
		# Отправляем на антикапчу пайлоад
		# в результате получаем JSON ответ содержащий номер решаемой капчи
		captcha_id = requests.post(create_task_url, json=self.task_payload).json()
		
		# Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
		if captcha_id['errorId'] == 0:
			captcha_id = captcha_id["taskId"]
			self.result_payload.update({"taskId": captcha_id})
		else:
			return captcha_id
		
		# Ожидаем решения капчи
		time.sleep(self.sleep_time)
		while True:
			# отправляем запрос на результат решения капчи, если не решена ожидаем
			captcha_response = requests.post(get_result_url, json=self.result_payload)
			
			# Если ошибки нет - проверяем статус капчи
			if captcha_response.json()['errorId'] == 0:
				# Если капча ещё не готова- ожидаем
				if captcha_response.json()["status"] == "processing":
					time.sleep(self.sleep_time)
				# если уже решена - возвращаем ответ сервера
				else:
					return captcha_response.json()
			# Иначе возвращаем ответ сервера
			else:
				return captcha_response.json()
