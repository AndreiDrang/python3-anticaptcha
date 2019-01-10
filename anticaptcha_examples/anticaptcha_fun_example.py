import asyncio
import requests

from python3_anticaptcha import FunCaptchaTask, FunCaptchaTaskProxyless, CallbackClient


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

# Пример работы антикапчи с фанкапчёй и с БЕЗ использования прокси при этом
result = FunCaptchaTaskProxyless.FunCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY)\
            .captcha_handler(websiteURL=WEB_URL,
                            websitePublicKey=SITE_KEY)

print(result)

# Асинхронный пример работы
async def run():
    try:
        # Пример работы антикапчи с фанкапчёй и с использованием прокси при этом
        result = FunCaptchaTask.aioFunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                               proxyType='http',
                                               proxyAddress="8.8.8.8",
                                               proxyPort=8080,
                                               proxyLogin="proxyLoginHere",
                                               proxyPassword="proxyPasswordHere") \
                    .captcha_handler(websiteURL=WEB_URL,
                                    websitePublicKey=SITE_KEY)
        
        print(result)
        # Пример работы антикапчи с фанкапчёй и БЕЗ использования прокси при этом
        result = FunCaptchaTaskProxyless.aioFunCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY) \
                    .captcha_handler(websiteURL=WEB_URL,
                                     websitePublicKey=SITE_KEY)
        
        print(result)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

"""
Callback example
"""
QUEUE_KEY = 'wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ_anticaptcha_queue'

"""
Перед тем как начать пользоваться сервисом нужно создать для своей задачи отдельную очередь
Очередь можно создать один раз и пользоваться постоянно

Для создания очереди нужно передать два параметра:
1. key - название очереди, чем оно сложнее тем лучше
2. vhost - название виртуального хоста(в данном случаи - `anticaptcha_vhost`)
"""

answer = requests.post('http://85.255.8.26:8001/register_key', json={'key':QUEUE_KEY, 
                                                                     'vhost':'anticaptcha_vhost'})
# если очередь успешно создана:                                                                     
if answer == 'OK':

    # создаём задание с callbackURL параметром
    result = FunCaptchaTask.FunCaptchaTask(anticaptcha_key=ANTICAPTCHA_KEY,
                                           proxyType='http',
                                           proxyAddress="8.8.8.8",
                                           proxyPort=8080,
                                           proxyLogin="proxyLoginHere",
                                           proxyPassword="proxyPasswordHere",
                                           callbackUrl=f'http://85.255.8.26:8001/anticaptcha/fun_captcha/{QUEUE_KEY}') \
            .captcha_handler(websiteURL=WEB_URL,
                             websitePublicKey=SITE_KEY)    
    print(result)

    # получение результата из кеша
    print(CallbackClient.CallbackClient(task_id=result['taskId']).captcha_handler())
    # получение результата из RabbitMQ очереди
    print(CallbackClient.CallbackClient(task_id=result['taskId'], queue_name=QUEUE_KEY, call_type='queue').captcha_handler())
    
    # создаём задание с callbackURL параметром
    result = FunCaptchaTaskProxyless.FunCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY,
                                                             callbackUrl=f'http://85.255.8.26:8001/anticaptcha/fun_captcha/{QUEUE_KEY}') \
                .captcha_handler(websiteURL=WEB_URL,
                                 websitePublicKey=SITE_KEY)    
    print(result)

    # получение результата из кеша
    print(CallbackClient.CallbackClient(task_id=result['taskId']).captcha_handler())
    # получение результата из RabbitMQ очереди
    print(CallbackClient.CallbackClient(task_id=result['taskId'], queue_name=QUEUE_KEY, call_type='queue').captcha_handler())
