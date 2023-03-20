from enum import Enum
from typing import List


class MyEnum(Enum):
    """
    Base class for work with updated Enums
    """

    @classmethod
    def list(cls) -> List[Enum]:
        return list(map(lambda c: c, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))


class EndpointPostfixEnm(str, MyEnum):
    """
    Enum stored URL postfixes for API endpoints
    """

    CREATE_TASK = "createTask"
    GET_TASK_RESULT = "getTaskResult"


class CaptchaTypeEnm(str, MyEnum):
    """
    Enum with all available captcha types
    """

    Control = "Control"  # custom captcha type
    ImageToTextTask = "ImageToTextTask"
    # Recaptcha
    RecaptchaV2Task = "RecaptchaV2Task"
    RecaptchaV2TaskProxyless = "RecaptchaV2TaskProxyless"
    RecaptchaV3TaskProxyless = "RecaptchaV3TaskProxyless"
    RecaptchaV2EnterpriseTask = "RecaptchaV2EnterpriseTask"
    RecaptchaV2EnterpriseTaskProxyless = "RecaptchaV2EnterpriseTaskProxyless"
    # FunCaptcha
    FunCaptchaTask = "FunCaptchaTask"
    FunCaptchaTaskProxyless = "FunCaptchaTaskProxyless"
    # GeeTest
    GeeTestTask = "GeeTestTask"
    GeeTestTaskProxyless = "GeeTestTaskProxyless"
    # HCaptcha
    HCaptchaTask = "HCaptchaTask"
    HCaptchaTaskProxyless = "HCaptchaTaskProxyless"
    # Turnstile
    TurnstileTask = "TurnstileTask"
    TurnstileTaskProxyless = "TurnstileTaskProxyless"
    # Custom
    AntiGateTask = "AntiGateTask"


class ResponseStatusEnm(str, MyEnum):
    """
    Enum store results `status` field variants
    """

    processing = "processing"  # Task is not ready yet
    ready = "ready"  # Task is complete; you'll find a solution in the solution property


class ProxyTypeEnm(str, MyEnum):
    """
    Enum store proxy types
    """

    http = "http"  # usual http / https
    https = "https"
    socks4 = "socks4"
    socks5 = "socks5"


class ControlPostfixEnm(str, MyEnum):
    """
    Enum store control methods URLs postfix
    """

    # get account info
    GET_BALANCE = "getBalance"
    GET_QUEUE_STATS = "getQueueStats"
    GET_APP_STATS = "getAppStats"
    GET_SPENDING_STATS = "getSpendingStats"
    # reports
    REPORT_INCORRECT_IMAGE_CAPTCHA = "reportIncorrectImageCaptcha"
    REPORT_INCORRECT_RECAPTCHA = "reportIncorrectRecaptcha"
    REPORT_CORRECT_RECAPTCHA = "reportCorrectRecaptcha"
    REPORT_INCORRECT_HCAPTCHA = "reportIncorrectHcaptcha"
