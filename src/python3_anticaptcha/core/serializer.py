from typing import Dict, Literal, Optional

from msgspec import Struct

from .enum import ResponseStatusEnm
from .const import APP_KEY


class MyBaseModel(Struct):
    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


"""
HTTP API Serializers
"""


class BaseAPIRequestSer(MyBaseModel):
    clientKey: str = None


class CreateTaskBaseSer(BaseAPIRequestSer):
    task: Dict = {}
    softId: Literal[APP_KEY] = APP_KEY
    callbackUrl: str = ""


class BaseAPIResponseSer(MyBaseModel):
    errorId: int = 0
    errorCode: str = None
    errorDescription: str = None


class CreateTaskResponseSer(BaseAPIResponseSer):
    taskId: int = None


class GetTaskResultRequestSer(BaseAPIResponseSer):
    clientKey: str = None
    taskId: int = None


class CaptchaOptionsSer(MyBaseModel):
    sleep_time: int = 10

    url_request: Optional[str] = None
    url_response: Optional[str] = None


"""
HTTP API Response
"""


class GetTaskResultResponseSer(BaseAPIResponseSer):
    status: ResponseStatusEnm = ResponseStatusEnm.error.value
    solution: dict = {}
    cost: float = 0.0
    ip: str = None
    endTime: int = None
    createTime: int = None
    solveCount: int = 0
    taskId: int = None
