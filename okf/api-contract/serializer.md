---
type: API Contract
title: Serializer
description: msgspec Struct definitions for AntiCaptcha API request and response envelopes
resource: src/python3_anticaptcha/core/serializer.py
tags:
  - serialization
  - msgspec
  - api-contract
  - struct
---

# Serializer

The `serializer.py` module defines msgspec `Struct` classes that represent the request and response envelopes for the AntiCaptcha API. These structs provide type-safe serialization and deserialization of API messages.

## Overview

All communication with the AntiCaptcha API uses a consistent envelope structure. The serializer module captures these structures as msgspec Structs, which are then used by both the synchronous and asynchronous transports.

## Base Model

### MyBaseModel

```python
class MyBaseModel(Struct):
    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}
```

Base class for all serializer structs, providing a `to_dict()` method to convert the struct to a plain dictionary. This is used to prepare payloads for HTTP requests.

## Request Serializers

### BaseAPIRequestSer

Base class for API requests.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `clientKey` | str | None | API key for authentication |

### CreateTaskBaseSer

Request payload for creating a new captcha solving task.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `task` | Dict | {} | The captcha task parameters |
| `softId` | Literal["867"] | "867" | Application identifier (constant) |
| `callbackUrl` | str | "" | Optional callback URL for results |

Inherits from `BaseAPIRequestSer`, so also has `clientKey`.

### GetTaskResultRequestSer

Request payload for retrieving task results.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `clientKey` | str | None | API key for authentication |
| `taskId` | int | None | The task ID to check |

Inherits from `BaseAPIResponseSer`.

## Response Serializers

### BaseAPIResponseSer

Base class for API responses.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `errorId` | int | 0 | Error code (0 = success) |
| `errorCode` | str | None | Error code string |
| `errorDescription` | str | None | Human-readable error description |

### CreateTaskResponseSer

Response from creating a task.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `taskId` | int | None | The created task ID |

Inherits from `BaseAPIResponseSer`.

### GetTaskResultResponseSer

Response from retrieving task results.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | ResponseStatusEnm | "error" | Task status (processing/ready/error) |
| `solution` | dict | {} | The captcha solution (when ready) |
| `cost` | float | 0.0 | Cost of solving this captcha |
| `ip` | str | None | IP address of the solving worker |
| `endTime` | int | None | Unix timestamp when task completed |
| `createTime` | int | None | Unix timestamp when task was created |
| `solveCount` | int | 0 | Number of solve attempts |
| `taskId` | int | None | The task ID |

Inherits from `BaseAPIResponseSer`.

### CaptchaOptionsSer

Configuration options for captcha solving.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sleep_time` | int | 10 | Seconds between polling attempts |
| `url_request` | Optional[str] | None | URL for request logging |
| `url_response` | Optional[str] | None | URL for response logging |

## Design Principles

- **Type Safety**: msgspec provides runtime type checking and validation
- **Shared Contract**: Both sync and async transports use the same structs
- **Dictionary Conversion**: All structs can be converted to dicts via `to_dict()`
- **Version Pinning**: msgspec is pinned to `>=0.18,<0.22` to avoid breaking changes

## Relationships

* Used by [CaptchaParams](../core-components/captcha-params.md) to construct payloads
* Used by [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for request/response handling
* Used by [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for request/response handling
* Depends on [ResponseStatusEnm](enums.md) for status values
* Depends on [APP_KEY](constants.md) for softId value

## Citations

[1] `src/python3_anticaptcha/core/serializer.py` — Defines all serializer structs.
[2] `src/python3_anticaptcha/core/base.py:17-18` — Uses CreateTaskBaseSer and GetTaskResultRequestSer.
[3] `pyproject.toml:37` — Pins msgspec version to >=0.18,<0.22.
[4] `AGENTS.md` — Notes that newer msgspec versions may break Struct-based serializers.
