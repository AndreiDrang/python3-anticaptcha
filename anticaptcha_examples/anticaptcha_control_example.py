import asyncio

from python3_anticaptcha import AntiCaptchaControl


ANTICAPTCHA_KEY = ""
# Пример метода, отправляющего жалобу на неправильно решённую капчу-изображение.
# В качестве параметра, принимает ключ антикапчи и ID неправильно решённой капчи + тип капчи
# Возвращает логические True(жалоба прошла)/False(ошибка при жалобе)
result = AntiCaptchaControl.AntiCaptchaControl(
    anticaptcha_key=ANTICAPTCHA_KEY
).complaint_on_result(reported_id=-5, captcha_type="image")
print(result)
# Пример метода, отправляющего жалобу на неправильно решённую ReCaptcha.
# В качестве параметра, принимает ключ антикапчи и ID неправильно решённой ReCaptcha + тип капчи
# Возвращает логические True(жалоба прошла)/False(ошибка при жалобе)
result = AntiCaptchaControl.AntiCaptchaControl(
    anticaptcha_key=ANTICAPTCHA_KEY
).complaint_on_result(reported_id=-5, captcha_type="recaptcha")
print(result)
# Пример метода, принимающего ключ аккаунта и возвращающего актуальный баланс
result = AntiCaptchaControl.AntiCaptchaControl(
    anticaptcha_key=ANTICAPTCHA_KEY
).get_balance()
print(result)
# Пример метода, выдающий информацию о загрузке очереди, в зависимости от ID очереди
# В данном случае queue_id = 1, то есть получаем информацию по загрузке очереди ImageToText (язык английский)
result = AntiCaptchaControl.AntiCaptchaControl(
    anticaptcha_key=ANTICAPTCHA_KEY
).get_queue_status(queue_id=1)
print(result)

# Асинхронный метод работы
async def run():
    try:
        # io.IOBase
        resolved = await AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=ANTICAPTCHA_KEY
        ).get_balance()
        print(resolved)

        resolved = await AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=ANTICAPTCHA_KEY
        ).complaint_on_result(reported_id=-8, captcha_type="image")
        print(resolved)

        resolved = await AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=ANTICAPTCHA_KEY
        ).complaint_on_result(reported_id=-8, captcha_type="recaptcha")
        print(resolved)

        resolved = await AntiCaptchaControl.aioAntiCaptchaControl(
            anticaptcha_key=ANTICAPTCHA_KEY
        ).get_queue_status(queue_id=1)
        print(resolved)
        
    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
