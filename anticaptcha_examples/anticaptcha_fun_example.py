from python3_anticaptcha import FunCaptchaTask


ANTICAPTCHA_KEY = ""
WEB_URL = ""
SITE_KEY = ""
# Пример работы антикапчи с фанкапчёй и с использованием прокси при этом
result = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                       proxyType='http',
                                       proxyAddress="8.8.8.8",
                                       proxyPort=8080,
                                       proxyLogin="proxyLoginHere",
                                       proxyPassword="proxyPasswordHere")\
		.captcha_handler(websiteURL=WEB_URL,
                         websitePublicKey=SITE_KEY)

print(result)