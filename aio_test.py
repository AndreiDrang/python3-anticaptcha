from python3_anticaptcha import aioAntiCaptchaControl

import time
print(aioAntiCaptchaControl.AntiCaptchaControl(anticaptcha_key='ae23fffcfaa29b170e3843e3a486ef19').get_balance())

print(aioAntiCaptchaControl.AntiCaptchaControl(anticaptcha_key='ae23fffcfaa29b170e3843e3a486ef19').complaint_on_result(reported_id=-7))