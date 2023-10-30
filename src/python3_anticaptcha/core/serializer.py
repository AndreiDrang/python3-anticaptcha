from typing import Dict, Literal

from pydantic import Field, BaseModel, constr

from python3_anticaptcha.core.enum import ProxyTypeEnm, CaptchaTypeEnm, ResponseStatusEnm
from python3_anticaptcha.core.config import APP_KEY


class MyBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        validate_assignment = True


class BaseAPIRequestSer(MyBaseModel):
    clientKey: constr(min_length=32, max_length=32)


class BaseAPIResponseSer(MyBaseModel):
    errorId: int = Field(None, description="Error identifier.")
    errorCode: str = Field(None, description="An error code.")
    errorDescription: str = Field(None, description="Short description of the error.")


class CreateTaskRequestSer(BaseAPIRequestSer):
    task: Dict = Field(None, description="Task object.")
    languagePool: str = Field("en", description="Sets workers' pool language. Only applies to image captchas.")
    callbackUrl: str = Field(None, description="Web address where we can send the results of captcha task processing.")
    softId: Literal[APP_KEY] = APP_KEY


class CreateTaskRequestTaskSer(MyBaseModel):
    type: CaptchaTypeEnm = Field(..., description="Captcha task type name")


class ProxyDataOptionsSer(MyBaseModel):
    proxyType: ProxyTypeEnm = Field(..., description="Type of proxy")
    proxyAddress: str = Field(
        ...,
        description="Proxy IP address ipv4/ipv6. No host names or IP addresses from local networks",
    )
    proxyPort: int = Field(..., description="Proxy port")


class CreateTaskResponseSer(BaseAPIResponseSer):
    taskId: int = Field(None, description="Task ID that you should later use in the `getTaskResult` method.")


class GetTaskResultRequestSer(BaseAPIRequestSer):
    taskId: int = Field(None, description="An identifier obtained in the createTask method.")


class GetTaskResultResponseSer(BaseAPIResponseSer):
    status: ResponseStatusEnm = Field(None, description="Captcha solving process status.")
    solution: Dict = Field(None, description="Task result data. Different for each type of task.")
    cost: float = Field(None, description="Cost of the task in USD.")
    ip: str = Field(None, description="IP from which the task was created.")
    createTime: int = Field(None, description="UNIX timestamp date of task creation.")
    endTime: int = Field(None, description="UNIX timestamp date of task completion.")
    solveCount: int = Field(None, description="Number of workers who tried to complete your task.")
    taskId: int = Field(None, description="Task ID.")


"""
Captcha tasks serializers
"""


class TurnstileProxylessOptionsSer(CreateTaskRequestTaskSer):
    websiteURL: str = Field(..., description="Address of a target web page. Can be located anywhere on the web site.")
    websiteKey: str = Field(..., description="Website key")


class TurnstileOptionsSer(TurnstileProxylessOptionsSer, ProxyDataOptionsSer):
    pass
