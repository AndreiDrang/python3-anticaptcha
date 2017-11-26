import requests
import time
import aiohttp
import asyncio

from .config import create_task_url, get_result_url, app_key, user_agent_data

class FunCaptchaTask:
	def __init__(self, anticaptcha_key, proxyAddress, proxyPort, sleep_time=5, proxyType = 'http', **kwargs):
		"""
		Модуль отвечает за решение FunCaptcha
		Параметр userAgent рандомно берётся из актульного списка браузеров-параметров
		:param anticaptcha_key: Ключ от АнтиКапчи
		:param sleep_time: Время ожидания решения
		:param proxyType: Тип прокси http/socks5/socks4
		:param proxyAddress: Адрес прокси-сервера
		:param proxyPort: Порт сервера
		:param kwargs: Можно передать необязательные параметры и переопределить userAgent, все необязательные параметры
						описаны в документации к API на сайте антикапчи
		"""
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": anticaptcha_key,
		                     "task":
			                     {
				                     "type": "FunCaptchaTask",
				                     "userAgent": user_agent_data,
				                     "proxyType": proxyType,
				                     "proxyAddress": proxyAddress,
				                     "proxyPort": proxyPort,
			                     },
		                     }
		
		# пайлоад для получения ответа сервиса
		self.result_payload = {"clientKey": anticaptcha_key}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
		
	# Работа с капчёй
	def captcha_handler(self, websiteURL, websitePublicKey):
		"""
		Метод получает ссылку на страницу на которпой расположена капча и ключ капчи
		:param websiteURL: Ссылка на страницу с капчёй
		:param websitePublicKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи)
		:return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
		"""
		self.task_payload['task'].update({"websiteURL": websiteURL,
		                                  "websiteKey": websitePublicKey})
		# Отправляем на антикапча параметры фанкапич,
		# в результате получаем JSON ответ содержащий номер решаемой капчи
		captcha_id = requests.post(create_task_url, json=self.task_payload).json()

		# Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
		if captcha_id['errorId'] == 0:
			captcha_id = captcha_id["taskId"]
			# обновляем пайлоад на получение решения капчи
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


class aioFunCaptchaTask:
	def __init__(self, anticaptcha_key, proxyAddress, proxyPort, sleep_time=5, proxyType='http', **kwargs):
		"""
		Модуль отвечает за асинхронное решение FunCaptcha
		Параметр userAgent рандомно берётся из актульного списка браузеров-параметров
		:param anticaptcha_key: Ключ от АнтиКапчи
		:param sleep_time: Время ожидания решения
		:param proxyType: Тип прокси http/socks5/socks4
		:param proxyAddress: Адрес прокси-сервера
		:param proxyPort: Порт сервера
		:param kwargs: Можно передать необязательные параметры и переопределить userAgent, все необязательные параметры
						описаны в документации к API на сайте антикапчи
		"""
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": anticaptcha_key,
		                     "task":
			                     {
				                     "type": "FunCaptchaTask",
				                     "userAgent": user_agent_data,
				                     "proxyType": proxyType,
				                     "proxyAddress": proxyAddress,
				                     "proxyPort": proxyPort,
			                     },
		                     }
		
		# пайлоад для получения ответа сервиса
		self.result_payload = {"clientKey": anticaptcha_key}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
	
	# Работа с капчёй
	async def captcha_handler(self, websiteURL, websitePublicKey):
		"""
		Метод получает ссылку на страницу на которпой расположена капча и ключ капчи
		:param websiteURL: Ссылка на страницу с капчёй
		:param websitePublicKey: Ключ капчи(как его получить - описано в документаии на сайте антикапчи)
		:return: Возвращает ответ сервера в виде JSON(ответ так же можно глянуть в документации антикапчи)
		"""
		self.task_payload['task'].update({"websiteURL": websiteURL,
		                                  "websiteKey": websitePublicKey})
		# Отправляем на антикапча параметры фанкапич,
		# в результате получаем JSON ответ содержащий номер решаемой капчи
		async with aiohttp.ClientSession() as session:
			async with session.post(create_task_url, json=self.task_payload) as resp:
				captcha_id = await resp.json()
		
		# Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
		if captcha_id['errorId'] == 0:
			captcha_id = captcha_id["taskId"]
			# обновляем пайлоад на получение решения капчи
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