from typing import Generator

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Адрес для создания задачи
create_task_url = "https://api.anti-captcha.com/createTask"
# Адрес для получения ответа
get_result_url = "https://api.anti-captcha.com/getTaskResult"
# ключ приложения
app_key = "867"


# Connection retry generator
def attempts_generator(amount: int = 5) -> Generator:
    """
    Function generates a generator of length equal to `amount`

    Args:
        amount: number of attempts generated

    Returns:
        Attempt number
    """
    for i in range(1, amount):
        yield i
