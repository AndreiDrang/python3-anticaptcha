from python3_anticaptcha import ImageToTextTask, config

key = config.TEST_KEY
print(ImageToTextTask.ImageToTextTask(key, save_format = 'const').captcha_handler('http://85.255.8.26/static/image/common_image_example/800070.png'))
print(ImageToTextTask.ImageToTextTask(key).captcha_handler('http://85.255.8.26/static/image/common_image_example/800070.png'))
