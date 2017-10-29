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