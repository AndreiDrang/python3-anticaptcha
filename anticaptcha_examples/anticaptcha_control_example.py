import asyncio

from python3_anticaptcha import AntiCaptchaControl


ANTICAPTCHA_KEY = ""
# Пример метода отправляющего жалобу на неправелно решённую капчи
# в качестве параметра принимает ключ антикапчи и ID неправильно решённой капчи
# Возвращает логические True(жалоба прошла)/False(ошибка при жалобе)
result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).complaint_on_result(reported_id = -5)
print(result)
# Прмиер метода принимающего ключ аккаунта и возвращающего актуальный баланс
result = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = ANTICAPTCHA_KEY).get_balance()
print(result)

# Асинхронный метод работы
async def run():
	try:
		# io.IOBase
		resolved = await AntiCaptchaControl.aioAntiCaptchaControl(anticaptcha_key=ANTICAPTCHA_KEY).get_balance()
		
		print(resolved)
		resolved = await AntiCaptchaControl.aioAntiCaptchaControl(anticaptcha_key=ANTICAPTCHA_KEY)\
																.complaint_on_result(reported_id = -8)
		
		print(resolved)
	except Exception as err:
		print(err)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	loop.close()