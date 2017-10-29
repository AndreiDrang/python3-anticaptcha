from python3_anticaptcha import NoCaptchaTaskProxyless, NoCaptchaTask

ANTICAPTCHA_KEY = ""

# Пример показывает работу антикапчи с "невидимой" рекапчёй от гугла, точно так же работает обычная рекапча от гугла.
# Это метод для работы без прокси
result = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = ANTICAPTCHA_KEY)\
									.captcha_handler(websiteURL='https://www.google.com/recaptcha/intro/android.html',
                                                     websiteKey='6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b')
print(result)

# Пример работы антикапчи с гугловской невидимой рекапчёй и обычной рекапчёй с использованием ПРОКСИ
result = NoCaptchaTask.NoCaptchaTask(anticaptcha_key = ANTICAPTCHA_KEY,
                                     proxyType='http',
                                     proxyAddress="8.8.8.8",
                                     proxyPort=8080,
                                     proxyLogin="proxyLoginHere",
                                     proxyPassword="proxyPasswordHere")\
		.captcha_handler(websiteURL='https://www.google.com/recaptcha/intro/android.html',
                         websiteKey='6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b')

print(result)
