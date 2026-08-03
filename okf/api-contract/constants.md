---
type: API Contract
title: Constants
description: Base URLs, endpoint postfixes, retry configuration, and application settings
resource: src/python3_anticaptcha/core/const.py
tags:
  - constants
  - configuration
  - retry
  - url
---

# Constants

The `const.py` module defines all constant values used throughout the library, including base URLs, endpoint postfixes, and retry configurations.

## HTTP Configuration

### Base URL

```python
BASE_REQUEST_URL = "https://api.anti-captcha.com/"
```

The base URL for all AntiCaptcha API requests. All endpoints are relative to this base.

### Endpoint Postfixes

```python
CREATE_TASK_POSTFIX = "/createTask"
GET_RESULT_POSTFIX = "/getTaskResult"
```

URL path postfixes appended to the base URL for specific endpoints. These are combined with `BASE_REQUEST_URL` to form complete endpoint URLs.

## Retry Configuration

### Synchronous Retry

```python
from requests.adapters import Retry

RETRIES = Retry(
    total=5,
    backoff_factor=0.9,
    status_forcelist=[500, 502, 503, 504]
)
```

Retry configuration for the synchronous (`requests`) transport:
- `total=5`: Maximum of 5 retry attempts
- `backoff_factor=0.9`: Exponential backoff multiplier
- `status_forcelist=[500, 502, 503, 504]`: Retry on these HTTP status codes

### Asynchronous Retry

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed

ASYNC_RETRIES = AsyncRetrying(
    wait=wait_fixed(5),
    stop=stop_after_attempt(5),
    reraise=True
)
```

Retry configuration for the asynchronous (`aiohttp`) transport:
- `wait=wait_fixed(5)`: Fixed 5-second wait between retries
- `stop=stop_after_attempt(5)`: Maximum of 5 retry attempts
- `reraise=True`: Re-raise the exception if all retries fail

## Application Key

```python
APP_KEY = "867"
```

The application identifier (softId) sent with all task creation requests. This is a constant value used to identify the python3-anticaptcha client to the AntiCaptcha service.

## Warning Suppression

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

Disables `InsecureRequestWarning` from urllib3. This is intentional to support proxy configurations that use self-signed certificates or have TLS verification disabled.

## Design Rationale

- **Centralized Constants**: All shared constants are defined in one place for easy maintenance
- **Symmetric Retry**: Sync and async transports have similar retry behavior (5 attempts each)
- **TLS Flexibility**: Warning suppression allows the library to work with various proxy configurations
- **Immutable**: All values are module-level constants that should not be modified at runtime

## Relationships

* Used by [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for base URL and retry config
* Used by [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for base URL and async retry config
* Used by [Serializer](serializer.md) for APP_KEY in CreateTaskBaseSer
* Duplicate warning suppression in [config.py](../core-components/config.md)

## Citations

[1] `src/python3_anticaptcha/core/const.py` — Defines all constant values.
[2] `src/python3_anticaptcha/core/sio_captcha_instrument.py:8` — Imports BASE_REQUEST_URL, RETRIES, CREATE_TASK_POSTFIX, GET_RESULT_POSTFIX.
[3] `src/python3_anticaptcha/core/aio_captcha_instrument.py:7` — Imports BASE_REQUEST_URL, ASYNC_RETRIES, CREATE_TASK_POSTFIX, GET_RESULT_POSTFIX.
[4] `src/python3_anticaptcha/core/serializer.py:12` — Uses APP_KEY as default softId.
[5] `AGENTS.md` — States that BASE_REQUEST_URL and RETRIES live in core/const.py, not config.py.
