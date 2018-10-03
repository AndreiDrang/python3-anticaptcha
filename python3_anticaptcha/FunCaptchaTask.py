import requests
import time
import aiohttp
import asyncio

from .config import create_task_url, app_key, user_agent_data
from .get_answer import get_sync_result, get_async_result


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
		if sleep_time < 5:
			raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
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
							 "softId": app_key
							 }
		
		# пайлоад для получения ответа сервиса
		self.result_payload = {"clientKey": anticaptcha_key}
		
		# Если переданы ещё параметры - вносим их в payload
		if kwargs:
			for key in kwargs:
				self.task_payload['task'].update({key: kwargs[key]})
		
	# Работа с капчёй
	def captcha_handler(self, websiteURL, websitePublicKey, **kwargs):
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
		captcha_id = requests.post(create_task_url, json=self.task_payload, **kwargs).json()

		# Проверка статуса создания задачи, если создано без ошибок - извлекаем ID задачи, иначе возвращаем ответ сервера
		if captcha_id['errorId'] == 0:
			captcha_id = captcha_id["taskId"]
			# обновляем пайлоад на получение решения капчи
			self.result_payload.update({"taskId": captcha_id})
		else:
			return captcha_id

		# Ждем решения капчи
		time.sleep(self.sleep_time)
		return get_sync_result(result_payload=self.result_payload, sleep_time=self.sleep_time)


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
		if sleep_time < 5:
			raise ValueError(f'Параметр `sleep_time` должен быть не менее 5. Вы передали - {sleep_time}')
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
							 "softId": app_key
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

		# Ждем решения капчи
		await asyncio.sleep(self.sleep_time)
		return await get_async_result(result_payload=self.result_payload, sleep_time=self.sleep_time)
