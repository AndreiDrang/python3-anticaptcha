"""Tests for ``core.serializer`` — msgspec Structs are the serialization contract.

Oracles are derived from the struct field definitions, not by calling other
production code. These pin down the exact wire shape every handler depends on.
"""

import pytest
from msgspec import Struct

from python3_anticaptcha.core.const import APP_KEY
from python3_anticaptcha.core.enum import ResponseStatusEnm
from python3_anticaptcha.core.serializer import (
    BaseAPIResponseSer,
    CaptchaOptionsSer,
    CreateTaskBaseSer,
    CreateTaskResponseSer,
    GetTaskResultRequestSer,
    GetTaskResultResponseSer,
    MyBaseModel,
)


class TestMyBaseModel:
    def test_to_dict_returns_only_struct_fields(self):
        # CreateTaskBaseSer has a known field set; to_dict must expose exactly it
        obj = CreateTaskBaseSer(clientKey="KEY")
        assert set(obj.to_dict()) == {"clientKey", "task", "softId", "callbackUrl"}

    def test_struct_instances_are_slotted(self):
        # msgspec Structs are slotted: arbitrary attributes cannot be added, so
        # nothing can leak into to_dict(). This pins that guarantee.
        obj = CreateTaskBaseSer(clientKey="KEY")
        with pytest.raises(AttributeError):
            object.__setattr__(obj, "secret", "leak")
        assert set(obj.to_dict()) == {"clientKey", "task", "softId", "callbackUrl"}

    def test_mymodel_is_msgspec_struct(self):
        assert issubclass(MyBaseModel, Struct)


class TestCreateTaskBaseSer:
    def test_defaults_match_api_contract(self):
        obj = CreateTaskBaseSer()
        assert obj.clientKey is None
        assert obj.task == {}
        assert obj.softId == APP_KEY  # APP_KEY == "867"
        assert obj.callbackUrl == ""

    def test_clientKey_is_preserved(self):
        obj = CreateTaskBaseSer(clientKey="abc123")
        assert obj.clientKey == "abc123"

    def test_softId_is_fixed_literal_app_key(self):
        # softId is a Literal[APP_KEY] — it can only ever be APP_KEY
        assert CreateTaskBaseSer(clientKey="x").softId == APP_KEY == "867"


class TestCreateTaskResponseSer:
    def test_defaults(self):
        obj = CreateTaskResponseSer()
        assert obj.errorId == 0
        assert obj.taskId is None
        assert obj.errorCode is None
        assert obj.errorDescription is None

    def test_parses_successful_create_response(self):
        obj = CreateTaskResponseSer(**{"errorId": 0, "taskId": 99})
        assert obj.errorId == 0
        assert obj.taskId == 99

    def test_unknown_kwargs_are_rejected(self):
        # NOTE: production constructs these via ``Ser(**resp.json())``. msgspec
        # Structs do NOT silently ignore unknown keyword args (unlike decode),
        # so any unexpected key from the API would raise. Pin this strictness.
        with pytest.raises(TypeError):
            CreateTaskResponseSer(**{"errorId": 0, "taskId": 1, "surprise": True})


class TestGetTaskResultRequestSer:
    def test_defaults(self):
        obj = GetTaskResultRequestSer()
        assert obj.clientKey is None
        assert obj.taskId is None
        assert obj.errorId == 0  # inherited from BaseAPIResponseSer

    def test_round_trip_to_dict(self):
        obj = GetTaskResultRequestSer(clientKey="K", taskId=7)
        assert obj.to_dict() == {
            "errorId": 0,
            "errorCode": None,
            "errorDescription": None,
            "clientKey": "K",
            "taskId": 7,
        }


class TestGetTaskResultResponseSer:
    def test_defaults(self):
        obj = GetTaskResultResponseSer()
        # NOTE: status defaults to ResponseStatusEnm.error.value — a documented,
        # arguably surprising default. We pin the *actual* behavior here.
        assert obj.status == ResponseStatusEnm.error.value
        assert obj.errorId == 0
        assert obj.solution == {}
        assert obj.cost == 0.0
        assert obj.taskId is None
        assert obj.solveCount == 0

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            ({"status": "ready", "solution": {"x": 1}}, "ready"),
            ({"status": "processing"}, "processing"),
            ({"status": "error"}, "error"),
        ],
    )
    def test_status_field_accepts_all_enum_values(self, payload, expected_status):
        obj = GetTaskResultResponseSer(**payload)
        assert obj.status == expected_status

    def test_parses_full_ready_response(self):
        payload = {
            "errorId": 0,
            "status": "ready",
            "solution": {"gRecaptchaResponse": "TOK"},
            "cost": 0.002,
            "ip": "1.1.1.1",
            "endTime": 100,
            "createTime": 90,
            "solveCount": 2,
            "taskId": 5,
        }
        obj = GetTaskResultResponseSer(**payload)
        assert obj.to_dict() == {**payload, "errorCode": None, "errorDescription": None}


class TestCaptchaOptionsSer:
    def test_defaults(self):
        obj = CaptchaOptionsSer()
        assert obj.sleep_time == 10
        assert obj.url_request is None
        assert obj.url_response is None


def test_base_api_response_defaults():
    obj = BaseAPIResponseSer()
    assert obj.errorId == 0
    assert obj.errorCode is None
    assert obj.errorDescription is None
