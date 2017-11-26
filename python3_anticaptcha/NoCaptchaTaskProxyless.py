import requests
import time
import asyncio
import aiohttp

from .config import create_task_url, get_result_url, app_key


class NoCaptchaTaskProxyless:
	def __init__(self, anticaptcha_key, sleep_time=5, **kwargs):
		"""
		Модуль отвечает за решение ReCaptcha без прокси
		:param anticaptcha_key: Ключ антикапчи
		:param sleep_time: Время ожидания решения капчи
		:param kwargs: Другие необязательные параметры из документации
		"""
		self.ANTICAPTCHA_KEY = anticaptcha_key
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": anticaptcha_key,
		                     "task":
			                     {
				                     "type": "NoCaptchaTaskProxyless",
			                     },
		                     }
		
		# Пайлоад для получения результата
		self.result_payload = {"clientKey": self.ANTICAPTCHA_KEY}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
	
	# Работа с капчёй
	def captcha_handler(self, websiteURL, websiteKey):
		"""
		Метод решения ReCaptcha
		:param websiteURL: Ссылка на страницу с капчёй
		:param websiteKey: Ключ капчи сайта(как получить - написано в документации)
		:return: Возвращает ответ сервера в виде JSON-строки
		"""
		
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


class aioNoCaptchaTaskProxyless:
	def __init__(self, anticaptcha_key, sleep_time=5, **kwargs):
		"""
		Модуль отвечает за решение ReCaptcha без прокси
		:param anticaptcha_key: Ключ антикапчи
		:param sleep_time: Время ожидания решения капчи
		:param kwargs: Другие необязательные параметры из документации
		"""
		self.ANTICAPTCHA_KEY = anticaptcha_key
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": anticaptcha_key,
		                     "task":
			                     {
				                     "type": "NoCaptchaTaskProxyless",
			                     },
		                     }
		
		# Пайлоад для получения результата
		self.result_payload = {"clientKey": self.ANTICAPTCHA_KEY}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
	
	# Работа с капчёй
	async def captcha_handler(self, websiteURL, websiteKey):
		"""
		Метод решения ReCaptcha
		:param websiteURL: Ссылка на страницу с капчёй
		:param websiteKey: Ключ капчи сайта(как получить - написано в документации)
		:return: Возвращает ответ сервера в виде JSON-строки
		"""
		
		# вставляем в пайлоад адрес страницы и ключ-индентификатор рекапчи
		self.task_payload['task'].update({"websiteURL": websiteURL,
		                                  "websiteKey": websiteKey})
		# Отправляем на антикапчу пайлоад
		# в результате получаем JSON ответ содержащий номер решаемой капчи
		async with aiohttp.ClientSession() as session:
			async with session.post(create_task_url, json=self.task_payload) as resp:
				captcha_id = await resp.json()
				
		# Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
		if captcha_id['errorId'] == 0:
			captcha_id = captcha_id["taskId"]
			self.result_payload.update({"taskId": captcha_id})
		else:
			return captcha_id
		
		# Ожидаем решения капчи
		await asyncio.sleep(self.sleep_time)
		# отправляем запрос на результат решения капчи, если не решена ожидаем
		async with aiohttp.ClientSession() as session:
			while True:
				async with session.post(get_result_url, json=self.result_payload) as resp:
					json_result = await resp.json()
					
					# Если ошибки нет - проверяем статус капчи
					if json_result['errorId'] == 0:
						# Если капча ещё не готова- ожидаем
						if json_result["status"] == "processing":
							await asyncio.sleep(self.sleep_time)
						# если уже решена - возвращаем ответ сервера
						else:
							return json_result
					# Иначе возвращаем ответ сервера
					else:
						return json_result