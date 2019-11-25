import asyncio

from python3_anticaptcha import CustomCaptchaTask


ANTICAPTCHA_KEY = ""

# Пример с созданием CustomCaptcha

# подробней - https://anticaptcha.atlassian.net/wiki/spaces/API/pages/241827850/CustomCaptchaTask
# ссылка на изображение
imageUrl = "https://files.anti-captcha.com/26/41f/c23/7c50ff19.jpg"
# кастомная форма для ответов пользователей
custom_form = """[
                {
                    "label": "Number",
                    "labelHint": false,
                    "contentType": false,
                    "name": "license_plate",
                    "inputType": "text",
                    "inputOptions": {
                        "width": "100",
                        "placeHolder": "Enter a letters and number without spaces"
                    }
                },{
                    "label": "Car color",
                    "labelHint": "Select color of the car",
                    "name": "color",
                    "inputType": "select",
                    "inputOptions": [
                        {
                            "value": "white",
                            "caption": "White color"
                        },
                        {
                            "value": "black",
                            "caption": "Black color"
                        },
                        {
                            "value": "grey",
                            "caption": "Grey color"
                        },
                        {
                            "value": "blue",
                            "caption": "Blue color"
                        },
                        {
                            "value": "red",
                            "caption": "Red color"
                        }
                    ]
                }
            ]"""

my_custom_task = CustomCaptchaTask.CustomCaptchaTask(
    anticaptcha_key=ANTICAPTCHA_KEY, assignment="Enter license plate number", forms=custom_form
).captcha_handler(imageUrl=imageUrl)


print(my_custom_task)


# Асинхронный пример работы
async def run():
    try:
        # Пример работы антикапчи с кастомной капчёй, асинхронно
        result = CustomCaptchaTask.aioCustomCaptchaTask(
            anticaptcha_key=ANTICAPTCHA_KEY,
            assignment="Enter license plate number",
            forms=custom_form,
        ).captcha_handler(imageUrl=imageUrl)

        print(result)

    except Exception as err:
        print(err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
