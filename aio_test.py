from python3_anticaptcha import aioAntiCaptchaControl, aioImageToTextTask
import asyncio
import aiohttp
import time
print(aioAntiCaptchaControl.AntiCaptchaControl(anticaptcha_key='ae23fffcfaa29b170e3843e3a486ef19').get_balance())

#print(aioAntiCaptchaControl.AntiCaptchaControl(anticaptcha_key='ae23fffcfaa29b170e3843e3a486ef19').complaint_on_result(reported_id=-7))

print(aioImageToTextTask.ImageToTextTask(anticaptcha_key='ae23fffcfaa29b170e3843e3a486ef19', save_format = 'const')\
									.captcha_handler('http://85.255.8.26/static/image/common_image_example/800070.png'))
