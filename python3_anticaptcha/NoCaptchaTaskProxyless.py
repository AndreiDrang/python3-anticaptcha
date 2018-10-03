import requests
import time
import asyncio
import aiohttp

from .config import create_task_url, get_result_url, app_key
from .get_answer import get_sync_result, get_async_result


class NoCaptchaTaskProxyless:
	def __init__(self, anticaptcha_key, sleep_time=5, **kwargs):
		"""
		Модуль отвечает за решение ReCaptcha без прокси
		:param anticaptcha_key: Ключ антикапчи
		:param sleep_time: Время ожидания решения капчи
		:param kwargs: Другие необязательные параметры из документации
		"""
		if sleep_time < 5:
			raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": anticaptcha_key,
		                     "task":
			                     {
				                     "type": "NoCaptchaTaskProxyless",
			                     },
                             "softId": app_key
		                     }
		
		# Пайлоад для получения результата
		self.result_payload = {"clientKey": anticaptcha_key}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
	
	# Работа с капчёй
	def captcha_handler(self, websiteURL, websiteKey, **kwargs):
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
		captcha_id = requests.post(create_task_url, json=self.task_payload, **kwargs).json()
		
		# Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
		if captcha_id['errorId'] == 0:
			captcha_id = captcha_id["taskId"]
			self.result_payload.update({"taskId": captcha_id})
		else:
			return captcha_id

		# Ждем решения капчи
		time.sleep(self.sleep_time)
		return get_sync_result(result_payload=self.result_payload, sleep_time=self.sleep_time)


class aioNoCaptchaTaskProxyless:
	def __init__(self, anticaptcha_key, sleep_time=5, **kwargs):
		"""
		Модуль отвечает за решение ReCaptcha без прокси
		:param anticaptcha_key: Ключ антикапчи
		:param sleep_time: Время ожидания решения капчи
		:param kwargs: Другие необязательные параметры из документации
		"""
		if sleep_time < 5:
			raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
		self.sleep_time = sleep_time
		
		# Пайлоад для создания задачи
		self.task_payload = {"clientKey": anticaptcha_key,
		                     "task":
			                     {
				                     "type": "NoCaptchaTaskProxyless",
			                     },
                             "softId": app_key
		                     }
		
		# Пайлоад для получения результата
		self.result_payload = {"clientKey": anticaptcha_key}
		
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

		# Ждем решения капчи
		await asyncio.sleep(self.sleep_time)
		return await get_async_result(result_payload=self.result_payload, sleep_time=self.sleep_time)
