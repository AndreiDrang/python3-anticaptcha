import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Адрес для создания задачи
create_task_url = "https://api.anti-captcha.com/createTask"
# Адрес для получения ответа
get_result_url = "https://api.anti-captcha.com/getTaskResult"
# ключ приложения
app_key = "867"
