import urllib3
from requests.adapters import Retry
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RETRIES = Retry(total=5, backoff_factor=0.9, status_forcelist=[500, 502, 503, 504])
ASYNC_RETRIES = AsyncRetrying(wait=wait_fixed(5), stop=stop_after_attempt(5), reraise=True)

BASE_REQUEST_URL = "https://api.anti-captcha.com/"
CREATE_TASK_POSTFIX = "/createTask"
GET_RESULT_POSTFIX = "/getTaskResult"
APP_KEY = "867"
