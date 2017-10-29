from python3_anticaptcha import ImageToTextTask, config, AntiCaptchaControl, FunCaptchaTask, NoCaptchaTaskProxyless

key = config.TEST_KEY
print(ImageToTextTask.ImageToTextTask(key, save_format = 'const').captcha_handler('http://85.255.8.26/static/image/common_image_example/800070.png'))
print(AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = config.TEST_KEY).complaint_on_result(reported_id = -5))
print(AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = config.TEST_KEY).get_balance())
'''
print(FunCaptchaTask.FunCaptchaTask(config.TEST_KEY,
                                    proxyType='HTTP',
                                    proxyAddress="8.8.8.8",
                                    proxyPort=8080,
                                    proxyLogin="proxyLoginHere",
                                    proxyPassword="proxyPasswordHere")
      .captcha_handler(websiteURL='85.450.48',
                       websitePublicKey='789456132'))
'''
print(NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key=config.TEST_KEY)
      .captcha_handler(websiteURL='https://www.google.com/recaptcha/intro/android.html',
                       websiteKey='6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'))
